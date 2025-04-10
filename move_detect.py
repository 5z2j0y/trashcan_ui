import cv2
import numpy as np
import time

def nothing(x):
    pass

def main():
    # 打开摄像头
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    # 设置分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # 创建窗口和调参滑块
    cv2.namedWindow('Motion Detection')
    cv2.createTrackbar('Threshold', 'Motion Detection', 30, 100, nothing)
    cv2.createTrackbar('Area Ratio (%)', 'Motion Detection', 2, 10, nothing)
    cv2.createTrackbar('Dilation', 'Motion Detection', 2, 10, nothing)
    
    # 初始化变量
    prev_frame = None
    motion_detected = False
    motion_start_time = 0
    
    while True:
        # 读取帧
        ret, frame = cap.read()
        if not ret:
            break
        
        # 调整大小确保尺寸一致
        frame = cv2.resize(frame, (640, 480))
        
        # 获取当前参数值
        motion_threshold = cv2.getTrackbarPos('Threshold', 'Motion Detection')
        motion_area_ratio = cv2.getTrackbarPos('Area Ratio (%)', 'Motion Detection') / 100.0
        dilation_iterations = cv2.getTrackbarPos('Dilation', 'Motion Detection')
        
        # 制作一个显示用的帧
        display_frame = frame.copy()
        
        # 第一帧无法比较，直接设置为第一帧
        if prev_frame is None:
            prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            prev_frame = cv2.GaussianBlur(prev_frame, (21, 21), 0)
            continue
        
        # 将当前帧转为灰度并模糊化
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        # 计算当前帧与上一帧的差异
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, motion_threshold, 255, cv2.THRESH_BINARY)[1]
        
        # 扩大白色区域以填补空隙
        thresh = cv2.dilate(thresh, None, iterations=dilation_iterations)
        
        # 找到轮廓
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 计算移动像素占比
        total_pixels = thresh.shape[0] * thresh.shape[1]
        white_pixels = cv2.countNonZero(thresh)
        movement_ratio = white_pixels / total_pixels
        
        # 在显示帧上绘制轮廓
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # 过滤小轮廓
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 更新上一帧
        prev_frame = gray
        
        # 如果移动区域比例超过阈值，则认为检测到运动
        if movement_ratio > motion_area_ratio:
            if not motion_detected:
                motion_detected = True
                motion_start_time = time.time()
                print(f"检测到运动! 移动区域占比: {movement_ratio:.4f}")
            
            # 显示运动状态
            cv2.putText(display_frame, "Motion Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            elapsed = time.time() - motion_start_time
            cv2.putText(display_frame, f"Duration: {elapsed:.1f}s", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            motion_detected = False
            
        # 在帧上显示参数和移动比例
        cv2.putText(display_frame, f"Threshold: {motion_threshold}", (10, 430), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(display_frame, f"Area Ratio: {motion_area_ratio:.2f}", (10, 450), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(display_frame, f"Movement: {movement_ratio:.4f}", (10, 470), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # 创建可视化显示
        # 将thresh转换为彩色以便叠加显示
        thresh_color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        delta_color = cv2.cvtColor(frame_delta, cv2.COLOR_GRAY2BGR)
        
        # 水平拼接原始帧和阈值帧
        top_row = np.hstack((display_frame, thresh_color))
        
        # 显示结果
        cv2.imshow('Motion Detection', top_row)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()