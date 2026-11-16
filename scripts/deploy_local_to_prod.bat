@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

pushd "%~dp0"

setlocal
  FOR /F "tokens=*" %%i in ('type ..\prod.env') do SET %%i
  
  tar --exclude="../vscode-extension/node_modules" --exclude="../.git" -czf %TEMP%\repo.tar.gz ..
  
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch rm -rf ~/prod_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch mkdir -p ~/prod_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < %TEMP%\repo.tar.gz "cat > ~/repo.tar.gz"
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch tar --strip-components 1 -xPvzf ~/repo.tar.gz -C ~/prod_app
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < .\compile_extension.sh "cat > ~/prod_app/compile_ext.sh"
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch chmod +777 ~/prod_app/compile_ext.sh
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch ~/prod_app/compile_ext.sh !APP_HOST!:!APP_PORT!
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < ..\prod.env "cat > ~/prod_app/.env"
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch < .\run_server.sh "cat > ~/prod_app/run.sh" 
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch chmod +777 ~/prod_app/run.sh
  plink !SSH_USER!@!SERVER_IP! -pw !SSH_PASSWORD! -batch ~/prod_app/run.sh %1 &

endlocal

popd
