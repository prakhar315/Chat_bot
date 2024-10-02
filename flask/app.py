from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Gemini API Configuration
GEMINI_API_ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini_api(message):
    # Prepare the request headers and payload for Gemini API
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
        # Make the API request to Gemini
        response = requests.post(f'{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}', headers=headers, json=payload)
        
        if response.status_code == 200:
            # Parse the response from Gemini
            response_data = response.json()
            
            # The 'candidates' list contains the generated content
            candidates = response_data.get('candidates', [])
            
            if candidates:
                # Extract the generated text from the first candidate
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

# if __name__ == '__main__':
    # app.run(debug=True)
