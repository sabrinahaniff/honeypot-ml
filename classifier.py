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

def train_classifier(df):
    features = [
        'username_length', 
        'password_length',
        'is_common_username',
        'is_common_password',
        'hour',
        'is_night',
        'password_has_numbers',
        'password_has_special'
    ]
    
    X = df[features].astype(float)
    y = df['is_bot']
    
    if len(df) < 4:
        print("not enough data yet! try more login attempts first.")
        return
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=10, random_state=42)
    clf.fit(X_train, y_train)
    
    print("\n=== Attacker Profile Results ===")
    print(classification_report(y_test, clf.predict(X_test), zero_division=0))
    print("\nFeature importance:")
    for feat, imp in zip(features, clf.feature_importances_):
        print(f"  {feat}: {imp:.3f}")
    
    return clf

if __name__ == "__main__":
    df = load_data()
    df = add_features(df)
    df = label_data(df)
    print(f"loaded {len(df)} attack attempts")
    train_classifier(df)