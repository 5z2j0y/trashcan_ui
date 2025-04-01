import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import cv2

from detector import TrashDetector
from gui.log_panel import ResultPanel, ArduinoPanel
from gui.video_panel import VideoPanel
from gui.control_panel import ControlPanel

class TrashCanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("垃圾分类检测系统")
        self.root.geometry("1200x700")  # 设置窗口大小
        self.root.resizable(True, True)
        
        # 创建主框架
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建演示视频面板 - 位于顶部
        self.demo_panel = VideoPanel(self.main_frame, title="演示视频")
        self.demo_panel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # 创建实时视频显示面板 - 位于演示视频下方
        self.video_panel = VideoPanel(self.main_frame, title="实时检测")
        self.video_panel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # 创建检测结果面板 - 位于右侧上方
        self.result_panel = ResultPanel(self.main_frame)
        self.result_panel.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        # 创建Arduino通信面板 - 位于右侧下方
        self.arduino_panel = ArduinoPanel(self.main_frame)
        self.arduino_panel.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        # 创建控制按钮面板 - 位于底部
        self.control_panel = ControlPanel(
            self.main_frame,
            on_start=self.start_detection,
            on_stop=self.stop_detection,
            on_clear=self.clear_logs
        )
        self.control_panel.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # 配置网格权重 - 调整为上下布局
        self.main_frame.columnconfigure(0, weight=2)  # 视频区域
        self.main_frame.columnconfigure(1, weight=1)  # 日志区域
        self.main_frame.rowconfigure(0, weight=1)     # 顶部行
        self.main_frame.rowconfigure(1, weight=1)     # 中间行
        
        # 检测器和视频变量
        self.detector = None
        self.is_running = False
        self.detection_thread = None
        self.demo_thread = None
        
        # 加载垃圾类别名称
        self.load_class_names()
        
        # 启动演示视频播放
        self.start_demo_video()
        
    def load_class_names(self):
        self.class_names = []
        try:
            with open("trash.names", "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("//"):
                        self.class_names.append(line)
            self.result_panel.log(f"已加载 {len(self.class_names)} 种垃圾类别")
        except Exception as e:
            self.result_panel.log(f"加载类别名称失败: {e}")
    
    def clear_logs(self):
        """清空日志文本框"""
        self.result_panel.clear()
        self.arduino_panel.clear()
    
    def start_detection(self):
        """开始检测"""
        if self.detection_thread and self.detection_thread.is_alive():
            return
        
        self.is_running = True
        self.detector = TrashDetector(
            on_detection=self.on_detection_callback,
            on_arduino=self.on_arduino_callback,
            camera_id=0  # 使用webcam1进行检测
        )
        
        self.detection_thread = threading.Thread(target=self.detection_loop)
        self.detection_thread.daemon = True
        self.detection_thread.start()
        
        self.result_panel.log("开始检测...")
    
    def stop_detection(self):
        """停止检测"""
        self.is_running = False
        if self.detector:
            self.detector.release()
        
        self.result_panel.log("检测已停止")
    
    def detection_loop(self):
        """检测循环"""
        try:
            self.detector.setup()
            while self.is_running:
                frame = self.detector.process_frame()
                if frame is not None:
                    self.video_panel.update(frame)
                else:
                    break
        except Exception as e:
            self.result_panel.log(f"检测过程出错: {e}")
        finally:
            if self.is_running:
                self.stop_detection()
    
    def start_demo_video(self):
        """开始播放演示视频"""
        self.demo_thread = threading.Thread(target=self.demo_video_loop)
        self.demo_thread.daemon = True
        self.demo_thread.start()
        
    def demo_video_loop(self):
        """演示视频循环播放"""
        video_path = "videos/demo_cropped.mp4"
        
        while True:
            if not os.path.exists(video_path):
                self.result_panel.log(f"演示视频文件不存在: {video_path}")
                time.sleep(5)
                continue
                
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                self.result_panel.log("无法打开演示视频")
                time.sleep(5)
                continue
                
            self._play_video(cap)
    
    def _play_video(self, cap):
        """播放视频的通用方法"""
        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    break
                    
                self.demo_panel.update(frame)
                # 控制播放速度
                time.sleep(0.03)
        except Exception as e:
            self.result_panel.log(f"视频播放出错: {e}")
        finally:
            cap.release()
    
    def on_detection_callback(self, cls_id, score):
        """检测回调函数"""
        if 0 <= cls_id < len(self.class_names):
            class_name = self.class_names[cls_id]
            self.result_panel.log_detection(class_name, score)
        else:
            self.result_panel.log_unknown(cls_id, score)
    
    def on_arduino_callback(self, cls_id):
        """Arduino通信回调函数"""
        if 0 <= cls_id < len(self.class_names):
            class_name = self.class_names[cls_id]
            self.arduino_panel.log_send(class_name, cls_id)
        else:
            self.arduino_panel.log_unknown_send(cls_id)

def main():
    root = tk.Tk()
    app = TrashCanApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
