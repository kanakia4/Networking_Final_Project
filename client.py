from socket import *
import threading
from image_feature import send_image, send_text, receive_packet, handle_received

class RecieveFromServer(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            try:
                header, data = receive_packet(self.socket)

                if header is None:
                    print("Server disconnected")
                    break

                handle_received(header, data)

            except:
                print("Error: Connection lost")
                break

#EVENTUALLY USE THIS TO GET SERVER
# if (len(sys.argv) < 2):
#   print("Usage: python3 " + sys.argv[0] + " relay_port")
#   sys.exit(1)
# assert(len(sys.argv) == 2)

server_IP= "127.0.0.1" #int(sys.argv[1])
server_port = 5050

client_socket=socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_IP, server_port))

username = input("Enter your username: ")
client_socket.send(username.encode())

# Create and start the thread
t1 = RecieveFromServer(client_socket)
t1.start()

while True:
    try:
        message = input("Enter your message: ")

        if not message.strip():  # ← add this
            continue

        if message.startswith("/sendimage"):

            parts = message.split(" ", 1)

            if len(parts) < 2:

                print("Use: /sendimage filename.jpg")

                continue
            send_image(client_socket, parts[1])

        else:
            send_text(client_socket, message)

        print("\n")
        # client_socket.send(message.encode())

    except:
        print("Error: Connection lost")
        break