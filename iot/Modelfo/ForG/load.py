import random
from flask import Flask, request, jsonify, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = '123456'  # Ensure you use a strong secret key for sessions

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.iotdb  # Connect to the 'iotdb' database
users_collection = db.users  # Access the 'users' collection

# Simulate customer points stored in MongoDB
def update_user_points(email, points_to_add):
    user = users_collection.find_one({"email": email})
    
    if user:
        new_points = user.get('points', 0) + points_to_add
        users_collection.update_one({"email": email}, {"$set": {"points": new_points}})
        return new_points
    else:
        return None

# Simulate weight reading (for now, fixed at 1000 grams)
def get_weight():
    return 1000  # Fixed weight for testing

@app.route('/update_points', methods=['POST'])
def update_points():
    if 'user' not in session:
        return jsonify({"error": "User not logged in"}), 401

    email = session['user']['email']  # Retrieve the logged-in user's email
    weight = get_weight()  # Get the weight (simulated)

    # Points calculation logic (1 point for every 100 grams)
    points_to_add = int(weight / 100)
    
    # Update user's points in MongoDB
    new_points = update_user_points(email, points_to_add)

    if new_points is not None:
        return jsonify({"email": email, "new_points": new_points})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5500)
