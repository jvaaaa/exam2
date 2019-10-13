# -*- coding: utf-8 -*-


import socket,re,threading,time
# 引入模块

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket

def khd():
	threading.Thread(target=read_server, args=(s, )).start()

	while True:
		x=input('请输入命令：')
		if re.match(r'^GET\s\S+$',x):
			s.send(x.encode('utf-8'))
			time.sleep(1)

		elif re.match(r'^SET\s\S+\s\S+$',x):
			s.send(x.encode('utf-8'))
			time.sleep(1)

		elif re.match(r'^AUTH\s\S+\s\S+$',x):
			s.send(x.encode('utf-8'))
			time.sleep(1)

		elif re.match(r'^URL\s\S+\s\S+$',x):
			s.send(x.encode('utf-8'))
			time.sleep(1)

		else:
			print('未知的命令')
#检测用户输入,发送至服务端(客户端开启后)并多线程运行read_server	  

def read_server(s):
	while True:
		message = s.recv(2048).decode('utf-8')	
		print(message)
#检测服务端反馈


def kv_client(host='localhost',port=5678):
	print('启动客户端')
	try:
		s.connect((host,port))
		khd()
	except:
		print('连接失败!(服务器无响应)')
#启动连接与服务器无响应错误处理

print('聊天工具启动成功\n')
print('启动客户端输入:kv_client --host [address] --port [port]  /  kv_client(默认为localhost:5678)\n')
#指引

while True:
	x=input('请输入命令：')
	if re.match(r'kv_client$',x):
		kv_client()
		break
	elif re.match(r'kv_client\s--host\s[\w\.]*\s--port\s\d*',x):
		f=re.match(r'kv_client\s--host\s(?P<address>[\w\.]*)\s--port\s(?P<port>\d*)',x)
		kv_client(f.group('address'),int(f.group('port')))
		break
	else:
		print("未知的命令")
		print('启动客户端输入:kv_client --host [address] --port [port]  /  kv_client(默认为localhost:5678)\n')
#检测用户输入(客户端开启前)
