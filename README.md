# videowall
简单的视频墙


cd /videowall
./auto_mount.sh
格式化并自动挂载U盘

安装基础服务
./install.sh

创建视频文件夹
config.json 可以手动配置或者install配置

安装好后测试videowall 指令
root@armbian:~/videowall# videowall
视频墙管理工具

用法: videowall <命令>

命令:
  start    启动视频墙应用（前台运行）
  init     初始化视频封面（为所有视频生成封面图）
  enable   创建并启用 systemd 服务（开机自启）
  disable  禁用并删除 systemd 服务
  status   查看视频墙服务状态
  help     显示此帮助信息

示例:
  videowall start
  videowall init
  sudo videowall enable
  videowall status


  
