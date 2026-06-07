import socket
import threading
import sys

class ServerUDP:
    def __init__(self, port):
        self.server_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_socket.bind(("0.0.0.0", self.server_port))

        self.clients = {}

    def broadcast(self, message, sender_addr=None):
        for addr in self.clients:
            if addr != sender_addr:
                self.server_socket.sendto(
                    message.encode("utf-8"),
                    addr
                )

    def run(self):
        print(f"UDP CHATROOM running on port {self.server_port}")
        print("Press CTRL+C to stop")

        while True:
            data, client_addr = self.server_socket.recvfrom(1024)

            message = data.decode("utf-8")

            if message.startswith("join:"):
                username = message.split(":")[1]

                self.clients[client_addr] = username

                join_msg = f"User {username} joined the chat."

                print(join_msg)

                self.broadcast(join_msg)

            else:
                print(message)

                self.broadcast(message, client_addr)


class ClientUDP:
    def __init__(self, name, port):
        self.client_name = name

        self.server_addr = ("127.0.0.1", port)

        self.client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

    def receive_messages(self):
        while True:
            try:
                data, _ = self.client_socket.recvfrom(1024)

                print("\n" + data.decode("utf-8"))

            except:
                break

    def run(self):
        join_msg = f"join:{self.client_name}"

        self.client_socket.sendto(
            join_msg.encode("utf-8"),
            self.server_addr
        )

        receive_thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )

        receive_thread.start()

        while True:
            text = input()

            if text.lower() == "exit":
                print("Leaving chat...")
                sys.exit()

            message = f"{self.client_name}: {text}"

            self.client_socket.sendto(
                message.encode("utf-8"),
                self.server_addr
            )