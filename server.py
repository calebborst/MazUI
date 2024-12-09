from flask import Flask, render_template, jsonify, send_from_directory
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import threading
import random
import time

app = Flask(__name__)

MUSIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music")

def get_mp3_metadata(file_path):
    """Extract metadata from an MP3 file."""
    try:
        audio = MP3(file_path, ID3=EasyID3)
        title = audio.get("title", [None])[0]
        artist = audio.get("artist", [None])[0]
        album = audio.get("album", [None])[0]
        metadata = {
            "title": title if title else os.path.splitext(os.path.basename(file_path))[0],
            "artist": artist if artist else "Unknown",
            "album": album if album else "Unknown",
            "length": round(audio.info.length),
            "file": os.path.relpath(file_path, MUSIC_DIR),
        }
    except Exception as e:
        print(f"Error reading metadata for {file_path}: {e}")
        metadata = {
            "title": os.path.splitext(os.path.basename(file_path))[0],
            "artist": "Unknown",
            "album": "Unknown",
            "length": 0,
            "file": os.path.relpath(file_path, MUSIC_DIR), 
        }
    return metadata



# Simulated data
obd_data = {"RPM": 0, "Speed": 0, "Coolant": 0}

def simulate_data():
    while True:
        obd_data["RPM"] = random.randint(500, 6000)
        obd_data["Speed"] = random.randint(0, 240)
        obd_data["Coolant"] = random.randint(70, 120)
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(obd_data)

@app.route("/music")
def list_music():
    """List all MP3 files and their metadata in the music directory, grouped by folders."""
    music_structure = {}

    for root, dirs, files in os.walk(MUSIC_DIR):
        rel_path = os.path.relpath(root, MUSIC_DIR)
        music_structure[rel_path] = []

        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                music_structure[rel_path].append(get_mp3_metadata(file_path))

    return jsonify(music_structure)


from flask import abort

@app.route("/play/<path:filename>")
def play_music(filename):
    """Serve MP3 files from the music directory, including subfolders."""
    file_path = os.path.join(MUSIC_DIR, filename)

    if not os.path.commonpath([MUSIC_DIR, os.path.abspath(file_path)]) == MUSIC_DIR or not os.path.exists(file_path):
        abort(404)

    return send_from_directory(MUSIC_DIR, filename)


if __name__ == '__main__':
    threading.Thread(target=simulate_data, daemon=True).start()
    app.run(debug=True)
