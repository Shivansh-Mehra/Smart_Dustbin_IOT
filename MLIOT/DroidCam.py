import cv2
import numpy as np
import joblib
import os

# Replace with your mobile camera URL
url = "http://192.168.25.14:4747/video"

# Load the trained model
model_path = 'Maindir/trained_model.pkl'
model = joblib.load(model_path)

# Categories (CardBoard, Plastic, Metal, Others)
categories = ['CardBoard', 'Plastic', 'Metal', 'Others']

# Create Capture directory if it doesn't exist
capture_dir = 'Capture'
os.makedirs(capture_dir, exist_ok=True)

# Start capturing video from the mobile camera
cap = cv2.VideoCapture(url)

def preprocess_image(image):
    resized_image = cv2.resize(image, (32, 32))
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    return rgb_image.flatten().reshape(1, -1)

def classify_image(image, model, threshold=0.3):
    processed_image = preprocess_image(image)
    probabilities = model.predict_proba(processed_image)
    max_prob = np.max(probabilities)
    prediction = model.predict(processed_image)
    
    # Print the probability array for each category
    print(f"Probability array: {probabilities}")
    
    # Determine the class label
    if max_prob < threshold:
        return [3], max_prob  # 'Others' category
    else:
        return prediction, max_prob

img_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Display the video feed
    cv2.imshow('Frame', frame)
    
    # Press 'f' to capture an image
    if cv2.waitKey(1) & 0xFF == ord('f'):
        img_name = os.path.join(capture_dir, f"capture_{img_count}.png")
        cv2.imwrite(img_name, frame)
        print(f"Image saved as {img_name}")
        
        # Classify the captured image using the trained model
        prediction, max_prob = classify_image(frame, model)
        class_label = categories[prediction[0]]
        print(f"Predicted class: {class_label}")
        print(f"Maximum probability: {max_prob:.2f}")
        
        img_count += 1
    
    # Press 'q' to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
