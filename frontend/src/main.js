import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import axios from 'axios'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

const getBaseURL = () => {
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8090'
  }
  return `http://${window.location.hostname}:8090`
}

axios.defaults.baseURL = getBaseURL()
axios.defaults.timeout = 30000

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
