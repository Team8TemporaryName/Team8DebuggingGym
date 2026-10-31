"use strict";

import * as vscode from "vscode";

export interface KindMeta {
  summary: string;
}

/** The base URL of the Debugging Gym web app, from settings. */
export function baseUrl(): string {
  const config = vscode.workspace.getConfiguration("debuggingGym");
  return (config.get<string>("baseUrl") || "http://localhost:8000").replace(/\/+$/, "");
}

/** A typed fetch helper for the Debugging Gym HTTP API. */
export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${baseUrl()}${path}`, init);
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`Debugging Gym API ${res.status}: ${body || res.statusText}`);
  }
  return (await res.json()) as T;
}