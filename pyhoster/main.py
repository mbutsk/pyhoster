#!/usr/bin/python3

import os
import json
from pathlib import Path
import subprocess
import psutil
import signal
import argparse

if os.name == "nt":
    print("pyhoster does not support Windows")
    exit()

def choose(text, post=None, **kwargs):
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
            choice = int(input(f"Choose (1-{len(kwargs)}): "))
        except ValueError:
            continue

        if len(kwargs) >= choice and choice != 0:
            return list(kwargs.keys())[choice - 1]


operations = {
    "reboot": "Reboot app",
    "kill": "Kill app",
    "start": "Start app",
    "rm": "Remove pyhoster from app",
    "create": "Create app",
}


def create():
    path = Path(input("Path to the Python executable file: ")).expanduser()
    if not path.exists():
        print("File not found")
        create()

    logfile = Path(input("Log file path (log.txt): ")
                   or "log.txt").expanduser()

    pypath = input("Python interpreter path (python): ") or "python"

    process = subprocess.Popen(f"{pypath} -u {path} > {logfile} 2>&1",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    with open(".pyhoster", 'w', encoding='utf-8') as cf:
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
    with open(".pyhoster", "w", encoding='utf-8') as cf:
        json.dump(config, cf)


def reboot():
    pid = config["pid"]
    if psutil.pid_exists(pid):
        os.kill(pid, signal.SIGTERM)
        os.kill(pid + 1, signal.SIGTERM)

    process = subprocess.Popen(f"{config['pypath']} -u {config['path']} > {config['logfile']} 2>&1",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    config["pid"] = process.pid

    with open(".pyhoster", 'w', encoding='utf-8') as cf:
        json.dump(config, cf)
    print("App rebooted succesfully")


def rm():
    if not os.path.exists(".pyhoster"):
        print("pyhoster isn't installed in this directory")
        return
    pid = config["pid"]

    if psutil.pid_exists(pid):
        os.kill(pid, signal.SIGTERM)
        os.kill(pid + 1, signal.SIGTERM)

    os.remove(".pyhoster")
    print("pyhoster removed succesfully")


def start():
    process = subprocess.Popen(f"{config['pypath']} -u {config['path']} > {config['logfile']} 2>&1",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    config["pid"] = process.pid

    with open(".pyhoster", 'w', encoding='utf-8') as cf:
        json.dump(config, cf)
    print("App started succesfully")


def main():
    global config
    argparser = argparse.ArgumentParser(usage="Just write `pyhoster` in root directory of your project", description="A simple tool for servers that host python projects")
    config = None
    if os.path.exists(".pyhoster"):
        with open(".pyhoster", "r", encoding="utf-8") as cf:
            config = json.load(cf)

        if config["pid"]:
            menu = ["reboot", "kill", "rm"]
        else:
            menu = ["start", "rm"]
    else:
        menu = ["create"]
    
    argparser.add_argument("operation", choices=menu, help="run operation CLI (not TUI)", default=None, nargs='?')
    args = argparser.parse_args()
    if args.operation:
        globals()[args.operation]()
    else:
        globals()[choose("What do you want to do?",
                       "Press Ctrl+C to stop", **{i: operations[i] for i in menu})]()


def launch():
    try:
        main()
    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    launch()