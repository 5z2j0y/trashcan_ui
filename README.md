# 垃圾分类检测系统

这是一个基于YOLO和tkinter的垃圾分类检测系统，可以实时检测并分类不同种类的垃圾。

## 功能特点

- 实时视频检测与显示
- 左侧垃圾分类宣传视频播放
- 基于YOLO的目标检测
- Arduino通信接口
- 用户友好的图形界面
- 检测结果与通信日志记录

## 安装与使用

1. 安装依赖包

```bash
pip install -r requirements.txt
```

2. 运行应用

```bash
python app.py
```

3. 命令行模式运行检测器

```bash
python detect_pc.py
```

## 项目结构

- `app.py` - 主应用程序（GUI界面）
- `detector.py` - 检测器模块
- `detect_pc.py` - 命令行检测脚本
- `models/trashcan.pt` - YOLO模型文件
- `trash.names` - 垃圾类别名称文件
- `videos/demo.mp4` - 垃圾分类宣传视频

## 系统要求

- Python 3.7+
- OpenCV
- PyTorch
- Ultralytics YOLO
- 一个摄像头(webcam1)
