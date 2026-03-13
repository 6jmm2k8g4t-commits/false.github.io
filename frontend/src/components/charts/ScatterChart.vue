<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>📊 震级-深度相关性分析</h3>
      <div class="chart-controls">
        <el-select v-model="depthRange" size="small" @change="updateChart" style="width: 120px;">
          <el-option label="全部深度" value="all" />
          <el-option label="浅源 (0-70km)" value="shallow" />
          <el-option label="中源 (70-300km)" value="intermediate" />
          <el-option label="深源 (>300km)" value="deep" />
        </el-select>
      </div>
    </div>
    <div ref="chartRef" class="chart-content" v-loading="loading"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const props = defineProps({
  data: Array
})

const chartRef = ref(null)
let chart = null
const loading = ref(false)
const chartData = ref([])
const depthRange = ref('all')

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

const depthConfig = {
  all: { min: 0, max: 700, title: '全部深度' },
  shallow: { min: 0, max: 70, title: '浅源地震' },
  intermediate: { min: 70, max: 300, title: '中源地震' },
  deep: { min: 300, max: 700, title: '深源地震' }
}

const initChart = async () => {
  if (!chartRef.value) return
  
  loading.value = true
  chart = echarts.init(chartRef.value)
  
  if (props.data && props.data.length > 0) {
    chartData.value = props.data
  } else {
    try {
      const response = await axios.get('/api/earthquake-distribution?limit=2000')
      if (response.data.success) {
        chartData.value = response.data.data.map(item => [
          item.magnitude,
          item.depth,
          item.magnitude
        ])
      }
    } catch (error) {
      console.error('加载散点图数据失败:', error)
    }
  }
  
  updateChart()
  loading.value = false
  window.addEventListener('resize', handleResize)
}

const updateChart = () => {
  if (!chart) return
  
  const config = depthConfig[depthRange.value]
  
  let filteredData = chartData.value
  if (depthRange.value !== 'all') {
    filteredData = chartData.value.filter(item => {
      const depth = item[1]
      if (depthRange.value === 'shallow') return depth >= 0 && depth <= 70
      if (depthRange.value === 'intermediate') return depth > 70 && depth <= 300
      if (depthRange.value === 'deep') return depth > 300
      return true
    })
  }
  
  const option = {
    animation: true,
    animationDuration: 800,
    animationEasing: 'cubicOut',
    tooltip: {
      trigger: 'item',
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
        const depthType = params.value[1] <= 70 ? '浅源地震' : params.value[1] <= 300 ? '中源地震' : '深源地震'
        const depthColor = params.value[1] <= 70 ? '#67c23a' : params.value[1] <= 300 ? '#e6a23c' : '#f56c6c'
        return `<div style="font-weight: bold; margin-bottom: 10px; font-size: 14px; color: #1e293b;">地震参数</div>
          <div style="padding: 2px 0;">震级: <span style="font-weight: bold; color: #f56c6c;">M${params.value[0].toFixed(1)}</span></div>
          <div style="padding: 2px 0;">深度: <span style="font-weight: bold;">${params.value[1].toFixed(1)} km</span></div>
          <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #e2e8f0;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${depthColor}; margin-right: 6px;"></span>
            <span style="color: ${depthColor}; font-weight: 500;">${depthType}</span>
          </div>`
      }
    },
    grid: {
      left: '10%',
      right: '12%',
      bottom: '12%',
      top: '8%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '震级 (M)',
      nameLocation: 'middle',
      nameGap: 35,
      nameTextStyle: {
        color: axisTheme.color.axisTitle,
        fontSize: axisTheme.fontSize.title,
        fontWeight: 'bold',
        padding: [0, 0, 0, 0]
      },
      min: 0,
      max: 10,
      interval: 1,
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
        formatter: 'M{value}'
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
      type: 'value',
      name: '震源深度 (km)',
      nameLocation: 'middle',
      nameGap: 50,
      nameTextStyle: {
        color: axisTheme.color.axisTitle,
        fontSize: axisTheme.fontSize.title,
        fontWeight: 'bold',
        padding: [0, 0, 0, 0]
      },
      min: config.min,
      max: config.max,
      interval: depthRange.value === 'all' ? 100 : depthRange.value === 'shallow' ? 10 : depthRange.value === 'intermediate' ? 50 : 80,
      inverse: true,
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
        formatter: '{value} km'
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
    visualMap: {
      min: 0,
      max: 10,
      dimension: 0,
      orient: 'vertical',
      right: '2%',
      top: 'center',
      text: ['高震级', '低震级'],
      textStyle: {
        color: axisTheme.color.axisLabel,
        fontSize: axisTheme.fontSize.label
      },
      calculable: true,
      itemWidth: 15,
      itemHeight: 120,
      inRange: {
        color: ['#52c41a', '#faad14', '#f5222d']
      }
    },
    series: [{
      type: 'scatter',
      data: filteredData,
      symbolSize: (val) => Math.max(6, Math.min(20, val[0] * 2.5)),
      itemStyle: {
        opacity: 0.7,
        shadowBlur: 8,
        shadowColor: 'rgba(0, 0, 0, 0.15)'
      },
      emphasis: {
        scale: 1.5,
        itemStyle: {
          opacity: 1,
          shadowBlur: 20,
          shadowColor: 'rgba(0, 0, 0, 0.4)',
          borderColor: '#fff',
          borderWidth: 2
        }
      },
      progressive: 200,
      progressiveThreshold: 500
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

watch(depthRange, updateChart)

watch(() => props.data, () => {
  if (props.data && props.data.length > 0) {
    chartData.value = props.data
    updateChart()
  }
}, { deep: true })
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
  align-items: center;
  gap: 10px;
}

.chart-content {
  height: 400px;
  width: 100%;
}
</style>
