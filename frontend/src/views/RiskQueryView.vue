<template>
  <div class="risk-query-view">
    <div class="page-header">
      <h1 class="page-title">
        <el-icon size="32" color="#f56c6c"><Search /></el-icon>
        风险查询
      </h1>
      <p class="page-subtitle">精准定位地震风险，智能分析地震数据</p>
      <p class="quick-tips">
        <el-icon><InfoFilled /></el-icon>
        选择查询条件后点击"查询"按钮获取数据，支持数据导出功能
      </p>
    </div>
    
    <el-row :gutter="20" class="query-section">
      <el-col :xs="24" :lg="8">
        <el-card class="query-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="header-icon">🎯</span>
              <span class="header-title">查询条件</span>
              <el-button type="primary" @click="handleQuery" :loading="loading" class="query-btn">
                <el-icon><Search /></el-icon> 查询
              </el-button>
            </div>
          </template>
          
          <el-form :model="queryForm" label-position="top" class="query-form">
            <el-form-item label="震级范围" class="form-item-compact">
              <div class="magnitude-buttons">
                <el-radio-group v-model="magnitudePreset" @change="handleMagnitudePresetChange" class="magnitude-radio-group">
                  <el-radio-button label="全部" value="all" />
                  <el-radio-button label="微震 (0-3级)" value="micro" />
                  <el-radio-button label="小震 (3-5级)" value="small" />
                  <el-radio-button label="中震 (5-7级)" value="medium" />
                  <el-radio-button label="大震 (7级+)" value="large" />
                </el-radio-group>
                <div class="range-display">
                  <el-tag :type="getMagnitudeTagType(queryForm.magnitudeRange[0], queryForm.magnitudeRange[1])" size="small">
                    {{ queryForm.magnitudeRange[0].toFixed(1) }} - {{ queryForm.magnitudeRange[1].toFixed(1) }} 级
                  </el-tag>
                </div>
              </div>
            </el-form-item>
            
            <el-form-item label="时间范围" class="form-item-compact">
              <el-date-picker
                v-model="queryForm.dateRange"
                type="datetimerange"
                range-separator="至"
                start-placeholder="开始时间"
                end-placeholder="结束时间"
                style="width: 100%"
                :shortcuts="dateShortcuts"
                value-format="YYYY-MM-DD HH:mm"
              />
            </el-form-item>
            
            <el-form-item label="风险等级" class="form-item-compact">
              <el-radio-group v-model="queryForm.riskLevel" class="risk-radio-group">
                <el-radio-button label="全部" value="" />
                <el-radio-button label="低风险" value="low" />
                <el-radio-button label="中风险" value="medium" />
                <el-radio-button label="高风险" value="high" />
              </el-radio-group>
            </el-form-item>
            
            <div class="quick-actions">
              <el-button @click="resetQuery" size="small">
                <el-icon><RefreshRight /></el-icon> 重置
              </el-button>
              <el-button type="success" @click="exportData" :disabled="stats.total === 0" size="small">
                <el-icon><Download /></el-icon> 导出CSV
              </el-button>
            </div>
          </el-form>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :lg="16">
        <div class="result-section" v-if="queryResult.data.length > 0 || loading">
          <el-row :gutter="16" class="stats-row">
            <el-col :xs="12" :sm="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #67c23a, #85ce61);">
                  <el-icon size="24"><DataLine /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ formatNumber(stats.total) }}</div>
                  <div class="stat-label">总记录数</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #e6a23c, #f5d0a0);">
                  <el-icon size="24"><TrendCharts /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ stats.avgMagnitude }}</div>
                  <div class="stat-label">平均震级</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #f56c6c, #fab6b6);">
                  <el-icon size="24"><WarningFilled /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ stats.maxMagnitude }}</div>
                  <div class="stat-label">最大震级</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #409eff, #a0cfff);">
                  <el-icon size="24"><Location /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ stats.avgDepth }} km</div>
                  <div class="stat-label">平均深度</div>
                </div>
              </div>
            </el-col>
          </el-row>
          
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span class="header-icon">📊</span>
                <span class="header-title">震级分布</span>
              </div>
            </template>
            <div ref="chartRef" class="chart-container" v-loading="loading"></div>
          </el-card>
          
          <el-card class="data-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span class="header-icon">📋</span>
                <span class="header-title">详细数据</span>
                <el-tag type="info" size="small">共 {{ formatNumber(queryResult.total) }} 条记录</el-tag>
              </div>
            </template>
            
            <el-table 
              :data="queryResult.data" 
              stripe 
              style="width: 100%"
              :max-height="400"
              v-loading="loading"
              element-loading-text="加载中..."
            >
              <el-table-column type="index" width="50" label="#" />
              <el-table-column prop="time" label="时间" width="160" sortable>
                <template #default="scope">
                  <el-icon><Clock /></el-icon>
                  {{ scope.row.time }}
                </template>
              </el-table-column>
              <el-table-column prop="place" label="位置" min-width="180" show-overflow-tooltip>
                <template #default="scope">
                  <el-icon><Location /></el-icon>
                  {{ scope.row.place }}
                </template>
              </el-table-column>
              <el-table-column prop="magnitude" label="震级" width="100" sortable>
                <template #default="scope">
                  <el-tag 
                    :type="getMagnitudeType(scope.row.magnitude)" 
                    effect="dark" 
                    size="small"
                  >
                    M{{ scope.row.magnitude.toFixed(1) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="depth" label="深度(km)" width="100" sortable>
                <template #default="scope">
                  {{ scope.row.depth.toFixed(1) }}
                </template>
              </el-table-column>
              <el-table-column prop="latitude" label="纬度" width="100">
                <template #default="scope">
                  {{ scope.row.latitude.toFixed(2) }}°
                </template>
              </el-table-column>
              <el-table-column prop="longitude" label="经度" width="100">
                <template #default="scope">
                  {{ scope.row.longitude.toFixed(2) }}°
                </template>
              </el-table-column>
            </el-table>
            
            <div class="pagination-wrapper">
              <el-pagination
                v-model:current-page="queryForm.page"
                v-model:page-size="queryForm.pageSize"
                :page-sizes="[20, 50, 100, 200]"
                :total="queryResult.total"
                layout="total, sizes, prev, pager, next, jumper"
                :background="true"
                @size-change="handlePageChange"
                @current-change="handlePageChange"
              />
            </div>
          </el-card>
        </div>
        
        <el-empty v-else description="暂无数据，请设置查询条件后点击查询按钮" :image-size="120">
          <template #description>
            <div class="empty-tips">
              <p>💡 提示：选择查询条件后点击"查询"按钮获取数据</p>
              <p>支持按震级、时间范围筛选地震数据</p>
            </div>
          </template>
        </el-empty>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, watch } from 'vue'
import { Search, Download, RefreshRight, InfoFilled, DataLine, TrendCharts, WarningFilled, Location, Clock } from '@element-plus/icons-vue'
import axios from 'axios'
import * as echarts from 'echarts'

const queryForm = reactive({
  magnitudeRange: [0, 10],
  dateRange: [],
  riskLevel: '',
  page: 1,
  pageSize: 50
})

const queryResult = reactive({
  data: [],
  total: 0
})

const stats = reactive({
  total: 0,
  avgMagnitude: 0,
  maxMagnitude: 0,
  avgDepth: 0,
  magnitudeDistribution: { micro: 0, small: 0, medium: 0, large: 0 }
})

const loading = ref(false)
const chartRef = ref(null)
let chartInstance = null

const magnitudePreset = ref('all')

const magnitudePresets = {
  all: [0, 10],
  micro: [0, 3],
  small: [3, 5],
  medium: [5, 7],
  large: [7, 10]
}

const handleMagnitudePresetChange = (value) => {
  if (value !== 'custom' && magnitudePresets[value]) {
    queryForm.magnitudeRange = [...magnitudePresets[value]]
  }
}

const getMagnitudeTagType = (min, max) => {
  if (max >= 7) return 'danger'
  if (min >= 5) return 'warning'
  if (min >= 3) return 'info'
  return 'success'
}

const dateShortcuts = [
  { text: '最近一周', value: () => { const end = new Date(); const start = new Date(); start.setTime(start.getTime() - 3600 * 1000 * 24 * 7); return [start, end] } },
  { text: '最近一月', value: () => { const end = new Date(); const start = new Date(); start.setTime(start.getTime() - 3600 * 1000 * 24 * 30); return [start, end] } },
  { text: '最近三月', value: () => { const end = new Date(); const start = new Date(); start.setTime(start.getTime() - 3600 * 1000 * 24 * 90); return [start, end] } }
]

const getMagnitudeType = (magnitude) => {
  if (magnitude >= 7) return 'danger'
  if (magnitude >= 5) return 'warning'
  return 'success'
}

const formatNumber = (num) => {
  if (num >= 1000000) return (num / 1000000).toFixed(2) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
  return num.toString()
}

const buildQueryParams = () => {
  const params = {
    page: queryForm.page,
    page_size: queryForm.pageSize,
    sort: 'time'
  }
  
  if (queryForm.riskLevel) {
    const riskRanges = {
      low: { min: 0, max: 4 },
      medium: { min: 4, max: 6 },
      high: { min: 6, max: 10 }
    }
    const range = riskRanges[queryForm.riskLevel]
    if (range) {
      params.min_magnitude = range.min
      params.max_magnitude = range.max
    }
  } else {
    if (queryForm.magnitudeRange[0] > 0) {
      params.min_magnitude = queryForm.magnitudeRange[0]
    }
    if (queryForm.magnitudeRange[1] < 10) {
      params.max_magnitude = queryForm.magnitudeRange[1]
    }
  }
  
  if (queryForm.dateRange && queryForm.dateRange.length === 2) {
    const startDate = queryForm.dateRange[0] instanceof Date ? queryForm.dateRange[0] : new Date(queryForm.dateRange[0])
    const endDate = queryForm.dateRange[1] instanceof Date ? queryForm.dateRange[1] : new Date(queryForm.dateRange[1])
    params.start_time = startDate.toISOString()
    params.end_time = endDate.toISOString()
  }
  
  return params
}

const fetchStats = async () => {
  try {
    const params = buildQueryParams()
    delete params.page
    delete params.page_size
    
    const response = await axios.get('/api/list-data-stats', { params })
    if (response.data.success) {
      const data = response.data.stats
      stats.total = data.total
      stats.avgMagnitude = data.avg_magnitude
      stats.maxMagnitude = data.max_magnitude
      stats.avgDepth = data.avg_depth
      stats.magnitudeDistribution = data.magnitude_distribution
    }
  } catch (error) {
    console.error('获取统计失败:', error)
  }
}

const handleQuery = async () => {
  loading.value = true
  try {
    const params = buildQueryParams()
    const response = await axios.get('/api/list-data', { params })
    
    if (response.data.success) {
      queryResult.data = response.data.data
      queryResult.total = response.data.total
      
      await fetchStats()
      
      nextTick(() => {
        updateChart()
      })
    }
  } catch (error) {
    console.error('查询失败:', error)
    queryResult.data = []
    queryResult.total = 0
  } finally {
    loading.value = false
  }
}

const handlePageChange = () => {
  handleQuery()
}

const updateChart = () => {
  if (!chartRef.value) return
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartRef.value)
  
  const magDist = stats.magnitudeDistribution
  const chartData = [
    { value: magDist.micro, name: '0-3级', itemStyle: { color: '#67c23a' } },
    { value: magDist.small, name: '3-5级', itemStyle: { color: '#e6a23c' } },
    { value: magDist.medium, name: '5-7级', itemStyle: { color: '#f56c6c' } },
    { value: magDist.large, name: '7级+', itemStyle: { color: '#f56c6c' } }
  ]
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} 次 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'middle'
    },
    series: [
      {
        name: '震级分布',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {c}次'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: chartData
      }
    ]
  }
  
  chartInstance.setOption(option)
}

const resetQuery = () => {
  queryForm.magnitudeRange = [0, 10]
  queryForm.dateRange = []
  queryForm.riskLevel = ''
  queryForm.page = 1
  magnitudePreset.value = 'all'
  handleQuery()
}

const exportData = async () => {
  try {
    const params = buildQueryParams()
    params.page = 1
    params.page_size = 100000
    
    const response = await axios.get('/api/list-data', { params })
    
    if (response.data.success) {
      const data = response.data.data
      const headers = ['时间', '位置', '震级', '深度(km)', '纬度', '经度']
      const rows = data.map(item => [
        item.time,
        item.place,
        item.magnitude,
        item.depth,
        item.latitude,
        item.longitude
      ])
      
      let csv = '\ufeff' + headers.join(',') + '\n'
      rows.forEach(row => {
        csv += row.map(cell => `"${cell}"`).join(',') + '\n'
      })
      
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `地震查询结果_${new Date().toISOString().slice(0, 10)}.csv`
      link.click()
    }
  } catch (error) {
    console.error('导出失败:', error)
  }
}

onMounted(() => {
  handleQuery()
})

watch(() => stats.magnitudeDistribution, () => {
  nextTick(() => {
    updateChart()
  })
}, { deep: true })
</script>

<style scoped>
.risk-query-view {
  padding: 20px;
  max-width: 1600px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
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
  margin: 0 0 8px 0;
}

.quick-tips {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #fff7ed, #fef3cd);
  border-radius: 8px;
  font-size: 13px;
  color: #856404;
}

.query-section {
  margin-bottom: 20px;
}

.query-card {
  height: 100%;
}

.magnitude-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.magnitude-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.magnitude-radio-group :deep(.el-radio-button) {
  flex: 1;
  min-width: 80px;
}

.magnitude-radio-group :deep(.el-radio-button__inner) {
  width: 100%;
  padding: 8px 12px;
  font-size: 12px;
}

.range-display {
  text-align: center;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 20px;
}

.header-title {
  font-weight: 600;
  font-size: 16px;
  flex: 1;
}

.query-btn {
  min-width: 100px;
}

.query-form {
  padding: 10px 0;
}

.form-item-compact {
  margin-bottom: 16px;
}

.risk-radio-group {
  width: 100%;
}

.risk-radio-group :deep(.el-radio-button) {
  flex: 1;
}

.quick-actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-container {
  height: 300px;
}

.data-card {
  margin-bottom: 20px;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.empty-tips {
  text-align: center;
  color: #909399;
  line-height: 1.8;
}

.empty-tips p {
  margin: 4px 0;
}

@media (max-width: 1200px) {
  .risk-query-view {
    padding: 15px;
  }
  
  .stat-card {
    padding: 12px;
  }
  
  .stat-value {
    font-size: 20px;
  }
  
  .chart-container {
    height: 250px;
  }
}
</style>
