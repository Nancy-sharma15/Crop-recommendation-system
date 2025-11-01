# 🌾 Crop Recommendation System

A full-stack machine learning web application that recommends the most suitable crop based on soil and climate conditions. Built with Python (Flask), HTML/CSS/JavaScript, and MongoDB.

---

## 🚀 Features

- Predicts crop using trained ML model (Random Forest)
- Interactive frontend with form and loading animation
- Stores user inputs and predictions in MongoDB
- Clean UI built with HTML, CSS, and JavaScript

---

## 🧠 Tech Stack

| Layer       | Technology         |
|-------------|--------------------|
| Frontend    | HTML, CSS, JavaScript |
| Backend     | Python, Flask       |
| ML Model    | scikit-learn        |
| Database    | MongoDB (via pymongo) |
| Styling     | CSS animations      |

---

## 📁 Project Structure
crop_recommendation/
├── model/               # Trained ML model (.pkl) 
├── static/              # CSS styles and animations 
├── templates/           # HTML frontend 
├── .env                 # MongoDB credentials 
├── app.py               # Flask backend 
├── requirements.txt     # Python dependencies 
└── README.md            # Project documentation

---

## 📊 Dataset

- Source: [Kaggle – Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
- Features: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall
- Target: Recommended crop label

---

## 🛠️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/crop-recommendation.git
   cd crop-recommendation
   