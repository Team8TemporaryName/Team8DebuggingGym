"use strict";

import * as vscode from "vscode";

interface KindMeta {
  summary: string;
}

interface Exercise {
  id: string;
  kind: string;
  task: string;
  generator: string;
  source: string;
  harness: string;
}

interface VerifyResult {
  passed: boolean;
  output: string;
}

const EXERCISE_FILE = "exercise.py";

function baseUrl(): string {
  const config = vscode.workspace.getConfiguration("debuggingGym");
  return (config.get<string>("baseUrl") || "http://localhost:8000").replace(/\/+$/, "");
}

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${baseUrl()}${path}`, init);
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Debugging Gym API ${res.status}: ${body || res.statusText}`);
  }
  return (await res.json()) as T;
}

async function pickKind(): Promise<string | undefined> {
  const kinds = await api<Record<string, KindMeta>>("/api/kinds");
  const entries = Object.entries(kinds);
  const picked = await vscode.window.showQuickPick(
    entries.map(([kind, meta]) => ({ label: kind, description: meta.summary, value:kind })),
    { placeHolder: "Choose a debugging problem kind" }
  );
  return picked?.value;
}

async function writeExerciseFile(source: string): Promise<vscode.Uri | undefined> {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) {
    await vscode.window.showWarningMessage("Open a workspace folder to save the exercise.");
    return undefined;
  }
  const uri = vscode.Uri.joinPath(folders[0].uri, EXERCISE_FILE);
  await vscode.workspace.fs.writeFile(uri, Buffer.from(source, "utf-8"));
  return uri;
}

let excerciseUri: vscode.Uri | undefined;

async function newExercise(): Promise<void> {
  const kind = await pickKind();
  if (!kind) {
    return;
  }
  currentExercise = await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: "Generating exercise…" },
    async () => {
      const exercise = await api<Exercise>("/api/exercises", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ kind }),
      });

      vscode.window.showInformationMessage(`Exercise generated (${exercise.generator}).`);
	  return exercise;
    }
  );
  excerciseUri = await writeExerciseFile(currentExercise.source);
  if (excerciseUri) {
	const doc = await vscode.workspace.openTextDocument(excerciseUri);
	await vscode.window.showTextDocument(doc, { preview: false });
  }

  const choice = await vscode.window.showInformationMessage(
	"Exercise ready. Verify your fix against the harness, or read the task first.",
	"Verify fix",
	"Show task"
  );
  if (choice === "Verify fix") {
	await verifyFix();
  } else if (choice === "Show task") {
	await showTask();
  }
}

async function currentSource(): Promise<string | undefined> {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    await vscode.window.showWarningMessage("Open exercise.py to verify your fix.");
    return undefined;
  }
  if (!excerciseUri) {
	await vscode.window.showWarningMessage("No excercise is opened");
	return undefined;
  }
  return Buffer.from(await vscode.workspace.fs.readFile(excerciseUri)).toString();
}

async function verifyFix(): Promise<void> {
  const exercise = await findExerciseInWorkspace();
  if (!exercise) {
    return;
  }
  const source = await currentSource();
  if (source === undefined) {
    return;
  }
  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: "Running the harness…" },
    async () => {
      const result = await api<VerifyResult>(`/api/exercises/${exercise.id}/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source }),
      });
      if (result.passed) {
        vscode.window.showInformationMessage("All harness cases passed — the bug is gone.");
      } else {
        vscode.window.showErrorMessage("The harness still fails. Keep debugging.");
      }
      const channel = vscode.window.createOutputChannel("Debugging Gym");
      channel.append(result.output);
      channel.show();
    }
  );
}

/** Persist the active exercise so verify can find it later. */
let currentExercise: Exercise | undefined;

async function findExerciseInWorkspace(): Promise<Exercise | undefined> {
  if (currentExercise) {
    return currentExercise;
  }
  await vscode.window.showWarningMessage("Generate an exercise first.");
  return undefined;
}

async function showTask(): Promise<void> {
  if (!currentExercise) {
    const folders = vscode.workspace.workspaceFolders;
    if (folders) {
	  try {
        const text = await vscode.workspace.fs.readFile(vscode.Uri.joinPath(folders[0].uri, EXERCISE_FILE));
      } catch (error) {
		const text = undefined;
	  }
      // No persisted task; prompt the user to generate.
    }
    await vscode.window.showInformationMessage("Generate an exercise to read its task.");
    return;
  }
  await vscode.window.showInformationMessage(currentExercise.task);
}

export function activate(context: vscode.ExtensionContext): void {
  context.subscriptions.push(
    vscode.commands.registerCommand("debuggingGym.newExercise", newExercise),
    vscode.commands.registerCommand("debuggingGym.chooseKind", newExercise),
    vscode.commands.registerCommand("debuggingGym.verifyFix", verifyFix),
    vscode.commands.registerCommand("debuggingGym.showTask", showTask)
  );
}

export function deactivate(): void {}