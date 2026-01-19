import socket
import threading
import json

class NetworkHandler:
    def __init__(self, message_callback):
        self.client = None
        self.message_callback = message_callback
        self.token = None
        
    def connect_to_server(self, host='localhost', port=5555):
        """Kết nối đến server"""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((host, port))
            threading.Thread(target=self.receive_messages, daemon=True).start()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def send_message(self, message):
        """Gửi tin nhắn đến server"""
        try:
            if self.client:
                self.client.send(json.dumps(message).encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_messages(self):
        """Nhận tin nhắn từ server"""
        while True:
            try:
                data = self.client.recv(4096).decode('utf-8')
                if data:
                    message = json.loads(data)
                    self.message_callback(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def close(self):
        """Đóng kết nối"""
        if self.client:
            self.client.close()