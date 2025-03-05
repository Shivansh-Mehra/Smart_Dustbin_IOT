import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from flask import Flask, jsonify
import serial
import time
import requests
from PIL import Image
from io import BytesIO
import smtplib  # Import the smtplib module for sending email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2
# import otpveri
app = Flask(__name__)
def send_notification(msg= "The dustbin has been filled. Please empty it at your earliest convenience.", sub ='Dustbin Full Notification'):
    email= "123102125@nitkkr.ac.in"
    sender_email = "raiharshit66@gmail.com"
    sender_password = "ogys sycu mman aqni"
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = sub
    body = msg
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        print("Notification sent successfully!")
    except Exception as e:
        print(f"Failed to send notification. Error: {e}")
# Load the trained model
model = tf.keras.models.load_model('currentmodel.h5')

def connect_to_serial():
    """Connect to the Arduino via serial."""
    try:
        ser = serial.Serial('COM9', 9600)
        time.sleep(10)  # Wait for the serial connection to initialize
        return ser,None
    except serial.SerialException as e:
        return None, str(e)

def capture_image_from_esp32():
    # """Capture an image from the ESP32-CAM."""
    # url = "http://192.168.51.193/capture"  # Replace with your ESP32-CAM IP
    # try:
    #     response = requests.get(url)
    #     response.raise_for_status()  # Check for request errors
    #     image = Image.open(BytesIO(response.content))
    #     image.save("captured_image.jpg")  # Save the captured image
    #     print("Image captured and saved successfully.")
    # except Exception as e:
    #     print("Failed to capture image. Using the previous image.")
    #     return "captured_image.jpg"  # Use existing image if capture fails
    # return "captured_image.jpg"
    # def capture_image_from_droidcam():
    # """Capture an image from the DroidCam."""
    # url = "http://192.168.51.21:4747/video"  # Replace with your DroidCam video stream URL
    # try:
    #     response = requests.get(url)
    #     response.raise_for_status()  # Check for request errors
    #     img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    #     image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Decode the image
    #     cv2.imwrite("captured_image.jpg", image)  # Save the captured image
    #     print("Image captured and saved successfully.")
    # except Exception as e:
    #     print("Failed to capture image. Using the previous image.")
    #     return "captured_image.jpg"  # Use existing image if capture fails
    # return "captured_image.jpg"
    """Capture an image from the DroidCam using OpenCV."""
    droidcam_url = 'http://192.168.51.21:4747/video'  # Replace with your DroidCam URL
    cap = cv2.VideoCapture(droidcam_url)

    # Check if the camera opened successfully
    if not cap.isOpened(): 
        print("Error: Could not open video stream from DroidCam.")
        return "captured_image.jpg"  # Use the previous image if capture fails

    # Capture a single frame (image) from the stream
    ret, frame = cap.read()

    if ret:
        # Save the captured frame as 'captured_image.jpg'
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured and saved as 'captured_image.jpg'.")
    else:
        print("Error: Could not capture image. Using the previous image.")
    
    # Release the video capture object
    cap.release()
    return "captured_image.jpg"


def predict_image(img_path):
    """Predict the class of the image."""
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize the image

    predictions = model.predict(img_array)
    class_labels = ['Cardboard', 'Glass', 'Metal', 'Plastic']

    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_label = class_labels[predicted_class_index]
    confidence = predictions[0][predicted_class_index]

    # ser, serial_error = connect_to_serial()
    ser = serial.Serial('COM9', 9600)
    time.sleep(10)
    points = 0  # Default value for points in case of serial error
    full = None  # Default value for fullness

    if ser is not None:
        try:
            # value = ord(predicted_class_label[0].lower())
            # ser.write(str(value).encode())
            # ser.write("s\n".encode())
            # time.sleep(4)
            # ser.write("d\n".encode())
            # time.sleep(4)
            # ser.write("w\n".encode())
            # time.sleep(8)
            # ser.readline().decode().strip()
            # d = ser.readline().decode().strip()[10:13]
            # w = ser.readline().decode().strip()[10:]
            # points = round(float(w) * 10) 
            # full = d
            value = ord(predicted_class_label[0].lower())
            ser.write(str(value).encode())
            time.sleep(1)
            ser.write("s\n".encode())
            time.sleep(4)
            ser.write("d\n".encode())
            time.sleep(4)
            ser.write("w\n".encode())
            time.sleep(8)
            ser.readline().decode().strip()
            d = ser.readline().decode().strip()[10:13]
            w = ser.readline().decode().strip()[10:]
            # Close the serial port
            # ser.close()
            points = round(float(w)*10)
            full = int(d)
            # Check if fullness is 70% or more, and send an email notification
            if full <= 1: 
                send_notification()
            
            result = {
                "points": points,
                "group": predicted_class_label,
                "confidence": float(confidence),
                "full": full,
            }
        except Exception as e:
            result = {
                "points": 0,  # Default points
                "group": predicted_class_label,
                "confidence": float(confidence),
                "full": None,
                "serial_error": str(e)
            }
            send_notification(msg="Some error has occured. Please check the dustbin.", sub='Error Ocuured')
        finally:
            ser.close()
    else:
        result = {
            "points": 0,
            "group": predicted_class_label,
            "confidence": float(confidence),
            "full": None,
            # "serial_error": serial_error
        }
        send_notification("Some error has occured. Please check the dustbin.", sub='Error Ocuured in Serial')
    # Save the result to a JSON file (optional)
    with open('result.json', 'w') as json_file:
        json.dump(result, json_file)

    return result

@app.route('/predict', methods=['GET'])
def predict_route():
    img_path = capture_image_from_esp32()  # Capture image or use existing one
    if os.path.exists(img_path):  # Check if the image exists
        result = predict_image(img_path)  # Call the prediction function
        return jsonify(result)  # Return the result as JSON
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
