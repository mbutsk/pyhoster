import os
import json
from pathlib import Path
import subprocess

def question(text, post=None, **kwargs):
    while True:
        if len(kwargs) == 1:
            print(post)
            return list(kwargs.keys())[0]
        print(text)
        for i, arg in enumerate(kwargs.values(), 1):
            print(f"({i}): {arg}")
        if post: print(post)
        try:
            choose = int(input(f"Choose (1-{len(kwargs)}): "))
        except ValueError:
            continue

        if len(kwargs) >= choose and choose != 0:
            return list(kwargs.keys())[choose - 1]

items = {
    "rb": "Reboot app",
    "kill": "Kill app",
    "start": "Start app",
    "rm": "Remove pyserve from app",
    "crt": "Create app",
}

def crt():
    path = Path(input("Path to the Python executable file: ")).expanduser()
    if not path.exists():
        print("File not found")
        crt()
    
    logfile = Path(input("Log file path (log.txt): ") or "log.txt").expanduser()

    pypath = input("Python interpreter path (python): ") or "python"

    process = subprocess.Popen(f"{pypath} -u {path} > {logfile} 2>&1", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    with open(".pyserve", 'w', encoding='utf-8') as cf:
        json.dump({"pid": process.pid, "logfile": str(logfile), "pypath": pypath, "path": path}, cf)

def main():
    config = None
    if os.path.exists(".pyserve"):
        with open(".pyserve", "r", encoding="utf-8") as cf:
            config = json.load(cf)
        
        if config["pid"]:
            menu = ["rb", "kill", "rm"]
        else:
            menu = ["start", "rm"]
    else:
        menu = ["crt"]
    
    globals()[question("What do you want to do?", "Press Ctrl+C to stop", **{i: items[i] for i in menu})]()


def start():
    try:
        main()
    except KeyboardInterrupt:
        exit()