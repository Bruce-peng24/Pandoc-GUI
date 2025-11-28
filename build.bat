@echo off
cd /d "C:\Practice-code\Pandoc-GUI"
pyinstaller --onefile --windowed --hidden-import=ui --hidden-import=ui.main_window --add-data "src/ui;ui" src/main.py
echo Packing complete. Check the dist folder for the executable.
pause