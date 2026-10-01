import sqlite3
import os
from datetime import datetime

def get_db_connection(db_path):
    """Establish and return a SQLite database connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path):
    """Initialize the SQLite database schema for users and predictions."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Predictions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                nitrogen REAL NOT NULL,
                phosphorus REAL NOT NULL,
                potassium REAL NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                ph REAL NOT NULL,
                rainfall REAL NOT NULL,
                predicted_crop TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Migration check: Ensure user_id column exists if table existed previously
        cursor.execute("PRAGMA table_info(predictions)")
        columns = [row["name"] for row in cursor.fetchall()]
        if "user_id" not in columns:
            try:
                cursor.execute("ALTER TABLE predictions ADD COLUMN user_id INTEGER")
            except Exception:
                pass

        conn.commit()

# -------------------------------------------------------------------
# User Authentication Helpers
# -------------------------------------------------------------------

def create_user(db_path, full_name, email, username, password_hash):
    """Create a new user record. Returns new user id."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (full_name, email, username, password_hash, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            full_name.strip(),
            email.strip().lower(),
            username.strip().lower(),
            password_hash,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        return cursor.lastrowid

def get_user_by_id(db_path, user_id):
    """Fetch user by id."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_user_by_username_or_email(db_path, identifier):
    """Fetch user by either username or email."""
    ident = identifier.strip().lower()
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM users 
            WHERE username = ? OR email = ?
            LIMIT 1
        """, (ident, ident))
        row = cursor.fetchone()
        return dict(row) if row else None

def email_or_username_exists(db_path, email, username):
    """Check if either email or username is already registered."""
    e = email.strip().lower()
    u = username.strip().lower()
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE email = ? LIMIT 1", (e,))
        if cursor.fetchone():
            return "Email is already registered. Please login instead."
        
        cursor.execute("SELECT 1 FROM users WHERE username = ? LIMIT 1", (u,))
        if cursor.fetchone():
            return "Username is already taken. Please choose another username."
            
    return None

# -------------------------------------------------------------------
# Predictions Data Helpers (User-Specific)
# -------------------------------------------------------------------

def insert_prediction(db_path, user_id, n, p, k, temperature, humidity, ph, rainfall, predicted_crop):
    """Insert a new prediction record for a specific user."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions (
                user_id, nitrogen, phosphorus, potassium,
                temperature, humidity, ph, rainfall,
                predicted_crop, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            float(n), float(p), float(k),
            float(temperature), float(humidity), float(ph), float(rainfall),
            str(predicted_crop).strip().lower(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        return cursor.lastrowid

def get_recent_predictions(db_path, user_id=None, limit=50):
    """Fetch recent predictions for a specific user or all if user_id is None."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("""
                SELECT id, user_id, nitrogen, phosphorus, potassium,
                       temperature, humidity, ph, rainfall,
                       predicted_crop, created_at
                FROM predictions
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
            """, (user_id, limit))
        else:
            cursor.execute("""
                SELECT id, user_id, nitrogen, phosphorus, potassium,
                       temperature, humidity, ph, rainfall,
                       predicted_crop, created_at
                FROM predictions
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
        return [dict(row) for row in cursor.fetchall()]

def get_prediction_stats(db_path, user_id=None):
    """Calculate summary statistics for predictions (filtered by user if supplied)."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        where_clause = "WHERE user_id = ?" if user_id else ""
        params = (user_id,) if user_id else ()
        
        # Total count
        cursor.execute(f"SELECT COUNT(*) AS total FROM predictions {where_clause}", params)
        total = cursor.fetchone()["total"]
        
        # Latest prediction
        cursor.execute(f"""
            SELECT predicted_crop, created_at 
            FROM predictions 
            {where_clause}
            ORDER BY id DESC 
            LIMIT 1
        """, params)
        latest_row = cursor.fetchone()
        latest = dict(latest_row) if latest_row else None
        
        # Most recommended crop
        cursor.execute(f"""
            SELECT predicted_crop, COUNT(*) as cnt 
            FROM predictions 
            {where_clause}
            GROUP BY predicted_crop 
            ORDER BY cnt DESC 
            LIMIT 1
        """, params)
        top_row = cursor.fetchone()
        top_crop = top_row["predicted_crop"].capitalize() if top_row else "None"
        
        # Crop frequency distribution
        cursor.execute(f"""
            SELECT predicted_crop, COUNT(*) as cnt 
            FROM predictions 
            {where_clause}
            GROUP BY predicted_crop 
            ORDER BY cnt DESC 
            LIMIT 10
        """, params)
        distribution = {row["predicted_crop"].capitalize(): row["cnt"] for row in cursor.fetchall()}
        
        return {
            "total_predictions": total,
            "latest_prediction": latest,
            "most_recommended_crop": top_crop,
            "distribution": distribution
        }

def clear_predictions(db_path, user_id=None):
    """Safely clear prediction history for a specific user (or all if user_id is None)."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("DELETE FROM predictions WHERE user_id = ?", (user_id,))
        else:
            cursor.execute("DELETE FROM predictions")
        conn.commit()
