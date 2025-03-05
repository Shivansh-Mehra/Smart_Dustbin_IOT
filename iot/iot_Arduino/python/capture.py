import requests
from PIL import Image
from io import BytesIO

# Replace with your ESP32-CAM IP and capture URL
url = "http://192.168.23.193/capture"

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
