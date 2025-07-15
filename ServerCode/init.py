import os
import sys
import importlib.util

def install_lib(lib):
    spec = importlib.util.find_spec(lib)
    print(f"检测 {lib} 的结果: {spec}")  # 添加调试信息
    if spec is None:
        print(f"缺少 {lib} 库")
        os.system(f"pip show {lib}")
    else:
        print(f"{lib} 已安装")
        return True

def check_lib():
    required_libs = ["requests", "PyInstaller", "Crypto", "mss", "pyautogui", "pyperclip"]
    all_installed = True
    
    for lib in required_libs:
        if not install_lib(lib):
            all_installed = False
    
    if not all_installed:
        print("\n --警告-- \n部分依赖库未安装，程序可能无法正常运行")

def init():
    print("初始化环境...")
    try:
        check_lib()
        print("初始化完成")
    except Exception as e:
        print(f"初始化失败: {e}")
        sys.exit()