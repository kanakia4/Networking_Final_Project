from socket import *
import threading

clients = []

class RecieveFromClient(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    print("Client disconnected")
                    break
                print("Data received: ", data.decode(), "\n")
                for client in clients:
                    if client != self.socket:
                        # client.send(data)
                        try:
                            client.send(data)
                        except:
                            pass
            except:
                print("Error: Connection lost")
                break
        if self.socket in clients:
            clients.remove(self.socket)
        self.socket.close()

#EVENTUALLY USE THIS TO GET SERVER
# if (len(sys.argv) < 2):
#   print("Usage: python3 " + sys.argv[0] + " relay_port")
#   sys.exit(1)
# assert(len(sys.argv) == 2)

server_IP = "127.0.0.1" #int(sys.argv[1])
server_port = 5000

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_IP, server_port))
server_socket.listen()

while True:
    try:
        client_socket, client_address = server_socket.accept()
        print("Client connected: ", client_address)
        clients.append(client_socket)
        # create and start thread
        t1 = RecieveFromClient(client_socket)
        t1.start()
    except:
        print("Error: Connection lost")
        break
