@echo off
setlocal

set "TS=Placeholder"

set /p T2S=^>
if not "%T2S%"=="" set "TS=%T2S%"

powershell -command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('%TS%');"

endlocal
