import os 
import json
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from flask import Flask, jsonify

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('currentmodel.h5')

# Function to get points based on weight from Serial Monitor
def getPoints():
    # Prototype logic for now (fixed weight of 2kg = 2000 grams)
    weight_in_grams = 10000
    points = weight_in_grams // 100  # 1 point for every 100 grams
    return points

# Function to predict the image
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Load and resize the image
    img_array = image.img_to_array(img)  # Convert the image to an array
    img_array = np.expand_dims(img_array, axis=0)  # Add a batch dimension
    img_array /= 255.0  # Normalize the image

    predictions = model.predict(img_array)
    class_labels = ['Cardboard', 'Glass', 'Metal', 'Plastic']

    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_label = class_labels[predicted_class_index]
    confidence = predictions[0][predicted_class_index]

    # Get the points based on weight
    points = getPoints()

    result = {
        "points": points,  # Add the calculated points to the result
        "group": predicted_class_label,
        "confidence": float(confidence)  # Convert confidence to float for JSON serialization
    }
    
    # Save the result to a JSON file (optional)
    with open('result.json', 'w') as json_file:
        json.dump(result, json_file)

    return result

@app.route('/predict', methods=['GET'])
def predict_route():
    img_path = 'captured_image.jpg'  # The specific image to classify
    if os.path.exists(img_path):  # Check if the image exists
        result = predict_image(img_path)  # Call the prediction function
        return jsonify(result)  # Return the result as JSON
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)