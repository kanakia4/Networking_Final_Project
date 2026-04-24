from socket import *
import threading
from image_feature import receive_packet, send_packet

clients = {}

class RecieveFromClient(threading.Thread):
    def __init__(self, socket, username):
        threading.Thread.__init__(self)
        self.socket = socket
        self.username = username

    def run(self):
        while True:
            try:
                header, data = receive_packet(self.socket)

                if header is None:
                    print("Client disconnected")
                    break

                if header["type"] == "TEXT":
                    text = data.decode()
                    print("Text received:", text)

                    if text.startswith("@"):
                        parts = text.split(" ", 1)
                        target = parts[0][1:] #gets rid of @ symbol, gets user of dest
                        if target in clients:
                            if len(parts) > 1:
                                message = f"[private from {self.username}]: {parts[1]}"
                            else:
                                message = "[private message]"
                            data2 = message.encode()
                            data2_header = {"type": "TEXT", "filename": "", "size": len(data2), "start_time": 0}
                            send_packet(clients[target], data2_header, data2)
                        else:
                            # user not found
                            error = f"User '{target}' not found.".encode()
                            error_header = {"type": "TEXT", "filename": "", "size": len(error), "start_time": 0}
                            send_packet(self.socket, error_header, error)
                    else:
                        for username, client in clients.items():
                            if client != self.socket:
                                try:
                                    send_packet(client, header, data)
                                except:
                                    pass


                elif header["type"] == "IMAGE":
                    print("Image received:", header["filename"])
                    for username, client in clients.items():
                            if client != self.socket:
                                try:
                                    send_packet(client, header, data)
                                except:
                                    pass

            except:
                print("Error: Connection lost")
                break


        for username, sock in list(clients.items()):
            if sock == self.socket:
                del clients[username]
                break
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
        username = client_socket.recv(1024).decode()
        clients[username] = client_socket
        print("Username registered: ", username)

        # create and start thread
        t1 = RecieveFromClient(client_socket, username)
        t1.start()
    except:
        print("Error: Connection lost")
        break
