import time
import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# --- MOCK AI FUNCTIONS (Replace these with real API calls later) ---

def get_ai1_response(prompt):
    """
    Simulates AI 1 (e.g., GPT-4)
    """
    time.sleep(2) # Simulate network delay
    return "This is the response from AI Model 1 (Simulated). It is usually very detailed."

def get_ai2_response(prompt):
    """
    Simulates AI 2 (e.g., Claude/Gemini)
    """
    time.sleep(1.5) # Faster simulated delay
    return "This is the response from AI Model 2 (Simulated). It focuses on brevity."

def get_ai3_response(prompt):
    """
    Simulates AI 3 (e.g., Open Source Model)
    """
    time.sleep(3) # Slower simulated delay
    return "This is the response from AI Model 3 (Simulated). It is open source."

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_prompt = data.get('prompt')

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    results = []

    # We execute calls sequentially for simplicity, but measure time individually
    # In a production app, you might use asyncio or threading for parallel execution
    
    # Call AI 1
    start = time.time()
    try:
        res1 = get_ai1_response(user_prompt)
        time1 = round(time.time() - start, 2)
        results.append({"model": "AI Model 1", "response": res1, "time": time1})
    except Exception as e:
        results.append({"model": "AI Model 1", "response": f"Error: {str(e)}", "time": 0})

    # Call AI 2
    start = time.time()
    try:
        res2 = get_ai2_response(user_prompt)
        time2 = round(time.time() - start, 2)
        results.append({"model": "AI Model 2", "response": res2, "time": time2})
    except Exception as e:
        results.append({"model": "AI Model 2", "response": f"Error: {str(e)}", "time": 0})

    # Call AI 3
    start = time.time()
    try:
        res3 = get_ai3_response(user_prompt)
        time3 = round(time.time() - start, 2)
        results.append({"model": "AI Model 3", "response": res3, "time": time3})
    except Exception as e:
        results.append({"model": "AI Model 3", "response": f"Error: {str(e)}", "time": 0})

    # Determine fastest
    fastest_index = min(range(len(results)), key=lambda i: results[i]['time'])
    
    # Add flag for fastest
    for i, res in enumerate(results):
        res['is_fastest'] = (i == fastest_index)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)