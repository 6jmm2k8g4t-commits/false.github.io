# 🚀 更多部署方案

## 方案总览

| 方案 | 适合人群 | 费用 | 国内访问 | 难度 |
|------|----------|------|----------|------|
| Vercel + Render | 海外用户 | 免费 | 较慢 | ⭐ |
| **Gitee Pages** | 国内用户 | 免费 | **很快** | ⭐ |
| **阿里云OSS** | 国内用户 | 极低 | **很快** | ⭐⭐ |
| **腾讯云Webify** | 国内用户 | 免费 | **很快** | ⭐ |
| Zeabur | 全球用户 | 免费 | 中等 | ⭐ |
| Koyeb | 海外用户 | 免费 | 较慢 | ⭐ |
| 阿里云学生机 | 长期使用 | **10元/月** | **很快** | ⭐⭐ |

---

## 方案一：Gitee Pages（国内推荐）⭐⭐⭐⭐⭐

**优点**：完全免费、国内访问快、无需备案

### 步骤

#### 1. 部署后端到Gitee Go

```bash
# 创建Gitee仓库
# 访问 https://gitee.com/projects/new

# 推送代码
git remote add gitee https://gitee.com/你的用户名/earthquake-system.git
git push gitee main
```

#### 2. 使用Gitee Pages部署前端

1. 访问 https://gitee.com/你的用户名/earthquake-system
2. **服务** → **Gitee Pages**
3. 选择分支和目录：`frontend/dist`
4. 点击 **启动**

#### 3. 后端使用免费云函数

**使用阿里云函数计算（免费额度）**：

```yaml
# 创建 s.yaml
edition: 1.0.0
name: earthquake-backend
access: default

services:
  earthquake-api:
    component: fc
    props:
      region: cn-hangzhou
      service:
        name: earthquake-service
      function:
        name: api
        runtime: python3.9
        codeUri: ./backend
        handler: app.app
        memorySize: 256
        timeout: 60
      triggers:
        - name: httpTrigger
          type: http
          config:
            authType: anonymous
            methods:
              - GET
              - POST
```

---

## 方案二：腾讯云 Webify（国内推荐）⭐⭐⭐⭐⭐

**优点**：完全免费、国内CDN、自动部署

### 步骤

1. 访问 https://webify.cloudbase.net
2. 用微信扫码登录
3. **新建应用** → **导入Git仓库**
4. 选择你的GitHub/Gitee仓库
5. 配置：

| 配置项 | 值 |
|--------|-----|
| 构建命令 | `cd frontend && npm install && npm run build` |
| 输出目录 | `frontend/dist` |

6. 点击 **部署**

**免费额度**：
- 5GB存储
- 5GB/月流量
- 1000次/天构建

---

## 方案三：阿里云OSS静态托管（最低成本）⭐⭐⭐⭐

**优点**：成本极低（约1元/月）、国内访问快

### 步骤

#### 1. 开通阿里云OSS

访问 https://oss.console.aliyun.com

#### 2. 创建Bucket

| 配置项 | 值 |
|--------|-----|
| Bucket名称 | earthquake-system |
| 地域 | 华东1（杭州） |
| 存储类型 | 标准存储 |
| 读写权限 | 公共读 |

#### 3. 配置静态网站

1. **基础设置** → **静态页面**
2. 默认首页：`index.html`
3. 默认404页：`index.html`

#### 4. 上传前端文件

```bash
# 安装ossutil
# 访问 https://help.aliyun.com/document_detail/120075.html

# 配置
ossutil config -e oss-cn-hangzhou.aliyuncs.com -i your-access-key -k your-secret-key

# 上传
ossutil cp -r frontend/dist/ oss://earthquake-system/ --update
```

#### 5. 后端使用函数计算

```bash
# 安装Serverless DevTools
npm install -g @serverless-devs/s

# 部署
s deploy
```

**费用估算**：
- OSS存储：0.12元/GB/月
- OSS流量：0.5元/GB
- 函数计算：免费额度足够

**月费用约：1-5元**

---

## 方案四：Zeabur（新兴平台）⭐⭐⭐⭐

**优点**：支持中文、一键部署、免费额度

### 步骤

1. 访问 https://zeabur.com
2. 用GitHub登录
3. **New Project**
4. 添加服务：
   - **Python** 服务（后端）
   - **Static** 服务（前端）
5. 配置环境变量
6. 一键部署

**免费额度**：
- 5美元/月额度
- 足够小型项目使用

---

## 方案五：Koyeb⭐⭐⭐

**优点**：完全免费、全球部署

### 步骤

1. 访问 https://www.koyeb.com
2. 用GitHub登录
3. **Create App**
4. 选择仓库
5. 配置：

```yaml
# koyeb.yaml
services:
  - name: earthquake-backend
    github:
      branch: main
      path: backend
    instance_type: free
    ports:
      - port: 8090
        protocol: http
    health_check:
      path: /api/stats
```

---

## 方案六：阿里云学生机（长期推荐）⭐⭐⭐⭐⭐

**优点**：完全控制、性能好、学习价值高

### 步骤

#### 1. 购买学生机

访问 https://university.aliyun.com

| 配置 | 价格 |
|------|------|
| 2核2G | **9.5元/月** |
| 2核4G | **19元/月** |

#### 2. 一键部署

```bash
# 连接服务器
ssh root@your-server-ip

# 安装Docker
curl -fsSL https://get.docker.com | bash

# 克隆项目
git clone https://github.com/your-username/earthquake-system.git
cd earthquake-system

# 一键部署
cd deploy
chmod +x deploy.sh
./deploy.sh
```

#### 3. 配置域名（可选）

阿里云提供免费域名备案服务。

---

## 方案七：内网穿透（临时演示）

### 使用Cloudflare Tunnel（免费）

```bash
# 安装cloudflared
# Windows: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

# 登录
cloudflared tunnel login

# 创建隧道
cloudflared tunnel create earthquake

# 运行隧道
cloudflared tunnel --url http://localhost:8090 run earthquake
```

### 使用ngrok（免费）

```bash
# 下载ngrok
# 访问 https://ngrok.com

# 运行
ngrok http 8090
```

---

## 💰 费用对比

| 方案 | 月费用 | 年费用 | 备注 |
|------|--------|--------|------|
| Vercel + Render | 0元 | 0元 | 海外访问 |
| Gitee Pages | 0元 | 0元 | 国内访问 |
| 腾讯云Webify | 0元 | 0元 | 国内访问 |
| 阿里云OSS | 1-5元 | 12-60元 | 国内访问 |
| 阿里云学生机 | 10元 | 120元 | 完全控制 |
| Zeabur | 0元 | 0元 | 新兴平台 |

---

## 🎯 推荐选择

| 场景 | 推荐方案 |
|------|----------|
| 毕业答辩演示 | 腾讯云Webify 或 阿里云OSS |
| 长期运行 | 阿里云学生机（10元/月） |
| 完全免费 | Vercel + Render 或 Gitee Pages |
| 国内用户为主 | 腾讯云Webify 或 阿里云OSS |
| 学习服务器运维 | 阿里云学生机 |

---

## 📱 快速决策

**如果你是...**

1. **学生党，想省钱** → 腾讯云Webify（免费）
2. **想学习运维** → 阿里云学生机（10元/月）
3. **临时演示** → ngrok内网穿透
4. **长期使用** → 阿里云OSS + 函数计算（约5元/月）
5. **海外用户** → Vercel + Render

---

## 🔗 相关链接

- 腾讯云Webify: https://webify.cloudbase.net
- 阿里云学生计划: https://university.aliyun.com
- Gitee: https://gitee.com
- Zeabur: https://zeabur.com
- Koyeb: https://www.koyeb.com
