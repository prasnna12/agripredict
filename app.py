"""
AgriPredict AI - Smart Crop Classification & Recommendation System
Flask Web Application Backend with Session Authentication & SQLite Persistence
"""

import os
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from functools import wraps
from flask import (
    Flask, request, render_template, redirect, url_for,
    session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

# Custom helper modules
from database import db
from crop_catalog import CROP_DETAILS, SAMPLE_PRESETS, validate_parameters, get_crop_metadata
from dataset_analyzer import load_dataset_stats
from model_info import get_model_diagnostics

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "predictions.db")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# Initialize Flask application
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
app.secret_key = os.environ.get("SECRET_KEY", "agripredict-ai-production-secret-key-2026")

# Initialize database schema automatically and seed default demo user
try:
    db.init_db(DB_PATH)
    # Check if any user exists; if not, create demo user
    with db.get_db_connection(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS cnt FROM users")
        if cursor.fetchone()["cnt"] == 0:
            db.create_user(
                DB_PATH,
                full_name="Dr. Alex Rivera",
                email="admin@agripredict.ai",
                username="admin",
                password_hash=generate_password_hash("password123")
            )
            print("Seeded default demo user: admin / password123")
except Exception as e:
    print(f"Warning: Database initialization exception: {e}")

# Load trained Random Forest model
FEATURE_NAMES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
model = None

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("Model loaded successfully from model.pkl")
    else:
        print("Warning: model.pkl not found at path:", MODEL_PATH)
except Exception as e:
    print("Error loading model.pkl:", str(e))

def get_current_user():
    """Retrieve logged in user dictionary from session if authenticated."""
    user_id = session.get("user_id")
    if user_id:
        return db.get_user_by_id(DB_PATH, user_id)
    return None

def login_required(f):
    """Decorator to protect routes requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_global_data():
    """Inject globally accessible template data."""
    return {
        "current_year": datetime.now().year,
        "current_user": get_current_user(),
        "presets": SAMPLE_PRESETS
    }

# -------------------------------------------------------------------
# Authentication Routes
# -------------------------------------------------------------------

@app.route("/")
@app.route("/home")
def index():
    """Application entry point: redirect to dashboard if authenticated, else login."""
    if "user_id" in session:
        return redirect(url_for("dashboard_page"))
    return redirect(url_for("login_page"))

@app.route("/home_alias")
def home():
    """Alias for backwards compatibility."""
    return index()

@app.route("/favicon.ico")
def favicon():
    """Favicon endpoint to avoid 404 error handler triggers."""
    return "", 204

@app.route("/login", methods=["GET"])
def login_page():
    """Render split-screen login page."""
    if "user_id" in session:
        return redirect(url_for("dashboard_page"))
    return render_template("login.html", active_page="login")

@app.route("/login", methods=["POST"])
def login_post():
    """Process user login credentials."""
    identifier = request.form.get("username_or_email", "").strip()
    password = request.form.get("password", "")

    if not identifier or not password:
        flash("Please enter both username/email and password.", "error")
        return redirect(url_for("login_page"))

    user = db.get_user_by_username_or_email(DB_PATH, identifier)
    if not user or not check_password_hash(user["password_hash"], password):
        flash("Invalid username/email or password. Please try again.", "error")
        return redirect(url_for("login_page"))

    # Login successful: store in session
    session.clear()
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    flash(f"Welcome back, {user['full_name']}!", "success")
    return redirect(url_for("dashboard_page"))

@app.route("/signup", methods=["GET"])
def signup_page():
    """Render registration page."""
    if "user_id" in session:
        return redirect(url_for("dashboard_page"))
    return render_template("signup.html", active_page="signup", form_data={})

@app.route("/signup", methods=["POST"])
def signup_post():
    """Process new user registration."""
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    form_data = {
        "full_name": full_name,
        "email": email,
        "username": username
    }

    if not full_name or not email or not username or not password:
        flash("All fields are required.", "error")
        return render_template("signup.html", form_data=form_data)

    if "@" not in email or "." not in email:
        flash("Please provide a valid email address.", "error")
        return render_template("signup.html", form_data=form_data)

    if len(password) < 6:
        flash("Password must be at least 6 characters long.", "error")
        return render_template("signup.html", form_data=form_data)

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return render_template("signup.html", form_data=form_data)

    # Check for duplicate email or username
    dup_error = db.email_or_username_exists(DB_PATH, email, username)
    if dup_error:
        flash(dup_error, "error")
        return render_template("signup.html", form_data=form_data)

    try:
        pw_hash = generate_password_hash(password)
        new_user_id = db.create_user(DB_PATH, full_name, email, username, pw_hash)
        session.clear()
        session["user_id"] = new_user_id
        session["username"] = username
        flash("Account created successfully! Welcome to AgriPredict AI.", "success")
        return redirect(url_for("dashboard_page"))
    except Exception as e:
        flash(f"Registration error: {str(e)}", "error")
        return render_template("signup.html", form_data=form_data)

@app.route("/logout")
def logout():
    """Log out current user and clear session."""
    session.clear()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for("login_page"))

# -------------------------------------------------------------------
# Protected Dashboard & History Routes
# -------------------------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard_page():
    """Main SaaS Dashboard with 100% clickable feature hub cards."""
    user = get_current_user()
    try:
        stats = db.get_prediction_stats(DB_PATH, user_id=user["id"])
        predictions = db.get_recent_predictions(DB_PATH, user_id=user["id"], limit=10)
    except Exception as e:
        print(f"Error fetching dashboard data: {e}")
        stats = {
            "total_predictions": 0,
            "latest_prediction": None,
            "most_recommended_crop": "None",
            "distribution": {}
        }
        predictions = []

    return render_template(
        "dashboard.html",
        active_page="dashboard",
        stats=stats,
        predictions=predictions
    )

@app.route("/history")
@login_required
def history_page():
    """Dedicated prediction history table for the authenticated user."""
    user = get_current_user()
    try:
        predictions = db.get_recent_predictions(DB_PATH, user_id=user["id"], limit=100)
    except Exception as e:
        print(f"Error fetching history: {e}")
        predictions = []

    return render_template(
        "history.html",
        active_page="history",
        predictions=predictions
    )

@app.route("/clear_history", methods=["POST"])
@login_required
def clear_history():
    """Safely clear prediction history for the current user."""
    user = get_current_user()
    try:
        db.clear_predictions(DB_PATH, user_id=user["id"])
        flash("Your prediction history has been cleared.", "success")
    except Exception as e:
        flash(f"Failed to clear history: {str(e)}", "error")
    return redirect(url_for("history_page"))

@app.route("/profile")
@login_required
def profile_page():
    """User account details, telemetry, and logout."""
    user = get_current_user()
    stats = db.get_prediction_stats(DB_PATH, user_id=user["id"])
    return render_template("profile.html", active_page="profile", stats=stats)

# -------------------------------------------------------------------
# Crop Prediction (Protected)
# -------------------------------------------------------------------

@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict_page():
    """Crop prediction page and form handler."""
    if request.method == "POST":
        return handle_prediction()
    return render_template("crop.html", active_page="predict", inputs=None, prediction=None)

@app.route("/predict_crop", methods=["POST"])
@login_required
def predict_endpoint():
    """Dedicated POST route for form submission."""
    return handle_prediction()

def handle_prediction():
    """Process crop prediction request, validate data, run inference, and log result."""
    user = get_current_user()
    if model is None:
        flash("Machine learning model is currently unavailable. Please verify model.pkl exists.", "error")
        return redirect(url_for("predict_page"))

    data = request.form
    n_raw = data.get("Nitrogen") or data.get("n")
    p_raw = data.get("Phosphorus") or data.get("p")
    k_raw = data.get("Potassium") or data.get("k")
    temp_raw = data.get("temperature") or data.get("temp")
    hum_raw = data.get("humidity") or data.get("hum")
    ph_raw = data.get("pH") or data.get("ph")
    rain_raw = data.get("rainfall") or data.get("rain")

    # Validate parameters
    cleaned, error_msg = validate_parameters(n_raw, p_raw, k_raw, temp_raw, hum_raw, ph_raw, rain_raw)
    
    inputs_dict = {
        "Nitrogen": n_raw or "",
        "Phosphorus": p_raw or "",
        "Potassium": k_raw or "",
        "temperature": temp_raw or "",
        "humidity": hum_raw or "",
        "pH": ph_raw or "",
        "rainfall": rain_raw or ""
    }

    if error_msg:
        flash(error_msg, "error")
        return render_template(
            "crop.html",
            active_page="predict",
            inputs=inputs_dict,
            prediction=None
        )

    try:
        feature_values = [
            cleaned["Nitrogen (N)"],
            cleaned["Phosphorus (P)"],
            cleaned["Potassium (K)"],
            cleaned["Temperature"],
            cleaned["Humidity"],
            cleaned["Soil pH"],
            cleaned["Rainfall"]
        ]
        features_df = pd.DataFrame([feature_values], columns=FEATURE_NAMES)

        # Run model inference
        prediction_result = model.predict(features_df)[0]
        crop_name = str(prediction_result).strip().lower()

        # Extract confidence score
        confidence = None
        if hasattr(model, "predict_proba"):
            try:
                probabilities = model.predict_proba(features_df)[0]
                confidence = round(float(max(probabilities)) * 100, 1)
            except Exception:
                pass

        # Log prediction to SQLite for current user
        try:
            db.insert_prediction(
                DB_PATH,
                user["id"] if user else None,
                cleaned["Nitrogen (N)"],
                cleaned["Phosphorus (P)"],
                cleaned["Potassium (K)"],
                cleaned["Temperature"],
                cleaned["Humidity"],
                cleaned["Soil pH"],
                cleaned["Rainfall"],
                crop_name
            )
        except Exception as db_err:
            print(f"Database logging error: {db_err}")

        crop_meta = get_crop_metadata(crop_name)

        return render_template(
            "crop.html",
            active_page="predict",
            inputs=inputs_dict,
            prediction=crop_name,
            crop_meta=crop_meta,
            confidence=confidence
        )

    except Exception as e:
        flash(f"Inference error: {str(e)}", "error")
        return render_template(
            "crop.html",
            active_page="predict",
            inputs=inputs_dict,
            prediction=None
        )

# -------------------------------------------------------------------
# Informational & Analytical Pages (Clickable from Hub & Sidebar)
# -------------------------------------------------------------------

@app.route("/how-it-works")
def how_it_works_page():
    """Visual workflow and 5-step explanation page."""
    return render_template("how-it-works.html", active_page="how_it_works")

@app.route("/dataset")
def dataset_page():
    """Dataset exploration and dynamic statistics page."""
    dataset_stats = load_dataset_stats(BASE_DIR)
    if dataset_stats is None:
        return render_template(
            "error.html",
            error_code=404,
            error_title="Dataset Not Found",
            error_message="The benchmark dataset Crop_recommendation.csv was not found on the server."
        ), 404
    return render_template("dataset.html", active_page="dataset", dataset_stats=dataset_stats)

@app.route("/model")
def model_page():
    """Model information and evaluation page."""
    model_diag = get_model_diagnostics(BASE_DIR)
    return render_template("model.html", active_page="model", model_diag=model_diag)

@app.route("/about")
def about_page():
    """About project, benefits, and contact page."""
    return render_template("about.html", active_page="about")

# Backward compatibility alias
@app.route("/report")
def report_alias():
    return redirect(url_for("history_page"))

# -------------------------------------------------------------------
# Error Handlers
# -------------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template(
        "error.html",
        error_code=404,
        error_title="Page Not Found",
        error_message="The page you are looking for does not exist or has been moved."
    ), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template(
        "error.html",
        error_code=500,
        error_title="Internal Server Error",
        error_message="A server error occurred. Please try again or return to the dashboard."
    ), 500

# -------------------------------------------------------------------
# Application Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="127.0.0.1", port=5000)