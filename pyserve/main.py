import os
import json
from pathlib import Path
import subprocess
import psutil
import signal


def question(text, post=None, **kwargs):
    while True:
        if len(kwargs) == 1:
            print(post)
            return list(kwargs.keys())[0]
        print(text)
        for i, arg in enumerate(kwargs.values(), 1):
            print(f"({i}): {arg}")
        if post:
            print(post)
        try:
            choose = int(input(f"Choose (1-{len(kwargs)}): "))
        except ValueError:
            continue

        if len(kwargs) >= choose and choose != 0:
            return list(kwargs.keys())[choose - 1]


items = {
    "rb": "Reboot app",
    "kill": "Kill app",
    "strt": "Start app",
    "rm": "Remove pyserve from app",
    "crt": "Create app",
}


def crt():
    path = Path(input("Path to the Python executable file: ")).expanduser()
    if not path.exists():
        print("File not found")
        crt()

    logfile = Path(input("Log file path (log.txt): ")
                   or "log.txt").expanduser()

    pypath = input("Python interpreter path (python): ") or "python"

    process = subprocess.Popen(f"{pypath} -u {path} > {logfile} 2>&1",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    with open(".pyserve", 'w', encoding='utf-8') as cf:
        json.dump({"pid": process.pid, "logfile": str(logfile),
                  "pypath": pypath, "path": str(path)}, cf)


def kill():
    pid = config["pid"]
    if not psutil.pid_exists(pid):
        print("Process not found. Maybe app has been turned off")
    else:
        os.kill(pid, signal.SIGTERM)
        os.kill(pid + 1, signal.SIGTERM)
        print("App killed succesfully")
    config["pid"] = None
    with open(".pyserve", "w", encoding='utf-8') as cf:
        json.dump(config, cf)


def rb():
    pid = config["pid"]
    if psutil.pid_exists(pid):
        os.kill(pid, signal.SIGTERM)
        os.kill(pid + 1, signal.SIGTERM)

    process = subprocess.Popen(f"{config["pypath"]} -u {config["path"]} > {config["logfile"]} 2>&1",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    config["pid"] = process.pid

    with open(".pyserve", 'w', encoding='utf-8') as cf:
        json.dump(config, cf)
    print("App rebooted succesfully")


def rm():
    if not os.path.exists(".pyserve"):
        print("Pyserve isn't installed in this directory")
        return
    os.remove(".pyserve")
    print("Pyserve removed succesfully")


def strt():
    process = subprocess.Popen(f"{config["pypath"]} -u {config["path"]} > {config["logfile"]} 2>&1",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    config["pid"] = process.pid

    with open(".pyserve", 'w', encoding='utf-8') as cf:
        json.dump(config, cf)
    print("App started succesfully")


def main():
    global config
    config = None
    if os.path.exists(".pyserve"):
        with open(".pyserve", "r", encoding="utf-8") as cf:
            config = json.load(cf)

        if config["pid"]:
            menu = ["rb", "kill", "rm"]
        else:
            menu = ["strt", "rm"]
    else:
        menu = ["crt"]

    globals()[question("What do you want to do?",
                       "Press Ctrl+C to stop", **{i: items[i] for i in menu})]()


def start():
    try:
        main()
    except KeyboardInterrupt:
        exit()
