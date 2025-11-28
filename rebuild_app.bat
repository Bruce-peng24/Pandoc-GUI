@echo off
cd /d "C:\Practice-code\Pandoc-GUI"

echo Rebuilding Pandoc-GUI with all necessary dependencies...
echo This script uses the configuration that successfully built your app
echo.

REM Build command with all required dependencies
pyinstaller --onefile --windowed --name="Pandoc-GUI" --add-data "src;src" --collect-all PyQt5 --collect-all docx --collect-all python-docx --collect-all ntplib app_minimal_fixed.py

echo.
echo Build complete! Executable located at dist\Pandoc-GUI.exe
echo Press any key to exit...
pause > nul