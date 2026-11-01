#!/usr/bin/env bash
cd "$(dirname "$0")"

set -a
. ./.env
set +a

git checkout $1

kill `lsof -t -i:${APP_PORT}`

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT}
