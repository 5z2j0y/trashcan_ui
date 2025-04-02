@echo off
REM Windows批处理脚本

REM 设置视频目录的绝对路径
set SCRIPT_DIR=%~dp0
set VIDEOS_DIR=%SCRIPT_DIR%videos

REM 确保videos目录存在
if not exist "%VIDEOS_DIR%" mkdir "%VIDEOS_DIR%"
echo 视频目录: %VIDEOS_DIR%

REM 检查是否存在demo.mp4
if not exist "%VIDEOS_DIR%\demo.mp4" (
  echo 警告：%VIDEOS_DIR%\demo.mp4 文件不存在，请添加宣传视频文件
)

REM 检查是否存在models目录和模型文件
if not exist "models\trashcan.pt" (
  echo 错误：models\trashcan.pt 模型文件不存在，请先添加模型文件
  exit /b 1
)

REM 启动应用
echo 启动垃圾检测系统...
python app.py
