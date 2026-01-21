import socket
import threading

SERVER = "127.0.0.1"
PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
server.listen()

clients = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle_client(client):
    while True:
        message = client.recv(1024)
        print(f'Message receive: {message}')
        broadcast(message)


print("Server is listening...")
while True:
    client, address = server.accept()
    print(f"Connect with {str(address)}")

    clients.append(client)
    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
