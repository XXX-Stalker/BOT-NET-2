from PyInstaller.__main__ import run

opts = [
    "--onefile",
    "--icon", "developer/BOTNET2.ico",
    "--name", "BOTNET-2",
    
    "Server.py",
    
    "ServerCode/Server.py",
    "ServerCode/__init__.py",
    "ServerCode/init.py",
    ]

run(opts)
