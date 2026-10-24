# Setup and run

This page tells a newcomer how to install, configure, run, and test the
Debugging Gym minimum usable product from a clean checkout. Following it end to
end completes the core task: choose a problem kind, get a generated exercise,
connect your own VS Code, and verify the fix against the harness.

## Prerequisites

- Python 3.11 or newer.
- A terminal. Docker is needed only for the real debug-environment container;
  the web slice runs without it.

## Install

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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

## Run the checks and the tests

Check Markdown and links (as CI does):

```bash
npx --yes markdownlint-cli2 '**/*.md'
lychee './**/*.md'
```

Run the automated tests:

```bash
python -m pytest tests/ -q
```

The tests assert that every generated exercise starts with a planted defect the
harness reports, and that the verdict flips to a pass once the fix is applied.