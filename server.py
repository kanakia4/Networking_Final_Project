from socket import *
import threading
from image_feature import receive_packet, send_packet

clients = []

class RecieveFromClient(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            try:

                header, data = receive_packet(self.socket)

                if header is None:

                    print("Client disconnected")

                    break

                if header["type"] == "TEXT":

                    print("Text received:", data.decode())

                elif header["type"] == "IMAGE":

                    print("Image received:", header["filename"])

                for client in clients:

                    if client != self.socket:

                        try:

                            send_packet(client, header, data)

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
server_port = 5050

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_IP, server_port))
server_socket.listen()

# Just a test to see if server started
print("Server started on", server_IP, server_port)

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
