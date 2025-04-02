import React, { useEffect, useRef } from 'react';
import { Paper, Box, Grid, Typography } from '@mui/material';

function VideoStream({ isDetecting, cameraId, streamKey }) {
  const videoFeedUrl = isDetecting 
    ? `${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/video_feed?camera=${cameraId}&key=${streamKey}`
    : null;
    
  // 使用videos端点获取视频文件，确保使用绝对路径
  const promoVideoUrl = `${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/videos/demo.mp4`;
  
  // 添加对视频元素的引用
  const mainVideoRef = useRef(null);
  const secondaryVideoRef = useRef(null);

  // 使用useEffect钩子来确保视频加载并播放
  useEffect(() => {
    // 对主视频元素进行处理
    if (!isDetecting && mainVideoRef.current) {
      mainVideoRef.current.load();
    }
    
    // 对次要视频元素进行处理(检测时显示的宣传视频)
    if (isDetecting && secondaryVideoRef.current) {
      secondaryVideoRef.current.load();
    }
  }, [isDetecting, promoVideoUrl]);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={isDetecting ? 6 : 12}>
        <Paper elevation={3}>
          <Box p={2}>
            <Typography variant="h6" gutterBottom>
              {isDetecting ? '垃圾检测' : '宣传视频'}
            </Typography>
            <Box 
              sx={{ 
                display: 'flex', 
                justifyContent: 'center', 
                overflow: 'hidden',
                height: '480px'
              }}
            >
              {isDetecting ? (
                <img 
                  src={videoFeedUrl} 
                  alt="视频流"
                  style={{ 
                    maxWidth: '100%', 
                    maxHeight: '100%', 
                    objectFit: 'contain' 
                  }}
                />
              ) : (
                <video
                  ref={mainVideoRef}
                  src={promoVideoUrl}
                  autoPlay
                  muted
                  loop
                  controls
                  playsInline
                  preload="auto"
                  style={{ 
                    maxWidth: '100%', 
                    maxHeight: '100%', 
                    objectFit: 'contain' 
                  }}
                />
              )}
            </Box>
          </Box>
        </Paper>
      </Grid>
      
      {isDetecting && (
        <Grid item xs={12} md={6}>
          <Paper elevation={3}>
            <Box p={2}>
              <Typography variant="h6" gutterBottom>
                宣传视频
              </Typography>
              <Box 
                sx={{ 
                  display: 'flex', 
                  justifyContent: 'center', 
                  overflow: 'hidden',
                  height: '480px'
                }}
              >
                <video
                  ref={secondaryVideoRef}
                  src={promoVideoUrl}
                  autoPlay
                  muted
                  loop
                  controls
                  playsInline
                  preload="auto"
                  style={{ 
                    maxWidth: '100%', 
                    maxHeight: '100%', 
                    objectFit: 'contain' 
                  }}
                />
              </Box>
            </Box>
          </Paper>
        </Grid>
      )}
    </Grid>
  );
}

export default VideoStream;