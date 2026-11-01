@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

pushd "%~dp0"

IF "%~1"=="" (
  set commit=main
) ELSE (
  set commit=%1
)

setlocal
  FOR /F "tokens=*" %%i in ('type ..\prod.env') do SET %%i
  
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch rm -rf ~/prod_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch mkdir -p ~/prod_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch git clone !REPO_LINK! ~/prod_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < ..\prod.env "cat > ~/prod_app/.env"
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < .\run_server.sh "cat > ~/prod_app/run.sh" 
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch chmod +777 ~/prod_app/run.sh
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch ~/prod_app/run.sh %commit% &

endlocal

popd
