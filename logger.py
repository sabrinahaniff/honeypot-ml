import json
import os
from datetime import datetime

LOG_FILE = 'attack_logs.json'

def log_attempt(ip, username, password):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "ip": ip,
        "username": username,
        "password": password,
        "username_length": len(username),
        "password_length": len(password),
        "is_common_username": username in ["admin", "root", "user", "test"],
        "is_common_password": password in ["password", "123456", "admin", "root", "test"]
    }
    
    # load existing logs
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    
    # append new entry
    logs.append(entry)
    
    # save back
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)
    
    return entry