from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import threading
import time

app = Flask(__name__)
CORS(app)

# Gemini API Configuration
GEMINI_API_ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PING_API_ENDPOINT = os.getenv("PING_API_ENDPOINT")  # Add the endpoint you want to ping
PING_INTERVAL = int(os.getenv("PING_INTERVAL", 20))  # Default to 60 seconds

def call_gemini_api(message):
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": message
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(f'{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}', headers=headers, json=payload)
        print(response.text)
        if response.status_code == 200:
            response_data = response.json()
            candidates = response_data.get('candidates', [])
            
            if candidates:
                generated_response = candidates[0]['content']['parts'][0]['text']
                return generated_response
            else:
                return "I couldn't understand that, please try again."
        else:
            print(f"Error from Gemini API: {response.status_code}, {response.text}")
            return "Sorry, I'm having trouble processing your request right now."
    
    except Exception as e:
        print(f"Exception occurred while calling Gemini API: {e}")
        return "There was an issue communicating with the AI service."

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = call_gemini_api(user_message)
    return jsonify({"response": response})

@app.route('/status', methods=['GET'])
def status():
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
