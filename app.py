from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def insert_to_db(genres, favorite, recommendations):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (genres, favorite, recommendations) VALUES (?, ?, ?)",
              (",".join(genres), favorite, ",".join(recommendations)))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        genres = request.form.getlist("genres")
        favorite = request.form["favorite"]

        recommendations = []
        if "Pop" in genres:
            recommendations.append("As It Was – Harry Styles")
        if "Rock" in genres:
            recommendations.append("Bohemian Rhapsody – Queen")
        if "Hip-Hop" in genres:
            recommendations.append("SICKO MODE – Travis Scott")
        if "R&B" in genres:
            recommendations.append("Blinding Lights – The Weeknd")

        # Save to the database
        insert_to_db(genres, favorite, recommendations)

        return render_template("result.html", recs=recommendations)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)

