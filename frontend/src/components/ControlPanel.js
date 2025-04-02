import React, { useState } from 'react';
import { 
  Box, 
  Button, 
  Paper, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem,
  Grid,
  Tooltip,
  Typography,
  Badge,
  Collapse,
  IconButton,
  Chip
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import RefreshIcon from '@mui/icons-material/Refresh';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';

const ControlPanel = ({ 
  isDetecting, 
  onStartDetection, 
  onStopDetection, 
  onCameraChange,
  currentCameraId,
  socketConnected = false
}) => {
  // 添加折叠状态
  const [expanded, setExpanded] = useState(true);

  // 切换折叠状态
  const toggleExpanded = () => {
    setExpanded(!expanded);
  };

  // 创建0-9的摄像头选项
  const cameraOptions = Array.from({ length: 10 }, (_, i) => i);
  
  // 刷新视频流
  const handleRefreshStream = () => {
    if (isDetecting) {
      onStopDetection();
      // 短暂延迟后重新开始检测
      setTimeout(() => {
        onStartDetection();
      }, 500);
    }
  };

  return (
    <Paper 
      elevation={3} 
      sx={{ 
        p: 3, 
        borderRadius: 2,
        backgroundColor: '#f9f9f9'
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: expanded ? 2 : 0 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="h6" gutterBottom sx={{ mb: 0, mr: 2 }}>
            摄像头控制面板
          </Typography>
          <Chip 
            label={socketConnected ? "服务已连接" : "服务未连接"} 
            color={socketConnected ? "success" : "error"}
            size="small"
          />
        </Box>
        <IconButton onClick={toggleExpanded} size="small">
          {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        </IconButton>
      </Box>
      
      <Collapse in={expanded} timeout="auto">
        <Grid container spacing={3} alignItems="center" sx={{ mt: 1 }}>
          <Grid item xs={12} md={5}>
            <FormControl fullWidth variant="outlined">
              <InputLabel id="camera-select-label">摄像头</InputLabel>
              <Select
                labelId="camera-select-label"
                id="camera-select"
                value={currentCameraId}
                onChange={(e) => onCameraChange(e.target.value)}
                label="摄像头"
                startAdornment={<CameraAltIcon sx={{ mr: 1 }} />}
                disabled={isDetecting}
              >
                {cameraOptions.map((id) => (
                  <MenuItem key={id} value={id}>
                    摄像头 {id}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
              {isDetecting ? '检测进行中时无法更改摄像头' : '请选择要使用的摄像头编号'}
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={7}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
              {isDetecting ? (
                <>
                  <Button
                    variant="contained"
                    color="secondary"
                    size="large"
                    startIcon={<StopIcon />}
                    onClick={onStopDetection}
                    sx={{ flex: 2 }}
                  >
                    停止检测
                  </Button>
                  <Tooltip title="刷新视频流">
                    <Button
                      variant="outlined"
                      color="primary"
                      size="large"
                      onClick={handleRefreshStream}
                      sx={{ flex: 1 }}
                    >
                      <RefreshIcon />
                    </Button>
                  </Tooltip>
                </>
              ) : (
                <Button
                  variant="contained"
                  color="primary"
                  size="large"
                  startIcon={<PlayArrowIcon />}
                  onClick={onStartDetection}
                  fullWidth
                  disabled={currentCameraId === null || !socketConnected}
                >
                  开始检测
                </Button>
              )}
            </Box>
            {!socketConnected && (
              <Typography variant="caption" color="error" sx={{ display: 'block', mt: 1 }}>
                服务未连接，无法开始检测
              </Typography>
            )}
          </Grid>
        </Grid>
      </Collapse>
    </Paper>
  );
};

export default ControlPanel;