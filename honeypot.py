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

