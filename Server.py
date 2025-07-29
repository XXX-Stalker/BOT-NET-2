import sys
import os
from ServerCode.init import init

script_path = os.path.abspath(__file__)

title = """
 ███████████     ███████    ███████████ ██████   █████ ██████████ ███████████             ████████ 
░░███░░░░░███  ███░░░░░███ ░█░░░███░░░█░░██████ ░░███ ░░███░░░░░█░█░░░███░░░█            ███░░░░███
 ░███    ░███ ███     ░░███░   ░███  ░  ░███░███ ░███  ░███  █ ░ ░   ░███  ░            ░░░    ░███
 ░██████████ ░███      ░███    ░███     ░███░░███░███  ░██████       ░███     ██████████   ███████ 
 ░███░░░░░███░███      ░███    ░███     ░███ ░░██████  ░███░░█       ░███    ░░░░░░░░░░   ███░░░░  
 ░███    ░███░░███     ███     ░███     ░███  ░░█████  ░███ ░   █    ░███                ███      █
 ███████████  ░░░███████░      █████    █████  ░░█████ ██████████    █████              ░██████████
░░░░░░░░░░░     ░░░░░░░       ░░░░░    ░░░░░    ░░░░░ ░░░░░░░░░░    ░░░░░               ░░░░░░░░░░ 
XXX-STALKER
---------------------------------------------------------------------------------------------------
"""

if __name__ == "__main__":
    with open("script_path.txt", 'w') as file:
        file.write(script_path)
    init()
    with open("ListenIP_PORT.txt", 'r') as file:
        address = file.read().strip()
        print(f"\n连接监听地址：{address}")
        if ':' in address:
            host, port_str = address.split(':', 1)
            try:
                port = int(port_str)
            except ValueError:
                print(f"错误：端口号必须为整数，当前为 '{port_str}'")
                sys.exit(1)
        else:
            print(f"错误：文件格式应为 'IP:PORT'，当前为 '{address}'")
            sys.exit(1)
    from ServerCode.Server import Server
    server = Server(host=host, port=port)
    server.root.mainloop()
