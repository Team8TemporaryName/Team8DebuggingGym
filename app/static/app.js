"use strict";

const state = { exercise: null, session: null, role: "student", currentCode: "" };

// ---- A small, dependency-free Python syntax highlighter ---------------------
function highlightPython(code) {
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

// ---- Helpers ----------------------------------------------------------------

function headers() {
  const h = { "Content-Type": "application/json" };
  if (state.session) h["x-session"] = state.session;
  return h;
}

function show(id) {
  document.getElementById(id).classList.remove("hidden");
}

function hide(id) {
  document.getElementById(id).classList.add("hidden");
}

function setRole(role) {
  state.role = role;
  document.getElementById("role-label").textContent =
    role === "teacher" ? "Teacher view" : "Student view";
  // Students can only browse and solve; only teachers can generate.
  hide("choose");
  if (role === "teacher") {
    show("teacher-panel");
  } else {
    hide("teacher-panel");
  }
}

function openExercise(id) {
  fetch(`/api/exercises/${id}`)
    .then((r) => r.json())
    .then((ex) => {
      state.exercise = ex;
      state.currentCode = ex.source;
      document.getElementById("task").textContent = ex.task;
      document.getElementById("editor").value = ex.source;
      document.getElementById("result").textContent = "";
      document.getElementById("result").className = "result";
      hide("finish");
      show("exercise");
      show("verify");
      setTab("source");
      document.getElementById("exercise").scrollIntoView({ behavior: "smooth" });
    });
}

// ---- Load the server's exercise library ------------------------------------

async function loadLibrary() {
  const res = await fetch("/api/exercises", { headers: headers() });
  const items = await res.json();
  const box = document.getElementById("library");
  box.innerHTML = "";
  if (!items.length) {
    box.innerHTML = '<p class="hint">No exercises on the server yet.</p>';
    return;
  }
  for (const item of items) {
    const btn = document.createElement("button");
    btn.className = "kind";
    const title = item.name || `${item.kind} (${item.id})`;
    const done = item.completed ? " ✓" : "";
    btn.innerHTML = `<strong>${title}${done}</strong><span>${item.description || item.task}</span>`;
    btn.addEventListener("click", () => openExercise(item.id));
    box.appendChild(btn);
  }
}

// ---- Teacher interface ------------------------------------------------------

async function teacherLogin() {
  const key = document.getElementById("teacher-key").value;
  const res = await fetch("/api/auth/teacher", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ key }),
  });
  if (!res.ok) {
    alert("Invalid teacher access key.");
    return;
  }
  const data = await res.json();
  state.session = data.session;
  setRole("teacher");
  document.getElementById("teacher-key").value = "";
}

async function teacherGenerate() {
  const prompt = document.getElementById("t-prompt").value;
  const name = document.getElementById("t-name").value;
  const description = document.getElementById("t-desc").value;
  const out = document.getElementById("t-result");
  out.textContent = "Generating…";
  const res = await fetch("/api/exercises/teacher", {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ prompt, name, description }),
  });
  const data = await res.json();
  out.textContent = res.ok
    ? `Stored exercise "${data.name}" (${data.id}).`
    : (data.detail || "Generation failed.");
  if (res.ok) loadLibrary();
}

// ---- Student exercise flow (existing) ---------------------------------------

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
    headers: headers(),
    body: JSON.stringify({ kind }),
  });
  state.exercise = await res.json();
  document.getElementById("task").textContent = state.exercise.task;
  state.currentCode = state.exercise.source;
  document.getElementById("editor").value = state.exercise.source;
  hide("finish");
  document.getElementById("result").textContent = "";
  document.getElementById("result").className = "result";
  show("exercise");
  show("verify");
  setTab("source");
  document.getElementById("exercise").scrollIntoView({ behavior: "smooth" });
  loadLibrary();
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
  }
}

function tabLabel(tab) {
  return { source: "Program", harness: "Harness" }[tab];
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
      headers: headers(),
      body: JSON.stringify({ source }),
    });
    const data = await res.json();
    result.textContent = data.output || (data.passed ? "All cases passed." : "Harness failed.");
    result.classList.toggle("ok", !!data.passed);
    result.classList.toggle("fail", !data.passed);
    if (data.passed) {
      show("finish");
      loadLibrary();
    } else {
      hide("finish");
    }
  } finally {
    runBtn.disabled = false;
    runBtn.classList.remove("busy");
  }
}

function finishExercise() {
  hide("finish");
  const result = document.getElementById("result");
  result.className = "result ok";
  result.textContent = "Exercise completed. You can choose another exercise to keep practising.";
  document.getElementById("browse").scrollIntoView({ behavior: "smooth" });
}

document.getElementById("tab-source").addEventListener("click", () => setTab("source"));
document.getElementById("tab-harness").addEventListener("click", () => setTab("harness"));
document.getElementById("run-verify").addEventListener("click", runVerify);
document.getElementById("finish").addEventListener("click", finishExercise);
document.getElementById("teacher-login").addEventListener("click", teacherLogin);
document.getElementById("t-generate").addEventListener("click", teacherGenerate);

loadLibrary();
loadKinds();
