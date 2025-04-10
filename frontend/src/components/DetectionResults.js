import React, { useState, useEffect } from 'react';
import { 
  Paper, 
  Box, 
  Typography, 
  List, 
  ListItem, 
  ListItemText, 
  Chip, 
  Divider,
  Alert,
  IconButton,
  Collapse
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import DeleteIcon from '@mui/icons-material/Delete';

// 中文垃圾类别映射
const trashTypeMap = {
  'bottle': '塑料瓶',
  'brick': '砖块',
  'battery': '电池',
  'can': '易拉罐',
  'carrot': '胡萝卜',
  'china': '陶瓷',
  'paperCup': '纸杯',
  'pill': '药片',
  'potato': '土豆',
  'radish': '萝卜',
  'stone': '石头',
  'potato_chip': '薯片'
};

// 垃圾分类映射
const trashCategoryMap = {
  'bottle': '可回收垃圾',
  'brick': '其他垃圾',
  'battery': '有害垃圾',
  'can': '可回收垃圾',
  'carrot': '厨余垃圾',
  'china': '其他垃圾',
  'paperCup': '可回收垃圾',
  'pill': '有害垃圾',
  'potato': '厨余垃圾',
  'radish': '厨余垃圾',
  'stone': '其他垃圾',
  'potato_chip': '其他垃圾'
};

// 垃圾分类颜色映射
const categoryColorMap = {
  '可回收垃圾': '#0074d9', // 蓝色
  '有害垃圾': '#ff4136',  // 红色
  '厨余垃圾': '#2ecc40',  // 绿色
  '其他垃圾': '#ff851b'   // 橙色
};

const DetectionResults = ({ results = [], onClearResults }) => {
  const [expanded, setExpanded] = useState(true);
  const [showAlert, setShowAlert] = useState(false);
  
  // 当有新结果时显示提示
  useEffect(() => {
    if (results.length > 0 && !expanded) {
      setShowAlert(true);
    }
  }, [results, expanded]);

  // 展开面板时隐藏提示
  useEffect(() => {
    if (expanded) {
      setShowAlert(false);
    }
  }, [expanded]);

  const toggleExpanded = () => {
    setExpanded(!expanded);
  };

  const handleClearResults = () => {
    if (onClearResults) {
      onClearResults();
    }
  };

  // 获取中文名称
  const getChineseName = (label) => {
    return trashTypeMap[label] || label;
  };

  // 获取垃圾分类
  const getCategory = (label) => {
    return trashCategoryMap[label] || '未知分类';
  };

  // 获取分类颜色
  const getCategoryColor = (label) => {
    const category = getCategory(label);
    return categoryColorMap[category] || 'default';
  };

  // 格式化检测置信度
  const formatConfidence = (score) => {
    return (score * 100).toFixed(1) + '%';
  };

  // 格式化时间 - 保留函数但不再使用
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('zh-CN');
  };

  return (
    <>
      <Collapse in={showAlert && !expanded}>
        <Alert 
          severity="info" 
          sx={{ 
            mb: 2,
            backgroundColor: 'rgba(163, 216, 244, 0.2)',
            color: 'var(--text-primary)',
            '& .MuiAlert-icon': {
              color: 'var(--primary-color)'
            }
          }}
          onClose={() => setShowAlert(false)}
        >
          有新的检测结果，点击展开查看
        </Alert>
      </Collapse>
      
      <Paper 
        elevation={3} 
        sx={{ 
          mb: 3, 
          borderRadius: '16px',
          overflow: 'hidden',
          border: '1px solid var(--border-color)',
          transition: 'transform 0.3s ease, box-shadow 0.3s ease',
          '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 8px 20px rgba(163, 216, 244, 0.2)'
          }
        }}
      >
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          p: 2,
          borderBottom: expanded ? '1px solid var(--border-color)' : 'none',
          background: 'linear-gradient(to right, var(--primary-color), var(--success-color))',
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="h6" sx={{ 
              fontWeight: 'bold',
              color: 'var(--text-primary)',
              textShadow: '1px 1px 2px rgba(255, 255, 255, 0.5)'
            }}>
              检测结果
            </Typography>
            {results.length > 0 && (
              <Chip 
                label={results.length} 
                size="small" 
                sx={{ 
                  ml: 1,
                  backgroundColor: '#ffffff',
                  color: 'var(--text-primary)',
                  fontWeight: 'bold'
                }} 
              />
            )}
          </Box>
          <Box>
            {results.length > 0 && (
              <IconButton 
                size="small" 
                onClick={handleClearResults} 
                sx={{ 
                  mr: 1,
                  color: 'var(--text-primary)',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.5)'
                  }
                }}
                title="清空检测结果"
              >
                <DeleteIcon />
              </IconButton>
            )}
            <IconButton 
              size="small" 
              onClick={toggleExpanded}
              title={expanded ? "收起" : "展开"}
              sx={{ 
                color: 'var(--text-primary)',
                '&:hover': {
                  backgroundColor: 'rgba(255, 255, 255, 0.5)'
                }
              }}
            >
              {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            </IconButton>
          </Box>
        </Box>
        
        <Collapse in={expanded}>
          <Box sx={{ maxHeight: '300px', overflow: 'auto', backgroundColor: 'var(--card-color)' }}>
            {results.length === 0 ? (
              <Box sx={{ p: 3, textAlign: 'center' }}>
                <Typography color="text.secondary">
                  暂无检测结果，开始检测后将在此处显示
                </Typography>
              </Box>
            ) : (
              <List dense>
                {results.map((item, index) => (
                  <React.Fragment key={index}>
                    <ListItem sx={{ 
                      transition: 'background-color 0.2s ease', 
                      '&:hover': { 
                        backgroundColor: 'var(--hover-color)' 
                      } 
                    }}>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 1 }}>
                            <Typography variant="body2" sx={{ color: 'grey.500' }}>
                              （{getChineseName(item.label)}）
                            </Typography>
                            <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: 'var(--text-primary)' }}>
                              {index + 1}
                            </Typography>
                            <Chip 
                              label={getCategory(item.label)} 
                              size="small" 
                              sx={{ 
                                fontWeight: 'bold', 
                                backgroundColor: categoryColorMap[getCategory(item.label)] || 'var(--warning-color)',
                                color: 'white'
                              }}
                            />
                            <Chip 
                              label="OK!" 
                              size="small" 
                              sx={{
                                fontWeight: 'bold',
                                backgroundColor: 'var(--success-color)',
                                color: 'black'
                              }}
                            />
                            <Typography variant="body2" sx={{ color: 'grey.500' }}>
                              （{formatConfidence(item.score)}）
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < results.length - 1 && <Divider component="li" />}
                  </React.Fragment>
                ))}
              </List>
            )}
          </Box>
        </Collapse>
      </Paper>
    </>
  );
};

export default DetectionResults;
