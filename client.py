import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = 'hello world'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

s.send(bytes(MESSAGE, 'UTF-8'))
data = s.recv(BUFFER_SIZE)

s.close()

print ('recieved data: {}'.format(data))
