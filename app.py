from flask import Flask, render_template, request, redirect, url_for, session
import os, random

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify embed track links by genre
sample_songs = {
    "Pop": [
        "https://open.spotify.com/embed/track/0VjIjW4GlUZAMYd2vXMi3b",
        "https://open.spotify.com/embed/track/4h9wh7iOZ0GGn8QVp4RAOB",
        "https://open.spotify.com/embed/track/4aWmUDTfIPGksMNLV2rQP2"
    ],
    "Rock": [
        "https://open.spotify.com/embed/track/7tFiyTwD0nx5a1eklYtX2J",
        "https://open.spotify.com/embed/track/5ghIJDpPoe3CfHMGu71E6T",
        "https://open.spotify.com/embed/track/40riOy7x9W7GXjyGp4pjAv"
    ],
    "Hip-Hop": [
        "https://open.spotify.com/embed/track/2xLMifQCjDGFmkHkpNLD9h",
        "https://open.spotify.com/embed/track/3qT4bUD1MaWpGrTwcvguhb",
        "https://open.spotify.com/embed/track/2dLLR6qlu5UJ5gk0dKz0h3"
    ],
    "R&B": [
        "https://open.spotify.com/embed/track/2BtE7qm1qzM80p9vLSiXkj",
        "https://open.spotify.com/embed/track/4RCwb5c5zQfQVsGiFOy1cM",
        "https://open.spotify.com/embed/track/4w8niZpiMy6qz1mntFA5uM"
    ],
    "Latin music": [
        "https://open.spotify.com/embed/track/1WkMMavIMc4x3bpaIw74v2",
        "https://open.spotify.com/embed/track/1z3HgkzqdeMPv9zM7EZGdh",
        "https://open.spotify.com/embed/track/7MAibcTli4IisCtbHKrGMh"
    ],
    "Afro-Beat": [
        "https://open.spotify.com/playlist/37i9dQZF1DZ06evO0vEAMw?si=4XKHagefQBubQcsx33xrCA",
        "https://open.spotify.com/track/2IBrgYf3Hjw16c6oNwkZ9M?si=1d776b19e1de48c0",
        "https://open.spotify.com/track/1mk8ZC9OeTZMr8Wy31LqRj?si=60e63076aee044d0"
    ]
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        genres = request.form.getlist("genres")
        if not genres:
            return render_template("index.html", error="Please select at least one genre.")

        recommendations = []
        if "Pop" in genres:
            recommendations.append("<a href='https://open.spotify.com/album/2pqdSWeJVsXAhHFuVLzuA8'>As It Was — Harry Styles</a>")
        if "Rock" in genres:
            recommendations.append("Bohemian Rhapsody — Queen")
        if "Hip-Hop" in genres:
            recommendations.append("SICKO MODE — Travis Scott")
        if "R&B" in genres:
            recommendations.append("Blinding Lights — The Weeknd")
        if "Afro-Beat" in genres:
            recommendations.append("Fall- Davvido")
        if "Afro-Beat" in genres:
            recommendations.append("Morayo - Wizkid")

        return render_template("result.html", recs=all_recs, genres=genres)

    return render_template("index.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

