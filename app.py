# app.py (Flask application)
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage (not persistent!)
users = []
next_id = 1

@app.route('/')
def home():
    return jsonify({"message": "User Service is running on Docker by Jenkins Pipeline"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "users"})

@app.route('/api/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json(silent=True)
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Missing name or email"}), 400
    
    user = {"id": next_id, "name": data['name'], "email": data['email']}
    users.append(user)
    next_id += 1
    return jsonify(user), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
