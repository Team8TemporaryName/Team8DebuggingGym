# Debugging Gym — VS Code extension

A VS Code extension that brings the Debugging Gym flow into the learner's own
editor, per the customer's Week 3 decision to move toward a VS Code extension
([`DEC-012`](../docs/decisions.md#dec-012)).

It offers the same functionality as the web app, so a learner never has to
leave VS Code:

1. **Choose a problem kind** (`Debugging Gym: Choose a problem kind`) — pick a
   kind from the catalogue served by the web app.
2. **New exercise** (`Debugging Gym: New exercise`) — generate an exercise for
   the kind, write the source to `exercise.py` in the workspace, and open it.
3. **Show task** (`Debugging Gym: Show task`) — read the exercise instruction.
4. **Verify fix** (`Debugging Gym: Verify fix against the harness`) — POST the
   current editor content to the harness and show the pass/fail verdict in the
   output channel.

## How it works

The extension is a thin client over the Debugging Gym web app's HTTP API. It
does not re-implement generation or the harness; it calls:

- `GET /api/kinds` — the catalogue.
- `POST /api/exercises` — generate an exercise.
- `POST /api/exercises/{id}/verify` — verify the fix against the harness.

Configure the app's base URL with the `debuggingGym.baseUrl` setting (default
`http://localhost:8000`).

## Build and run

```bash
cd vscode-extension
npm install
npm run compile        # compiles src/ to out/
code --extensionDevelopmentPath=.   # or F5 from the extension in VS Code
```

## Run the app it talks to

```bash
# from the repository root
. .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then open a folder in VS Code, run the extension, and use its commands.
