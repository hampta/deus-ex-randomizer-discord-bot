@echo off
.\venv\scripts\python -m nuitka --onefile --show-modules --enable-plugin=upx --upx-binary=.\upx.exe --standalone --output-dir=build --windows-icon-from-ico=./icon.ico --prefer-source-code -o ./DiscordCrowdControl.exe --lto=yes --jobs=8 --no-pyi-file ./OfflineCrowdControl.py
pause