from flask import Flask, render_template, send_from_directory, make_response
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(BASE_DIR, 'config.json')

# ========== 读取配置 ==========
if os.path.exists(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    VIDEO_DIR = config.get('VIDEO_DIR', '/mnt/usb/videos')
    COVER_DIR = config.get('COVER_DIR', '/mnt/usb/covers')
else:
    VIDEO_DIR = '/mnt/usb/videos'
    COVER_DIR = '/mnt/usb/covers'

app = Flask(__name__)

# ========== 首页 ==========
@app.route("/")
def index():
    videos = []
    cover_mtime = {}

    try:
        file_list = os.listdir(VIDEO_DIR)
    except FileNotFoundError:
        file_list = []

    for name in file_list:
        if not name.lower().endswith('.mp4'):
            continue

        videos.append(name)

        cover_name = name.rsplit('.', 1)[0] + '.jpg'
        cover_path = os.path.join(COVER_DIR, cover_name)

        if os.path.exists(cover_path):
            cover_mtime[name] = int(os.path.getmtime(cover_path))
        else:
            cover_mtime[name] = 0

    # 排序，保证刷新顺序稳定
    videos.sort()

    return render_template(
        'index.html',
        videos=videos,
        cover_mtime=cover_mtime
    )

# ========== 播放页面 ==========
@app.route("/play/<path:name>")
def play(name):
    return render_template("play.html", video=name)

# ========== 视频文件 ==========
@app.route("/videos/<path:filename>")
def videos_file(filename):
    return send_from_directory(VIDEO_DIR, filename)

# ========== 封面文件（强制不缓存） ==========
@app.route("/covers/<path:filename>")
def covers_file(filename):
    response = make_response(send_from_directory(COVER_DIR, filename))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# ========== 启动 ==========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
