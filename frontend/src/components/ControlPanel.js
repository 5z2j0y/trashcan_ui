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
        borderRadius: '16px',
        backgroundColor: 'var(--card-color)',
        boxShadow: '0 6px 16px rgba(163, 216, 244, 0.15)',
        border: '1px solid var(--border-color)',
        transition: 'transform 0.3s ease',
        '&:hover': {
          transform: 'translateY(-5px)'
        }
      }}
    >
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        mb: expanded ? 2 : 0,
        pb: expanded ? 2 : 0,
        borderBottom: expanded ? '1px solid var(--border-color)' : 'none'
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography 
            variant="h6" 
            gutterBottom 
            sx={{ 
              mb: 0, 
              mr: 2, 
              fontWeight: 'bold', 
              color: 'var(--text-primary)' 
            }}
          >
            摄像头控制面板
          </Typography>
          <Chip 
            label={socketConnected ? "服务已连接" : "服务未连接"} 
            color={socketConnected ? "success" : "error"}
            size="small"
            sx={{ 
              fontWeight: 'bold',
              backgroundColor: socketConnected ? 'var(--success-color)' : 'var(--error-color)',
              color: 'var(--text-primary)'
            }}
          />
        </Box>
        <IconButton 
          onClick={toggleExpanded} 
          size="small"
          sx={{ 
            color: 'var(--primary-color)', 
            backgroundColor: 'var(--hover-color)',
            '&:hover': {
              backgroundColor: 'var(--border-color)'
            }
          }}
        >
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
                startAdornment={<CameraAltIcon sx={{ mr: 1, color: 'var(--primary-color)' }} />}
                disabled={isDetecting}
                sx={{
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'var(--border-color)'
                  },
                  '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'var(--primary-color)'
                  },
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'var(--primary-color)'
                  }
                }}
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
                    sx={{ 
                      flex: 2,
                      backgroundColor: 'var(--secondary-color)',
                      color: 'var(--text-primary)',
                      '&:hover': {
                        backgroundColor: '#f4b8b8'
                      }
                    }}
                  >
                    停止检测
                  </Button>
                  <Tooltip title="刷新视频流">
                    <Button
                      variant="outlined"
                      color="primary"
                      size="large"
                      onClick={handleRefreshStream}
                      sx={{ 
                        flex: 1,
                        borderColor: 'var(--primary-color)',
                        color: 'var(--text-primary)',
                        '&:hover': {
                          borderColor: 'var(--primary-color)',
                          backgroundColor: 'rgba(163, 216, 244, 0.1)'
                        }
                      }}
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
                  sx={{ 
                    backgroundColor: 'var(--primary-color)',
                    color: 'var(--text-primary)',
                    '&:hover': {
                      backgroundColor: '#90c7e3'
                    },
                    fontWeight: 'bold',
                    py: 1.2
                  }}
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