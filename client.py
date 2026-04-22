from socket import *
import threading

class RecieveFromServer(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    print("Server disconnected")
                    break
                print("Data received: ", data.decode(), "\n")
            except:
                print("Error: Connection lost")
                break

#EVENTUALLY USE THIS TO GET SERVER
# if (len(sys.argv) < 2):
#   print("Usage: python3 " + sys.argv[0] + " relay_port")
#   sys.exit(1)
# assert(len(sys.argv) == 2)

server_IP= "127.0.0.1" #int(sys.argv[1])
server_port = 5000

client_socket=socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_IP, server_port))

# Create and start the thread
t1 = RecieveFromServer(client_socket)
t1.start()

while True:
    try:
        data = input("Enter your message: ")
        print("\n")
        client_socket.send(data.encode())
    except:
        print("Error: Connection lost")
        break