# 地震数据可视化平台 - 部署助手脚本
# 使用方法: 在 PowerShell 中运行: .\deploy-helper.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  地震数据可视化平台 - 部署助手" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Git 状态
Write-Host "📋 步骤 1: 检查 Git 状态..." -ForegroundColor Yellow
git status
Write-Host ""

# 推送到 GitHub
Write-Host "📤 步骤 2: 推送到 GitHub..." -ForegroundColor Yellow
Write-Host "如果提示输入用户名，请输入: 6jmm2k8g4t-commits" -ForegroundColor Gray
Write-Host "如果提示输入密码，请输入你的 Personal Access Token" -ForegroundColor Gray
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 代码推送成功!" -ForegroundColor Green
} else {
    Write-Host "❌ 推送失败，请检查错误信息" -ForegroundColor Red
    Write-Host "提示: 你可能需要创建 Personal Access Token" -ForegroundColor Yellow
    Write-Host "访问: https://github.com/settings/tokens" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  下一步操作" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 访问 GitHub 仓库确认代码已推送:" -ForegroundColor White
Write-Host "   https://github.com/6jmm2k8g4t-commits/false.github.io" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 部署后端到 Render:" -ForegroundColor White
Write-Host "   a) 访问 https://render.com 并登录" -ForegroundColor Cyan
Write-Host "   b) 点击 'New Web Service'" -ForegroundColor Cyan
Write-Host "   c) 选择 GitHub 仓库" -ForegroundColor Cyan
Write-Host "   d) 填写配置:" -ForegroundColor Cyan
Write-Host "      - Name: earthquake-backend" -ForegroundColor Gray
Write-Host "      - Runtime: Python 3" -ForegroundColor Gray
Write-Host "      - Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "      - Start Command: gunicorn backend.app:app --bind 0.0.0.0:`$PORT" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 启用 GitHub Pages:" -ForegroundColor White
Write-Host "   a) 访问 https://github.com/6jmm2k8g4t-commits/false.github.io/settings/pages" -ForegroundColor Cyan
Write-Host "   b) Source 选择 'GitHub Actions'" -ForegroundColor Cyan
Write-Host "   c) 点击 Save" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. 更新 API 地址:" -ForegroundColor White
Write-Host "   a) 获取 Render 部署地址 (如: https://earthquake-backend.onrender.com)" -ForegroundColor Cyan
Write-Host "   b) 修改 frontend/src/utils/api.js 中的 API 地址" -ForegroundColor Cyan
Write-Host "   c) 重新推送代码" -ForegroundColor Cyan
Write-Host ""
Write-Host "详细说明请查看 DEPLOY.md" -ForegroundColor Yellow
