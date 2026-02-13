import socket

HOST = "127.0.0.1"
PORT = 5050

class SocketServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(1)
        print("Waiting for Unity connection...")
        self.client, addr = self.server.accept()
        print("Unity connected:", addr)

    def send(self, message):
        try:
            self.client.sendall(message.encode("utf-8"))
        except:
            print("Unity disconnected")
