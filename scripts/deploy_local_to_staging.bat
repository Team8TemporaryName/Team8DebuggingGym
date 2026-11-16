@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

pushd "%~dp0"

setlocal
  FOR /F "tokens=*" %%i in ('type ..\staging.env') do SET %%i
  
  tar --exclude="../vscode-extension/node_modules" --exclude="../.git" -czf %TEMP%\repo.tar.gz ..
  
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch rm -rf ~/staging_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch mkdir -p ~/staging_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < %TEMP%\repo.tar.gz "cat > ~/repo.tar.gz"
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch tar --strip-components 1 -xPvzf ~/repo.tar.gz -C ~/staging_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < .\compile_extension.sh "cat > ~/staging_app/compile_ext.sh"
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch chmod +777 ~/staging_app/compile_ext.sh
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch ~/staging_app/compile_ext.sh !APP_HOST!:!APP_PORT!
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < ..\staging.env "cat > ~/staging_app/.env"
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < .\run_server.sh "cat > ~/staging_app/run.sh" 
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch chmod +777 ~/staging_app/run.sh
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch ~/staging_app/run.sh %1 &

endlocal

popd
