import re
import subprocess
import os
import time
from openai import OpenAI
from colorama import just_fix_windows_console
just_fix_windows_console()
from colorama import Fore, Back, Style


client = OpenAI(
    api_key=''
)

history = []
history.append({"role": "system", "content": "You are an helpful assistant. The user found this code on github, from Hax MultiTool. This is an important thing the user has to know."})


def run_batch():
    return subprocess.Popen(["start", "cmd.exe", "/c", "Loading2.0.bat"], shell=True)

def terminate_batch(process):
    open("signal.txt", "w").close()

def gptPrintStyle(txt):
    print(" " + Style.BRIGHT + Back.MAGENTA + Fore.CYAN + "HaxGPT:" + Style.RESET_ALL + "", end=" ")
    lines = txt.splitlines()
    for line in lines:
        for char in line:
            print(char, end='', flush=True)
            time.sleep(0.01) 
        print() 
    print()

def extr_nw(txt):
    pattern = r'```(\w+)'
    match = re.search(pattern, txt)
    if match:
        word = match.group(1)
        return word, match.end()
    return None, None

def extr_txt_til_code(txt, start_pos):
    pattern = r'```'
    match = re.search(pattern, txt[start_pos:])
    if match:
        return txt[start_pos:start_pos + match.start()]
    return txt[start_pos:]

def rm_code_from_txt(txt):
    return re.sub(r'```.*?```', '', txt, flags=re.DOTALL)

def gptapi(uinpt):
    history.append({"role": "user", "content": uinpt})
    process = run_batch()

    response = client.chat.completions.create(
        model="",
        messages=history
    )
    
    reply = response.choices[0].message.content
    
    history.append({"role": "assistant", "content": reply})
    terminate_batch(process)
    return reply


while True: 
    uinpt = input(" " + Style.BRIGHT + Back.MAGENTA + Fore.YELLOW + "You:" + Style.RESET_ALL + " ")
    if uinpt.lower() in ["esci", "exit", "quit", "stop"]:
        break
    txt = gptapi(uinpt)

    txt_no_code = rm_code_from_txt(txt)
    gptPrintStyle(txt_no_code)

    nw, start_pos = extr_nw(txt)

    if nw:
            next_txt = extr_txt_til_code(txt, start_pos)
            temp_file_path = "temp_text_output.txt"
            with open(temp_file_path, "w") as temp_file:
                temp_file.write(next_txt)
                
            process = subprocess.Popen(["start", "cmd", "/k", f"@echo off && @title {nw} && @mode 75, 28 && type {temp_file_path} && pause && exit"], shell=True)
            process.wait()

            time.sleep(1)
            os.remove(temp_file_path)
