import tkinter as tk
from tkinter import ttk, scrolledtext
import time

class LogPanel(ttk.LabelFrame):
    """通用日志面板基类"""
    def __init__(self, parent, title="日志", **kwargs):
        super().__init__(parent, text=title, **kwargs)
        
        # 创建文本区域
        self.text = scrolledtext.ScrolledText(self, width=30, height=15)
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def log(self, message):
        """记录消息到日志"""
        current_time = time.strftime("%H:%M:%S", time.localtime())
        self.text.insert(tk.END, f"[{current_time}] {message}\n")
        self.text.see(tk.END)
    
    def clear(self):
        """清空日志"""
        self.text.delete(1.0, tk.END)


class ResultPanel(LogPanel):
    """检测结果面板"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="检测结果", **kwargs)
    
    def log_detection(self, class_name, score):
        """记录检测结果"""
        self.log(f"检测到: {class_name} (置信度: {score:.2f})")
    
    def log_unknown(self, cls_id, score):
        """记录未知类别"""
        self.log(f"检测到未知类别 ID: {cls_id} (置信度: {score:.2f})")


class ArduinoPanel(LogPanel):
    """Arduino通信面板"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Arduino通信", **kwargs)
    
    def log_send(self, class_name, cls_id):
        """记录发送到Arduino的消息"""
        self.log(f"发送到Arduino: {class_name} (ID: {cls_id})")
    
    def log_unknown_send(self, cls_id):
        """记录发送到Arduino的未知类别"""
        self.log(f"发送到Arduino: 未知类别 (ID: {cls_id})")
