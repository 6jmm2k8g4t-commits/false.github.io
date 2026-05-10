import axios from 'axios'

const getBaseURL = () => {
  const hostname = window.location.hostname
  
  // GitHub Pages 部署环境 - 使用 PythonAnywhere 后端（免费）
  if (hostname.includes('github.io')) {
    console.log('[INFO] Using PythonAnywhere API: https://flase.pythonanywhere.com')
    return 'https://flase.pythonanywhere.com'
  }
  
  // 本地开发环境
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    console.log('[INFO] Using local API: http://localhost:8090')
    return 'http://localhost:8090'
  }
  
  // 其他生产环境（默认回退）
  console.log('[WARN] Using default API:', `http://${hostname}:8090`)
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
