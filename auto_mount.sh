#!/bin/sh

set -e

MOUNT_POINT="/mnt/usb"
FS_TYPE="ext4"
LABEL="USBSTORE"

echo "=== 自动格式化并挂载 U 盘脚本 ==="

# 必须 root
if [ "$(id -u)" != "0" ]; then
    echo "请使用 root 运行"
    exit 1
fi

# 找可移动磁盘（排除系统盘）
DEV=$(lsblk -dpno NAME,RM | awk '$2==1 {print $1}' | head -n 1)

if [ -z "$DEV" ]; then
    echo "未检测到 U 盘"
    exit 1
fi

echo "检测到设备: $DEV"

# 卸载已有分区
umount ${DEV}?* 2>/dev/null || true

echo "清空分区表..."
wipefs -a "$DEV"

echo "创建新分区..."
parted -s "$DEV" mklabel gpt
parted -s "$DEV" mkpart primary 0% 100%

PART="${DEV}1"

sleep 2

echo "格式化为 $FS_TYPE..."
mkfs.$FS_TYPE -F -L "$LABEL" "$PART"

mkdir -p "$MOUNT_POINT"

UUID=$(blkid -s UUID -o value "$PART")

if [ -z "$UUID" ]; then
    echo "获取 UUID 失败"
    exit 1
fi

# 移除旧的挂载项
sed -i "\|$MOUNT_POINT|d" /etc/fstab

echo "写入 /etc/fstab..."
echo "UUID=$UUID $MOUNT_POINT $FS_TYPE defaults,nofail 0 2" >> /etc/fstab

echo "立即挂载..."
mount -a

echo "完成："
df -h | grep "$MOUNT_POINT"
