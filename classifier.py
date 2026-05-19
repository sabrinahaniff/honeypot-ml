import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

def load_data():
    with open('attack_logs.json', 'r') as f:
        logs = json.load(f)
    return pd.DataFrame(logs)

def add_features(df):
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['is_night'] = df['hour'].apply(lambda x: 1 if x < 6 or x > 22 else 0)
    df['password_has_numbers'] = df['password'].apply(lambda x: int(any(c.isdigit() for c in x)))
    df['password_has_special'] = df['password'].apply(lambda x: int(any(not c.isalnum() for c in x)))
    return df

def label_data(df):
    # bots mostly common username and short/common password and fast attempts
    df['is_bot'] = (
        (df['is_common_username'] == True) & 
        (df['is_common_password'] == True)
    ).astype(int)
    return df