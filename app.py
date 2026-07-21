from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from routes.auth import auth
from routes.dashboard import dashboard
from routes.quiz import quiz

app = Flask(__name__)
app.secret_key = "sonal123"
app.register_blueprint(auth)

app.register_blueprint(dashboard)

app.register_blueprint(quiz)


# -----------------------------
# Database Initialization
# -----------------------------
def init_db():

    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT,

        email TEXT UNIQUE,

        password TEXT

    )
    """)

    # Quizzes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizzes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        description TEXT,

        created_by TEXT

    )
    """)

    # Questions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        quiz_id INTEGER,

        question TEXT,

        option_a TEXT,

        option_b TEXT,

        option_c TEXT,

        option_d TEXT,

        correct_answer TEXT

    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -----------------------------


# -----------------------------




# -----------------------------
# About
# -----------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -----------------------------
# Main
# -----------------------------
init_db()

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
