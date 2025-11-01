import pandas as pd

df = pd.read_csv("D:/crop_recommend/data/Crop_recommendation.csv")

df = df.iloc[:, :-2]
print(df.columns)
print(df.head())
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle

# Load and clean data
df = pd.read_csv("D:/crop_recommend/data/Crop_recommendation.csv")
df = df.dropna(axis=1, how="all")  # Removes empty columns

# Features and target
X = df.drop("label", axis=1)
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
with open("D:/crop_recommend/model/crop_model.pkl", "wb") as f:
    pickle.dump(model, f)

print(" Model trained and saved successfully.")