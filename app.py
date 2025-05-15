from flask import Flask, render_template, request, redirect, url_for, session
import random, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Sample song data: (artist, title, Spotify embed URL)
sample_songs = {
    "Pop": [
        ("The Weeknd", "Blinding Lights", "https://open.spotify.com/embed/track/0VjIjW4GlUZAMYd2vXMi3b"),
        ("Dua Lipa", "Levitating", "https://open.spotify.com/embed/track/463CkQjx2Zk1yXoBuierM9"),
        ("Harry Styles", "As It Was", "https://open.spotify.com/embed/track/4LRPiXqCikLlN15c3yImP7")
    ],
    "Rock": [
        ("Queen", "Bohemian Rhapsody", "https://open.spotify.com/embed/track/7tFiyTwD0nx5a1eklYtX2J"),
        ("Nirvana", "Smells Like Teen Spirit", "https://open.spotify.com/embed/track/5ghIJDpPoe3CfHMGu71E6T"),
        ("Eagles", "Hotel California", "https://open.spotify.com/embed/track/40riOy7x9W7GXjyGp4pjAv")
    ],
    "Hip-Hop": [
        ("Travis Scott", "SICKO MODE", "https://open.spotify.com/embed/track/2xLMifQCjDGFmkHkpNLD9h"),
        ("Drake", "God's Plan", "https://open.spotify.com/embed/track/6DCZcSspjsKoFjzjrWoCdn"),
        ("Kendrick Lamar", "Money Trees", "https://open.spotify.com/embed/track/2vwlzO0Qp8kfEtzTsCXfyE")
    ],
    "R&B": [
        ("Mariah Carey", "We Belong Together", "https://open.spotify.com/embed/track/4pbJqGIASGPr0ZpGpnWkDn"),
        ("Jamie Foxx", "Blame It", "https://open.spotify.com/embed/track/0xYTqQeNBMZ5tPjUOJF1EC"),
        ("Miguel", "Adorn", "https://open.spotify.com/embed/track/0iM1M9CzZkLXEfpKzRddHI")
    ],
    "Norteñas": [
        ("Peso Pluma", "LADY GAGA", "https://open.spotify.com/embed/track/0fZKkcrbZk4WkOrcFJbrZT"),
        ("Natanael Cano", "AMG", "https://open.spotify.com/embed/track/5odlY52u43F5BjByhxg7wg"),
        ("Peso Pluma", "PRC", "https://open.spotify.com/embed/track/6UjfByV0nHNs5WJvTPAsvm")
    ]
}

# In-memory user store (temporary)
users = {"test": "test"}  # username: password

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_genres = request.form.getlist("genres")
        if not selected_genres:
            return redirect(url_for("home"))

        recs = []
        for genre in selected_genres:
            if genre in sample_songs:
                recs.extend(random.sample(sample_songs[genre], min(1, len(sample_songs[genre]))))

        # Save to history
        if "history" not in session:
            session["history"] = []

        for artist, title, url in recs:
            session["history"].append(
                (session.get("username", "Guest"), artist, title, url, datetime.now().strftime("%Y-%m-%d %H:%M"))
            )

        return render_template("result.html", recs=recs)

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        if users.get(u) == p:
            session["username"] = u
            return redirect(url_for("home"))
        return "Invalid login", 401
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        users[u] = p
        session["username"] = u
        return redirect(url_for("home"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/history")
def history():
    h = session.get("history", [])
    return render_template("history.html", history=h[::-1])  # reverse chronological

if __name__ == "__main__":
    app.run(debug=True)

