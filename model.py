import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv('Crop_recommendation.csv')

# Features and labels
X = data[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
y = data["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train
model.fit(X_train, y_train)

# Accuracy check (optional)
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)

# Save model
pickle.dump(model, open("model.pkl", "wb"))