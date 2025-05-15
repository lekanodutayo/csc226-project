import os
import sqlite3
import csv
import random
import requests
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own

# Spotify Credentials from environment variables (Render Dashboard)
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/set_user', methods=['POST'])
def set_user():
    session['username'] = request.form['username']
    return redirect('/')

@app.route('/guest')
def guest():
    session['guest'] = True
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_genres = request.form.getlist('genre')
    if not selected_genres:
        return redirect('/')

    selected_genre = random.choice(selected_genres)

    # Load songs from CSV
    with open('songs.csv', newline='') as csvfile:
        songs = [row for row in csv.DictReader(csvfile) if row['genre'] == selected_genre]

    recommendations = random.sample(songs, min(4, len(songs)))

    # Save history if not guest
    if not session.get('guest'):
        username = session.get('username')
        conn = get_db_connection()
        for song in recommendations:
            conn.execute(
                'INSERT INTO history (username, genre, song, artist, spotify_link) VALUES (?, ?, ?, ?, ?)',
                (username, selected_genre, song['song'], song['artist'], song['spotify_link'])
            )
        conn.commit()
        conn.close()

    return render_template('result.html', recommendations=recommendations)

@app.route('/history')
def history():
    username = session.get('username')
    if username:
        conn = get_db_connection()
        rows = conn.execute(
            'SELECT * FROM history WHERE username = ? ORDER BY timestamp DESC LIMIT 10',
            (username,)
        ).fetchall()
        conn.close()
        return render_template('history.html', history=rows)
    return render_template('history.html', history=[])

# ------------------ SPOTIFY LOGIN ------------------ #

@app.route('/login')
def login():
    scope = "user-read-private user-read-email"
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?response_type=code&client_id={CLIENT_ID}"
        f"&scope={scope}&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=payload, headers=headers)
    tokens = response.json()
    access_token = tokens.get('access_token')

    if access_token:
        user_info = requests.get(
            'https://api.spotify.com/v1/me',
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()
        session['username'] = user_info.get('display_name', user_info.get('id'))
        session['guest'] = False
    return redirect('/')

# ---------------------------------------------------- #

if __name__ == '__main__':
    app.run(debug=True)

