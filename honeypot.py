import socket
import threading
import paramiko
import logging
from datetime import datetime
from logger import log_attempt

HOST = '0.0.0.0'
PORT = 2222

class FakeSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        entry = log_attempt(self.client_ip, username, password)
        print(f"[ATTACK] {self.client_ip} tried {entry['username']}:{entry['password']} | common_user={entry['is_common_username']} | common_pass={entry['is_common_password']}")
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

def handle_connection(client_socket, client_ip):
    transport = paramiko.Transport(client_socket)
    host_key = paramiko.RSAKey.generate(2048)
    transport.add_server_key(host_key)
    server = FakeSSHServer(client_ip)
    try:
        transport.start_server(server=server)
        channel = transport.accept(20)
        if channel:
            channel.close()
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        transport.close()

def start_honeypot():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(100)
    print(f"[*] Honeypot listening on port {PORT}...")
    while True:
        client, addr = sock.accept()
        client_ip = addr[0]
        print(f"[*] Connection from {client_ip}")
        thread = threading.Thread(target=handle_connection, args=(client, client_ip))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    start_honeypot()