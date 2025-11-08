import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# If you decide to use an LLM later, e.g. OpenAI, Gemini, etc.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # You can set this later in Render

@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.get_json()
    user_message = data.get("message", "").lower()

    # ---  WEATHER HANDLER ---
    if "weather" in user_message:
        latitude = data.get("latitude", 28.625)
        longitude = data.get("longitude", 77.25)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)
        weather_data = response.json()
        current = weather_data.get("current_weather", {})
        reply = (
            f"The current temperature is {current.get('temperature')}°C "
            f"with wind speed {current.get('windspeed')} km/h."
        )
        return jsonify({"response": reply})

    # --- GENERAL QUESTION HANDLER (AI API) ---
    else:
        # For now, if you don’t have an API key, use a placeholder reply
        reply = "I'm your assistant! I can answer your general questions too."
        return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

