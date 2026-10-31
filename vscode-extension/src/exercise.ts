"use strict";

import * as vscode from "vscode";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

/**
 * Per-exercise folder management (DEC-018).
 *
 * Each exercise opens in its own folder under the workspace, containing
 * `exercise.py` (the learner edits this), `harness.py` (a pytest file the
 * learner may also edit, DEC-017), and `task.md` (the task statement). The
 * folder is git-initialized so a learner does not lose progress and can back
 * up or revert.
 */

export interface ExerciseFiles {
  source: string;
  harness: string;
  task: string;
  id: string;
  kind: string;
}

function slugify(kind: string): string {
  return kind.replace(/[^a-z0-9]+/gi, "-").toLowerCase().replace(/(^-|-$)/g, "");
}

/**
 * Create a per-exercise folder for ``exercise`` in the first workspace folder
 * and write its files. Returns the folder URI.
 */
export async function createExerciseFolder(
  exercise: ExerciseFiles,
): Promise<vscode.Uri> {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) {
    throw new Error("Open a workspace folder to save the exercise.");
  }
  const root = folders[0].uri;
  const folderName = `exercise-${slugify(exercise.kind)}-${exercise.id.slice(0, 6)}`;
  const dir = vscode.Uri.joinPath(root, folderName);

  await vscode.workspace.fs.createDirectory(dir);
  await vscode.workspace.fs.writeFile(
    vscode.Uri.joinPath(dir, "exercise.py"),
    Buffer.from(exercise.source, "utf-8"),
  );
  await vscode.workspace.fs.writeFile(
    vscode.Uri.joinPath(dir, "harness.py"),
    Buffer.from(exercise.harness, "utf-8"),
  );
  await vscode.workspace.fs.writeFile(
    vscode.Uri.joinPath(dir, "task.md"),
    Buffer.from(exercise.task, "utf-8"),
  );

  // Dynamic recommended settings (DEC-019): enable format-on-save for Python.
  const settingsDir = vscode.Uri.joinPath(dir, ".vscode");
  await vscode.workspace.fs.createDirectory(settingsDir);
  await vscode.workspace.fs.writeFile(
    vscode.Uri.joinPath(settingsDir, "settings.json"),
    Buffer.from(
      JSON.stringify(
        {
          "editor.formatOnSave": true,
          "python.defaultInterpreterPath": "python",
        },
        null,
        2,
      ),
      "utf-8",
    ),
  );

  await gitInit(dir);
  return dir;
}

/** Initialise a git repository in the exercise folder, if git is available. */
async function gitInit(dir: vscode.Uri): Promise<void> {
  try {
    const local = dir.fsPath;
    await execAsync("git init -q", { cwd: local });
    await execAsync('git add -A && git -c user.name="Debugging Gym" -c user.email="gym@localhost" commit -qm "Initial exercise"', {
      cwd: local,
    });
  } catch {
    // git may be unavailable; the exercise still works without versioning.
  }
}

/** The folders of saved exercises under ``root``, as {name, uri} pairs. */
export async function listExerciseFolders(root: vscode.Uri): Promise<{ name: string; uri: vscode.Uri }[]> {
  const entries = await vscode.workspace.fs.readDirectory(root);
  return entries
    .filter(([name, type]) => type === vscode.FileType.Directory && name.startsWith("exercise-"))
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([name]) => ({ name, uri: vscode.Uri.joinPath(root, name) }));
}

/** A saved exercise loaded from its folder on disk. */
export interface SavedExercise {
  name: string;
  uri: vscode.Uri;
  source: string;
  harness: string;
  task: string;
  id: string;
  kind: string;
}

/** Load the program, harness, task, and metadata from an exercise folder. */
export async function loadExerciseFolder(dir: vscode.Uri): Promise<SavedExercise> {
  const read = async (file: string): Promise<string> => {
    try {
      const data = await vscode.workspace.fs.readFile(vscode.Uri.joinPath(dir, file));
      return Buffer.from(data).toString("utf-8");
    } catch {
      return "";
    }
  };
  const name = dir.path.split("/").pop() || dir.fsPath.split(/[\\/]/).pop() || "";
  // Metadata: kind and id are encoded in the folder name exercise-<kind>-<id>.
  const match = name.match(/^exercise-(.+)-([a-f0-9]{6})$/);
  const kind = match ? match[1] : "unknown";
  const id = match ? `ex-${match[2]}` : name;
  return {
    name,
    uri: dir,
    source: await read("exercise.py"),
    harness: await read("harness.py"),
    task: await read("task.md"),
    id,
    kind,
  };
}

/** Open the exercise folder's files for editing. */
export async function openExerciseFolder(dir: vscode.Uri): Promise<void> {
  const doc = await vscode.workspace.openTextDocument(vscode.Uri.joinPath(dir, "exercise.py"));
  await vscode.window.showTextDocument(doc, { preview: false });
}

/**
 * Run the exercise's pytest harness locally in a real VS Code terminal.
 *
 * Running in a terminal gives the learner the live, coloured pytest output
 * (expected vs. got and stack traces on failure) exactly as if they had typed
 * ``python -m pytest harness.py`` themselves. This is the "run the harness
 * yourself" path — the server-side hidden tests still decide the final verdict.
 */
export function runHarnessLocally(dir: vscode.Uri): void {
  const terminal = vscode.window.createTerminal({
    name: "Debugging Gym",
    cwd: dir.fsPath,
  });
  terminal.show(true);
  terminal.sendText("python -m pytest harness.py -q");
}