from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to something secure!
bcrypt = Bcrypt(app)

# ---------------------- DB Connection ----------------------
def get_db_connection():
    return sqlite3.connect("database.db")

# ---------------------- User Functions ----------------------
def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_user(username, hashed_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

# ---------------------- Recommendations ----------------------
def get_recommendations_from_db(selected_genres, limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()

    if not selected_genres:
        cursor.execute('''
            SELECT artist, song_name, spotify_url
            FROM songs
            ORDER BY RANDOM()
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

    if len(selected_genres) == 1:
        cursor.execute('''
            SELECT artist, song_name, spotify_url
            FROM songs
            WHERE genre = ?
            ORDER BY RANDOM()
            LIMIT ?
        ''', (selected_genres[0], limit))
        return cursor.fetchall()

    per_genre = max(1, limit // len(selected_genres))
    results = []

    for genre in selected_genres:
        cursor.execute('''
            SELECT artist, song_name, spotify_url
            FROM songs
            WHERE genre = ?
            ORDER BY RANDOM()
            LIMIT ?
        ''', (genre, per_genre))
        results.extend(cursor.fetchall())

    if len(results) < limit:
        placeholders = ','.join('?' for _ in selected_genres)
        query = f'''
            SELECT artist, song_name, spotify_url
            FROM songs
            WHERE genre IN ({placeholders})
            ORDER BY RANDOM()
            LIMIT ?
        '''
        cursor.execute(query, (*selected_genres, limit - len(results)))
        results.extend(cursor.fetchall())

    conn.close()
    return results[:limit]

def save_history(genres, recs):
    if 'user_id' not in session:
        return  # only save for logged-in users
    conn = get_db_connection()
    cursor = conn.cursor()
    for artist, song, url in recs:
        cursor.execute('''
            INSERT INTO history (genres, artist, song_name, spotify_url, user_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (",".join(genres), artist, song, url, session['user_id']))
    conn.commit()
    conn.close()

# ---------------------- Routes ----------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genres = request.form.getlist("genres")
        recommendations = get_recommendations_from_db(genres, 5)

        # Save to database if logged in, else store in session
        if 'user_id' in session:
            save_history(genres, recommendations)
        else:
            session['guest_recs'] = recommendations

        return render_template("result.html", recs=recommendations)
    return render_template("index.html")

@app.route('/history')
def view_history():
    if 'user_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT genres, artist, song_name, spotify_url, timestamp
            FROM history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 50
        ''', (session['user_id'],))
        rows = cursor.fetchall()
        conn.close()
        return render_template("history.html", history=rows)

    elif 'guest_recs' in session:
        guest_history = [
            ("Guest", artist, song, url, "Session only")
            for artist, song, url in session['guest_recs']
        ]
        return render_template("history.html", history=guest_history)

    else:
        return "No history available. Please get recommendations first!"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            save_user(username, hashed_pw)
            return redirect(url_for('login'))
        except:
            return "Username already exists!"
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and bcrypt.check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return "Invalid login credentials"
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ---------------------- Run App ----------------------

if __name__ == "__main__":
    app.run(debug=True)

