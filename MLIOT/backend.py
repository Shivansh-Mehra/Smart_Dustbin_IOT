import serial
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulate customer points stored in memory (could be a database in reality)
customer_points = {"customer1": 0}

# Serial input handling
def read_weight_from_serial():
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port
    weight = ser.readline().decode('utf-8').strip()
    return float(weight)

@app.route('/update_points', methods=['POST'])
def update_points():
    customer_id = request.json['customer_id']
    weight = read_weight_from_serial()

    # Points calculation logic (1 point for every 100 grams)
    points_to_add = int(weight / 100)  # Calculate points based on 100 grams
    customer_points[customer_id] += points_to_add

    return jsonify({"customer_id": customer_id, "new_points": customer_points[customer_id]})

if __name__ == '__main__':
    app.run(debug=True)
