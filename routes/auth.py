from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

auth = Blueprint("auth", __name__)


# -----------------------------
# Register
# -----------------------------
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO users(fullname, email, password) VALUES (?, ?, ?)",
                (fullname, email, password)
            )

            conn.commit()
            conn.close()

            return redirect(url_for("auth.login"))

        except sqlite3.IntegrityError:

            conn.close()
            return "<h2>Email already registered!</h2>"

    return render_template("register.html")


# -----------------------------
# Login
# -----------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("quiz.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user"] = user[1]

            return redirect(url_for("dashboard.dashboard_page"))

        else:

            return "<h2>Invalid Email or Password ❌</h2>"

    return render_template("login.html")


# -----------------------------
# Logout
# -----------------------------
@auth.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("home"))