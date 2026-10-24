"use strict";

const state = { exercise: null, activeTab: "source", currentCode: "" };

async function loadKinds() {
  const res = await fetch("/api/kinds");
  const kinds = await res.json();
  const box = document.getElementById("kinds");
  box.innerHTML = "";
  for (const [kind, meta] of Object.entries(kinds)) {
    const btn = document.createElement("button");
    btn.className = "kind";
    btn.innerHTML = `<strong>${kind}</strong><span>${meta.summary}</span>`;
    btn.addEventListener("click", () => newExercise(kind));
    box.appendChild(btn);
  }
}

async function newExercise(kind) {
  const res = await fetch("/api/exercises", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ kind }),
  });
  state.exercise = await res.json();
  document.getElementById("task").textContent = state.exercise.task;
  document.getElementById("code").textContent = state.exercise.source;
  state.currentCode = state.exercise.source;
  document.getElementById("editor").value = state.exercise.source;
  show("exercise");
  show("verify");
  setTab("source");
  document.getElementById("exercise").scrollIntoView({ behavior: "smooth" });
}

function show(id) {
  document.getElementById(id).classList.remove("hidden");
}

function setTab(tab) {
  const code = document.getElementById("code");
  const editor = document.getElementById("editor");
  if (state.activeTab === "source") {
    state.currentCode = code.textContent;
  }
  state.activeTab = tab;
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t.textContent.trim() === tabLabel(tab)));
  if (tab === "source") {
    code.textContent = state.currentCode;
    code.contentEditable = "true";
    code.classList.remove("hidden");
    editor.classList.add("hidden");
  } else if (tab === "harness") {
    code.textContent = state.exercise.harness;
    code.contentEditable = "false";
    code.classList.remove("hidden");
    editor.classList.add("hidden");
  } else if (tab === "launch") {
    showLaunch();
    code.contentEditable = "false";
  }
}

function tabLabel(tab) {
  return { source: "Program", harness: "Harness", launch: "VS Code" }[tab];
}

async function showLaunch() {
  const code = document.getElementById("code");
  const editor = document.getElementById("editor");
  const res = await fetch(`/api/exercises/${state.exercise.id}/launch`);
  const data = await res.json();
  code.textContent = JSON.stringify(data.launch_json, null, 2);
  code.classList.remove("hidden");
  editor.classList.add("hidden");
}

async function runVerify() {
  const result = document.getElementById("result");
  result.className = "result";
  result.textContent = "Running the harness…";
  const res = await fetch(`/api/exercises/${state.exercise.id}/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source: document.getElementById("code").textContent }),
  });
  const data = await res.json();
  result.textContent = data.output || (data.passed ? "All cases passed." : "Harness failed.");
  result.classList.toggle("ok", !!data.passed);
  result.classList.toggle("fail", !data.passed);
}

document.getElementById("tab-source").addEventListener("click", () => setTab("source"));
document.getElementById("tab-harness").addEventListener("click", () => setTab("harness"));
// document.getElementById("tab-launch").addEventListener("click", () => setTab("launch"));
document.getElementById("run-verify").addEventListener("click", runVerify);

loadKinds();