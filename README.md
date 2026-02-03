# videowall
简单的视频墙

拉取项目

    git clone https://github.com/chem4111/videowall.git
    
    cd /videowall

首先挂载U盘或者SD卡，格式化并自动挂载U盘

    ./auto_mount.sh

安装基础服务，创建必要文件夹，可手动输入

    ./install.sh

或者打开config.json 编辑路径

    nano config.json 

安装好后测试videowall 指令，任意目录下输入 videowall

    videowall

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


  
