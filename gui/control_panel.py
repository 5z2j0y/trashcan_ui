import tkinter as tk
from tkinter import ttk

class ControlPanel(ttk.Frame):
    """控制按钮面板"""
    def __init__(self, parent, on_start=None, on_stop=None, on_clear=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        # 回调函数
        self.on_start = on_start or (lambda: None)
        self.on_stop = on_stop or (lambda: None)
        self.on_clear = on_clear or (lambda: None)
        
        # 创建按钮
        self.start_button = ttk.Button(self, text="开始检测", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_button = ttk.Button(self, text="停止检测", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.clear_button = ttk.Button(self, text="清空日志", command=self.clear)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def start(self):
        """开始按钮点击"""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.on_start()
    
    def stop(self):
        """停止按钮点击"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.on_stop()
    
    def clear(self):
        """清空按钮点击"""
        self.on_clear()
