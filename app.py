from flask import Flask, render_template, request, redirect, url_for, session
import os, random

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify Embed URIs (just the embed part, not full iframe yet)
sample_songs = {
    "Pop": [
        "https://open.spotify.com/embed/track/0VjIjW4GlUZAMYd2vXMi3b",  # Blinding Lights
        "https://open.spotify.com/embed/track/4h9wh7iOZ0GGn8QVp4RAOB",  # Levitating
        "https://open.spotify.com/embed/track/4aWmUDTfIPGksMNLV2rQP2"   # As It Was
    ],
    "Rock": [
        "https://open.spotify.com/embed/track/7tFiyTwD0nx5a1eklYtX2J",  # Bohemian Rhapsody
        "https://open.spotify.com/embed/track/5ghIJDpPoe3CfHMGu71E6T",  # Smells Like Teen Spirit
        "https://open.spotify.com/embed/track/40riOy7x9W7GXjyGp4pjAv"   # Hotel California
    ],
    "Hip-hop": [
        "https://open.spotify.com/embed/track/2xLMifQCjDGFmkHkpNLD9h",  # SICKO MODE
        "https://open.spotify.com/embed/track/3qT4bUD1MaWpGrTwcvguhb",  # God's Plan
        "https://open.spotify.com/embed/track/2dLLR6qlu5UJ5gk0dKz0h3"   # Money Trees
    ],
    "R&B": [
        "https://open.spotify.com/embed/track/2BtE7qm1qzM80p9vLSiXkj",  # We Belong Together
        "https://open.spotify.com/embed/track/4RCwb5c5zQfQVsGiFOy1cM",  # Blame It
        "https://open.spotify.com/embed/track/4w8niZpiMy6qz1mntFA5uM"   # Adorn
    ],
    "Norteñas": [
        "https://open.spotify.com/embed/track/1WkMMavIMc4x3bpaIw74v2",  # LADY GAGA
        "https://open.spotify.com/embed/track/1z3HgkzqdeMPv9zM7EZGdh",  # AMG
        "https://open.spotify.com/embed/track/7MAibcTli4IisCtbHKrGMh"   # PRC
    ]
}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    genre = request.form.get("genre")
    if not genre or genre not in sample_songs:
        return redirect(url_for("home"))

    recommended = random.sample(sample_songs[genre], min(3, len(sample_songs[genre])))
    return render_template("result.html", songs=recommended)

if __name__ == "__main__":
    app.run(debug=True)

