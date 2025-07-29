import os
import sys
import base64
import importlib.util

def check_file(file_path):
    try:
        def space(file_path):
            if not os.path.exists(file_path):
                return False
            return os.path.getsize(file_path) == 0
        if space(file_path):
            print(f"[-] 文件 {file_path} 不正常 - 为空!")
            print(f"[remove] 删除空文件：{file_path} 方便初始化解决问题")
            os.remove(file_path)
            print(f"[remove] 文件 {file_path} 已删除！")
            with open("script_path.txt", 'r', encoding='utf-8') as file:
                script_path = file.read()
                print(script_path)
            _, ext = os.path.splitext(script_path)
            if ext == ".py":
                os.system(f"python {script_path}")
            if ext == ".exe":
                os.system(f"start {script_path}")
            sys.exit(1)
        else:
            print(f"[+] 文件 {file_path} 正常 - 不为空！")
    except FileNotFoundError as e:
        print(f"[-] 文件 {file_path} 不存在 {e}")
        sys.exit(1)

def check_lib():
    def check_package(package_name):
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            return False
        return True

    required_packages = [
        'requests',
        'PyInstaller',
        'Crypto',
        'mss',
        'pyautogui',
        'pyperclip'
    ]

    missing_packages = []
    for package in required_packages:
        if not check_package(package):
            missing_packages.append(package)

    if missing_packages:
        print("以下必需库未安装:")
        for pkg in missing_packages:
            print(f"- {pkg}")
        
        print("\n可以使用以下命令安装缺失的库:")
        print(f"pip install {' '.join(missing_packages)}")

        if 'Crypto' in missing_packages:
            print("\n注意：'Crypto' 通常来自 'pycryptodome' 包，可以尝试:")
            print("pip install pycryptodome")
            print("pip install pycrypto - 不推荐\n⚠注意：pycrypto 已停止维护，可能存在安全漏洞，建议使用 pycryptodome\n")
            print("如果以上指令成功安装，但是还是报错，可以尝试输入 'pip uninstall crypto pycrypto pycryptodome -y' 后再次执行以上命令")
        
        print(f"\n{'=' * 20}  ⚠  注意  ⚠  {'=' * 20}\n如果继续运行程序很有可能出错！\n当前脚本仅支持 Python3-Windows 运行使用\n如果打包成 EXE 可能检测 第三方库 脚本会出现问题！\n{'=' * 54}")
        choose = input("是否继续运行? [Y/N]")
        if choose.lower() in ["Y", "y"]:
            print(f"{choose} | 正在运行...")
            return True
        else:
            print(f"{choose} | 已取消运行")
            sys.exit(1)
    
    print("所有需要的库均已安装！")
    return True

def init():
    print("初始化环境...")
    try:
        print("检查第三方库...")
        print("已安装库的详细信息:")
        os.system(f"pip show requests PyInstaller pycryptodome mss pyautogui pyperclip")
        if not check_lib():
            print("存在未安装的必需库，程序终止运行！")
            sys.exit(1)

        if not os.path.exists("ListenIP_PORT.txt"):
            print("正在创建初始IP:PORT文件...")
            with open("ListenIP_PORT.txt", 'w') as file:
                file.write("127.0.0.1:1000")
                print("初始化IP为127.0.0.1:1000")
        else:
            print("已存在IP_PORT文件...")
            check_file("ListenIP_PORT.txt")

        if not os.path.exists("KEY.txt"):
            print("正在创建初始IP:PORT文件...")
            with open("KEY.txt", 'w') as file:
                key = input("请输入密钥KEY [留空回车使用默认] <KEY>")

                if key == "":
                    key_bytes = os.urandom(32)
                    key_str = base64.b64encode(key_bytes).decode("utf-8")
                else:
                    key_str = key

                file.write(key_str)
                print(f"密钥已设置为：{key}\n后续可以直接在 KEY.txt 文件中修改")
        else:
            print("已存在KEY文件...")
            check_file("KEY.txt")
        
        print("\n初始化完成")
        return True
    except Exception as e:
        print(f"\n初始化错误: {e}")
        sys.exit(1)
