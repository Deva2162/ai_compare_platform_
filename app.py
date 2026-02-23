import time
import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ===============================
# AI 1 - OpenAI (GPT)
# ===============================
def get_ai1_response(prompt):
    api_key = os.getenv("OPENAI_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )

    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {result}"


# ===============================
# AI 2 - Claude (Anthropic)
# ===============================
def get_ai2_response(prompt):
    api_key = os.getenv("ANTHROPIC_API_KEY")

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 500,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data,
        timeout=30
    )

    result = response.json()

    if "content" in result:
        return result["content"][0]["text"]
    else:
        return f"Error: {result}"


# ===============================
# AI 3 - Gemini (Google)
# ===============================
def get_ai3_response(prompt):
    api_key = os.getenv("GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=30
    )

    result = response.json()

    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {result}"


# ===============================
# ROUTES
# ===============================
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

    # AI 1
    start = time.time()
    try:
        res1 = get_ai1_response(user_prompt)
        time1 = round(time.time() - start, 2)
        results.append({"model": "OpenAI GPT", "response": res1, "time": time1})
    except Exception as e:
        results.append({"model": "OpenAI GPT", "response": str(e), "time": 0})

    # AI 2
    start = time.time()
    try:
        res2 = get_ai2_response(user_prompt)
        time2 = round(time.time() - start, 2)
        results.append({"model": "Claude", "response": res2, "time": time2})
    except Exception as e:
        results.append({"model": "Claude", "response": str(e), "time": 0})

    # AI 3
    start = time.time()
    try:
        res3 = get_ai3_response(user_prompt)
        time3 = round(time.time() - start, 2)
        results.append({"model": "Gemini", "response": res3, "time": time3})
    except Exception as e:
        results.append({"model": "Gemini", "response": str(e), "time": 0})

    # Fastest Model Detection
    valid_times = [r["time"] for r in results if r["time"] > 0]

    if valid_times:
        fastest_time = min(valid_times)
        for r in results:
            r["is_fastest"] = (r["time"] == fastest_time)
    else:
        for r in results:
            r["is_fastest"] = False

    return jsonify(results)


# ===============================
# Render Production Run
# ===============================
if __name__ == '__main__':
    app.run()