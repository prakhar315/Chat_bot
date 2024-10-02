from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Define keywords for time management
keywords = {
    "time_management": [
        "have too much to study", " running out of time", "can't finish my assignments",
        " have a lot of work to do", " feel overwhelmed by my workload",
        " can’t keep up with my studies", "My deadlines are approaching",
        " have too many exams coming up", "I’m juggling too many tasks",
        " don’t have enough time to prepare", " stressed about my workload","can’t keep up with my studies", "deadlines are approaching",
        "have too many exams coming up", "juggling too many tasks",
        "don’t have enough time to prepare", "stressed about my workload",
        "have multiple assignments due soon", "can't balance my studies and personal life",
        "falling behind in my classes", "overwhelmed with projects",
        "have too many subjects to study for", "can’t manage my time effectively",
        "not sure how to prioritize my tasks", "procrastinate and then panic",
        "feel like I’m running out of time", "anxious about my grades",
        "feel like I’m going to fail", "worried about not finishing on time",
        "feeling stressed about my studies", "have no motivation to study",
        "exhausted from studying too much", "feel trapped by my responsibilities",
        "can’t concentrate on my studies", "struggling to manage my study schedule",
        "need to get organized", "can’t find a study routine that works",
        "keep getting distracted while studying", "don’t know how to study effectively",
        "feel like I’m wasting time", "need better time management skills",
        "urgent", "immediate", "critical", "last-minute",
        "keep putting things off", "procrastinate on my assignments",
        "waited too long to start studying", "need study tips",
        "I want to learn how to manage my time", "need help organizing my tasks",
        "have a project due tomorrow", "have a midterm next week",
        "Finals are just around the corner", "paper is due in two days",
        "have a presentation to prepare for", "have a deadline coming up"
    ]
}
GEMINI_API_ENDPOINT = os.getenv("Gemini_api_endpoint")  # Example endpoint
GEMINI_API_KEY = os.getenv("Gemini_api_key")

def categorize_message_with_gemini(message):
    # Prepare the request headers and payload for Gemini API
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "text": message
    }

    try:
   # Make the API request to Gemini
        response = requests.post(GEMINI_API_ENDPOINT, headers=headers, json=payload)

        if response.status_code == 200:
        # Assuming the API returns a JSON object with a 'category' field
            response_data = response.json()
            return response_data.get('category', None)
        else:
            print(f"Error from Gemini API: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred while calling Gemini API: {e}")
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
    category = categorize_message_with_gemini(user_message)
    if not category:
        category = categorize_message(user_message)

    if category == "time_management":
        response = "Ohh that time management thing managing your time and studies is really not a big task if you just listen the story am going to tell."
    else:
        response = "Don't worry champ think me as your good friend and help me more to so that I undertsand you Let's talk more about your situation."

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
 
