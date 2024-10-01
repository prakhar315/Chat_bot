from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define keywords for time management
keywords = {
    "time_management": [
        "have too much to study", " running out of time", "can't finish my assignments",
        " have a lot of work to do", " feel overwhelmed by my workload",
        " can’t keep up with my studies", "My deadlines are approaching",
        " have too many exams coming up", "I’m juggling too many tasks",
        " don’t have enough time to prepare", " stressed about my workload"
    ]
}
GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest"  # Example endpoint
GEMINI_API_KEY = "AIzaSyBm2N_eVqKHtmi7LxCG-yF7FuQRSfS6RRE"

def categorize_message_with_gemini(message):
    # Prepare the request headers and payload for Gemini API
    headers = {
        'Authorization': f'Bearer {AIzaSyBm2N_eVqKHtmi7LxCG-yF7FuQRSfS6RRE}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "text": message
    }

    # Make the API request to Gemini
    response = requests.post(GEMINI_API_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        # Assuming the API returns a JSON object with a 'category' field
        response_data = response.json()
        return response_data.get('category', None)
    else:
        return None

def categorize_message(message):
    message_lower = message.lower()
    for category, phrases in keywords.items():
        if any(phrase.lower() in message_lower for phrase in phrases):
            return category
    return None

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    category = categorize_message(user_message)

    if category == "time_management":
        response = "It sounds like you're feeling stressed about managing your time and studies. How can I assist you with that?"
    else:
        response = "Let's talk more about your situation."

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
 
