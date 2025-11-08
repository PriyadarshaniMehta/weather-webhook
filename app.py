import requests
from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


@app.route("/", methods=["GET"])
def home():
    return "AI Weather + Chat Assistant is running!"


@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.get_json()

    # Watson input format
    user_message = (
        data.get("input", {}).get("text", "") or
        data.get("message", "")
    ).lower()

    # ✅ WEATHER HANDLER (stop here)
    if "weather" in user_message:
        latitude = 28.625
        longitude = 77.25

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}&longitude={longitude}&current_weather=true"
        )

        weather_data = requests.get(url).json()
        current = weather_data.get("current_weather", {})

        reply = (
            f"The current temperature is {current.get('temperature')}°C "
            f"with wind speed {current.get('windspeed')} km/h."
        )

        return jsonify({"output": {"text": [reply]}})

    # ✅ OPENAI HANDLER — only if weather was NOT matched
    elif OPENAI_API_KEY:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response["choices"][0]["message"]["content"]
            return jsonify({"output": {"text": [reply]}})

        except Exception as e:
            return jsonify({"output": {"text": [f"OpenAI error: {e}"]}})

    # FALLBACK
    return jsonify({"output": {"text": ["I'm here to help!"]}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

