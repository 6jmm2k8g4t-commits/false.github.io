import axios from 'axios'

const getBaseURL = () => {
  const hostname = window.location.hostname
  
  // GitHub Pages 部署环境 - 使用 Railway 后端（必须放在最前面）
  if (hostname.includes('github.io')) {
    console.log('🚀 Using Railway API: https://earthquake-backend-production-d098.up.railway.app')
    return 'https://earthquake-backend-production-d098.up.railway.app'
  }
  
  // 本地开发环境
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    console.log(' Using local API: http://localhost:8090')
    return 'http://localhost:8090'
  }
  
  // 其他生产环境（默认回退）
  console.log('⚠️ Using default API:', `http://${hostname}:8090`)
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
