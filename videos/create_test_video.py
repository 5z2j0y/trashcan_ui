import cv2
import numpy as np
import os

def create_test_video(output_path, duration=10, fps=30, width=640, height=480):
    """
    创建一个简单的测试视频
    
    参数:
        output_path: 输出视频的路径
        duration: 视频时长(秒)
        fps: 每秒帧数
        width: 视频宽度
        height: 视频高度
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # MP4格式
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # 生成帧
    total_frames = duration * fps
    for i in range(total_frames):
        # 创建渐变彩色背景
        t = i / total_frames
        r = int(255 * (0.5 + 0.5 * np.sin(t * 2 * np.pi)))
        g = int(255 * (0.5 + 0.5 * np.sin(t * 2 * np.pi + 2 * np.pi / 3)))
        b = int(255 * (0.5 + 0.5 * np.sin(t * 2 * np.pi + 4 * np.pi / 3)))
        
        # 创建彩色帧
        frame = np.ones((height, width, 3), dtype=np.uint8)
        frame[:] = (b, g, r)
        
        # 添加文本
        cv2.putText(frame, 
                    'Trash Sort Promotion Video Test', 
                    (width // 4, height // 2 - 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1, 
                    (255, 255, 255), 
                    2, 
                    cv2.LINE_AA)
        
        cv2.putText(frame, 
                    f'Test Frame {i+1}/{total_frames}', 
                    (width // 4, height // 2 + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, 
                    (255, 255, 255), 
                    2, 
                    cv2.LINE_AA)
        
        # 写入帧
        out.write(frame)
    
    # 释放资源
    out.release()
    print(f"测试视频已创建: {output_path}")

if __name__ == "__main__":
    # 视频输出路径
    video_path = os.path.join('videos', 'demo.mp4')
    
    # 输出绝对路径以便确认
    abs_path = os.path.abspath(video_path)
    print(f"将创建测试视频: {abs_path}")
    
    # 创建测试视频
    create_test_video(video_path)