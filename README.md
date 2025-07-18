![BOT-NET-Logo](developer/BOTNETLogo-2.jpg)

<span style="font-size:48px;">BOT-NET-2</span>

<span style="font-size:24px;">概述</span>

这是一个基于Python实现的僵尸网络(BOTNET)服务器控制程序，提供图形化界面(GUI)用于管理和控制被感染的客户端机器。该程序允许服务器操作者向连接的客户端发送命令、发起分布式拒绝服务(DDoS)攻击、进行CC攻击等。

<span style="font-size:24px;">主要功能</span>

客户端管理：

实时显示所有连接的客户端IP、端口和状态

支持断开或删除选中的客户端

可创建自定义客户端程序并打包为可执行文件

远程命令执行：

向所有或选中的客户端发送任意系统命令

命令执行结果加密传输回服务器

攻击功能：

DDoS攻击：支持UDP和SYN洪水攻击

CC攻击：模拟大量HTTP请求压垮目标网站

客户端特性：

支持开机自启动

可自删除功能

加密通信防止内容被截获

技术特点
加密通信：使用AES-256 CBC模式加密所有网络通信

跨平台：客户端仅支持Windows，我们后续在适配其它系统

图形界面：基于Tkinter的直观GUI操作界面

模块化设计：攻击模块与核心控制分离

<span style="font-size:24px;">安全警告</span>

此程序仅限合法授权下的网络安全研究使用。未经授权使用此程序攻击他人系统是违法行为，可能导致严重后果。开发者不对任何滥用行为负责。

<span style="font-size:24px;">使用方法</span>
运行Server.py启动控制服务器

通过"创建客户端"功能生成客户端程序

客户端程序在目标机器运行后会自动连接服务器

通过GUI界面管理客户端并发起各种操作

<span style="font-size:24px;">免责声明</span>

本介绍仅供技术研究参考，请遵守当地法律法规，勿将此程序用于非法用途。

<span style="font-size:24px;">注意</span>

需要安装指定的python第三方库，否则无法打包！
