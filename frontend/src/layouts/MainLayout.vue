<template>
  <div class="main-layout" :class="{ 'dark-mode': themeStore.isDark }">
    <!-- 顶部导航栏 -->
    <header class="top-header">
      <div class="header-left">
        <div class="logo">
          <el-icon size="32" color="#667eea"><MapLocation /></el-icon>
          <span class="logo-text">地震数据分析平台</span>
        </div>
      </div>
      
      <nav class="main-nav">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
        >
          <el-icon :size="20">
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.title }}</span>
          <div class="nav-indicator" :style="{ background: item.color }"></div>
        </router-link>
      </nav>
      
      <div class="header-right">
        <el-tooltip content="切换主题">
          <el-switch
            :model-value="themeStore.isDark"
            active-text="🌙"
            inactive-text="☀️"
            inline-prompt
            @change="themeStore.toggleTheme"
          />
        </el-tooltip>
        
        <el-dropdown trigger="click">
          <el-avatar :size="36" :icon="UserFilled" class="user-avatar" />
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item>系统设置</el-dropdown-item>
              <el-dropdown-item divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>
    
    <!-- 主内容区域 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade-transform" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <!-- 底部信息 -->
    <footer class="main-footer">
      <p>© 2026 全球地震活动分析平台 | 基于 Vue3 + Flask + MySQL 构建</p>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { MapLocation, UserFilled } from '@element-plus/icons-vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

const navItems = [
  { 
    path: '/', 
    title: '数据看板', 
    icon: 'DataLine',
    color: '#667eea'
  },
  { 
    path: '/query', 
    title: '风险查询', 
    icon: 'Search',
    color: '#f56c6c'
  },
  { 
    path: '/prediction', 
    title: '模型预测', 
    icon: 'TrendCharts',
    color: '#67c23a'
  }
]

onMounted(() => {
  themeStore.initTheme()
})
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
}

.main-layout.dark-mode {
  background: linear-gradient(135deg, #1a1f2e 0%, #0f1419 100%);
}

/* 顶部导航栏 */
.top-header {
  height: 64px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.dark-mode .top-header {
  background: rgba(30, 35, 48, 0.95);
  border-bottom-color: rgba(255, 255, 255, 0.05);
}

.header-left .logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 主导航 */
.main-nav {
  display: flex;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 8px;
  color: #606266;
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-item:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.nav-item.active {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
  font-weight: 600;
}

.dark-mode .nav-item {
  color: #a0a5b1;
}

.dark-mode .nav-item:hover,
.dark-mode .nav-item.active {
  color: #fff;
}

.nav-indicator {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 3px;
  border-radius: 3px 3px 0 0;
  transition: width 0.3s ease;
}

.nav-item.active .nav-indicator {
  width: 60%;
}

/* 右侧操作区 */
.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-avatar {
  cursor: pointer;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 主内容区域 */
.main-content {
  flex: 1;
  margin-top: 64px;
  padding: 24px;
  min-height: calc(100vh - 64px - 60px);
}

/* 底部 */
.main-footer {
  height: 60px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 14px;
}

.dark-mode .main-footer {
  background: rgba(30, 35, 48, 0.8);
  border-top-color: rgba(255, 255, 255, 0.05);
  color: #606873;
}

/* 页面切换动画 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s ease;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* 响应式适配 */
@media (max-width: 768px) {
  .top-header {
    padding: 0 16px;
  }
  
  .logo-text {
    display: none;
  }
  
  .main-nav {
    gap: 4px;
  }
  
  .nav-item {
    padding: 8px 12px;
  }
  
  .nav-item span {
    display: none;
  }
  
  .main-content {
    padding: 16px;
  }
}
</style>
