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
import numpy as np

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
last_send_time = 0  # 上次发送信号的时间
cooldown_period = 7  # 冷却时间，单位为秒

# 添加运动检测相关变量
prev_frame = None
motion_threshold = 30  # 运动检测阈值
motion_area_ratio = 0.02  # 移动区域占比阈值
motion_detected = False
motion_start_time = 0
detection_conf = 0.8  # 初始置信度
detection_state = "NORMAL"  # 状态: NORMAL, REDUCED_CONF, TIMEOUT

# 在全局变量区域添加Arduino初始化代码
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    time.sleep(2)
    print("已连接到 Arduino on COM3")
except Exception as e:
    arduino = None
    print(f"无法初始化Arduino连接: {e}")

def send_message(cls_id, score, label):
    global last_send_time
    
    # 检查是否在冷却期内
    current_time = time.time()
    if current_time - last_send_time < cooldown_period:
        # 在冷却期内，不发送消息
        print(f"在冷却期内 ({cooldown_period}秒), 跳过发送")
        return
    
    # 更新最后发送时间
    last_send_time = current_time
    
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
            arduino.write(json.dumps({"cls_id": cls_id}).encode('utf-8'))
            print("已发送检测结果到Arduino")
        except Exception as e:
            print(f"发送到Arduino错误: {e}")
    
    # 重置运动检测和状态
    global motion_detected, detection_state
    motion_detected = False
    detection_state = "NORMAL"
    
def detect_motion(frame):
    """帧差法检测运动"""
    global prev_frame, motion_detected, motion_start_time
    
    # 第一帧无法比较，直接设置为第一帧
    if prev_frame is None:
        prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        prev_frame = cv2.GaussianBlur(prev_frame, (21, 21), 0)
        return False
    
    # 将当前帧转为灰度并模糊化
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # 计算当前帧与上一帧的差异
    frame_delta = cv2.absdiff(prev_frame, gray)
    thresh = cv2.threshold(frame_delta, motion_threshold, 255, cv2.THRESH_BINARY)[1]
    
    # 扩大白色区域以填补空隙
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    # 找到轮廓
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 计算移动像素占比
    total_pixels = thresh.shape[0] * thresh.shape[1]
    white_pixels = cv2.countNonZero(thresh)
    movement_ratio = white_pixels / total_pixels
    
    # 更新上一帧
    prev_frame = gray
    
    # 如果移动区域比例超过阈值，则认为检测到运动
    if movement_ratio > motion_area_ratio:
        if not motion_detected:
            motion_detected = True
            motion_start_time = time.time()
            print(f"检测到运动! 移动区域占比: {movement_ratio:.4f}")
        return True
    
    return False

def generate_frames(camera_id):
    video_cap = None
    try:
        video_cap = cv2.VideoCapture(camera_id)
        if not video_cap.isOpened():
            print(f"无法打开摄像头 {camera_id}")
            return

        global last_cls_id, frame_count, motion_detected, motion_start_time, detection_state, detection_conf

        # 设置摄像头分辨率为640x480
        video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while video_cap.isOpened():
            success, frame = video_cap.read()
            if not success:
                break

            # 确保帧的尺寸是640x480
            frame = cv2.resize(frame, (640, 480))
            
            # 运动检测（仅在正常状态下检测）
            if not motion_detected:
                motion_detected = detect_motion(frame)
            
            # 如果检测到运动，根据时间动态调整置信度和状态
            if motion_detected:
                current_time = time.time()
                elapsed_time = current_time - motion_start_time
                
                # 状态转换逻辑
                if detection_state == "NORMAL" and elapsed_time >= 7:
                    detection_state = "REDUCED_CONF"
                    detection_conf = 0.5
                    print(f"已经过7秒未识别，降低置信度到: {detection_conf}")
                elif detection_state == "REDUCED_CONF" and elapsed_time >= 14:
                    detection_state = "TIMEOUT"
                    print("已经过14秒未识别，将使用默认分类")
            
            # 根据当前状态进行检测
            try:
                if detection_state == "TIMEOUT":
                    # 超时状态：使用默认分类（随机或固定）
                    default_cls_id = 0  # 设置默认分类ID
                    default_label = model.names[default_cls_id]
                    send_message(default_cls_id, 0.5, default_label)
                    # 重置状态
                    detection_conf = 0.8
                    detection_state = "NORMAL"
                    motion_detected = False
                else:
                    # 使用当前置信度进行检测
                    results = model.predict(frame, conf=detection_conf, verbose=False)
                    
                    # 处理检测结果
                    detection_found = False
                    for result in results:
                        # 绘制检测结果到帧上
                        frame = result.plot()
                        # 取出结果的类别、置信度、标签
                        boxes = result.boxes
                        for box in boxes:
                            cls_id = int(box.cls.item())
                            score = box.conf.item()
                            label = model.names[cls_id]
                            detection_found = True

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
                                # 重置运动检测状态
                                motion_detected = False
                                detection_conf = 0.8  # 恢复原始置信度
                                detection_state = "NORMAL"
                    
                    # 在帧上显示当前状态
                    status_text = f"状态: {detection_state} | 置信度: {detection_conf}"
                    if motion_detected:
                        elapsed = time.time() - motion_start_time
                        status_text += f" | 已检测 {elapsed:.1f}秒"
                    cv2.putText(frame, status_text, (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
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