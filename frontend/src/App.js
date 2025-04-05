import React, { useState, useEffect } from 'react';
import './App.css';
import VideoStream from './components/VideoStream';
import ControlPanel from './components/ControlPanel';
import DetectionResults from './components/DetectionResults';
import { Container, Grid, Box, Typography, Snackbar, Alert } from '@mui/material';
import { initSocket, closeSocket } from './services/socketService';

function App() {
  const [isDetecting, setIsDetecting] = useState(false);
  const [currentCameraId, setCurrentCameraId] = useState(0);
  const [streamKey, setStreamKey] = useState(Date.now());
  const [detectionResults, setDetectionResults] = useState([]);
  const [socketConnected, setSocketConnected] = useState(false);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'info' });

  // 初始化WebSocket连接
  useEffect(() => {
    const handleDetectionResult = (data) => {
      // 添加时间戳
      const resultWithTimestamp = {
        ...data,
        timestamp: Date.now()
      };
      
      // 添加到结果列表（最新的在前面）
      setDetectionResults(prevResults => [resultWithTimestamp, ...prevResults]);
      
      // 显示通知
      showNotification(`检测到 ${data.label}`, 'success');
    };

    const handleConnect = () => {
      setSocketConnected(true);
      showNotification('已连接到检测服务', 'success');
    };

    const handleDisconnect = () => {
      setSocketConnected(false);
      showNotification('与检测服务的连接已断开', 'warning');
    };

    // 初始化WebSocket
    initSocket(handleDetectionResult, handleConnect, handleDisconnect);

    // 组件卸载时关闭连接
    return () => {
      closeSocket();
    };
  }, []);

  const handleStartDetection = () => {
    setStreamKey(Date.now()); // 更新流密钥以刷新视频
    setIsDetecting(true);
  };

  const handleStopDetection = () => {
    setIsDetecting(false);
  };

  const handleCameraChange = (cameraId) => {
    setCurrentCameraId(cameraId);
  };

  const handleClearResults = () => {
    setDetectionResults([]);
  };

  // 显示通知
  const showNotification = (message, severity = 'info') => {
    setNotification({
      open: true,
      message,
      severity
    });
  };

  // 关闭通知
  const handleCloseNotification = () => {
    setNotification(prev => ({ ...prev, open: false }));
  };

  return (
    <div className="App">
      <Container maxWidth="lg">
        <Box sx={{ my: 3 }}>
          <Typography 
            variant="h3" 
            component="h1" 
            align="center" 
            gutterBottom
            sx={{ 
              letterSpacing: '1px',
              color: '#333333', // 灰黑色标题
              fontWeight: 'bold'
            }}
          >
            智能垃圾检测系统
          </Typography>
        </Box>
        
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <ControlPanel 
              isDetecting={isDetecting}
              onStartDetection={handleStartDetection}
              onStopDetection={handleStopDetection}
              onCameraChange={handleCameraChange}
              currentCameraId={currentCameraId}
              socketConnected={socketConnected}
            />
          </Grid>
          
          <Grid item xs={12}>
            <DetectionResults 
              results={detectionResults} 
              onClearResults={handleClearResults}
            />
          </Grid>
          
          <Grid item xs={12}>
            <VideoStream 
              isDetecting={isDetecting}
              cameraId={currentCameraId}
              streamKey={streamKey}
            />
          </Grid>
        </Grid>
      </Container>
      
      <Snackbar 
        open={notification.open} 
        autoHideDuration={5000} 
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
      >
        <Alert 
          onClose={handleCloseNotification} 
          severity={notification.severity} 
          sx={{ 
            width: '100%',
            boxShadow: '0 4px 12px rgba(163, 216, 244, 0.15)',
            color: 'var(--text-primary)',
            backgroundColor: notification.severity === 'success' ? 'rgba(181, 230, 181, 0.9)' : 
                          notification.severity === 'warning' ? 'rgba(255, 227, 179, 0.9)' : 
                          notification.severity === 'error' ? 'rgba(255, 182, 182, 0.9)' : 'rgba(163, 216, 244, 0.9)',
            '& .MuiAlert-icon': {
              color: 'var(--text-primary)'
            } 
          }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
      
      <footer style={{ backgroundColor: 'var(--hover-color)', borderTop: '1px solid var(--border-color)' }}>
        <p style={{ color: 'var(--text-secondary)' }}>智能垃圾分类监测系统 © {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;
