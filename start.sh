#!/bin/bash
# 在Windows上可以创建start.bat文件

# 设置视频目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VIDEOS_DIR="$SCRIPT_DIR/videos"

# 确保videos目录存在
mkdir -p "$VIDEOS_DIR"
echo "视频目录: $VIDEOS_DIR"

# 检查是否存在demo.mp4
if [ ! -f "$VIDEOS_DIR/demo.mp4" ]; then
  echo "警告：$VIDEOS_DIR/demo.mp4 文件不存在，请添加宣传视频文件"
fi

# 检查是否存在models目录和模型文件
if [ ! -f "models/trashcan.pt" ]; then
  echo "错误：models/trashcan.pt 模型文件不存在，请先添加模型文件"
  exit 1
fi

# 启动应用
echo "启动垃圾检测系统..."
npm start
