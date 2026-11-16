@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

pushd "%~dp0"

setlocal
  FOR /F "tokens=*" %%i in ('type ..\.env') do SET %%i
  pushd ..
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  popd
endlocal

popd
