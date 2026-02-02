#!/bin/bash
# 视频海报墙环境安装与配置脚本
# 需使用sudo权限运行

# 第一步：安装必要依赖包
echo "======================================"
echo "开始安装所需依赖（python3、flask、ffmpeg）..."
echo "======================================"
apt update -y
apt install -y python3 python3-flask ffmpeg

# 检查安装是否成功
if [ $? -eq 0 ]; then
    echo "✅ 依赖包安装完成！"
else
    echo "❌ 依赖包安装失败，请检查网络或软件源配置后重试。"
    exit 1
fi

# 第二步：交互式输入路径并创建目录
echo ""
echo "======================================"
echo "配置视频和封面目录..."
echo "======================================"

read -p "请输入视频目录路径 [默认: /mnt/usb/videos]: " VIDEO_DIR_INPUT
VIDEO_DIR="${VIDEO_DIR_INPUT:-/mnt/usb/videos}"

read -p "请输入封面目录路径 [默认: /mnt/usb/covers]: " COVER_DIR_INPUT
COVER_DIR="${COVER_DIR_INPUT:-/mnt/usb/covers}"

echo ""
echo "创建目录..."
mkdir -p "$VIDEO_DIR"
mkdir -p "$COVER_DIR"

echo "✅ 视频目录: $VIDEO_DIR"
echo "✅ 封面目录: $COVER_DIR"

# 更新 JSON 配置文件
cat > ./config.json <<EOF
{
    "VIDEO_DIR": "$VIDEO_DIR",
    "COVER_DIR": "$COVER_DIR"
}
EOF
echo "✅ 配置文件 config.json 已更新"

# 生成说明文档（仅当README.txt不存在时创建）
if [ ! -f "$VIDEO_DIR/../README.txt" ]; then
    cat <<EOF > "$VIDEO_DIR/../README.txt"
这是视频海报墙的内容目录
videos/  放视频文件（mp4）
covers/  放封面图片（jpg/png）
EOF
    echo "✅ 说明文档已创建"
fi

# 同步数据到磁盘
sync
echo "✅ 目录结构初始化完成！"

# 第三步：安装 videowall 命令
echo ""
echo "======================================"
echo "安装 videowall 命令..."
echo "======================================"

cp videowall /usr/local/bin/
chmod +x /usr/local/bin/videowall
echo "✅ videowall 命令已安装到 /usr/local/bin/"

echo ""
echo "🎉 所有操作执行完毕，脚本运行结束。"
echo ""
echo "使用方法:"
echo "  videowall start    # 启动应用"
echo "  videowall enable   # 设置开机自启"
echo "  videowall status   # 查看状态"