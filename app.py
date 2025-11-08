from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    city = data.get("city", "Delhi")

    url = f"https://api.open-meteo.com/v1/forecast?latitude=28.6139&longitude=77.2090&current_weather=true"
    response = requests.get(url)
    weather_data = response.json()

    current_weather = weather_data.get("current_weather", {})
    temperature = current_weather.get("temperature")
    windspeed = current_weather.get("windspeed")

    return jsonify({
        "temperature": temperature,
        "windspeed": windspeed,
        "city": city
    })

@app.route('/', methods=['GET'])
def home():
    return "Weather Chatbot Webhook is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
