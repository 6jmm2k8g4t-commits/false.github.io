import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import DashboardView from '@/views/DashboardView.vue'
import RiskQueryView from '@/views/RiskQueryView.vue'
import PredictionView from '@/views/PredictionView.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: DashboardView,
        meta: { 
          title: '数据看板', 
          icon: 'DataLine',
          description: '全球地震数据可视化看板'
        }
      },
      {
        path: 'query',
        name: 'RiskQuery',
        component: RiskQueryView,
        meta: { 
          title: '风险查询', 
          icon: 'Search',
          description: '多条件地震风险查询'
        }
      },
      {
        path: 'prediction',
        name: 'Prediction',
        component: PredictionView,
        meta: { 
          title: '模型预测', 
          icon: 'TrendCharts',
          description: 'ARIMA/Prophet时序预测'
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 地震数据分析平台`
  }
  next()
})

export default router
