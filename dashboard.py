from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

def load_logs():
    if not os.path.exists('attack_logs.json'):
        return []
    with open('attack_logs.json', 'r') as f:
        try:
            return json.load(f)
        except:
            return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/attacks')
def attacks():
    logs = load_logs()
    return jsonify(logs)

@app.route('/api/stats')
def stats():
    logs = load_logs()
    if not logs:
        return jsonify({})
    
    total = len(logs)
    bots = sum(1 for l in logs if l.get('is_common_username') and l.get('is_common_password'))
    humans = total - bots
    unique_ips = len(set(l['ip'] for l in logs))
    common_usernames = {}
    common_passwords = {}
    
    for l in logs:
        u = l['username']
        p = l['password']
        common_usernames[u] = common_usernames.get(u, 0) + 1
        common_passwords[p] = common_passwords.get(p, 0) + 1
    
    top_usernames = sorted(common_usernames.items(), key=lambda x: x[1], reverse=True)[:5]
    top_passwords = sorted(common_passwords.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return jsonify({
        'total': total,
        'bots': bots,
        'humans': humans,
        'unique_ips': unique_ips,
        'top_usernames': top_usernames,
        'top_passwords': top_passwords
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)