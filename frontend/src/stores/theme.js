import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 状态
  const isDark = ref(false)
  
  // 初始化主题
  const initTheme = () => {
    const savedTheme = localStorage.getItem('app_theme')
    if (savedTheme) {
      isDark.value = savedTheme === 'dark'
    } else {
      // 检测系统主题偏好
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    applyTheme()
  }
  
  // 切换主题
  const toggleTheme = () => {
    isDark.value = !isDark.value
    applyTheme()
    saveTheme()
  }
  
  // 应用主题
  const applyTheme = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }
  
  // 保存主题到localStorage
  const saveTheme = () => {
    localStorage.setItem('app_theme', isDark.value ? 'dark' : 'light')
  }
  
  return {
    isDark,
    initTheme,
    toggleTheme
  }
})
