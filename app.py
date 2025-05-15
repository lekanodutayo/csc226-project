from flask import Flask, render_template, request, redirect, url_for, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Sample data by genre
sample_songs = {
    "Pop": [("Blinding Lights", "The Weeknd"), ("Levitating", "Dua Lipa"), ("As It Was", "Harry Styles")],
    "Rock": [("Bohemian Rhapsody", "Queen"), ("Smells Like Teen Spirit", "Nirvana"), ("Hotel California", "Eagles")],
    "Hip-Hop": [("SICKO MODE", "Travis Scott"), ("God's Plan", "Drake"), ("Money Trees", "Kendrick Lamar")],
    "R&B": [("We Belong Together", "Mariah Carey"), ("Blame It", "Jamie Foxx"), ("Adorn", "Miguel")],
    "Norteñas": [("LADY GAGA", "Peso Pluma"), ("AMG", "Natanael Cano"), ("PRC", "Peso Pluma")]
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    genre = request.form.get("genre")
    if not genre or genre not in sample_songs:
        return redirect(url_for("home"))

    # Randomly choose 3 songs from the genre
    recommended = random.sample(sample_songs[genre], min(3, len(sample_songs[genre])))

    return render_template("result.html", songs=recommended)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

