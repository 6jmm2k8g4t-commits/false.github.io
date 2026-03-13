<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>🔥 全球地震风险热力图</h3>
      <div class="chart-controls">
        <el-select v-model="selectedMode" size="small" @change="updateChart" style="width: 120px;">
          <el-option label="原始分布" value="raw" />
          <el-option label="核密度估计" value="kde" />
        </el-select>
        <el-slider 
          v-if="selectedMode === 'kde'" 
          v-model="bandwidth" 
          :min="0.5" 
          :max="5" 
          :step="0.5" 
          :show-tooltip="true"
          :format-tooltip="(val) => `带宽: ${val}`"
          style="width: 120px; margin-left: 10px;"
        />
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
const selectedMode = ref('raw')
const bandwidth = ref(2.0)

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
  
  if (props.data && props.data.length > 0) {
    chartData.value = props.data
  } else {
    try {
      const response = await axios.get('/api/earthquake-distribution?limit=2000')
      if (response.data.success) {
        chartData.value = response.data.data
      }
    } catch (error) {
      console.error('加载热力图数据失败:', error)
    }
  }
  
  updateChart()
  loading.value = false
  window.addEventListener('resize', handleResize)
}

const updateChart = async () => {
  if (!chart) return
  
  let data = []
  
  let maxDataValue = 8 // 默认值
  
  if (selectedMode.value === 'kde') {
    try {
      const response = await axios.get(`/api/kernel-density?bandwidth=${bandwidth.value}&grid_size=60`)
      if (response.data.success) {
        // 过滤掉低密度的点，只显示高密度区域
        const heatmapData = response.data.data.heatmap
        const maxDensity = Math.max(...heatmapData.map(item => item.density))
        maxDataValue = maxDensity
        const threshold = maxDensity * 0.1 // 只显示密度值大于最大密度10%的点
        data = heatmapData
          .filter(item => item.density > threshold)
          .map(item => ({
            value: [item.longitude, item.latitude, item.density]
          }))
      }
    } catch (error) {
      console.error('加载核密度数据失败:', error)
      data = chartData.value.map(item => ({
        value: [item.longitude, item.latitude, item.magnitude]
      }))
    }
  } else {
    data = chartData.value.map(item => ({
      value: [item.longitude, item.latitude, item.magnitude]
    }))
  }
  
  const option = {
    animation: true,
    animationDuration: 1000,
    animationEasing: 'elasticOut',
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
        const lon = params.value[0]
        const lat = params.value[1]
        const value = params.value[2]
        const lonDir = lon >= 0 ? '东经' : '西经'
        const latDir = lat >= 0 ? '北纬' : '南纬'
        return `<div style="font-weight: bold; margin-bottom: 10px; font-size: 14px; color: #1e293b;">位置信息</div>
          <div style="padding: 2px 0;">${lonDir}: ${Math.abs(lon)}°</div>
          <div style="padding: 2px 0;">${latDir}: ${Math.abs(lat)}°</div>
          <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #e2e8f0;">
            <span style="color: #64748b;">${selectedMode.value === 'kde' ? '密度值' : '震级'}:</span>
            <span style="font-weight: bold; color: #f56c6c;"> ${value.toFixed(2)}</span>
          </div>`
      }
    },
    grid: {
      left: '8%',
      right: '8%',
      bottom: '15%',
      top: '8%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '经度 (°)',
      nameLocation: 'middle',
      nameGap: 35,
      nameTextStyle: {
        color: axisTheme.color.axisTitle,
        fontSize: axisTheme.fontSize.title,
        fontWeight: 'bold',
        padding: [0, 0, 0, 0]
      },
      min: -180,
      max: 180,
      interval: 60,
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
        formatter: (value) => {
          const dir = value >= 0 ? 'E' : 'W'
          return `${Math.abs(value)}°${dir}`
        }
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
      name: '纬度 (°)',
      nameLocation: 'middle',
      nameGap: 45,
      nameTextStyle: {
        color: axisTheme.color.axisTitle,
        fontSize: axisTheme.fontSize.title,
        fontWeight: 'bold',
        padding: [0, 0, 0, 0]
      },
      min: -90,
      max: 90,
      interval: 30,
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
        formatter: (value) => {
          const dir = value >= 0 ? 'N' : 'S'
          return `${Math.abs(value)}°${dir}`
        }
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
      max: maxDataValue,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '2%',
      itemWidth: 20,
      itemHeight: 140,
      text: ['高风险', '低风险'],
      textStyle: {
        color: axisTheme.color.axisLabel,
        fontSize: axisTheme.fontSize.label
      },
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', 
                '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      },
      formatter: (value) => {
        if (typeof value === 'number') {
          return value.toFixed(1)
        }
        return value
      }
    },
    series: [{
      type: 'scatter',
      data: data,
      symbolSize: (val) => Math.max(4, Math.min(20, val[2] * 2)),
      itemStyle: {
        color: (params) => {
          const value = params.value[2]
          const ratio = value / maxDataValue
          // 根据值返回颜色
          const colors = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', 
                          '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
          const index = Math.min(Math.floor(ratio * colors.length), colors.length - 1)
          return colors[index]
        },
        opacity: 0.7,
        shadowBlur: 5,
        shadowColor: 'rgba(0, 0, 0, 0.2)'
      },
      emphasis: {
        itemStyle: {
          opacity: 1,
          shadowBlur: 15,
          shadowColor: 'rgba(0, 0, 0, 0.4)',
          borderColor: '#fff',
          borderWidth: 2
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

watch([selectedMode, bandwidth], updateChart)

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
  flex-wrap: wrap;
  gap: 10px;
}

.chart-content {
  height: 400px;
  width: 100%;
}
</style>
