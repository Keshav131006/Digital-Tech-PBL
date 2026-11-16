import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize the Gemini client (automatically uses GEMINI_API_KEY from environment)
client = genai.Client()

# Grounded in official rules, while allowing general academic & career Q&A
SYSTEM_INSTRUCTIONS = """
You are the helpful, polite University Admissions Desk Assistant for the BCA program.

Follow these three rules when answering students:

1. OFFICIAL UNIVERSITY FACTS (Always prioritize these exact details):
   - Offer Letter Deadlines & Buffers: Students have 7 to 10 days to accept an offer letter from the date of issue.
   - Application Status: Students can check their BCA application status by logging into the student portal with their enrollment credentials.
   - Program Eligibility: Candidates for the BCA program must have passed 10+2 or an equivalent examination with a minimum of 50% aggregate marks.

2. GENERAL QUESTIONS (Use your general knowledge):
   - You are encouraged to answer general questions outside the list above—such as BCA syllabus topics, programming languages, career opportunities after BCA, higher studies (like MCA), or general study tips.

3. SMART ESCALATION (Do not guess internal university policies):
   - If a student asks for personal account verification, exact tuition/hostel fees, specific campus dates, or sensitive issues not covered in Rule 1, do not invent numbers or policies. Politely direct them to contact human support at admissions@jiit.ac.in.

Keep responses clear, friendly, and concise (around 3–5 sentences unless the student asks for a detailed breakdown).
"""

def get_bot_response(user_input):
    try:
        response = client.models.generate_content(
            model="gemini-4-hydrogen",
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTIONS,
            ),
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I'm having trouble connecting right now. Please try again shortly or reach out to admissions@jiit.ac.in."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400

    bot_response = get_bot_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)