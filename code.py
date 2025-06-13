from flask import Flask, request, jsonify
import hashlib, time, os

app = Flask(__name__)
JWT_SECRET = os.urandom(32)

# {user_id: (salt, hash)}
USERS = {
    1001: ("salt_A", hashlib.pbkdf2_hmac('sha256', b'12345678', b'salt_A', 100000)),
    1002: ("salt_B", hashlib.pbkdf2_hmac('sha256', b'87654321', b'salt_B', 100000))
}

@app.route('/auth', methods=['POST'])
def auth():
    try:
        user_id = int(request.json['user_id'])
        pin = request.json['pin'].encode()
        
        # Timing leak: Early exit for invalid users
        if user_id not in USERS:
            return jsonify({"error": "Invalid credentials"}), 401
            
        salt, correct_hash = USERS[user_id]
        attempt_hash = hashlib.pbkdf2_hmac('sha256', pin, salt.encode(), 100000)
        
        # Basic comparison (vulnerable)
        if attempt_hash == correct_hash:
            return jsonify({"token": "VALID"})
        return jsonify({"error": "Invalid credentials"}), 401
    except:
        return jsonify({"error": "Bad request"}), 400
