import socket
import threading
import paramiko
import logging
from datetime import datetime

# setup logging
logging.basicConfig(
    filename='attack_logs.json',
    level=logging.INFO,
    format='%(message)s'
)

HOST = '0.0.0.0'
PORT = 2222  # fake SSH port

class FakeSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        # log every login attempt
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "ip": self.client_ip,
            "username": username,
            "password": password
        }
        logging.info(str(log_entry))
        print(f"[ATTACK] {self.client_ip} tried {username}:{password}")
        return paramiko.AUTH_FAILED  # always fail

    def get_allowed_auths(self, username):
        return 'password'
    
def handle_connection(client_socket, client_ip):
    transport = paramiko.Transport(client_socket)
    
    # generate a fake server key
    host_key = paramiko.RSAKey.generate(2048)
    transport.add_server_key(host_key)
    
    server = FakeSSHServer(client_ip)
    
    try:
        transport.start_server(server=server)
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