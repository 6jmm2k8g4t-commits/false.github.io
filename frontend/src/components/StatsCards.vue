<template>
  <div class="stats-cards">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
            <el-icon size="32" color="#fff"><DataLine /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ formatNumber(dataStore.stats.total_count) }}</div>
            <div class="stat-label">地震记录总数</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
            <el-icon size="32" color="#fff"><Warning /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dataStore.stats.max_magnitude.toFixed(1) }}</div>
            <div class="stat-label">最大震级</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
            <el-icon size="32" color="#fff"><Bottom /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dataStore.stats.avg_depth.toFixed(1) }}km</div>
            <div class="stat-label">平均深度</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)">
            <el-icon size="32" color="#fff"><MapLocation /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ dataStore.stats.high_risk_areas }}</div>
            <div class="stat-label">高风险区域</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const dataStore = useDataStore()

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

onMounted(() => {
  dataStore.fetchStats()
})
</script>

<style scoped>
.stats-cards {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
}

:deep(.dark) .stat-card {
  background: rgba(30, 41, 59, 0.95);
}

:deep(.dark) .stat-value {
  color: #f1f5f9;
}

:deep(.dark) .stat-label {
  color: #94a3b8;
}
</style>
