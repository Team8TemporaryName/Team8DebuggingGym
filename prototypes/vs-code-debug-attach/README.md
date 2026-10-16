# VS Code debugging prototype

A disposable spike that answers the riskiest Week 2 question:

> Can a learner attach their **own VS Code** to a hosted exercise runtime
> (a container we run) and debug a buggy program with breakpoints?

This is a **code spike, not the product**. It lives on the branch
`feat/vs-code-debug-prototype` and is deliberately **never merged to `main`**.
The record that survives is `reports/week-02/prototypes.md` plus a screenshot;
this folder is throwaway evidence.

## What it does

- `app/buggy_program.py` — a small program with a planted off-by-one bug.
- `app/harness.py` — the pass/fail signal: runs the buggy function against
  known cases and reports which defect is present.
- `Dockerfile` — the exercise runtime: installs `debugpy` (the Python DAP
  server) and exposes port 5678, so VS Code can attach over the network.

## How to run it

### 1. Show the defect is present (harness fails)

```bash
docker build -t debugging-gym-spike .
docker run --rm debugging-gym-spike
```

Expected: the "single element", "three elements", and "two elements" cases
`FAIL` (the loop skips the last element).

### 2. Attach VS Code and debug

Start the container with the debugpy attach server running:

```bash
docker run --rm -p 5678:5678 \
  -e PYTHONUNBUFFERED=1 \
  debugging-gym-spike \
  python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app/harness.py
```

In VS Code:

1. Open a `.vscode/launch.json` in any folder with this configuration:

   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Attach to Debugging Gym container",
         "type": "debugpy",
         "request": "attach",
         "connect": { "host": "localhost", "port": 5678 },
         "pathMappings": [{ "localRoot": "${workspaceFolder}", "remoteRoot": "/app" }]
       }
     ]
   }
   ```

2. Set a breakpoint on `for i in range(len(nums) - 1):` in
   `app/buggy_program.py`.
3. Press the Debug ▶ button and choose **Attach to Debugging Gym container**.
4. Watch execution stop at the breakpoint with a visible stack and variables,
   and confirm the bug by inspecting `i` and `nums`.

## What the spike must prove (acceptance)

- [ ] A container runs the buggy program and the harness reports the defect.
- [ ] VS Code attaches to the container over DAP and hits a breakpoint with a
      visible stack.
- [ ] The spike stays on a feature branch and is never merged to `main`.

## Evidence for the week report

- [ ] Screenshot of VS Code attached with the breakpoint hit → `reports/week-02/images/`
- [ ] Outcome recorded in `reports/week-02/prototypes.md`