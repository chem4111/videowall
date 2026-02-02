import os
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(BASE_DIR, 'config.json')

# ========== 配置 ==========
if os.path.exists(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    VIDEO_DIR = config.get('VIDEO_DIR', '/mnt/usb/videos')
    COVER_DIR = config.get('COVER_DIR', '/mnt/usb/covers')
else:
    VIDEO_DIR = '/mnt/usb/videos'
    COVER_DIR = '/mnt/usb/covers'

os.makedirs(COVER_DIR, exist_ok=True)

# ========== 主逻辑 ==========
for name in os.listdir(VIDEO_DIR):
    if not name.lower().endswith('.mp4'):
        continue

    video_path = os.path.join(VIDEO_DIR, name)
    cover_name = os.path.splitext(name)[0] + '.jpg'
    cover_path = os.path.join(COVER_DIR, cover_name)

    if os.path.exists(cover_path):
        print('已存在，跳过:', cover_name)
        continue

    print('生成封面:', cover_name)

    cmd = [
        'ffmpeg',
        '-loglevel', 'error',   # 关键：防止刷屏和假死感
        '-y',
        '-ss', '00:00:20',      # input seek，快
        '-i', video_path,
        '-frames:v', '1',
        '-q:v', '2',
        cover_path
    ]

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print('失败:', video_path)
