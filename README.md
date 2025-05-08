# pyhoster

pyhoster is a tool for those who host Python projects on their servers. It can reboot, kill processes, and more.

## Usage

### TUI

Just write pyhoster in the root directory of the project and follow the instructions.

### CLI

In the root directory of the project, write `pyhoster kill` to kill the process, `pyhoster reboot` to reboot, etc.
`pyhoster -h` / `pyhoster --help` for full list available commands in moment

## Installation

### Windows / MacOS

The project is available on Pypi, so you can run:

```bash
pip install pyhoster
```

### Arch Linux

[![AUR Version](https://img.shields.io/aur/version/pyhoster?style=for-the-badge&logo=arch%20linux&logoColor=white)](https://aur.archlinux.org/packages/pyhoster)

If you use [yay](https://github.com/Jguer/yay) as an AUR helper, run

```bash
yay -S pyhoster
```

### MacOS / Windows / Linux

You can install pyhoster with [pipx](https://github.com/pypa/pipx). It downloads command-line programs using virtual environments.
Just run:

```bash
pipx install pyhoster
```
