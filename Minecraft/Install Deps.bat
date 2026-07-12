echo off
echo Upgrading Pip
echo.
python -m pip install --upgrade pip
echo.
echo Installing Dependencies
echo.
python -m pip install -r requirements.txt
echo Dependencies Installed
echo.
pause