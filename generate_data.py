import json
import random
from datetime import datetime, timedelta

COMMON_USERNAMES = ["admin", "root", "user", "test", "guest", "ubuntu", "pi"]
COMMON_PASSWORDS = ["123456", "password", "admin", "root", "test", "12345", "qwerty"]

HUMAN_USERNAMES = ["john_smith", "sarah_dev", "m.jones", "carlos99", "dev_user", "webmaster", "sysadmin2024"]
HUMAN_PASSWORDS = ["MyP@ssw0rd!", "S3cur!ty2024", "L0gin#Now", "Tr0ub4dor&3", "C0rrect-H0rse", "B4ttery!Stap1e"]

BOT_IPS = ["185.234.219.15", "103.21.59.8", "45.153.160.2", "194.165.16.11", "91.240.118.99"]
HUMAN_IPS = ["72.38.154.201", "156.223.89.44", "98.114.205.75", "24.205.163.12"]

def generate_bot_attempt(timestamp):
    return {
        "timestamp": timestamp.isoformat(),
        "ip": random.choice(BOT_IPS),
        "username": random.choice(COMMON_USERNAMES),
        "password": random.choice(COMMON_PASSWORDS),
        "username_length": 0,
        "password_length": 0,
        "is_common_username": True,
        "is_common_password": True,
        "label": 1
    }

def generate_human_attempt(timestamp):
    username = random.choice(HUMAN_USERNAMES)
    password = random.choice(HUMAN_PASSWORDS)
    return {
        "timestamp": timestamp.isoformat(),
        "ip": random.choice(HUMAN_IPS),
        "username": username,
        "password": password,
        "username_length": len(username),
        "password_length": len(password),
        "is_common_username": False,
        "is_common_password": False,
        "label": 0
    }

def generate_dataset(n_bots=150, n_humans=50):
    logs = []
    start = datetime.now() - timedelta(hours=24)
    
    for i in range(n_bots):
        # bots attack in bursts
        timestamp = start + timedelta(seconds=random.randint(0, 86400))
        entry = generate_bot_attempt(timestamp)
        entry["username_length"] = len(entry["username"])
        entry["password_length"] = len(entry["password"])
        logs.append(entry)
    
    for i in range(n_humans):
        # humans are more spread out
        timestamp = start + timedelta(seconds=random.randint(0, 86400))
        logs.append(generate_human_attempt(timestamp))
    
    logs.sort(key=lambda x: x["timestamp"])
    
    with open("attack_logs.json", "w") as f:
        json.dump(logs, f, indent=2)
    
    print(f"generated {n_bots} bot attempts and {n_humans} human attempts")
    print(f"total: {len(logs)} attack logs saved to attack_logs.json")

if __name__ == "__main__":
    generate_dataset()