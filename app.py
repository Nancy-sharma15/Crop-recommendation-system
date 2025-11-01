from urllib import request
from flask import Flask, render_template, request, redirect
import pandas as pd
import pickle
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
app = Flask(__name__)

# Load model
model_path = os.path.join(os.path.dirname(__file__), "model", "crop_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"), tls=True)
db = client[os.getenv("DB_NAME")]
collection = db["predictions"]
users = db["users"]

@app.route("/")
def root():
    return redirect("/splash")

@app.route("/splash")
def splash():
    return render_template("splash.html")
@app.route("/insights")
def insights():
    crop = request.args.get("crop")
    tips = []
    tutorials = []

    if crop:
        crop_name = crop.strip().lower()

        # Crop-specific tips
        crop_tips = {
            "rice": [
                "Maintain standing water during early growth.",
                "Use nitrogen fertilizer in split doses.",
                "Watch for blast and bacterial leaf blight."
            ],
            "wheat": [
                "Sow in well-drained loamy soil.",
                "Apply phosphorus before sowing.",
                "Protect from rust and aphids."
            ],
            "maize": [
                "Ensure good drainage and sunlight.",
                "Use balanced NPK fertilizer.",
                "Monitor for stem borers and leaf blight."
            ],
            "cotton": [
                "Use drip irrigation to conserve water.",
                "Apply potassium during flowering stage.",
                "Watch for bollworms and whiteflies."
            ],
            "sugarcane": [
                "Maintain soil moisture during tillering.",
                "Use organic mulch to retain moisture.",
                "Control shoot borer with pheromone traps."
            ]
        }

        tips = crop_tips.get(crop_name, [
            "General tip: Ensure proper irrigation and pest control.",
            "Use compost and test soil pH weekly.",
            "Apply fertilizers based on crop growth stage."
        ])

        # Crop-specific YouTube tutorials
        crop_tutorials = {
            "rice": [
                {"title": "Rice Farming Techniques", "url": "https://www.youtube.com/watch?v=xRi6U4Ke8mM"},
                {"title": "Paddy Field Management", "url": "https://www.youtube.com/watch?v=example2"}
            ],
            "wheat": [
                {"title": "Wheat Cultivation Guide", "url": "https://www.youtube.com/watch?v=8D_1j8e7v3M"},
                {"title": "Fertilizer Tips for Wheat", "url": "https://www.youtube.com/watch?v=example4"}
            ],
            "maize": [
                {"title": "Maize Farming Tips", "url": "https://www.youtube.com/watch?v=3wz6YVZJw9A"},
                {"title": "Maize Pest Management", "url": "https://www.youtube.com/watch?v=example6"}
            ],
            "cotton": [
                {"title": "Cotton Farming Basics", "url": "https://www.youtube.com/watch?v=1gkZzNQ9z9g"},
                {"title": "Cotton Pest Control", "url": "https://www.youtube.com/watch?v=example7"}
            ],
            "sugarcane": [
                {"title": "Sugarcane Cultivation Tips", "url": "https://www.youtube.com/watch?v=2bKZzNQ9z9g"},
                {"title": "Sugarcane Irrigation Methods", "url": "https://www.youtube.com/watch?v=example8"}
            ]
        }

        tutorials = crop_tutorials.get(crop_name, [
            {"title": "General Crop Care Tips", "url": "https://www.youtube.com/watch?v=fMQwUXNpHnE"},
            {"title": "Organic Pest Control Methods", "url": "https://www.youtube.com/watch?v=abc123xyz"}
        ])

    return render_template("insights.html", crop=crop, tips=tips, tutorials=tutorials)
import requests

@app.route("/weather")
def weather():
    api_key = os.getenv("WEATHER_API_KEY")
    city = "Kharar"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url).json()
        if "main" not in response:
            raise ValueError(response.get("message", "Unexpected API response"))

        temperature = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        rainfall = response.get("rain", {}).get("1h", 0)

        alerts = []
        if rainfall and rainfall > 100:
            alerts.append("🚨 High rainfall detected! Risk of waterlogging. Consider raised beds or drainage.")
        if temperature and temperature > 35:
            alerts.append("🌡️ Heat stress warning. Use shade nets or mulch to protect crops.")
            if humidity and humidity > 80:
                alerts.append("💧 High humidity may cause fungal infections. Apply preventive fungicide.")

        return render_template("weather.html", temperature=temperature, humidity=humidity, rainfall=rainfall, alerts=alerts)

    except Exception as e:
        return render_template("weather.html", temperature="N/A", humidity="N/A", rainfall="N/A", alerts=[f"Error: {str(e)}"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = users.find_one({"email": email, "password": password})
        if user:
            return redirect("/home")
        else:
            error = "Invalid credentials."
    return render_template("login.html", error=error)

@app.route("/home", methods=["GET", "POST"])
def home():
    crop = None
    error = None

    if request.method == "POST":
        try:
            data = [
                float(request.form["N"]),
                float(request.form["P"]),
                float(request.form["K"]),
                float(request.form["temperature"]),
                float(request.form["humidity"]),
                float(request.form["ph"]),
                float(request.form["rainfall"])
            ]

            df = pd.DataFrame([data], columns=[
                "Nitrogen", "phosphorus", "potassium",
                "temperature", "humidity", "ph", "rainfall"
            ])

            crop = model.predict(df)[0]

            record = {
                "input": {
                    "N": data[0], "P": data[1], "K": data[2],
                    "temperature": data[3], "humidity": data[4],
                    "ph": data[5], "rainfall": data[6]
                },
                "predicted_crop": crop,
                "timestamp": datetime.now()
            }

            collection.insert_one(record)

            # Redirect to insights page with crop name
            return redirect(f"/insights?crop={crop}")

        except Exception as e:
            error = f"Error: {str(e)}"
            crop = error

    return render_template("index.html", crop=crop, error=error)
if __name__ == "__main__":
    app.run(debug=True)