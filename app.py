from flask import Flask, render_template, send_from_directory, url_for
import paho.mqtt.client as mqtt
import json
import time
from art_generator import generate_art
from qr_code_generator import generate_qr_code
import os

app = Flask(__name__)

# Global variables
latest_data = None
last_art_time = 0
art_exists = False
qr_exists = False

# Define a base URL that can be used for QR code generation
BASE_URL = "https://c398-193-191-137-219.ngrok-free.app"  # Replace with your ngrok or public URL once you configure it

# MQTT callback function
def on_message(client, userdata, msg):
    global latest_data, last_art_time, art_exists, qr_exists
    try:
        payload = json.loads(msg.payload.decode())
        latest_data = payload
        print(f"Message received: {latest_data}")

        heart_rate = latest_data.get('heart_rate', 60)
        temperature = latest_data.get('temperature', None)
        print(f"Heart Rate: {heart_rate}, Temperature: {temperature}")

        current_time = time.time()
        if current_time - last_art_time >= 60:
            # Pass both heart_rate and temperature to generate_art function
            art_path = generate_art(heart_rate, temperature)
            last_art_time = current_time
            qr_path = generate_qr_code(f'{BASE_URL}/download')
            
            # Set art_exists and qr_exists based on file existence
            art_exists = os.path.exists('static/images/current_art.png')
            qr_exists = os.path.exists('static/images/qrcode.png')

            print(f"QR code generated at {qr_path}")
    except Exception as e:
        print(f"Failed to decode message: {e}")


# MQTT setup
client = mqtt.Client()
client.on_message = on_message
client.connect("192.168.0.65", 1883, 60)  # Replace with your MQTT broker address
client.subscribe("sensor/ifdata")  # Replace with your MQTT topic
client.loop_start()

@app.route('/')
def index():
    # Pass the latest data, art_exists flag, qr_exists flag, and current_time to force image reload
    return render_template('index.html', 
                           data=latest_data, 
                           art_exists=art_exists, 
                           qr_exists=qr_exists,
                           current_time=int(time.time()))  # Pass current timestamp to force image reload


# New route to show the image and provide a download button
@app.route('/download')
def download_page():
    return render_template('download.html', image_url=url_for('serve_image', filename='current_art.png'))


# Serve static images
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

# Route for downloading the image
@app.route('/download_image')
def download_image():
    return send_from_directory('static/images', 'current_art.png', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
