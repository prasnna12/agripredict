"""
Model information and evaluation engine for AgriPredict AI.
Loads model.pkl, inspects architecture, and calculates genuine empirical accuracy.
"""

import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

MODEL_FILENAME = "model.pkl"
DATASET_FILENAME = "Crop_recommendation.csv"

def get_model_diagnostics(base_dir):
    """
    Load the trained model and extract genuine metrics without falsifying data.
    """
    model_path = os.path.join(base_dir, MODEL_FILENAME)
    dataset_path = os.path.join(base_dir, DATASET_FILENAME)
    
    if not os.path.exists(model_path):
        return {
            "status": "error",
            "message": f"Model file '{MODEL_FILENAME}' not found."
        }
    
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to load model file: {str(e)}"
        }
        
    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    display_names = [
        "Nitrogen (N)", "Phosphorus (P)", "Potassium (K)",
        "Temperature", "Humidity", "Soil pH", "Rainfall"
    ]
    
    # Feature importances
    importances = []
    if hasattr(model, "feature_importances_"):
        raw_imp = model.feature_importances_
        for feat, disp, val in zip(features, display_names, raw_imp):
            importances.append({
                "feature": feat,
                "display_name": disp,
                "importance": round(float(val) * 100, 2)
            })
        importances.sort(key=lambda x: x["importance"], reverse=True)
    
    # Genuine evaluation accuracy
    test_accuracy = None
    overall_accuracy = None
    train_size = 0
    test_size = 0
    
    if os.path.exists(dataset_path):
        try:
            df = pd.read_csv(dataset_path)
            X = df[features]
            y = df["label"]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            train_size = len(X_train)
            test_size = len(X_test)
            test_accuracy = round(float(model.score(X_test, y_test)) * 100, 2)
            overall_accuracy = round(float(model.score(X, y)) * 100, 2)
        except Exception:
            pass
            
    # Hyperparameters
    params = {}
    if hasattr(model, "get_params"):
        all_params = model.get_params()
        key_params = ["n_estimators", "criterion", "max_depth", "min_samples_split", "min_samples_leaf", "random_state", "bootstrap"]
        params = {k: all_params.get(k) for k in key_params if k in all_params}

    return {
        "status": "success",
        "algorithm": "Random Forest Classifier",
        "algorithm_class": type(model).__name__,
        "trees_count": getattr(model, "n_estimators", 100),
        "classes_count": len(getattr(model, "classes_", [])),
        "classes": sorted(list(getattr(model, "classes_", []))),
        "features": features,
        "importances": importances,
        "test_accuracy": test_accuracy,
        "overall_accuracy": overall_accuracy,
        "train_size": train_size,
        "test_size": test_size,
        "hyperparameters": params
    }
