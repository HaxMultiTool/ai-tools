@echo off
pyinstaller --hidden-import openai --hidden-import colorama --icon=ico.ico --onefile moderated.py
pause