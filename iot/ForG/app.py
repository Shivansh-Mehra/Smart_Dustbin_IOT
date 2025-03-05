import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from flask import Flask, jsonify
import requests
from PIL import Image
from io import BytesIO


app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('currentmodel.h5')

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

    result = {
        "points" : 0,
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
    # Replace with your ESP32-CAM IP and capture URL
    url = "http://192.168.56.193/capture"

    # Make the request to the ESP32-CAM
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the image from the content
        image = Image.open(BytesIO(response.content))

        # Show the image
        image.show()

        # Optionally, save the image
        image.save("captured_image.jpg")

        print("Image captured and saved successfully.")
    else:
        print("Failed to capture image. Status code:", response.status_code)

    if os.path.exists(img_path):  # Check if the image exists
        result = predict_image(img_path)  # Call the prediction function
        return jsonify(result)  # Return the result as JSON
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
