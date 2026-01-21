import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))


def receive():
    while True:
        message = client.recv(1024).decode('ascii')
        print(message)


def write():
    while True:
        message = input('')
        client.send(message.encode('ascii'))


thread = threading.Thread(target=receive)
thread.start()

write()
