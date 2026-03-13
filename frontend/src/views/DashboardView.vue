<template>
  <div class="dashboard-view">
    <div class="page-header">
      <h1 class="page-title">
        <el-icon size="32" color="#667eea"><DataLine /></el-icon>
        数据看板
      </h1>
      <p class="page-subtitle">全球地震数据可视化看板 - 6大核心图表</p>
    </div>
    
    <StatsCards />
    
    <el-row :gutter="20" class="charts-grid">
      <el-col :xs="24" :lg="12">
        <TimeSeriesChart />
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <HeatmapChart />
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <PlateBoundaryChart />
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <ScatterChart />
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <TopRiskRegionsChart />
      </el-col>
      
      <el-col :xs="24" :lg="12">
        <EarthquakeTimeline />
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { DataLine } from '@element-plus/icons-vue'
import StatsCards from '@/components/StatsCards.vue'
import TimeSeriesChart from '@/components/charts/TimeSeriesChart.vue'
import HeatmapChart from '@/components/charts/HeatmapChart.vue'
import PlateBoundaryChart from '@/components/charts/PlateBoundaryChart.vue'
import ScatterChart from '@/components/charts/ScatterChart.vue'
import TopRiskRegionsChart from '@/components/charts/TopRiskRegionsChart.vue'
import EarthquakeTimeline from '@/components/charts/EarthquakeTimeline.vue'
</script>

<style scoped>
.dashboard-view {
  padding: 20px;
  max-width: 1600px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.filter-bar {
  margin-bottom: 20px;
}

.filter-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #64748b;
  white-space: nowrap;
}

.range-text {
  font-size: 13px;
  color: #409eff;
  min-width: 60px;
}

.charts-grid {
  margin-bottom: 20px;
}

.charts-grid .el-col {
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .dashboard-view {
    padding: 12px;
  }
  
  .filter-controls {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-group {
    width: 100%;
  }
}
</style>
