@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo   🌍 地震分析系统 - 多平台部署助手
echo ==========================================
echo.
echo 请选择部署平台：
echo.
echo   1) 腾讯云 Webify (国内推荐，免费)
echo   2) 阿里云 OSS (国内推荐，低成本)
echo   3) 阿里云学生机 (长期运行，10元/月)
echo   4) Vercel + Render (海外推荐，免费)
echo   5) Gitee Pages (国内免费)
echo   6) Zeabur (新兴平台，免费)
echo   7) 内网穿透 (临时演示)
echo   8) 本地局域网访问 (其他设备访问)
echo.

set /p choice="请输入选项 [1-8]: "

if "%choice%"=="1" goto tencent
if "%choice%"=="2" goto aliyun_oss
if "%choice%"=="3" goto aliyun_student
if "%choice%"=="4" goto vercel
if "%choice%"=="5" goto gitee
if "%choice%"=="6" goto zeabur
if "%choice%"=="7" goto tunnel
if "%choice%"=="8" goto local
goto invalid

:tencent
echo.
echo 📦 腾讯云 Webify 部署步骤：
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 1. 访问: https://webify.cloudbase.net
echo 2. 用微信扫码登录
echo 3. 点击「新建应用」→「导入Git仓库」
echo 4. 选择你的GitHub/Gitee仓库
echo 5. 配置构建命令: cd frontend ^&^& npm install ^&^& npm run build
echo 6. 配置输出目录: frontend/dist
echo 7. 点击「部署」
echo.
echo ✅ 完全免费，国内访问快！
goto end

:aliyun_oss
echo.
echo 📦 阿里云 OSS 部署步骤：
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 1. 访问: https://oss.console.aliyun.com
echo 2. 创建Bucket (公共读)
echo 3. 配置静态网站托管
echo 4. 上传frontend/dist目录
echo.
echo 💰 费用: 约1-5元/月
echo.
echo 正在构建前端...
cd ..\frontend
call npm install
call npm run build
echo ✅ 构建完成！请手动上传dist目录到OSS
goto end

:aliyun_student
echo.
echo 📦 阿里云学生机部署步骤：
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 1. 访问: https://university.aliyun.com
echo 2. 完成学生认证
echo 3. 购买学生机 (9.5元/月起)
echo 4. 连接服务器后运行以下命令：
echo.
echo    curl -fsSL https://get.docker.com ^| bash
echo    git clone https://github.com/your-username/earthquake-system.git
echo    cd earthquake-system/deploy
echo    docker-compose up -d
echo.
echo 💰 费用: 9.5元/月
goto end

:vercel
echo.
echo 📦 Vercel + Render 部署步骤：
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 【后端 - Render】
echo 1. 访问: https://render.com
echo 2. New Web Service → 选择仓库
echo 3. Environment: Python 3
echo 4. Build: pip install -r requirements.txt
echo 5. Start: python app.py
echo.
echo 【前端 - Vercel】
echo 1. 访问: https://vercel.com
echo 2. New Project → 选择仓库
echo 3. Root Directory: frontend
echo 4. 自动检测Vue.js
echo.
echo ✅ 完全免费！
goto end

:gitee
echo.
echo 📦 Gitee Pages 部署步骤：
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 1. 访问: https://gitee.com
echo 2. 创建仓库并推送代码
echo 3. 服务 → Gitee Pages
echo 4. 选择分支和frontend/dist目录
echo 5. 启动
echo.
echo 正在构建前端...
cd ..\frontend
call npm install
call npm run build
echo ✅ 构建完成！
goto end

:zeabur
echo.
echo 📦 Zeabur 部署步骤：
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 1. 访问: https://zeabur.com
echo 2. 用GitHub登录
echo 3. New Project
echo 4. 添加Python服务（后端）
echo 5. 添加Static服务（前端）
echo 6. 一键部署
echo.
echo ✅ 完全免费，支持中文！
goto end

:tunnel
echo.
echo 📦 内网穿透部署：
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 【方式一：ngrok】
echo 1. 访问 https://ngrok.com 注册
echo 2. 下载ngrok
echo 3. 运行: ngrok http 8090
echo.
echo 【方式二：Cloudflare Tunnel】
echo 1. 安装cloudflared
echo 2. 运行: cloudflared tunnel --url http://localhost:8090
echo.
echo ✅ 适合临时演示！
goto end

:local
echo.
echo 📦 本地局域网访问配置：
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 正在获取本机IP地址...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set ip=%%a
    goto :gotip
)
:gotip
set ip=%ip: =%
echo.
echo ✅ 本机IP: %ip%
echo.
echo 其他设备访问地址：
echo   前端: http://%ip%:8080
echo   后端: http://%ip%:8090
echo.
echo 步骤：
echo 1. 确保后端正在运行 (python app.py)
echo 2. 启动前端: cd frontend ^&^& npm run serve
echo 3. 其他设备输入上述地址即可访问
echo.
echo ⚠️ 如无法访问，请检查防火墙设置：
echo    控制面板 → Windows Defender防火墙 → 高级设置
echo    → 入站规则 → 新建规则 → 端口 → TCP 8080,8090 → 允许连接
goto end

:invalid
echo 无效选项
goto end

:end
echo.
echo ==========================================
echo   详细文档: deploy/MORE_OPTIONS.md
echo ==========================================
pause
