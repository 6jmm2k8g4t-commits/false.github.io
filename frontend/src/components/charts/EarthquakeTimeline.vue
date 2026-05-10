<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>📅 重大地震事件时间轴</h3>
      <div class="chart-controls">
        <el-select v-model="selectedYear" placeholder="选择年份" size="small" clearable @change="filterEvents">
          <el-option v-for="year in years" :key="year" :label="year + '年'" :value="year" />
        </el-select>
        <el-button size="small" @click="resetFilter">重置</el-button>
      </div>
    </div>
    <div class="timeline-content" v-loading="loading">
      <div class="timeline" v-if="filteredEvents.length > 0">
        <div 
          v-for="(event, index) in filteredEvents" 
          :key="index" 
          class="timeline-item"
          :class="{ 'major': event.magnitude >= 7 }"
        >
          <div class="timeline-marker">
            <div class="marker-dot" :style="{ backgroundColor: getMagnitudeColor(event.magnitude) }">
              <span>M{{ event.magnitude.toFixed(1) }}</span>
            </div>
            <div class="marker-line"></div>
          </div>
          <div class="timeline-content-card">
            <div class="event-time">{{ formatTime(event.time) }}</div>
            <div class="event-title">
              <el-tag :type="getMagnitudeType(event.magnitude)" effect="dark" size="small">
                M{{ event.magnitude.toFixed(1) }}
              </el-tag>
              {{ event.place }}
            </div>
            <div class="event-details">
              <span class="detail-item">
                <el-icon><Location /></el-icon>
                {{ event.latitude.toFixed(2) }}°, {{ event.longitude.toFixed(2) }}°
              </span>
              <span class="detail-item">
                <el-icon><Coin /></el-icon>
                深度: {{ event.depth.toFixed(1) }} km
              </span>
            </div>
          </div>
        </div>
      </div>
      <el-empty v-else description="暂无重大地震事件数据" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Location, Coin } from '@element-plus/icons-vue'
import axios from 'axios'

const loading = ref(false)
const selectedYear = ref(null)
const majorEvents = ref([])

const filteredEvents = computed(() => {
  if (!selectedYear.value) return majorEvents.value
  return majorEvents.value.filter(e => new Date(e.time).getFullYear() === selectedYear.value)
})

const years = computed(() => {
  const yearSet = new Set()
  majorEvents.value.forEach(e => {
    yearSet.add(new Date(e.time).getFullYear())
  })
  return Array.from(yearSet).sort((a, b) => b - a)
})

const getMagnitudeColor = (magnitude) => {
  if (magnitude >= 8) return '#f56c6c'
  if (magnitude >= 7) return '#e6a23c'
  if (magnitude >= 6) return '#409eff'
  return '#67c23a'
}

const getMagnitudeType = (magnitude) => {
  if (magnitude >= 8) return 'danger'
  if (magnitude >= 7) return 'warning'
  return 'info'
}

const formatTime = (time) => {
  const date = new Date(time)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

const filterEvents = () => {}

const resetFilter = () => {
  selectedYear.value = null
}

const loadData = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/major-earthquakes?min_magnitude=6.5&limit=20')
    if (response.data.success) {
      majorEvents.value = response.data.data
    }
  } catch (error) {
    console.error('加载重大地震事件失败:', error)
    majorEvents.value = generateMockEvents()
  }
  loading.value = false
}

const generateMockEvents = () => [
  { time: '2023-02-06T01:17:00Z', place: '土耳其-叙利亚边境', magnitude: 7.8, depth: 10, latitude: 37.23, longitude: 37.02 },
  { time: '2023-02-06T10:24:00Z', place: '土耳其卡赫拉曼马拉什', magnitude: 7.5, depth: 10, latitude: 38.02, longitude: 37.20 },
  { time: '2022-09-11T07:46:00Z', place: '巴布亚新几内亚', magnitude: 7.6, depth: 90, latitude: -3.45, longitude: 143.12 },
  { time: '2022-06-22T06:04:00Z', place: '阿富汗霍斯特省', magnitude: 6.1, depth: 10, latitude: 33.37, longitude: 69.49 },
  { time: '2021-07-29T06:15:00Z', place: '美国阿拉斯加', magnitude: 8.2, depth: 32, latitude: 55.36, longitude: -157.89 },
  { time: '2021-03-04T19:28:00Z', place: '新西兰克马德克群岛', magnitude: 8.1, depth: 28, latitude: -29.72, longitude: -177.28 },
  { time: '2020-10-30T11:51:00Z', place: '土耳其伊兹密尔', magnitude: 7.0, depth: 10, latitude: 37.91, longitude: 26.79 },
  { time: '2020-01-28T19:10:00Z', place: '古巴格拉玛省', magnitude: 7.7, depth: 10, latitude: 19.44, longitude: -78.76 },
  { time: '2019-07-06T03:19:00Z', place: '美国加利福尼亚', magnitude: 7.1, depth: 8, latitude: 35.77, longitude: -117.60 },
  { time: '2018-09-28T10:02:00Z', place: '印度尼西亚苏拉威西', magnitude: 7.5, depth: 10, latitude: -0.56, longitude: 119.85 },
  { time: '2018-08-19T21:19:00Z', place: '斐济', magnitude: 8.2, depth: 600, latitude: -18.11, longitude: -178.15 },
  { time: '2017-09-08T04:49:00Z', place: '墨西哥恰帕斯', magnitude: 8.2, depth: 47, latitude: 15.02, longitude: -93.90 },
  { time: '2017-09-07T12:53:00Z', place: '墨西哥莫雷洛斯', magnitude: 7.1, depth: 48, latitude: 18.46, longitude: -98.63 },
  { time: '2016-11-13T11:02:00Z', place: '新西兰凯库拉', magnitude: 7.8, depth: 15, latitude: -42.69, longitude: 173.02 },
  { time: '2016-04-16T23:58:00Z', place: '日本熊本', magnitude: 7.3, depth: 11, latitude: 32.79, longitude: 130.75 }
]

onMounted(loadData)
</script>

<style scoped>
.chart-container {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
}

.chart-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.chart-controls {
  display: flex;
  gap: 8px;
}

.timeline-content {
  padding: 20px;
  max-height: 450px;
  overflow-y: auto;
}

.timeline {
  position: relative;
  padding-left: 20px;
}

.timeline-item {
  display: flex;
  margin-bottom: 20px;
  position: relative;
}

.timeline-item:last-child .marker-line {
  display: none;
}

.timeline-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 16px;
}

.marker-dot {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  z-index: 1;
  transition: all 0.3s ease;
  cursor: pointer;
}

.marker-dot:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
}

.marker-line {
  width: 3px;
  flex: 1;
  background: linear-gradient(to bottom, #cbd5e1, #e2e8f0);
  margin-top: 8px;
  border-radius: 2px;
}

.timeline-content-card {
  flex: 1;
  background: #f8fafc;
  border-radius: 10px;
  padding: 14px 18px;
  border-left: 4px solid #cbd5e1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.timeline-item.major .timeline-content-card {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border-left-color: #f56c6c;
}

.timeline-content-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  transform: translateX(6px);
  border-left-width: 5px;
}

.event-time {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 6px;
}

.event-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.event-details {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: #64748b;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 6px;
  transition: all 0.2s ease;
}

.detail-item:hover {
  background: rgba(0, 0, 0, 0.06);
}

@media (max-width: 768px) {
  .timeline-content {
    padding: 12px;
  }
  
  .marker-dot {
    width: 40px;
    height: 40px;
    font-size: 10px;
  }
  
  .event-details {
    flex-direction: column;
    gap: 4px;
  }
}
</style>
