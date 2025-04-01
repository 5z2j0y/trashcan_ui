import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class VideoPanel(ttk.LabelFrame):
    """视频显示面板"""
    def __init__(self, parent, title="视频显示", **kwargs):
        super().__init__(parent, text=title, **kwargs)
        
        # 创建标签用于显示视频
        self.video_label = ttk.Label(self)
        self.video_label.pack(padx=5, pady=5)
        
        # 设置默认尺寸
        self.max_width = 640
        self.max_height = 480
    
    def update(self, frame):
        """更新视频帧"""
        if frame is None:
            return
            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        
        # 调整图像大小以适应界面
        scale = min(self.max_width/width, self.max_height/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        frame = cv2.resize(frame, (new_width, new_height))
        
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
    
    def set_max_size(self, width, height):
        """设置最大尺寸"""
        self.max_width = width
        self.max_height = height
