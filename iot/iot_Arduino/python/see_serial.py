import serial
import time

# Replace 'COM3' or '/dev/ttyUSB0' with your Arduino's port
ser = serial.Serial('COM9', 9600)  # Open serial port
time.sleep(2)  # Wait for Arduino to reset

while True:
    if ser.in_waiting > 0:
        line = ser.readline()
        print(line)
