"use strict";

import * as vscode from "vscode";
import { api, KindMeta } from "./api";
import {
  createExerciseFolder,
  listExerciseFolders,
  loadExerciseFolder,
  openExerciseFolder,
  runHarnessLocally,
} from "./exercise";

/**
 * The Debugging Gym sidebar (a WebviewView).
 *
 * The sidebar is the primary learner surface (DEC-015): it shows the problem
 * kinds, generates exercises, shows the task, verifies against the harness,
 * and lists the learner's saved exercise folders read from disk. It also shows
 * the verification output so the learner does not rely on the output channel.
 */

interface ExerciseMeta {
  id: string;
  kind: string;
  task: string;
  generator: string;
  source: string;
  harness: string;
}

export class DebuggingGymSidebar implements vscode.WebviewViewProvider {
  public static readonly viewType = "debuggingGym.sidebar";

  private view?: vscode.WebviewView;
  private current?: ExerciseMeta;
  private currentFolder?: vscode.Uri;
  private lastKinds: string[] = [];

  resolveWebviewView(view: vscode.WebviewView): void {
    this.view = view;
    view.webview.options = { enableScripts: true };
    view.webview.html = this.html();
    view.webview.onDidReceiveMessage(async (msg) => {
      await this.handle(msg);
    });
    void this.refreshKinds();
    void this.refreshExercises();
  }

  private html(): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); padding: 0.5rem; }
  h3 { margin: 0 0 0.5rem; }
  button { display: block; width: 100%; margin: 0.25rem 0; padding: 0.4rem;
    background: var(--vscode-button-background); color: var(--vscode-button-foreground);
    border: none; cursor: pointer; }
  button.secondary { background: var(--vscode-button-secondaryBackground); color: var(--vscode-button-secondaryForeground); }
  select { width: 100%; margin: 0.25rem 0; }
  .section { margin-top: 1rem; }
  .item { margin: 0.25rem 0; cursor: pointer; }
  .item:hover { text-decoration: underline; }
  .status { margin-top: 0.5rem; font-style: italic; white-space: pre-wrap; }
  .task { margin-top: 0.5rem; padding: 0.4rem; background: var(--vscode-editor-inactiveSelectionBackground); white-space: pre-wrap; }
  .row { display: flex; gap: 0.25rem; }
  .row button { flex: 1; }
</style>
</head>
<body>
  <h3>Debugging Gym</h3>
  <div class="section">
    <label for="kind">Problem kind</label>
    <select id="kind"></select>
    <button id="generate">Generate exercise</button>
  </div>
  <div id="task" class="task" style="display:none"></div>
  <div class="section">
    <button id="verify" class="secondary">Verify fix against the harness</button>
    <button id="runLocal" class="secondary">Run tests locally</button>
  </div>
  <div class="section">
    <div class="row">
      <h3 style="flex:1">Saved exercises</h3>
      <button id="refresh" title="Refresh">↻</button>
    </div>
    <div id="exercises"><span class="status">No exercises yet.</span></div>
  </div>
  <div id="status" class="status"></div>
  <script>
    const vscode = acquireVsCodeApi();
    const kindSel = document.getElementById('kind');
    const list = document.getElementById('exercises');
    const status = document.getElementById('status');
    const taskEl = document.getElementById('task');

    function setStatus(text) { status.textContent = text; }

    document.getElementById('generate').onclick = () =>
      vscode.postMessage({ command: 'generate', kind: kindSel.value });
    document.getElementById('verify').onclick = () =>
      vscode.postMessage({ command: 'verify' });
    document.getElementById('runLocal').onclick = () =>
      vscode.postMessage({ command: 'runLocal' });
    document.getElementById('refresh').onclick = () =>
      vscode.postMessage({ command: 'refresh' });

    window.addEventListener('message', event => {
      const msg = event.data;
      if (msg.command === 'kinds') {
        kindSel.innerHTML = '';
        for (const [kind, meta] of Object.entries(msg.kinds)) {
          const opt = document.createElement('option');
          opt.value = kind;
          opt.textContent = kind + ' — ' + meta.summary;
          kindSel.appendChild(opt);
        }
      } else if (msg.command === 'exercises') {
        list.innerHTML = '';
        if (!msg.exercises.length) {
          list.innerHTML = '<span class="status">No exercises yet.</span>';
          return;
        }
        for (const ex of msg.exercises) {
          const div = document.createElement('div');
          div.className = 'item';
          div.textContent = ex.name;
          div.onclick = () => vscode.postMessage({ command: 'open', name: ex.name });
          list.appendChild(div);
        }
      } else if (msg.command === 'task') {
        if (msg.task) {
          taskEl.style.display = 'block';
          taskEl.textContent = msg.task;
        } else {
          taskEl.style.display = 'none';
        }
      } else if (msg.command === 'status') {
        setStatus(msg.text);
      }
    });
  </script>
</body>
</html>`;
  }

  private post(msg: unknown): void {
    this.view?.webview.postMessage(msg);
  }

  private async refreshKinds(): Promise<void> {
    try {
      const kinds = await api<Record<string, KindMeta>>("/api/kinds");
      this.lastKinds = Object.keys(kinds);
      this.post({ command: "kinds", kinds });
    } catch (e) {
      this.post({ command: "status", text: `Cannot reach the Debugging Gym server: ${String(e)}` });
    }
  }

  private async refreshExercises(): Promise<void> {
    const folders = vscode.workspace.workspaceFolders;
    if (!folders) {
      return;
    }
    try {
      const saved = await listExerciseFolders(folders[0].uri);
      this.post({ command: "exercises", exercises: saved.map((s) => ({ name: s.name })) });
    } catch (e) {
      this.post({ command: "status", text: `Cannot read exercises: ${String(e)}` });
    }
  }

  private async handle(msg: { command: string; kind?: string; name?: string }): Promise<void> {
    switch (msg.command) {
      case "generate":
        await this.generate(msg.kind);
        break;
      case "verify":
        await this.verify();
        break;
      case "runLocal":
        await this.runLocal();
        break;
      case "refresh":
        await this.refreshExercises();
        break;
      case "open":
        if (msg.name) {
          await this.open(msg.name);
        }
        break;
    }
  }

  async generate(kind?: string): Promise<void> {
    if (!kind) {
      if (this.lastKinds.length === 0) {
        this.post({ command: "status", text: "Cannot reach the Debugging Gym server. Try the refresh button once it is back." });
        return;
      }
      const picked = await vscode.window.showQuickPick(this.lastKinds, {
        placeHolder: "Choose a debugging problem kind",
      });
      if (!picked) {
        return;
      }
      kind = picked;
    }
    this.post({ command: "status", text: "Generating exercise…" });
    try {
      const ex = await vscode.window.withProgress(
        { location: vscode.ProgressLocation.Notification, title: "Generating exercise…" },
        async () =>
          api<ExerciseMeta>("/api/exercises", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ kind }),
          }),
      );
      const folder = await createExerciseFolder(ex);
      this.currentFolder = folder;
      await openExerciseFolder(folder);
      this.current = ex;
      this.post({ command: "task", task: ex.task });
      this.post({ command: "status", text: `Exercise generated (${ex.generator}). Folder saved.` });
      void this.refreshExercises();
    } catch (e) {
      this.post({ command: "status", text: `Error: ${String(e)}` });
    }
  }

  async verify(): Promise<void> {
    if (!this.current) {
      this.post({ command: "status", text: "Generate or open an exercise first." });
      return;
    }
    try {
      const source = await this.readActiveSource();
      // Use the generic endpoint so a reopened saved exercise (whose id may be
      // out of the server's memory) still verifies (feedback point 4).
      const result = await api<{ passed: boolean; output: string }>("/api/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source, harness: this.current.harness }),
      });
      const rawOutput = result.output;
      const msg = result.passed
        ? "All harness cases passed — the bug is gone."
        : "The harness still fails. Keep debugging.";
      if (result.passed) {
        vscode.window.showInformationMessage(msg);
      } else {
        vscode.window.showErrorMessage(msg);
      }
      // Print the raw (ANSI-coloured) output in a terminal, where the colours
      // render, instead of stripping them into the sidebar.
      this.printOutput(rawOutput);
    } catch (e) {
      this.post({ command: "status", text: `Error: ${String(e)}` });
    }
  }

  async runLocal(): Promise<void> {
    if (!this.currentFolder) {
      this.post({ command: "status", text: "Generate or open an exercise first." });
      return;
    }
    // Runs the pytest harness in a real terminal, which shows the coloured
    // expected-vs-got output and stack traces so the learner sees what failed.
    runHarnessLocally(this.currentFolder);
  }

  /**
   * Show raw ANSI-coloured output in a real terminal so the colours render.
   * Writes the output to a temporary file and cats it, preserving the escape
   * codes.
   */
  private printOutput(raw: string): void {
    const { tmpdir } = require("os");
    const { writeFileSync } = require("fs");
    const { join } = require("path");
    const file = join(tmpdir(), `debugging-gym-${Date.now()}.log`);
    writeFileSync(file, raw, "utf-8");
    const terminal = vscode.window.createTerminal({ name: "Debugging Gym output" });
    terminal.show(true);
    terminal.sendText(`cat "${file}"`);
  }

  async showTask(): Promise<void> {
    if (!this.current) {
      this.post({ command: "status", text: "Generate or open an exercise first." });
      return;
    }
    this.post({ command: "task", task: this.current.task });
  }

  private async open(name: string): Promise<void> {
    const folders = vscode.workspace.workspaceFolders;
    if (!folders) {
      return;
    }
    const saved = await listExerciseFolders(folders[0].uri);
    const found = saved.find((s) => s.name === name);
    if (!found) {
      this.post({ command: "status", text: `Exercise not found: ${name}` });
      return;
    }
    // Load the files from disk so reopening works after a reset (point 3),
    // and set the current exercise to the reopened one (point 4).
    const ex = await loadExerciseFolder(found.uri);
    this.current = {
      id: ex.id,
      kind: ex.kind,
      task: ex.task || "Read the task in task.md.",
      generator: "saved",
      source: ex.source,
      harness: ex.harness,
    };
    this.currentFolder = found.uri;
    await openExerciseFolder(found.uri);
    this.post({ command: "task", task: this.current.task });
    this.post({ command: "status", text: `Opened ${name}.` });
  }

  private async readActiveSource(): Promise<string> {
    const editor = vscode.window.activeTextEditor;
    if (editor && editor.document.fileName.endsWith("exercise.py")) {
      return editor.document.getText();
    }
    // Fall back to the in-memory source if no editor is focused.
    if (this.current) {
      return this.current.source;
    }
    throw new Error("Open exercise.py to verify your fix.");
  }
}