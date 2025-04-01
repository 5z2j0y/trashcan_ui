import cv2
import os

def crop_video(input_path):
    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")
    
    # 获取文件名和扩展名
    base_name, ext = os.path.splitext(os.path.basename(input_path))
    output_path = os.path.join(os.path.dirname(input_path), f"{base_name}_cropped{ext}")
    
    # 打开视频文件
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {input_path}")
    
    # 获取视频属性
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 计算裁切区域，保持高度不变，宽度调整为满足 3:2 比例
    target_width = int(frame_height * 3 / 2)
    if target_width > frame_width:
        raise ValueError("Video width is too small to achieve a 3:2 aspect ratio.")
    x = (frame_width - target_width) // 2
    
    # 初始化视频写入器
    out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, frame_height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # 裁切帧
        cropped_frame = frame[:, x:x+target_width]
        out.write(cropped_frame)
    
    # 释放资源
    cap.release()
    out.release()
    print(f"Cropped video saved to: {output_path}")

# 示例调用
crop_video("videos\demo.mp4")
