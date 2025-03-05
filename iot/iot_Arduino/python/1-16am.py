import serial
import time
import threading

# Configure the serial port
ser = serial.Serial('COM9', 9600)  # Replace with your Arduino's serial port
time.sleep(2)  # Wait for the serial connection to initialize

# Function to read data from Arduino
def read_from_arduino():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline()
            print(line.decode().strip())  # Decode and print the received line

# Function to send data to Arduino
def send_to_arduino(value):
    ser.write(str(value).encode())  # Send the integer value
    print(f"Sent: {value}")

# Start the reading thread
reading_thread = threading.Thread(target=read_from_arduino)
reading_thread.daemon = True  # Allow the program to exit even if the thread is running
reading_thread.start()

# Main loop to send values to Arduino
try:
    while True:
        value = int(input("Enter a value to send to Arduino: "))  # Get user input
        send_to_arduino(value)
        time.sleep(1)  # Adjust the sleep time as needed
except KeyboardInterrupt:
    print("Exiting...")

# Close the serial port before exiting
ser.close()
