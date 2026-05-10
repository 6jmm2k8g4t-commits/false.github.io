# 免费部署指南

## 1. 后端部署到 Render（免费）

### 步骤：

1. **注册 Render 账号**
   - 访问 https://render.com
   - 使用 GitHub 账号登录

2. **创建 New Web Service**
   - 选择你的 GitHub 仓库
   - 填写配置：
     - **Name**: earthquake-backend
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn backend.app:app --bind 0.0.0.0:$PORT`

3. **添加环境变量**
   - 在 Render Dashboard → Environment 中添加：
     - `DATA_FILE_PATH`: `/data/earthquake_dataset.csv`

4. **上传数据文件**
   - 在 Render Dashboard → Disks 中查看磁盘挂载路径
   - 通过 Render Shell 上传 `earthquake_dataset.csv` 到 `/data/` 目录

5. **获取部署地址**
   - 部署成功后，你会得到一个类似 `https://earthquake-backend.onrender.com` 的地址
   - 将这个地址更新到 `frontend/src/utils/api.js` 中

---

## 2. 前端部署到 GitHub Pages（免费）

GitHub Actions 已配置好，推送代码后会自动部署。

### 启用 GitHub Pages：

1. 访问仓库 Settings → Pages
2. Source 选择 "GitHub Actions"
3. 保存

---

## 3. 更新前端 API 地址

部署后端后，需要更新前端代码中的 API 地址：

1. 打开 `frontend/src/utils/api.js`
2. 将 `https://earthquake-backend.onrender.com` 替换为你实际的 Render 地址
3. 重新构建并推送前端代码

---

## 备选方案：Railway（免费额度）

如果 Render 不满意，可以使用 Railway：

1. 访问 https://railway.app
2. 从 GitHub 导入项目
3. 添加环境变量 `PORT=8080`
4. 部署命令：`gunicorn backend.app:app --bind 0.0.0.0:$PORT`

---

## 注意事项

1. **Render 免费版限制**：
   - 15 分钟无请求后会休眠
   - 首次访问可能需要等待唤醒（约 30 秒）

2. **数据文件**：
   - 确保 `earthquake_dataset.csv` 已上传到 Render 的磁盘
   - 或使用环境变量 `DATA_FILE_PATH` 指定路径

3. **CORS**：
   - 后端已配置 CORS，支持 GitHub Pages 域名访问
