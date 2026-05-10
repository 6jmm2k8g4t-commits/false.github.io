<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>🏆 高风险区域TOP10</h3>
      <div class="chart-controls">
        <el-radio-group v-model="sortBy" size="small" @change="loadData">
          <el-radio-button label="frequency">按频次</el-radio-button>
          <el-radio-button label="magnitude">按最大震级</el-radio-button>
        </el-radio-group>
      </div>
    </div>
    <div ref="chartRef" class="chart-content" v-loading="loading"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const chartRef = ref(null)
let chart = null
const loading = ref(false)
const sortBy = ref('frequency')
const rankingData = ref([])

const axisTheme = {
  color: {
    axisLine: '#8c9bb0',
    axisLabel: '#4a5568',
    axisTitle: '#2d3748',
    splitLine: '#e2e8f0'
  },
  fontSize: {
    title: 14,
    label: 12
  }
}

const initChart = async () => {
  if (!chartRef.value) return
  
  loading.value = true
  chart = echarts.init(chartRef.value)
  
  await loadData()
  loading.value = false
  window.addEventListener('resize', handleResize)
}

const loadData = async () => {
  try {
    const response = await axios.get(`/api/high-risk-regions?sort=${sortBy.value}&limit=10`)
    if (response.data.success) {
      rankingData.value = response.data.data
      updateChart()
    }
  } catch (error) {
    console.error('加载高风险区域数据失败:', error)
    rankingData.value = generateMockData()
    updateChart()
  }
}

const generateMockData = () => {
  const regions = [
    { name: '日本', frequency: 125680, maxMagnitude: 9.1, avgMagnitude: 2.8 },
    { name: '印度尼西亚', frequency: 98540, maxMagnitude: 8.6, avgMagnitude: 2.6 },
    { name: '智利', frequency: 76230, maxMagnitude: 9.5, avgMagnitude: 2.9 },
    { name: '美国加利福尼亚', frequency: 65890, maxMagnitude: 7.9, avgMagnitude: 2.4 },
    { name: '土耳其', frequency: 54320, maxMagnitude: 7.8, avgMagnitude: 2.7 },
    { name: '中国四川', frequency: 48760, maxMagnitude: 8.0, avgMagnitude: 2.5 },
    { name: '菲律宾', frequency: 42150, maxMagnitude: 7.6, avgMagnitude: 2.4 },
    { name: '墨西哥', frequency: 38920, maxMagnitude: 8.2, avgMagnitude: 2.6 },
    { name: '新西兰', frequency: 35680, maxMagnitude: 7.8, avgMagnitude: 2.5 },
    { name: '秘鲁', frequency: 31240, maxMagnitude: 8.4, avgMagnitude: 2.7 }
  ]
  
  if (sortBy.value === 'magnitude') {
    return regions.sort((a, b) => b.maxMagnitude - a.maxMagnitude)
  }
  return regions.sort((a, b) => b.frequency - a.frequency)
}

const updateChart = () => {
  if (!chart || rankingData.value.length === 0) return
  
  const data = [...rankingData.value]
  const values = sortBy.value === 'frequency' 
    ? data.map(d => d.frequency) 
    : data.map(d => d.maxMagnitude)
  const maxValue = Math.max(...values)
  
  const sortedData = data.reverse()
  const sortedValues = values.reverse()
  
  const option = {
    animation: true,
    animationDuration: 1000,
    animationEasing: 'elasticOut',
    tooltip: {
      trigger: 'axis',
      axisPointer: { 
        type: 'shadow',
        shadowStyle: {
          color: 'rgba(150, 150, 150, 0.1)'
        }
      },
      backgroundColor: 'rgba(255, 255, 255, 0.98)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      padding: [12, 16],
      textStyle: {
        color: '#2d3748',
        fontSize: 13
      },
      extraCssText: 'box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); border-radius: 8px;',
      formatter: (params) => {
        const item = sortedData[params[0].dataIndex]
        const riskLevel = item.maxMagnitude >= 8 ? '极高风险' : item.maxMagnitude >= 7 ? '高风险' : '中风险'
        const riskColor = item.maxMagnitude >= 8 ? '#f56c6c' : item.maxMagnitude >= 7 ? '#e6a23c' : '#409eff'
        return `<div style="font-weight: bold; margin-bottom: 10px; font-size: 14px; color: #1e293b;">${item.name}</div>
          <div style="padding: 2px 0;">地震频次: <span style="font-weight: bold;">${item.frequency.toLocaleString()}</span> 次</div>
          <div style="padding: 2px 0;">最大震级: <span style="font-weight: bold; color: #f56c6c;">M${item.maxMagnitude.toFixed(1)}</span></div>
          <div style="padding: 2px 0;">平均震级: M${(item.avgMagnitude || 2.5).toFixed(2)}</div>
          <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #e2e8f0;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${riskColor}; margin-right: 6px;"></span>
            <span style="color: ${riskColor}; font-weight: 500;">${riskLevel}</span>
          </div>`
      }
    },
    grid: {
      left: '5%',
      right: '18%',
      top: '5%',
      bottom: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: sortBy.value === 'frequency' ? '地震频次 (次)' : '最大震级 (M)',
      nameLocation: 'middle',
      nameGap: 30,
      nameTextStyle: {
        color: axisTheme.color.axisTitle,
        fontSize: axisTheme.fontSize.title,
        fontWeight: 'bold',
        padding: [0, 0, 0, 0]
      },
      min: 0,
      max: sortBy.value === 'frequency' ? Math.ceil(maxValue * 1.1 / 10000) * 10000 : 10,
      interval: sortBy.value === 'frequency' ? Math.ceil(maxValue / 5 / 10000) * 10000 : 2,
      axisLine: {
        show: true,
        lineStyle: {
          color: axisTheme.color.axisLine,
          width: 1.5
        }
      },
      axisTick: {
        show: true,
        length: 5,
        lineStyle: {
          color: axisTheme.color.axisLine,
          width: 1
        }
      },
      axisLabel: {
        color: axisTheme.color.axisLabel,
        fontSize: axisTheme.fontSize.label,
        margin: 10,
        formatter: sortBy.value === 'frequency' 
          ? (val) => val >= 1000 ? (val / 1000) + 'K' : val
          : (val) => 'M' + val.toFixed(1)
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: axisTheme.color.splitLine,
          type: 'dashed',
          width: 1,
          opacity: 0.5
        }
      }
    },
    yAxis: {
      type: 'category',
      data: sortedData.map(d => d.name),
      axisLine: {
        show: true,
        lineStyle: {
          color: axisTheme.color.axisLine,
          width: 1.5
        }
      },
      axisTick: {
        show: true,
        length: 5,
        lineStyle: {
          color: axisTheme.color.axisLine,
          width: 1
        }
      },
      axisLabel: {
        color: axisTheme.color.axisLabel,
        fontSize: axisTheme.fontSize.label,
        margin: 12,
        width: 100,
        overflow: 'truncate',
        ellipsis: '...'
      },
      splitLine: {
        show: false
      }
    },
    series: [{
      type: 'bar',
      data: sortedValues.map((val, index) => ({
        value: val,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: index < 3 ? '#f56c6c' : index < 6 ? '#e6a23c' : '#67c23a' },
            { offset: 1, color: index < 3 ? '#fab6b6' : index < 6 ? '#f3d19e' : '#b3e19d' }
          ]),
          borderRadius: [0, 6, 6, 0]
        }
      })),
      barMaxWidth: 35,
      label: {
        show: true,
        position: 'right',
        color: axisTheme.color.axisLabel,
        fontSize: axisTheme.fontSize.label,
        fontWeight: 'bold',
        formatter: (params) => {
          return sortBy.value === 'frequency' 
            ? params.value.toLocaleString()
            : 'M' + params.value.toFixed(1)
        }
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 20,
          shadowColor: 'rgba(0, 0, 0, 0.25)'
        }
      }
    }]
  }
  
  chart.setOption(option, true)
}

const handleResize = () => chart?.resize()

onMounted(initChart)
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})

watch(sortBy, loadData)
</script>

<style scoped>
.chart-container {
  background: var(--card-bg, #fff);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.chart-header h3 {
  margin: 0;
  color: var(--text-primary, #1e293b);
  font-size: 18px;
}

.chart-controls {
  display: flex;
  gap: 8px;
}

.chart-content {
  height: 400px;
  width: 100%;
}
</style>
