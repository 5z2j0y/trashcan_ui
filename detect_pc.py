import cv2
from ultralytics import YOLO
import argparse
import serial
import time

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='垃圾检测程序')
    parser.add_argument('--headless', action='store_true', help='以无界面模式运行')
    parser.add_argument('--camera', type=int, default=0, help='摄像头ID (默认: 0)')
    args = parser.parse_args()
    
    # 加载模型
    model = YOLO("models/trashcan.pt") 

    # 初始化Arduino串口连接
    try:
        arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        time.sleep(2)
        print("已连接到 Arduino")
    except Exception as e:
        print(f"Arduino连接错误: {e}")
        arduino = None

    def send_message(cls_id, score, label):
        # 发送检测结果到Arduino
        message = f"{cls_id},{score:.2f},{label}"
        print("发送消息:", message)
        if arduino:
            arduino.write(message.encode('utf-8'))

    # 打开视频捕捉，默认使用摄像头1
    video_cap = cv2.VideoCapture(args.camera)
    if not video_cap.isOpened():
        print(f"无法打开摄像头 {args.camera}")
        return

    # 初始化变量
    last_cls_id = None
    frame_count = 0
    threshold = 5  # 连续帧数阈值

    while video_cap.isOpened():
        success, frame = video_cap.read()
        if not success:
            break

        # 设置置信度
        conf = 0.8
        # 进行YOLO预测
        results = model.predict(frame, conf=conf, verbose=False)
        
        for result in results:
            # 绘制结果
            frame = result.plot()
            # 取出结果的类别、置信度、坐标
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls.item())
                score = box.conf.item()
                label = model.names[cls_id]

                # 检测相同的cls_id
                if cls_id == last_cls_id:
                    frame_count += 1
                else:
                    last_cls_id = cls_id
                    frame_count = 1
                # 如果连续帧数超过阈值, 发送消息
                if frame_count >= threshold:
                    send_message(cls_id, score, label)
                    frame_count = 0  # 重置计数器

        # 如果不是无界面模式，显示图像
        if not args.headless:
            cv2.imshow('Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # 释放资源
    video_cap.release()
    cv2.destroyAllWindows()
    if arduino:
        arduino.close()
        print("Arduino连接已关闭")

if __name__ == "__main__":
    main()