@echo off
pyinstaller --hidden-import openai --hidden-import colorama --hidden-import requests --icon=ico.ico --onefile hmini.py
pause