# PythonAnywhere 部署指南

## 🚀 快速部署步骤

### 第一步：注册账号
1. 访问 https://www.pythonanywhere.com
2. 点击 "Start running Python online in less than a minute"
3. 填写用户名、邮箱、密码
4. 点击 "Create account"

### 第二步：上传代码
**方式一：使用 Git（推荐）**
1. 登录后点击顶部 "Consoles"
2. 点击 "Bash" 打开终端
3. 运行以下命令：
```bash
cd ~
git clone https://github.com/6jmm2k8g4t-commits/false.github.io.git 地震可视化平台
cd 地震可视化平台
```

**方式二：上传 ZIP 文件**
1. 在本地将项目打包成 ZIP
2. 点击顶部 "Files"
3. 点击 "Upload a file"
4. 选择 ZIP 文件上传
5. 在 Bash 中解压：
```bash
unzip 地震可视化平台.zip
cd 地震可视化平台
```

### 第三步：上传数据文件
1. 点击 "Files" 标签
2. 进入 `地震可视化平台` 目录
3. 点击 "Upload a file"
4. 选择 `earthquake_dataset.csv` 上传（约177MB）

### 第四步：创建 Web 应用
1. 点击顶部 "Web"
2. 点击 "Add a new web app"
3. 选择 "Manual configuration (including virtualenvs)"
4. 选择 Python 3.9
5. 点击 "Next"

### 第五步：配置 WSGI
1. 在 Web 页面找到 "Code" 部分
2. 点击 "WSGI configuration file" 链接（如 `/var/www/username_pythonanywhere_com_wsgi.py`）
3. **删除原有内容**，替换为：

```python
import sys
import os

# 添加项目路径
project_home = '/home/你的用户名/地震可视化平台'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 设置环境变量
os.environ['DATA_FILE_PATH'] = '/home/你的用户名/地震可视化平台/earthquake_dataset.csv'

# 导入 Flask 应用
from backend.app import app as application
```

**注意**：将 `你的用户名` 替换为您的实际用户名

### 第六步：安装依赖
1. 点击 "Consoles" → "Bash"
2. 运行：
```bash
cd ~/地震可视化平台
pip install -r requirements.txt
```

### 第七步：配置虚拟环境（可选但推荐）
1. 在 Bash 中运行：
```bash
cd ~/地震可视化平台
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. 在 Web 页面找到 "Virtualenv" 部分
3. 填写路径：`/home/你的用户名/地震可视化平台/venv`

### 第八步：重启应用
1. 回到 "Web" 标签
2. 点击 "Reload" 按钮
3. 等待应用启动（约30秒）

### 第九步：验证部署
1. 访问您的域名：`https://你的用户名.pythonanywhere.com`
2. 测试 API：`https://你的用户名.pythonanywhere.com/api/health`
3. 应该返回：`{"status": "healthy"}`

---

## 🔧 常见问题解决

### 问题1：ImportError: No module named 'flask'
**解决**：确保在正确的虚拟环境中安装了依赖
```bash
source /home/你的用户名/地震可视化平台/venv/bin/activate
pip install -r requirements.txt
```

### 问题2：数据文件找不到
**解决**：检查环境变量路径是否正确
```python
# 在 WSGI 文件中确认路径
os.environ['DATA_FILE_PATH'] = '/home/你的用户名/地震可视化平台/earthquake_dataset.csv'
```

### 问题3：内存不足
**解决**：PythonAnywhere 免费版有内存限制，可以尝试：
1. 减少数据加载量
2. 使用数据采样
3. 升级付费版

### 问题4：启动超时
**解决**：数据文件太大导致启动慢
1. 预加载数据到内存
2. 使用更小的测试数据集
3. 优化代码启动速度

---

## 📊 免费版限制

| 限制项 | 免费版 | 付费版 |
|--------|--------|--------|
| CPU 时间 | 每天有限制 | 无限制 |
| 磁盘空间 | 512MB | 10GB+ |
| 内存 | 512MB | 2GB+ |
| 带宽 | 有限制 | 无限制 |
| 自定义域名 | ❌ | ✅ |
|  always-on | ❌ | ✅ |

**注意**：免费版应用会在一段时间无访问后休眠，首次访问需要唤醒（约10-30秒）

---

## 🎯 部署后配置

### 更新前端 API 地址
前端代码已配置为自动识别环境：
- GitHub Pages 环境 → 使用 PythonAnywhere API
- 本地环境 → 使用 localhost:8090

### 配置 CORS
后端已配置支持 PythonAnywhere 域名访问，无需额外设置。

---

## 🆘 获取帮助

如果遇到问题：
1. 查看 PythonAnywhere 日志：Web → "Logs" 部分
2. 在 Bash 中测试：`python -c "from backend.app import app; print('OK')"`
3. 访问论坛：https://www.pythonanywhere.com/forums/

---

## ✅ 部署检查清单

- [ ] 注册 PythonAnywhere 账号
- [ ] 上传项目代码
- [ ] 上传数据文件
- [ ] 创建 Web 应用
- [ ] 配置 WSGI 文件
- [ ] 安装依赖
- [ ] 配置环境变量
- [ ] 重启应用
- [ ] 测试 API 访问
- [ ] 更新前端代码（如需要）
