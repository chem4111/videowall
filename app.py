from flask import Flask, render_template, send_from_directory
import os
import json

config_file = os.path.join(os.path.dirname(__file__), 'config.json')
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    VIDEO_DIR = config.get('VIDEO_DIR', '/mnt/usb/videos')
    COVER_DIR = config.get('COVER_DIR', '/mnt/usb/covers')
else:
    VIDEO_DIR = '/mnt/usb/videos'
    COVER_DIR = '/mnt/usb/covers'

app = Flask(__name__)

@app.route("/")
def index():
    videos = []
    for f in os.listdir(VIDEO_DIR):
        if f.lower().endswith(".mp4"):
            videos.append(f)
    return render_template("index.html", videos=videos)

@app.route("/play/<path:name>")
def play(name):
    return render_template("play.html", video=name)

@app.route("/videos/<path:filename>")
def videos(filename):
    return send_from_directory(VIDEO_DIR, filename)

@app.route("/covers/<path:filename>")
def covers(filename):
    return send_from_directory(COVER_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
