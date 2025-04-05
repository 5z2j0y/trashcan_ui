from flask import Flask, Response, request, send_from_directory
import cv2
from ultralytics import YOLO
import argparse
import os
from flask_cors import CORS
from flask_socketio import SocketIO
import json
import threading
import serial
import time

app = Flask(__name__, static_folder='frontend/build')
CORS(app)  # 添加CORS支持
# 修改socketio初始化，使用threading模式
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')  # 初始化SocketIO

# 添加静态视频文件目录，使用绝对路径
VIDEOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videos')
app.config['VIDEOS_FOLDER'] = VIDEOS_DIR
print(f"视频文件目录绝对路径: {VIDEOS_DIR}")

# 加载模型
model = YOLO("models/trashcan.pt")

# 全局变量
last_cls_id = None
frame_count = 0
threshold = 5  # 连续帧数阈值

# 在全局变量区域添加Arduino初始化代码
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    print("已连接到 Arduino on COM3")
except Exception as e:
    arduino = None
    print(f"无法初始化Arduino连接: {e}")

def send_message(cls_id, score, label):
    # 通过WebSocket发送检测结果
    detection_data = {
        'cls_id': int(cls_id),
        'score': float(score),
        'label': label
    }
    print(f"发送检测结果: {detection_data}")
    socketio.emit('detection_result', detection_data)
    # 向Arduino发送检测结果
    if arduino is not None:
        try:
            arduino.write(json.dumps(detection_data).encode('utf-8'))
            print("已发送检测结果到Arduino")
        except Exception as e:
            print(f"发送到Arduino错误: {e}")

def generate_frames(camera_id):
    video_cap = None
    try:
        video_cap = cv2.VideoCapture(camera_id)
        if not video_cap.isOpened():
            print(f"无法打开摄像头 {camera_id}")
            return

        global last_cls_id, frame_count

        # 设置摄像头分辨率为640x480
        video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while video_cap.isOpened():
            success, frame = video_cap.read()
            if not success:
                break

            # 确保帧的尺寸是640x480
            frame = cv2.resize(frame, (640, 480))

            # 设置置信度
            conf = 0.8
            try:
                # 进行 YOLO 预测
                results = model.predict(frame, conf=conf, verbose=False)
                
                for result in results:
                    # 绘制检测结果到帧上
                    frame = result.plot()
                    # 取出结果的类别、置信度、标签
                    boxes = result.boxes
                    for box in boxes:
                        cls_id = int(box.cls.item())
                        score = box.conf.item()
                        label = model.names[cls_id]

                        # 检测连续相同的 cls_id
                        if cls_id == last_cls_id:
                            frame_count += 1
                        else:
                            last_cls_id = cls_id
                            frame_count = 1
                        # 如果连续帧数超过阈值，发送消息
                        if frame_count >= threshold:
                            send_message(cls_id, score, label)
                            frame_count = 0  # 重置计数器
            except Exception as e:
                print(f"预测过程中发生错误: {e}")

            # 将帧编码为 JPEG 格式
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # 生成 MJPEG 流
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    except Exception as e:
        print(f"视频流处理过程中发生错误: {e}")
    finally:
        # 确保释放摄像头资源
        if video_cap is not None and video_cap.isOpened():
            video_cap.release()
            print(f"摄像头 {camera_id} 资源已释放")

@app.route('/video_feed')
def video_feed():
    # 从请求参数中获取摄像头 ID，默认为 0
    camera_id = request.args.get('camera', default=0, type=int)
    return Response(generate_frames(camera_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# 修改视频文件访问路由以支持跨源请求和正确的MIME类型
@app.route('/videos/<path:filename>')
def serve_video(filename):
    response = send_from_directory(app.config['VIDEOS_FOLDER'], filename)
    response.headers['Content-Type'] = 'video/mp4'
    response.headers['Accept-Ranges'] = 'bytes'
    print(f"提供视频文件: {os.path.join(app.config['VIDEOS_FOLDER'], filename)}")
    return response

# 添加前端静态文件服务
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# 添加WebSocket事件处理
@socketio.on('connect')
def handle_connect():
    print('客户端已连接')

@socketio.on('disconnect')
def handle_disconnect():
    print('客户端已断开连接')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='垃圾检测 Flask 后端')
    parser.add_argument('--port', type=int, default=5000, help='Flask 端口 (默认: 5000)')
    args = parser.parse_args()
    
    # 使用threading模式运行
    print("使用threading模式启动服务器...")
    socketio.run(app, host='0.0.0.0', port=args.port, debug=True, allow_unsafe_werkzeug=True)