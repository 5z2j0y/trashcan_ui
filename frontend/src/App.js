import React, { useState } from 'react';
import './App.css';
import VideoStream from './components/VideoStream';
import ControlPanel from './components/ControlPanel';
import { Container, Grid, Box, Typography } from '@mui/material';

function App() {
  const [isDetecting, setIsDetecting] = useState(false);
  const [currentCameraId, setCurrentCameraId] = useState(0);
  const [streamKey, setStreamKey] = useState(Date.now());

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

  return (
    <div className="App">
      <Container maxWidth="lg">
        <Box sx={{ my: 3 }}>
          <Typography variant="h3" component="h1" align="center" gutterBottom>
            垃圾检测系统
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
      
      <footer>
        <p>智能垃圾分类监测系统 © {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;
