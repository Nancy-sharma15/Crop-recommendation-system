import pickle
import pandas as pd

# Load model
with open("D:/crop_recommend/model/crop_model.pkl", "rb") as f:
    model = pickle.load(f)

# Sample input as DataFrame
sample = pd.DataFrame([[70, 52, 42, 19.8, 67, 4.5, 102.9]],
                      columns=["Nitrogen", "phosphorus", "potassium", "temperature", "humidity", "ph", "rainfall"])

prediction = model.predict(sample)
print(" Recommended Crop:", prediction[0])