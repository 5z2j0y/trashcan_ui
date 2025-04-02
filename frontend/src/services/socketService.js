import { io } from 'socket.io-client';

let socket = null;

// 获取WebSocket服务器URL
const getSocketUrl = () => {
  const protocal = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = process.env.REACT_APP_API_URL || window.location.host;
  
  // 开发环境使用localhost:5000
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:5000';
  }
  
  return `${protocal}//${host}`;
};

// 初始化WebSocket连接
export const initSocket = (onDetectionResult, onConnect, onDisconnect) => {
  // 如果已存在连接，先关闭
  if (socket) {
    socket.disconnect();
  }

  // 创建新连接
  socket = io(getSocketUrl(), {
    transports: ['websocket', 'polling']
  });

  // 设置事件处理函数
  socket.on('connect', () => {
    console.log('WebSocket连接已建立');
    if (onConnect) onConnect();
  });

  socket.on('disconnect', () => {
    console.log('WebSocket连接已断开');
    if (onDisconnect) onDisconnect();
  });

  socket.on('detection_result', (data) => {
    console.log('收到检测结果:', data);
    if (onDetectionResult) onDetectionResult(data);
  });

  return socket;
};

// 关闭WebSocket连接
export const closeSocket = () => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
};
