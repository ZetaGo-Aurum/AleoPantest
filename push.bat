@echo off
cd /d "c:\Users\rayhan\Documents\PantestTool\AleoPantest"
git reset --hard HEAD
git pull origin main --rebase
git push origin main
echo Push completed
