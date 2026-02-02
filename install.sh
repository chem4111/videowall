#!/bin/sh
# 视频海报墙安装脚本（一次安装，路径固化）

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "======================================"
echo "开始安装所需依赖（python3、flask、ffmpeg）"
echo "======================================"

apt update
apt install -y python3 python3-flask

if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "未检测到 ffmpeg，尝试安装..."
    apt install -y ffmpeg || echo "❌ ffmpeg 安装失败（需手动处理）"
fi

echo ""
echo "======================================"
echo "配置视频和封面目录"
echo "======================================"

printf "请输入视频目录路径 [默认: /mnt/usb/videos]: "
read VIDEO_DIR_INPUT
VIDEO_DIR=${VIDEO_DIR_INPUT:-/mnt/usb/videos}

printf "请输入封面目录路径 [默认: /mnt/usb/covers]: "
read COVER_DIR_INPUT
COVER_DIR=${COVER_DIR_INPUT:-/mnt/usb/covers}

mkdir -p "$VIDEO_DIR" "$COVER_DIR"

cat > "$PROJECT_DIR/config.json" <<EOF
{
  "VIDEO_DIR": "$VIDEO_DIR",
  "COVER_DIR": "$COVER_DIR"
}
EOF

if [ ! -f "$VIDEO_DIR/../README.txt" ]; then
cat > "$VIDEO_DIR/../README.txt" <<EOF
这是视频海报墙的内容目录
videos/  放视频文件（mp4）
covers/  放封面图片（jpg/png）
EOF
fi

sync

echo ""
echo "======================================"
echo "生成 videowall 命令"
echo "======================================"

if [ ! -f "$PROJECT_DIR/videowall.in" ]; then
    echo "未找到 videowall.in"
    exit 1
fi

sed "s|__VIDEOWALL_PROJECT_DIR__|$PROJECT_DIR|g" \
    "$PROJECT_DIR/videowall.in" \
    > /usr/local/bin/videowall

chmod +x /usr/local/bin/videowall

echo " videowall 已安装到 /usr/local/bin"
echo "   绑定项目目录: $PROJECT_DIR"

echo ""
echo "安装完成"
echo ""
