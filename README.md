# honeypot-ml

an ssh honeypot that logs attack attempts and uses machine learning to classify whether the attacker is a bot or a human.

## what it does

- runs a fake ssh server on port 2222 that captures every login attempt
- logs credentials, timestamps, and behavioral features to json
- trains a random forest classifier to profile attackers as bots vs humans
- generates synthetic attack data for training
- visualizes everything in a live soc-style dashboard

## how to run

**start the honeypot:**
```bash
python3 honeypot.py
```

**start the dashboard:**
```bash
python3 dashboard.py
```

open `http://localhost:5000` to see live attack data.

**generate synthetic training data:**
```bash
python3 generate_data.py
```

**run the classifier:**
```bash
python3 classifier.py
```

## how it works

the honeypot uses paramiko to simulate a real ssh server. when an attacker connects and tries a username/password, it logs the attempt with behavioral features like password length, whether common credentials were used, and time of attack. a random forest classifier then uses these features to distinguish bots (which spray common credentials fast) from human attackers (who tend to use more creative, longer passwords).

## features used for classification

| feature | why it matters |
|---|---|
| `is_common_username` | bots almost always try root, admin, user |
| `password_has_special` | humans use special characters, bots rarely do |
| `username_length` | human usernames tend to be longer |
| `password_length` | humans use longer passwords |
| `password_has_numbers` | another behavioral signal |
| `hour` | bots often run on schedules |

## stack

python · paramiko · flask · scikit-learn · pandas · chart.js

## notes

built this to learn how ssh brute force attacks work in practice and how ml can be used to detect behavioral patterns in attack data. all testing is done locally so don't deploy without proper network isolation ;p.