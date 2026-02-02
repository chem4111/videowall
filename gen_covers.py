import os
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(BASE_DIR, 'config.json')

# ================= 配置读取 =================
if os.path.exists(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    VIDEO_DIR = config.get('VIDEO_DIR', '/mnt/usb/videos')
    COVER_DIR = config.get('COVER_DIR', '/mnt/usb/covers')
else:
    VIDEO_DIR = '/mnt/usb/videos'
    COVER_DIR = '/mnt/usb/covers'

os.makedirs(COVER_DIR, exist_ok=True)

# ================= 主逻辑 =================
for name in os.listdir(VIDEO_DIR):
    if not name.lower().endswith('.mp4'):
        continue

    video_path = os.path.join(VIDEO_DIR, name)
    cover_name = os.path.splitext(name)[0] + '.jpg'
    cover_path = os.path.join(COVER_DIR, cover_name)

    if os.path.exists(cover_path):
        print('已存在，跳过:', cover_name)
        continue

    # ffmpeg：精确 seek，稳定优先
    cmd = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-ss', '00:00:20',
        '-vframes', '1',
        '-q:v', '2',
        cover_path
    ]

    print('生成封面:', cover_name)

    result = subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode != 0:
        print('生成失败:', video_path)
