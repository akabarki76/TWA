from hmac import compare_digest
import secrets

def constant_time_lookup(user_id):
    dummy_salt = secrets.token_hex(8)
    dummy_hash = hashlib.pbkdf2_hmac('sha256', b'00000000', dummy_salt.encode(), 100000)
    return USERS.get(user_id, (dummy_salt, dummy_hash))

@app.route('/auth', methods=['POST'])
def auth():
    user_id = int(request.json['user_id'])
    pin = request.json['pin'].encode()
    salt, correct_hash = constant_time_lookup(user_id)  # Always takes time
    
    attempt_hash = hashlib.pbkdf2_hmac('sha256', pin, salt.encode(), 100000)
    if compare_digest(attempt_hash, correct_hash):  # Constant-time
        return jsonify({"token": "VALID"})
    return jsonify({"error": "Invalid credentials"}), 401
