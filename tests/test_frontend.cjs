"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { test } = require("node:test");

const frontendPath = path.join(__dirname, "..", "app", "static", "app.js");
const frontendSource = fs.readFileSync(frontendPath, "utf8");

class FakeClassList {
  constructor(owner) {
    this.owner = owner;
  }

  _tokens() {
    return new Set(this.owner.className.split(/\s+/).filter(Boolean));
  }

  add(...tokens) {
    const current = this._tokens();
    tokens.forEach((token) => current.add(token));
    this.owner.className = [...current].join(" ");
  }

  remove(...tokens) {
    const current = this._tokens();
    tokens.forEach((token) => current.delete(token));
    this.owner.className = [...current].join(" ");
  }

  contains(token) {
    return this._tokens().has(token);
  }

  toggle(token, force) {
    const current = this._tokens();
    const shouldAdd = force === undefined ? !current.has(token) : force;
    if (shouldAdd) current.add(token);
    else current.delete(token);
    this.owner.className = [...current].join(" ");
    return shouldAdd;
  }
}

class FakeElement {
  constructor(id = "created") {
    this.id = id;
    this.value = "";
    this.textContent = "";
    this.innerHTML = "";
    this._className = "";
    this.classList = new FakeClassList(this);
    this.listeners = new Map();
    this.children = [];
    this.disabled = false;
  }

  get className() {
    return this._className;
  }

  set className(value) {
    this._className = value || "";
  }

  addEventListener(eventName, callback) {
    this.listeners.set(eventName, callback);
  }

  async click() {
    const callback = this.listeners.get("click");
    assert.ok(callback, `No click handler registered for ${this.id}`);
    return callback();
  }

  appendChild(child) {
    this.children.push(child);
  }

  scrollIntoView() {}
}

function jsonResponse(value) {
  return { json: async () => value };
}

function makeFrontend(verificationResult) {
  const ids = [
    "kinds",
    "task",
    "editor",
    "finish",
    "result",
    "exercise",
    "verify",
    "code",
    "tab-source",
    "tab-harness",
    "run-verify",
    "choose",
  ];
  const elements = new Map(ids.map((id) => [id, new FakeElement(id)]));
  const tabs = ["Program", "Harness", "VS Code"].map((label) => {
    const tab = new FakeElement(`tab-${label}`);
    tab.textContent = label;
    tab.className = "tab";
    return tab;
  });
  const requests = [];

  const document = {
    getElementById(id) {
      if (!elements.has(id)) elements.set(id, new FakeElement(id));
      return elements.get(id);
    },
    querySelectorAll(selector) {
      return selector === ".tab" ? tabs : [];
    },
    createElement(tagName) {
      return new FakeElement(tagName);
    },
  };

  const fetch = async (url, options = {}) => {
    requests.push({ url, options });
    if (url === "/api/kinds") {
      return jsonResponse({ "off-by-one": { summary: "A sequence ends too early." } });
    }
    if (url === "/api/exercises" && options.method === "POST") {
      return jsonResponse({
        id: "ex-test",
        kind: "off-by-one",
        task: "Fix the off-by-one defect.",
        source: "def total(nums):\n    return 0\n",
        harness: "def run():\n    return True\n",
      });
    }
    if (url === "/api/exercises/ex-test/verify" && options.method === "POST") {
      return jsonResponse(verificationResult);
    }
    throw new Error(`Unexpected fetch request: ${url}`);
  };

  const context = vm.createContext({ document, fetch, console, JSON, Object, Promise });
  vm.runInContext(frontendSource, context, { filename: "app/static/app.js" });
  return { context, elements, requests, tabs };
}

async function flushInitialLoad() {
  await new Promise((resolve) => setImmediate(resolve));
}

test("loads the problem catalogue and displays a selected exercise", async () => {
  const app = makeFrontend({ passed: true, output: "PASS" });
  await flushInitialLoad();

  const kinds = app.elements.get("kinds");
  assert.equal(kinds.children.length, 1);
  assert.match(kinds.children[0].innerHTML, /off-by-one/);

  await kinds.children[0].click();
  assert.equal(app.elements.get("task").textContent, "Fix the off-by-one defect.");
  assert.match(app.elements.get("editor").value, /def total/);
  assert.ok(app.elements.get("verify").classList.contains("hidden") === false);
  assert.ok(app.requests.some((request) => request.url === "/api/exercises"));
});

test("submits edited source and displays a passing verification result", async () => {
  const app = makeFrontend({ passed: true, output: "PASS: all cases passed" });
  await app.context.newExercise("off-by-one");
  const source = "def total(nums):\n    return sum(nums)\n";
  app.elements.get("editor").value = source;

  await app.context.runVerify();

  const request = app.requests.find((item) => item.url === "/api/exercises/ex-test/verify");
  assert.ok(request, "verification API must be called");
  assert.equal(request.options.method, "POST");
  assert.deepEqual(JSON.parse(request.options.body), { source });
  assert.equal(app.elements.get("result").textContent, "PASS: all cases passed");
  assert.ok(app.elements.get("result").classList.contains("ok"));
  assert.ok(!app.elements.get("result").classList.contains("fail"));
  assert.ok(!app.elements.get("finish").classList.contains("hidden"));
  assert.equal(app.elements.get("run-verify").disabled, false);
  assert.ok(!app.elements.get("run-verify").classList.contains("busy"));
});

test("displays a failing verification result without offering completion", async () => {
  const app = makeFrontend({ passed: false, output: "FAIL: one case failed" });
  await app.context.newExercise("off-by-one");

  await app.context.runVerify();

  assert.equal(app.elements.get("result").textContent, "FAIL: one case failed");
  assert.ok(app.elements.get("result").classList.contains("fail"));
  assert.ok(!app.elements.get("result").classList.contains("ok"));
  assert.ok(app.elements.get("finish").classList.contains("hidden"));
  assert.equal(app.elements.get("run-verify").disabled, false);
  assert.ok(!app.elements.get("run-verify").classList.contains("busy"));
});
