
## USB Relay Application
![GuiApp](https://i.imgur.com/pDwbruV.png)
### Description

RelayApp is a Python application designed to provide a user-friendly interface for controlling USB relays. It allows you to easily manage the state of your relays, view their status, and potentially integrate with other systems or devices.
**Prerequisites:**

-   Python 3.x 
-   Relay 1 and 2 is set to GPIO4 and GPIO5 respectively (D2 and D1 in NodeMCU and D1 Mini)

There are two main ways to install RelayApp:

**Running GuiApp:** 
 - Create virtual environment `python -m venv <venv_name>`![enter image description here](https://imgur.com/rmleTFB)
 - Install necessary library `pip install -r requirements.txt`
 - run gui.py `python gui.py`

**Building GuiApp:** 

 - Create virtual environment `python -m venv <venv_name>`
 - Install necessary library `pip install -r requirements.txt`

- Go to your program’s directory and run:
`pyinstaller --noconsole gui.py`

- This will generate the bundle in a subdirectory called `dist`.
 `pyinstaller -F --noconsole gui.py`

- Adding -F (or --onefile) parameter will pack everything into single "exe".
`pyinstaller -F --paths=<venv_name>\Lib\site-packages --noconsole  gui.py`
- Executable file can be found in dist\gui\gui.exe

