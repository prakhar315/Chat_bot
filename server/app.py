from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import threading
import time
import google.generativeai as genai
import requests
app = Flask(__name__)
CORS(app)

# Google Generative AI Configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create a generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model with the specified model name and configuration
model = genai.GenerativeModel(
    model_name="tunedModels/customdata-1-wkpce19h9ggt",
    generation_config=generation_config,
)

# Pinging Configuration
PING_API_ENDPOINT = "https://chat-bot-vsbx.onrender.com/status"  # Add the endpoint you want to ping
PING_INTERVAL = int(10)  # Default to 20 seconds

def send_message_to_model(user_message):
    # Send a message to the generative model
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_message)
    return response.text

@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the POST request
    user_message = request.json.get('message', '')
    
    # Generate a response using the Google AI model
    response_text = send_message_to_model(user_message)
    
    # Return the generated response as JSON
    return jsonify({"response": response_text})

@app.route('/status', methods=['GET'])
def status():
    # Simple status check endpoint
    return jsonify({"status": "ok"})

def ping_api():
    while True:
        try:
            # Send a GET request to the PING_API_ENDPOINT
            response = requests.get(PING_API_ENDPOINT)
            if response.status_code == 200:
                print(f"Ping successful: {response.status_code}")
            else:
                print(f"Ping failed with status: {response.status_code}")
        except Exception as e:
            print(f"Exception occurred while pinging API: {e}")
        
        # Wait for the next ping
        time.sleep(PING_INTERVAL)

# Start the ping script in a background thread
def start_background_ping():
    ping_thread = threading.Thread(target=ping_api, daemon=True)
    ping_thread.start()

start_background_ping()