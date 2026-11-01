@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

pushd "%~dp0"

setlocal
  FOR /F "tokens=*" %%i in ('type ..\staging.env') do SET %%i
  
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch rm -rf ~/staging_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch mkdir -p ~/staging_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch git clone !REPO_LINK! ~/staging_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < ..\staging.env "cat > ~/staging_app/.env"
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < .\run_server.sh "cat > ~/staging_app/run.sh" 
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch chmod +777 ~/staging_app/run.sh
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch ~/staging_app/run.sh %1 &

endlocal

popd
