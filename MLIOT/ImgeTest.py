import cv2
import joblib

# Load the trained model
model_path = 'Maindir/trained_model.pkl'
model = joblib.load(model_path)

# Categories based on the specified order
categories = ['CardBoard', 'Metal', 'Plastic', 'Others']

def preprocess_image(image):
    resized_image = cv2.resize(image, (32, 32))
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    return rgb_image.flatten().reshape(1, -1)

def classify_image(image, model, threshold=0.3):
    processed_image = preprocess_image(image)
    probabilities = model.predict_proba(processed_image)
    max_prob = np.max(probabilities)
    prediction = model.predict(processed_image)

    print(f"Probabilities: {probabilities}")
    print(f"Max Probability: {max_prob}")

    if max_prob < threshold:
        return [3]  # 'Others' category
    else:
        return prediction

def test_model_with_image(image_path, model_path, threshold=0.75):
    model = joblib.load(model_path)
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image from {image_path}")
        return
    
    prediction = classify_image(image, model, threshold=threshold)
    class_label = categories[prediction[0]]
    print(f"Predicted class: {class_label} (Confidence: {threshold * 100:.0f}% or higher)")

def main():
    image_path = 'test_image.jpeg'  # Update this path as needed
    model_path = 'Maindir/trained_model.pkl'
    test_model_with_image(image_path, model_path)

if __name__ == "__main__":
    main()
