"use strict";

const state = { exercise: null, activeTab: "source", currentCode: "" };

// ---- A small, dependency-free Python syntax highlighter ---------------------
const KEYWORDS =
  /\b(def|return|if|elif|else|for|while|import|from|as|class|with|pass|None|True|False|not|and|or|in|is|lambda|raise|try|except|finally|yield|global|del|break|continue)\b/;

function highlightPython(code) {
  // Escape HTML first, then wrap tokens in spans. Split lines to preserve layout.
  const esc = code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return esc.replace(
    /(\/\/.*$)|('''[\s\S]*?'''|"""(?:[^"\\]|\\.|"(?!""))*""")|(#.*$)|(\b\d+(?:\.\d+)?\b)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b(?:def|return|if|elif|else|for|while|import|from|as|class|with|pass|None|True|False|not|and|or|in|is|lambda|raise|try|except|finally|yield|global|del|break|continue)\b)/gm,
    (match, lineComment, triple, hash, num, str, kw) => {
      if (lineComment) return `<span class="tok-line">${lineComment}</span>`;
      if (triple) return `<span class="tok-doc">${triple}</span>`;
      if (hash) return `<span class="tok-comment">${hash}</span>`;
      if (num) return `<span class="tok-num">${num}</span>`;
      if (str) return `<span class="tok-str">${str}</span>`;
      if (kw) return `<span class="tok-kw">${kw}</span>`;
      return match;
    }
  );
}

function renderHighlighted(source) {
  document.getElementById("code").innerHTML = highlightPython(source);
}

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
  state.currentCode = state.exercise.source;
  document.getElementById("editor").value = state.exercise.source;
  document.getElementById("finish").classList.add("hidden");
  document.getElementById("result").textContent = "";
  document.getElementById("result").className = "result";
  show("exercise");
  show("verify");
  setTab("source");
  document.getElementById("exercise").scrollIntoView({ behavior: "smooth" });
}

function show(id) {
  document.getElementById(id).classList.remove("hidden");
}

function setTab(tab) {
  const editor = document.getElementById("editor");
  const code = document.getElementById("code");
  state.activeTab = tab;
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t.textContent.trim() === tabLabel(tab)));
  if (tab === "source") {
    editor.value = state.currentCode;
    code.classList.add("hidden");
    editor.classList.remove("hidden");
  } else if (tab === "harness") {
    renderHighlighted(state.exercise.harness);
    code.classList.remove("hidden");
    editor.classList.add("hidden");
  } else if (tab === "launch") {
    showLaunch();
    code.classList.remove("hidden");
    editor.classList.add("hidden");
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
  const runBtn = document.getElementById("run-verify");
  result.className = "result";
  result.textContent = "Running the harness…";
  runBtn.disabled = true;
  runBtn.classList.add("busy");
  const source = document.getElementById("editor").value;
  try {
    const res = await fetch(`/api/exercises/${state.exercise.id}/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source }),
    });
    const data = await res.json();
    result.textContent = data.output || (data.passed ? "All cases passed." : "Harness failed.");
    result.classList.toggle("ok", !!data.passed);
    result.classList.toggle("fail", !data.passed);
    const finish = document.getElementById("finish");
    if (data.passed) {
      finish.classList.remove("hidden");
    } else {
      finish.classList.add("hidden");
    }
  } finally {
    runBtn.disabled = false;
    runBtn.classList.remove("busy");
  }
}

function finishExercise() {
  const finish = document.getElementById("finish");
  finish.classList.add("hidden");
  const result = document.getElementById("result");
  result.className = "result ok";
  result.textContent = "Exercise completed. You can choose another problem kind to keep practising.";
  document.getElementById("choose").scrollIntoView({ behavior: "smooth" });
}

document.getElementById("tab-source").addEventListener("click", () => setTab("source"));
document.getElementById("tab-harness").addEventListener("click", () => setTab("harness"));
document.getElementById("run-verify").addEventListener("click", runVerify);
document.getElementById("finish").addEventListener("click", finishExercise);

loadKinds();