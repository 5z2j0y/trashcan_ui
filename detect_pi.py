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

    # 定义垃圾分类映射
    # 1: 可回收垃圾, 2: 有害垃圾, 3: 厨余垃圾, 4: 其他垃圾
    trash_category_map = {
        'bottle': 1,    # 可回收垃圾
        'brick': 4,     # 其他垃圾
        'battery': 2,   # 有害垃圾
        'can': 1,       # 可回收垃圾
        'carrot': 3,    # 厨余垃圾
        'china': 4,     # 其他垃圾
        'paperCup': 4,  # 其他垃圾
        'pill': 2,      # 有害垃圾
        'potato': 3,    # 厨余垃圾
        'radish': 3,    # 厨余垃圾
        'stone': 4,     # 其他垃圾
        'potato_chip': 4, # 其他垃圾
    }
    
    # 垃圾分类的中文名称
    category_names = {
        1: "可回收垃圾",
        2: "有害垃圾",
        3: "厨余垃圾",
        4: "其他垃圾"
    }

    # 初始化Arduino串口连接
    try:
        arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        time.sleep(2)
        print("已连接到 Arduino")
    except Exception as e:
        print(f"Arduino连接错误: {e}")
        arduino = None

    def send_message(label, score):
        # 根据垃圾标签获取分类编号
        category_id = trash_category_map.get(label, 4)  # 默认为其他垃圾
        category_name = category_names[category_id]
        
        # 发送分类编号到Arduino
        message = f"{category_id}"
        print(f"检测到: {label} (置信度: {score:.2f}) - 分类为: {category_name} (编号: {category_id})")
        if arduino:
            arduino.write(message.encode('utf-8'))
            time.sleep(7)  # 等待Arduino处理数据

    # 打开视频捕捉，默认使用摄像头1
    video_cap = cv2.VideoCapture(args.camera)
    if not video_cap.isOpened():
        print(f"无法打开摄像头 {args.camera}")
        return

    # 初始化变量
    last_label = None
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

                # 检测相同的标签
                if label == last_label:
                    frame_count += 1
                else:
                    last_label = label
                    frame_count = 1
                # 如果连续帧数超过阈值, 发送消息
                if frame_count >= threshold:
                    send_message(label, score)
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