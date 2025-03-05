import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the trained model
model = tf.keras.models.load_model('currentmodel.h5')

# Load the image to test
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Load and resize the image

    # Preprocess the image
    img_array = image.img_to_array(img)  # Convert the image to an array
    img_array = np.expand_dims(img_array, axis=0)  # Add a batch dimension (1, 224, 224, 3)
    img_array /= 255.0  # Normalize the image (same as training)

    # Make a prediction
    predictions = model.predict(img_array)

    # Class labels (you should adjust these based on your dataset structure)
    class_labels = ['Cardboard', 'Glass', 'Metal', 'Plastic']

    # Print the probability of each class
    for i, label in enumerate(class_labels):
        print(f"Class: {label}, Probability: {predictions[0][i]:.4f}")

    # Get the predicted class index
    predicted_class_index = np.argmax(predictions, axis=1)[0]

    # Get the class label
    predicted_class_label = class_labels[predicted_class_index]

    # Get the confidence of the prediction
    confidence = predictions[0][predicted_class_index]

    # Print the prediction
    print(f"\nPredicted class: {predicted_class_label} with confidence {confidence:.2f}")

    # Optional: You can display the image alongside the prediction
    import matplotlib.pyplot as plt

    plt.imshow(img)
    plt.title(f"Prediction: {predicted_class_label} ({confidence:.2f})")
    plt.axis('off')
    plt.show()
    return predicted_class_index

predict_image('ete.jpeg')