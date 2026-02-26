@echo off
echo [+] Starting Aleopantest Fast Install...
echo [+] Using --no-cache-dir to conserve RAM

python -m pip install setuptools wheel --no-cache-dir
python -m pip install -r requirements.txt --no-cache-dir
python -m pip install -e . --no-cache-dir

echo [+] Installation complete!
echo [+] Run 'alpnts --version' to test.
pause
