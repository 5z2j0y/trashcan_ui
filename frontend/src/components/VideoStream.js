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
    <Grid container spacing={3} direction="column">
      {/* 宣传视频始终在上方 */}
      <Grid item xs={12}>
        <Paper elevation={3} sx={{ 
          borderRadius: '16px', 
          overflow: 'hidden',
          transition: 'transform 0.3s ease, box-shadow 0.3s ease',
          '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 8px 20px rgba(163, 216, 244, 0.25)'
          }
        }}>
          <Box p={2} sx={{ 
            background: 'linear-gradient(to right, #a3d8f4, #b5e6b5)',
            color: 'white'
          }}>
            <Typography variant="h6" gutterBottom sx={{ 
              fontWeight: 'bold',
              color: '#555b6e',
              textShadow: '1px 1px 2px rgba(255, 255, 255, 0.5)'
            }}>
              宣传视频
            </Typography>
          </Box>
          <Box 
            sx={{ 
              display: 'flex', 
              justifyContent: 'center', 
              overflow: 'hidden',
              height: '480px',
              backgroundColor: '#f5f8fa',
              padding: '10px'
            }}
          >
            <video
              ref={isDetecting ? secondaryVideoRef : mainVideoRef}
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
                objectFit: 'contain',
                borderRadius: '12px',
                boxShadow: '0 4px 8px rgba(163, 216, 244, 0.15)'
              }}
            />
          </Box>
        </Paper>
      </Grid>
      
      {/* 垃圾检测视频在下方，仅当检测开始时显示 */}
      {isDetecting && (
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ 
            borderRadius: '16px', 
            overflow: 'hidden',
            transition: 'transform 0.3s ease, box-shadow 0.3s ease',
            '&:hover': {
              transform: 'translateY(-5px)',
              boxShadow: '0 8px 20px rgba(247, 197, 197, 0.25)'
            }
          }}>
            <Box p={2} sx={{ 
              background: 'linear-gradient(to right, #f7c5c5, #ffe3b3)',
              color: 'white'
            }}>
              <Typography variant="h6" gutterBottom sx={{ 
                fontWeight: 'bold',
                color: '#555b6e',
                textShadow: '1px 1px 2px rgba(255, 255, 255, 0.5)'
              }}>
                垃圾检测
              </Typography>
            </Box>
            <Box 
              sx={{ 
                display: 'flex', 
                justifyContent: 'center', 
                overflow: 'hidden',
                height: '480px',
                backgroundColor: '#f5f8fa',
                padding: '10px'
              }}
            >
              <img 
                src={videoFeedUrl} 
                alt="视频流"
                style={{ 
                  maxWidth: '100%', 
                  maxHeight: '100%', 
                  objectFit: 'contain',
                  borderRadius: '12px',
                  boxShadow: '0 4px 8px rgba(247, 197, 197, 0.15)'
                }}
              />
            </Box>
          </Paper>
        </Grid>
      )}
    </Grid>
  );
}

export default VideoStream;