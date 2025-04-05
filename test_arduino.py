import serial
import time

# 配置串口
port = 'COM3'  # Windows下的串口号
baud_rate = 9600

try:
    # 初始化串口连接
    arduino = serial.Serial(port, baud_rate, timeout=1)
    # 等待Arduino准备好
    time.sleep(2)
    
    print(f"已连接到 {port}")
    
    while True:
        # 获取用户输入
        message = input("请输入要发送的消息 (输入'quit'退出): ")
        
        if message.lower() == 'quit':
            break
            
        # 发送消息给Arduino
        arduino.write(message.encode('utf-8'))
        
        # 等待片刻以接收返回数据
        time.sleep(0.1)
        
        # 读取Arduino的返回消息
        if arduino.in_waiting > 0:
            response = arduino.readline().decode('utf-8', errors='replace').strip()
            print(f"Arduino返回: {response}")
            
except serial.SerialException as e:
    print(f"串口错误: {e}")
finally:
    # 关闭串口连接
    if 'arduino' in locals():
        arduino.close()
        print("串口已关闭")