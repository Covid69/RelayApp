
## USB Relay Application

### Description

RelayApp is a Python application designed to provide a user-friendly interface for controlling USB relays. It allows you to easily manage the state of your relays, view their status, and potentially integrate with other systems or devices.
**Prerequisites:**

-   Python 3.x 

There are two main ways to install RelayApp:

**Running GuiApp:** 
 - Create virtual environment `python -m venv <venv_name>`
 - Install necessary library `pip install -r requirements.txt`
 - run gui.py `python gui.py`

**Building GuiApp:** 

 - Create virtual environment `python -m venv <venv_name>`
 - Install necessary library `pip install -r requirements.txt`

- Go to your program’s directory and run:
`python pyinstaller gui.py`

- This will generate the bundle in a subdirectory called `dist`.
 `python pyinstaller -F gui.py`

- Adding -F (or --onefile) parameter will pack everything into single "exe".
`python pyinstaller -F --paths=<venv_name>\Lib\site-packages  gui.py`
- Executable file can be found in dist\gui\gui.exe

