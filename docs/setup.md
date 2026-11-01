# Setup and run

This page tells a newcomer how to install, configure, run, and test the
Debugging Gym minimum usable product from a clean checkout. Following it end to
end completes the core task: choose a problem kind, get a generated exercise,
connect your own VS Code, and verify the fix against the harness.

## Prerequisites

- Python 3.11 or newer.
- Node.js 22 or newer, required for the browser frontend tests.
- A terminal.
- Docker, required only for the real debug-environment container.

## Install

Create a virtual environment and install the Python dependencies, including the
pinned development linter:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Install the VS Code extension's locked dependencies:

```bash
npm ci --prefix vscode-extension
```

## Configure

Copy the example configuration and edit it:

```bash
cp .env.example .env
```

Leave `LLM_API_KEY` empty to use the deterministic local generator, which needs
no network or budget. To use the LLM, set `LLM_API_KEY` to your provider key
and, if needed, `LLM_ENDPOINT` and `LLM_MODEL`. `.env` is git-ignored and never
committed.

## Run the product

Start the web server:

```bash
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. Choose a problem kind, read the generated
exercise, and edit the program in the editor. Press **Run the harness** to get
a pass/fail verdict: it fails while the planted defect is present and passes
once you fix it.

### Connect your own VS Code

The web slice returns a `launch.json` (the **VS Code** tab) that connects your
editor to the debug environment over the Debug Adapter Protocol. To run the
real debug environment container:

```bash
docker build -t debugging-gym-debug deploy/
docker run --rm -p 5678:5678 -v "$PWD/deploy/example/exercise.py:/app/exercise.py" debugging-gym-debug
```

Then, in VS Code, paste the `launch.json` from the app, set a breakpoint, and
attach. This is the same path the Week 2 prototype proved.

## Run the checks and tests

Run Python linting and formatting checks:

```bash
ruff check app tests
ruff format --check app tests
```

Type-check and build the VS Code extension:

```bash
cd vscode-extension
npm ci
npx tsc --noEmit -p tsconfig.json
npm run compile
cd ..
```

Check Markdown and links (as CI does):

```bash
npx --yes markdownlint-cli2 '**/*.md'
lychee './**/*.md'
```

Run the full automated test suite from the repository root. This runs the Python
tests and the Node.js tests for `app/static/app.js`:

```bash
python -m pytest tests/ -q
```

Run the frontend tests directly when debugging them:

```bash
node --test tests/test_frontend.cjs
```
