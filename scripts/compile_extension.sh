#!/usr/bin/env bash

cd "$(dirname "$0")"
cd vscode-extension

sed -i -e "s/http:\/\/localhost:8000/$1/g" ./package.json

npm ci
npx vsce package
