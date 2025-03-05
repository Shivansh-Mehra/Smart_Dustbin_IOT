import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_otp():
    """Generate a 6-digit OTP."""
    otp = random.randint(100000, 999999)
    return otp

def send_notification(email, otp):
    sender_email = "raiharshit66@gmail.com"
    sender_password = "ogys sycu mman aqni"
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'Your OTP for Registration'
    body = f"Your OTP for registration is: {otp}\nPlease use it to complete your registration."
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

# Flask app setup
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/views/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']  # Hash the password here for security

    # Generate OTP
    otp = generate_otp()

    # Send OTP to user's email
    send_notification(email, otp)

    # Store OTP for verification (e.g., in a session or database)
    # session['otp'] = otp

    return jsonify({"message": "OTP sent to your email. Please verify it to complete registration."})

if __name__ == '__main__':
    app.run(debug=True)
