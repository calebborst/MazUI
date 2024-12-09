from flask import Flask, render_template, jsonify, send_from_directory, request, abort
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import threading
import random
import time
import xml.etree.ElementTree as ET

app = Flask(__name__)

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
MUSIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music")
gpx_track = []


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














gps_data = {
    "latitude": -36.8485,  
    "longitude": 174.7633,
    "speed": 0, 
    "nextDirection": "straight"
}
def simulate_gps_data():
    directions = ["left", "right", "straight", "uturn"]
    while True:
        gps_data["latitude"] += random.uniform(-0.0001, 0.0001)
        gps_data["longitude"] += random.uniform(-0.0001, 0.0001)
        gps_data["speed"] = random.randint(0, 100)
        gps_data["nextDirection"] = random.choice(directions)  
        time.sleep(1)


@app.route('/gps-data')
def get_gps_data():
    """Return current simulated GPS data."""
    return jsonify(gps_data)


@app.route('/gpx-track')
def get_gpx_track():
    """Return the parsed GPX track points."""
    return jsonify(gpx_track)


@app.route('/upload-gpx', methods=['POST'])
def upload_gpx():
    print("Received a request to upload GPX.")
    if 'file' not in request.files:
        abort(400, description="No file part in the request.")

    file = request.files['file']
    if file.filename == '':
        abort(400, description="No file selected for uploading.")

    if not file.filename.endswith('.gpx'):
        abort(400, description="Invalid file type. Only .gpx files are allowed.")

    filepath = os.path.join(UPLOAD_DIR, file.filename)
    file.save(filepath)
    print(f"Saved file to {filepath}")

    try:
        gpx_track = parse_gpx_custom(filepath)
        #print("Parsed GPX data:", gpx_track)
    except Exception as e:
        #print("Failed to parse GPX:", e)
        abort(500, description="Failed to parse GPX file.")

    return jsonify({"track_points": gpx_track})

def parse_gpx_custom(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            print("Opening file:", filepath)
            track_points = []
            for line in file:
                line = line.strip()
                if '<trkpt' in line:
                    lat = line.split('lat="')[1].split('"')[0]
                    lon = line.split('lon="')[1].split('"')[0]
                    track_points.append({'latitude': float(lat), 'longitude': float(lon)})
        return track_points
    except Exception as e:
        print("Error parsing file:", e)
        raise







@app.route('/upload-directions', methods=['POST'])
def upload_directions():
    print("Received a request to upload GPX for directions.")
    if 'file' not in request.files:
        abort(400, description="No file part in the request.")

    file = request.files['file']
    if file.filename == '':
        abort(400, description="No file selected for uploading.")

    if not file.filename.endswith('.gpx'):
        abort(400, description="Invalid file type. Only .gpx files are allowed.")

    filepath = os.path.join(UPLOAD_DIR, file.filename)
    file.save(filepath)
    print(f"Saved file to {filepath}")

    try:
        directions = parse_rtept(filepath)
        print("Parsed Directions:", directions)
    except Exception as e:
        print("Failed to parse GPX for directions:", e)
        abort(500, description="Failed to parse GPX file.")

    return jsonify({"route_points": directions})


def parse_rtept(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            print("Opening file:", filepath)
            route_points = []
            current_point = None
            buffer = ""

            for line in file:
                line = line.strip()
                buffer += line

                if '</rtept>' in line:
                    if '<rtept' in buffer:
                        try:
                            lat = buffer.split('lat="')[1].split('"')[0]
                            lon = buffer.split('lon="')[1].split('"')[0]
                            desc = buffer.split('<desc>')[1].split('</desc>')[0]
                            route_points.append({
                                'latitude': float(lat),
                                'longitude': float(lon),
                                'instruction': desc
                            })
                            print(f"Captured route point: {route_points[-1]}") 
                        except (IndexError, ValueError) as e:
                            print(f"Error parsing buffer: {buffer} - {e}")
                    buffer = ""  

            print("Captured route points:", len(route_points))
            return route_points

    except Exception as e:
        print("Error parsing file:", e)
        raise













if __name__ == '__main__':
    threading.Thread(target=simulate_data, daemon=True).start()
    threading.Thread(target=simulate_gps_data, daemon=True).start()
    app.run(debug=True)
