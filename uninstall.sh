#!/bin/sh
# 视频海报墙卸载脚本（安全卸载）

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "======================================"
echo "开始卸载 视频海报墙"
echo "======================================"

# 1. 删除命令
if [ -f /usr/local/bin/videowall ]; then
    rm -f /usr/local/bin/videowall
    echo "✔ 已移除命令: /usr/local/bin/videowall"
else
    echo "ℹ 未找到 videowall 命令，跳过"
fi

# 2. 是否删除配置文件
if [ -f "$PROJECT_DIR/config.json" ]; then
    printf "是否删除配置文件 config.json？[y/N]: "
    read CONFIRM
    case "$CONFIRM" in
        y|Y)
            rm -f "$PROJECT_DIR/config.json"
            echo "✔ 已删除 config.json"
            ;;
        *)
            echo "ℹ 保留 config.json"
            ;;
    esac
fi

echo ""
echo "======================================"
echo "卸载完成"
echo "--------------------------------------"
echo "说明："
echo "1) 视频目录、封面目录未删除（属于用户数据）"
echo "2) python / ffmpeg 未卸载（避免影响系统）"
echo "3) 如需彻底清理，请手动删除项目目录"
echo "======================================"
echo ""

