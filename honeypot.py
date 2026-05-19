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