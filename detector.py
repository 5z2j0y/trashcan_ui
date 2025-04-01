import cv2
from ultralytics import YOLO

class TrashDetector:
    def __init__(self, on_detection=None, on_arduino=None, camera_id=0):
        self.model_path = "models/trashcan.pt"
        self.video_cap = None
        self.model = None
        self.conf_threshold = 0.8
        self.camera_id = camera_id  # 明确指定摄像头ID
        
        # 回调函数
        self.on_detection = on_detection or (lambda cls_id, score: None)
        self.on_arduino = on_arduino or (lambda cls_id: None)
        
        # 跟踪变量
        self.last_cls_id = None
        self.frame_count = 0
        self.threshold = 5  # 连续帧数阈值
    
    def setup(self):
        """设置模型和视频捕获"""
        # 加载YOLO模型
        self.model = YOLO(self.model_path, verbose=False)
        
        # 打开视频捕捉 - 明确使用摄像头0
        self.video_cap = cv2.VideoCapture(self.camera_id)
        if not self.video_cap.isOpened():
            raise Exception(f"无法打开摄像头 {self.camera_id}")
    
    def send_to_arduino(self, cls_id):
        """发送到Arduino的函数"""
        print(f"Sending to Arduino: {cls_id}")
        if self.on_arduino:
            self.on_arduino(cls_id)
    
    def process_frame(self):
        """处理单个帧并返回处理后的帧"""
        if not self.video_cap or not self.model:
            return None
        
        success, frame = self.video_cap.read()
        if not success:
            return None
        
        # 进行YOLO预测
        results = self.model.predict(frame, conf=self.conf_threshold, verbose=False)
        
        for result in results:
            # 绘制结果
            frame = result.plot()
            # 取出结果的类别、置信度、坐标
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls.item())
                score = box.conf.item()
                
                # 通知检测结果
                if self.on_detection:
                    self.on_detection(cls_id, score)
                
                # 检测相同的cls_id
                if cls_id == self.last_cls_id:
                    self.frame_count += 1
                else:
                    self.last_cls_id = cls_id
                    self.frame_count = 1
                
                # 如果连续帧数超过阈值, 发送到Arduino
                if self.frame_count >= self.threshold:
                    self.send_to_arduino(cls_id)
                    self.frame_count = 0  # 重置计数器
        
        return frame
    
    def release(self):
        """释放资源"""
        if self.video_cap:
            self.video_cap.release()
            self.video_cap = None
