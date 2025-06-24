from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db_connection()
    cursor = db.cursor()

    edit_id = None

    if request.method == "POST":
        if "start_edit_id" in request.form:
            edit_id = int(request.form["start_edit_id"])

        elif "edit_id" in request.form:
            song_id = request.form["edit_id"]
            new_title = request.form["new_title"]
            new_artist = request.form["new_artist"]
            cursor.execute("UPDATE songs SET title=%s, artist=%s WHERE id=%s", (new_title, new_artist, song_id))
            db.commit()

        elif "title" in request.form and "artist" in request.form:
            title = request.form["title"]
            artist = request.form["artist"]
            cursor.execute("INSERT INTO songs (title, artist) VALUES (%s, %s)", (title, artist))
            db.commit()

    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", songs=songs, edit_id=edit_id)

@app.route("/delete/<int:song_id>")
def delete_song(song_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM songs WHERE id = %s", (song_id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
