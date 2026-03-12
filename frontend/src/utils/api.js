import axios from 'axios'

const getBaseURL = () => {
  const hostname = window.location.hostname
  
  // 本地开发环境
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8090'
  }
  
  // GitHub Pages 部署环境 - 使用 Render 后端
  if (hostname.includes('github.io')) {
    // 替换为你的 Render 后端地址
    return 'https://earthquake-backend.onrender.com'
  }
  
  // 其他生产环境
  return `http://${hostname}:8090`
}

const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default api
