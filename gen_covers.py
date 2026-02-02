import os
import subprocess
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

os.makedirs(COVER_DIR, exist_ok=True)

for name in os.listdir(VIDEO_DIR):
    if not name.lower().endswith(".mp4"):
        continue

    video_path = os.path.join(VIDEO_DIR, name)
    cover_name = os.path.splitext(name)[0] + ".jpg"
    cover_path = os.path.join(COVER_DIR, cover_name)

    if os.path.exists(cover_path):
        print("已存在，跳过:", cover_name)
        continue

    cmd = [
        "ffmpeg",
        "-y",
        "-ss", "00:00:10",
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        cover_path
    ]

    print("生成封面:", cover_name)
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
