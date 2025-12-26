@echo off
cd /d "%~dp0"
git reset --hard HEAD
git pull origin main --rebase
git push origin main
echo Push completed
