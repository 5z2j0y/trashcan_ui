import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import './VideoDisplay.css';
import VideoStream from './VideoStream';

const VideoDisplay = () => {
  return (
    <Box className="video-container">
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} className="video-box">
            <Typography variant="h6" sx={{ mb: 1 }}>垃圾分类宣传</Typography>
            <img 
              src="/promo_video" 
              alt="宣传视频" 
              style={{ width: '100%', height: 'auto', maxHeight: '480px' }}
            />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} className="video-box">
            <Typography variant="h6" sx={{ mb: 1 }}>实时垃圾检测</Typography>
            <img 
              src="/video_feed" 
              alt="检测视频" 
              style={{ width: '100%', height: 'auto', maxHeight: '480px' }}
            />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default VideoDisplay;
