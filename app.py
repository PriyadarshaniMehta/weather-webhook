from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Weather Webhook is running!"

@app.route('/weather', methods=['GET'])
def get_weather():
    latitude = 26.4499   #change the latitude and logitude as per your location
    longitude = 80.3319  

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

    try:
        response = requests.get(url)
        response.raise_for_status()  # raise error if bad response
        data = response.json()
        weather = data.get("current_weather", {})

        return jsonify({
            "temperature": weather.get("temperature"),
            "windspeed": weather.get("windspeed"),
            "unit": "°C"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
