import serial
import time

# Configure the serial port
ser = serial.Serial('COM9', 9600)  # Replace 'COM3' with your Arduino's serial port
time.sleep(3)  # Wait for the serial connection to initialize
# print("Connected to Arduino.")
time.sleep(3)
# print("Sending data...")
ser.write("s\n".encode())
value = 99
ser.write(str(value).encode())
time.sleep(4)
# print("sending d.")
ser.write("d\n".encode())
time.sleep(4)
# print("sending w.")
ser.write("w\n".encode())
time.sleep(8)
ser.readline().decode().strip()
print(ser.readline().decode().strip()[10:])
print(ser.readline().decode().strip()[10:])
# Close the serial port
ser.close()
