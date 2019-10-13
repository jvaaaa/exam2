# -*- coding: utf-8 -*-

import socket,re,threading,time,os,requests
# 引入模块

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
#socket

qwq=1
d={}

def client(sock,addr):
	print('%s:%s已连接' % addr)
	while True:
		data = sock.recv(2048).decode('utf-8')

		if re.match(r'GET\s\S*',data):
			f=re.match(r'GET\s(?P<key>\S*)',data)
			try:
				m=d[f.group('key')]
				sock.send(m.encode('utf-8'))
			except:
				sock.send(' '.encode('utf-8'))

		elif re.match(r'SET\s\S*\s\S*',data):
			f=re.match(r'SET\s(?P<key>\S*)\s(?P<value>\S*)',data)
			d[f.group('key')]=f.group('value')

		elif re.match(r'AUTH\s\S+\s\S+',data):
			f=re.match(r'AUTH\s(?P<username_input>\S+)\s(?P<password_input>\S+)',data)
			username_input=f.group('username_input')
			password_input=f.group('password_input')
			with open('auth.conf','r') as file:
				global qwq
				for line in file:
					text=re.match(r'username\:(?P<username>\S+)\spassword\:(?P<password>\S+)',line)
					username=text.group('username')
					password=text.group('password')
					if username_input==username and password_input==password:
						sock.send('0'.encode('utf-8'))
						qwq=2
				if qwq==1:
					sock.send('-1'.encode('utf-8'))

		elif re.match(r'URL\s\S+\s\S+',data):
			if qwq==2:
				f=re.match(r'URL\s(?P<key>\S+)\s(?P<url>\S+)',data)
				try:
					m=d[f.group('key')]
					sock.send(m.encode('utf-8'))
				except:
					r=requests.get(f.group('url'))
					sock.send(str(len(r.text)).encode('utf-8'))
					d[f.group('key')]=str(len(r.text))
			elif qwq==1:
				sock.send(' '.encode('utf-8'))
#检测客户端输入并反馈

def kv_server(host='localhost',port=5678):
	print('启动服务端')
	return s.bind((host, port))
#服务端启动

print('聊天工具启动成功\n')
print('启动服务端输入:kv_server --host [address] --port [port]  /  kv_server(默认为localhost:5678)\n')
#指引

while True:
	x=input('请输入命令：')
	if re.match(r'kv_server$',x):
		kv_server()
		break
	elif re.match(r'kv_server\s--host\s[\w\.]*\s--port\s\d*',x):
		f=re.match(r'kv_server\s--host\s(?P<address>[\w\.]*)\s--port\s(?P<port>\d*)',x)
		kv_server(f.group('address'),int(f.group('port')))
		break
	else:
		print("未知的命令")
		print('启动服务端输入:kv_server --host [address] --port [port]  /  kv_server(默认为localhost:5678)\n')
#检测用户输入(服务端启动前)

s.listen(5)
print('等待连接...')
#开启监听

while True:
	sock,addr=s.accept()
	threading.Thread(target=client, args=(sock, addr)).start()
#多线程分配
