from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Get song recommendations from the database
def get_recommendations_from_db(selected_genres, limit=5):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    placeholders = ','.join('?' for _ in selected_genres)
    query = f'''
        SELECT artist, song_name, spotify_url
        FROM songs
        WHERE genre IN ({placeholders})
        ORDER BY RANDOM()
        LIMIT ?
    '''
    cursor.execute(query, (*selected_genres, limit))
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genres = request.form.getlist('genres')  # from checkboxes
        recommendations = get_recommendations_from_db(genres)
        return render_template('result.html', recs=recommendations)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

