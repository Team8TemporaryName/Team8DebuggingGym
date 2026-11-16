@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

pushd "%~dp0/.."

markdownlint-cli2 "./**/*.md" --config .markdownlint-cli2.jsonc --fix

popd
