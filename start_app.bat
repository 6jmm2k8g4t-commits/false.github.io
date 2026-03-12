@echo off

echo 全球地震活动分析平台启动脚本
echo ===============================
echo.

rem 切换到backend目录
cd /d "%~dp0backend"

rem 检查前端文件是否存在
if exist simple-frontend.html (
    echo 前端文件已就绪
) else (
    echo 错误：前端文件不存在
    pause
    exit /b 1
)

rem 检查数据文件是否存在
if exist ..\earthquake_dataset.csv (
    echo 数据文件已就绪
) else (
    echo 警告：数据文件不存在
)

rem 启动后端服务器
echo.
echo 正在启动后端服务器...
echo.
echo 请等待服务器启动完成...
echo.
echo 服务器将在 http://localhost:8084 启动
echo.
echo 启动后请在浏览器中访问上述地址
echo.

python simple_server_simple.py

pause
