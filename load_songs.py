import sqlite3
import csv

# Connect to your database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Open the CSV file
with open('songs.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('''
            INSERT INTO songs (artist, genre, song_name, spotify_url)
            VALUES (?, ?, ?, ?)
        ''', (row['artist'], row['genre'], row['song_name'], row['spotify_url']))

# Commit and close
conn.commit()
conn.close()

print("✅ Songs inserted successfully!")

