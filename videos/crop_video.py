import cv2
import os
import argparse
import numpy as np
from tqdm import tqdm

def crop_video_to_4_3(input_path, output_path=None):
    """
    将视频裁切为4:3比例，保持高度不变，居中裁切。
    
    参数:
        input_path (str): 输入视频的路径
        output_path (str, optional): 输出视频的路径。如果为None，将在输入视频名后添加"_cropped"
    
    返回:
        str: 输出视频的路径
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"找不到输入视频: {input_path}")
    
    # 如果没有指定输出路径，则自动生成
    if output_path is None:
        filename, ext = os.path.splitext(input_path)
        output_path = f"{filename}_cropped{ext}"
    
    # 打开视频
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise Exception(f"无法打开视频: {input_path}")
    
    # 获取视频基本信息
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 计算4:3比例下的新宽度（保持高度不变）
    new_width = int(height * 4 / 3)
    
    # 计算裁切区域（居中）
    if new_width > width:
        print(f"警告: 视频宽度 ({width}px) 小于所需的4:3宽度 ({new_width}px)。将保持原始宽度。")
        new_width = width
        x_start = 0
    else:
        x_start = (width - new_width) // 2
    
    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # 可以根据需要更改编码格式
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, height))
    
    # 处理每一帧
    print(f"开始裁切视频: {input_path}")
    print(f"从 {width}x{height} 裁切到 {new_width}x{height} (4:3 比例)")
    
    try:
        for _ in tqdm(range(frame_count)):
            ret, frame = cap.read()
            if not ret:
                break
            
            # 裁切帧
            cropped_frame = frame[:, x_start:x_start + new_width]
            
            # 写入新视频
            out.write(cropped_frame)
    
    finally:
        # 释放资源
        cap.release()
        out.release()
    
    print(f"视频裁切完成，已保存至: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='将视频裁切为4:3比例，保持高度不变，居中裁切')
    parser.add_argument('input', help='输入视频的路径')
    parser.add_argument('-o', '--output', help='输出视频的路径（可选）')
    
    args = parser.parse_args()
    
    try:
        crop_video_to_4_3(args.input, args.output)
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()
