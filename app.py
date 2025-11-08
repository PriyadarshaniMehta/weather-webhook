import requests
from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Load API key for OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

@app.route("/", methods=["GET"])
def home():
    return "AI Weather + Chat Assistant is running!"


@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.get_json()
    user_message = data.get("message", "").lower()

    # WEATHER HANDLER
    if "weather" in user_message:
        latitude = float(data.get("latitude", 28.625))
        longitude = float(data.get("longitude", 77.25))

        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)
        weather_data = response.json()
        current = weather_data.get("current_weather", {})

        reply = (
            f"The current temperature is {current.get('temperature')}°C "
            f"with wind speed {current.get('windspeed')} km/h."
        )
        return jsonify({"response": reply})

    #  GENERAL QUESTION HANDLER USING OPENAI
    if OPENAI_API_KEY:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful personal AI assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response["choices"][0]["message"]["content"]
            return jsonify({"response": reply})
        except Exception as e:
            return jsonify({"response": f"Error from OpenAI: {str(e)}"})

    # FALLBACK
    return jsonify({"response": "I'm your assistant! I can answer weather and general questions."})


# public weather endpoint
@app.route("/weather", methods=["GET"])
def weather_only():
    url = "https://api.open-meteo.com/v1/forecast?latitude=28.625&longitude=77.25&current_weather=true"
    response = requests.get(url).json()
    current = response.get("current_weather", {})
    return jsonify({
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "unit": "°C"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


