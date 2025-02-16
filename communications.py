import socket
import threading
from message import Message


##################
#This Class is only for IOT Devices, it defines sending and receiving basic tcp messages with:
#Connect, Send, Receive, Close

class IOTServerCommunicator:
    def __init__(self, host: str = "localhost", port: int = 8089):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.running = False

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"IoT Server listening on {self.host}:{self.port}")

        while self.running:
            client_socket, addr = self.server_socket.accept()
            print(f"New IoT device connected from {addr}")
            self.clients.append(client_socket)
            threading.Thread(target=self._handle_client, args=(client_socket,), daemon=True).start()

    def _handle_client(self, client_socket):
        try:
            while True:
                message = Message.read_bytes(client_socket)
                print(f"Received: Device {message.get_deviceId()}, Session {message.get_sessionId()}, Type {message.get_type()}, Data {message.get_data()}")

                response = Message(
                    device_id=message.get_deviceId(),
                    session_id=message.get_sessionId(),
                    type=b'\x02',
                    data=b"ACK"
                )
                response.write_bytes(client_socket)

        except (ConnectionResetError, BrokenPipeError):
            print("IoT device disconnected")
        finally:
            client_socket.close()
            self.clients.remove(client_socket)

    def stop(self):
        self.running = False
        for client in self.clients:
            client.close()
        self.server_socket.close()
        print("IoT Server stopped")


##################
#This Class is only for IOT Devices, it defines sending and receiving basic tcp messages with:
#Connect, Send, Receive, Close
class IOTDeviceCommunicator:
    def __init__(self, host: str = "localhost", port: int = 8089):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
 
        self.client_socket.connect((self.host, self.port))
        print(f"IoT Device connected to server {self.host}:{self.port}")

    def send_message(self, message: Message):

        message.write_bytes(self.client_socket)

    def receive_message(self) -> Message:

        return Message.read_bytes(self.client_socket)

    def close(self):
        self.client_socket.close()
        print("IoT Device disconnected from server")



# Testing to see if it works
if __name__ == "__main__":
    server = IOTServerCommunicator()
    threading.Thread(target=server.start, daemon=True).start()

    device = IOTDeviceCommunicator()
    device.connect()

    msg = Message(device_id=1, session_id=1234, type=b'\x01', data=b"Hello, IoT Server!")
    device.send_message(msg)

    response = device.receive_message()
    print(f"Server Response: Device {response.get_deviceId()}, Session {response.get_sessionId()}, Type {response.get_type()}, Data {response.get_data()}")

    device.close()
