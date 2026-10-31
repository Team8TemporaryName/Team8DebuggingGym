"use strict";

import * as vscode from "vscode";
import { DebuggingGymSidebar } from "./sidebar";

/**
 * The Debugging Gym VS Code extension.
 *
 * The primary learner surface (DEC-015) is the sidebar, which drives the
 * choose, generate, and verify flow and lists the learner's saved exercises.
 * The commands keep working for users who prefer the command palette.
 */

export function activate(context: vscode.ExtensionContext): void {
  const provider = new DebuggingGymSidebar();
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider(
      DebuggingGymSidebar.viewType,
      provider,
    ),
    vscode.commands.registerCommand("debuggingGym.newExercise", async () => {
      await provider.generate();
    }),
    vscode.commands.registerCommand("debuggingGym.verifyFix", async () => {
      await provider.verify();
    }),
    vscode.commands.registerCommand("debuggingGym.showTask", async () => {
      await provider.showTask();
    }),
  );
}

export function deactivate(): void {}