import struct
import json
import time
import os

# -----------------------------
# Helper: send packet
# -----------------------------
def send_packet(sock, header, data):
    header_bytes = json.dumps(header).encode()

    # send header size first
    sock.sendall(struct.pack("!I", len(header_bytes)))

    # send header
    sock.sendall(header_bytes)

    # send actual data
    sock.sendall(data)


# -----------------------------
# Helper: receive exact bytes
# -----------------------------
def receive_exact(sock, size):
    data = b""
    while len(data) < size:
        part = sock.recv(size - len(data))
        if not part:
            return None
        data += part
    return data


# -----------------------------
# Receive full packet
# -----------------------------
def receive_packet(sock):
    header_size_data = receive_exact(sock, 4)
    if not header_size_data:
        return None, None

    header_size = struct.unpack("!I", header_size_data)[0]

    header_data = receive_exact(sock, header_size)
    if not header_data:
        return None, None

    header = json.loads(header_data.decode())

    data_size = header["size"]
    data = receive_exact(sock, data_size)

    return header, data


# -----------------------------
# Client: send image
# -----------------------------
def send_image(sock, filepath):
    if not os.path.exists(filepath):
        print("Image not found.")
        return

    with open(filepath, "rb") as f:
        image_data = f.read()

    header = {
        "type": "IMAGE",
        "filename": os.path.basename(filepath),
        "size": len(image_data),
        "start_time": time.time()
    }

    send_packet(sock, header, image_data)
    print("Image sent:", filepath)


# -----------------------------
# Client: send text
# -----------------------------
def send_text(sock, message):
    data = message.encode()

    header = {
        "type": "TEXT",
        "filename": "",
        "size": len(data),
        "start_time": time.time()
    }

    send_packet(sock, header, data)


# -----------------------------
# Client: handle received data
# -----------------------------
def handle_received(header, data):
    if header["type"] == "TEXT":
        print("\nData received:", data.decode(), "\n")

    elif header["type"] == "IMAGE":
        filename = "received_" + header["filename"]

        with open(filename, "wb") as f:
            f.write(data)

        end_time = time.time()
        transfer_time = end_time - header["start_time"]

        print("\nImage received:", filename)
        print("Size:", header["size"], "bytes")
        print("Time:", round(transfer_time, 4), "sec")

        if transfer_time > 0:
            speed = header["size"] / transfer_time
            print("Speed:", round(speed, 2), "bytes/sec\n")