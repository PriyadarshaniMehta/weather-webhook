#  Weather Chatbot Webhook

This is a simple Flask-based webhook designed to connect IBM Watson Assistant to a weather API.  
It fetches real-time weather data and returns temperature and wind speed to the chatbot.

#  Deployment
1. Fork or clone this repo.
2. Connect it to [Render.com](https://render.com/).
3. Create a new Web Service → select your repo.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Copy the public URL provided by Render.

#  Integration with IBM Watson
- In Watson Assistant:
  - Add a **Webhook** in the “Actions” section.
  - Use your Render public URL followed by `/get_weather`.
  - Set the request type to **POST**.
  - Pass parameters like:
    ```json
    {
      "city": "$location"
    }
    ```

#  Example Response
```json
{
  "temperature": 29.5,
  "windspeed": 10.2,
  "city": "Delhi"
}
