"""
Dataset analyzer for AgriPredict AI.
Extracts empirical metrics and distributions from Crop_recommendation.csv.
"""

import os
import pandas as pd
import numpy as np

CSV_FILENAME = "Crop_recommendation.csv"

def load_dataset_stats(base_dir):
    """
    Load and calculate real summary statistics from Crop_recommendation.csv.
    Returns a structured dictionary of metadata, distributions, and summary stats.
    """
    csv_path = os.path.join(base_dir, CSV_FILENAME)
    if not os.path.exists(csv_path):
        return None
    
    df = pd.read_csv(csv_path)
    
    total_rows = int(len(df))
    total_cols = int(df.shape[1])
    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    target_col = "label"
    
    unique_crops = sorted([str(c) for c in df[target_col].unique()])
    crop_counts = df[target_col].value_counts().to_dict()
    
    # Feature summary statistics
    stats_df = df[features].describe().round(2).to_dict()
    feature_stats = []
    
    display_names = {
        "N": "Nitrogen (N)",
        "P": "Phosphorus (P)",
        "K": "Potassium (K)",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "ph": "Soil pH",
        "rainfall": "Rainfall"
    }
    units = {
        "N": "kg/ha / ppm",
        "P": "kg/ha / ppm",
        "K": "kg/ha / ppm",
        "temperature": "°C",
        "humidity": "%",
        "ph": "pH",
        "rainfall": "mm"
    }
    
    for feat in features:
        feature_stats.append({
            "feature": feat,
            "display_name": display_names.get(feat, feat),
            "unit": units.get(feat, ""),
            "min": stats_df[feat]["min"],
            "max": stats_df[feat]["max"],
            "mean": stats_df[feat]["mean"],
            "std": stats_df[feat]["std"],
            "median": stats_df[feat]["50%"]
        })
        
    # Crop-wise parameter means for comparison charts
    crop_means = df.groupby(target_col)[features].mean().round(1).to_dict(orient="index")
    
    # First 15 preview rows
    sample_preview = df.head(15).to_dict(orient="records")
    
    return {
        "filename": CSV_FILENAME,
        "total_rows": total_rows,
        "total_cols": total_cols,
        "unique_crops_count": len(unique_crops),
        "crops_list": unique_crops,
        "crop_counts": crop_counts,
        "feature_stats": feature_stats,
        "crop_means": crop_means,
        "sample_preview": sample_preview
    }
