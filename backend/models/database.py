"""
Database Models and Initialization
====================================
Uses SQLite for local development (simulating a cloud database).
In production, this can be swapped for a cloud-managed database
like Firestore, Supabase, or Cloud SQL without changing the API layer.

Cloud Computing Concept Demonstrated:
- Cloud Database: Centralized data storage accessible via API
- Data Isolation: Each user can only access their own data
- Schema Design: Normalized tables for users, plans, and files
"""

import sqlite3
import os
from datetime import datetime

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'diet_planner.db')


def get_db():
    """Get a database connection with row factory enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Initialize the database schema.
    Creates tables for users, diet plans, and user files.
    
    Tables:
    - users: Stores user credentials and profile information
    - diet_plans: Stores AI-generated diet plans linked to users
    - user_files: Stores metadata for uploaded files (cloud storage simulation)
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()

    # ── Users Table ────────────────────────────────────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            age INTEGER,
            height_cm REAL,
            weight_kg REAL,
            sex TEXT DEFAULT 'not_specified',
            activity_level TEXT DEFAULT 'moderate',
            dietary_preference TEXT DEFAULT 'vegetarian',
            goal TEXT DEFAULT 'maintain',
            allergies TEXT DEFAULT '[]',
            cuisines TEXT DEFAULT '[]',
            budget_per_day REAL DEFAULT 0,
            timeline_weeks INTEGER DEFAULT 4,
            profile_completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ── Diet Plans Table ───────────────────────────────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diet_plans (
            plan_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            plan_name TEXT DEFAULT 'My Diet Plan',
            breakfast TEXT NOT NULL,
            lunch TEXT NOT NULL,
            snack TEXT NOT NULL,
            dinner TEXT NOT NULL,
            total_calories INTEGER DEFAULT 0,
            protein_g REAL DEFAULT 0,
            carbs_g REAL DEFAULT 0,
            fat_g REAL DEFAULT 0,
            nutrition_summary TEXT DEFAULT '',
            hydration_reminder TEXT DEFAULT 'Drink at least 8 glasses (2L) of water daily',
            diet_type TEXT DEFAULT 'vegetarian',
            goal_type TEXT DEFAULT 'maintain',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')

    # ── User Files Table (Cloud Storage Simulation) ────────────────
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_files (
            file_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            storage_path TEXT NOT NULL,
            file_size INTEGER DEFAULT 0,
            file_type TEXT DEFAULT 'unknown',
            uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")
