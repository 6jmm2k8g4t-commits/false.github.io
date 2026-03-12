<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>🌍 板块边界与地震分布</h3>
      <div class="chart-controls">
        <el-select v-model="selectedPlate" size="small" @change="updateChart" style="width: 150px;">
          <el-option label="全部板块" value="all" />
          <el-option label="太平洋板块" value="pacific" />
          <el-option label="欧亚板块" value="eurasian" />
          <el-option label="非洲板块" value="african" />
          <el-option label="美洲板块" value="american" />
          <el-option label="印澳板块" value="indoaustralian" />
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
const selectedPlate = ref('all')

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

const plateBoundaries = {
  pacific: [
    [[-180, 65], [-170, 60], [-160, 55], [-150, 50], [-140, 45], [-130, 40], [-125, 35], [-120, 30], [-115, 25], [-110, 20], [-105, 15], [-100, 10], [-85, 5], [-80, 0], [-75, -5], [-70, -15], [-75, -25], [-80, -35], [-75, -45], [-70, -55], [-65, -60], [-60, -65], [-55, -70], [-70, -75], [-85, -70], [-100, -65], [-115, -60], [-130, -55], [-145, -50], [-160, -45], [-175, -40], [-170, -35], [-165, -30], [-160, -25], [-155, -20], [-150, -15], [-145, -10], [-140, -5], [-135, 0], [-130, 5], [-125, 10], [-120, 15], [-115, 20], [-110, 25], [-105, 30], [-100, 35], [-95, 40], [-90, 45], [-85, 50], [-80, 55], [-75, 60], [-70, 65], [-180, 65]]
  ],
  eurasian: [
    [[-10, 35], [0, 40], [10, 45], [20, 50], [30, 55], [40, 60], [50, 65], [60, 70], [70, 75], [80, 75], [90, 70], [100, 65], [110, 60], [120, 55], [130, 50], [140, 45], [150, 45], [160, 50], [170, 55], [180, 60]]
  ],
  african: [
    [[-20, 35], [-10, 30], [0, 25], [10, 20], [20, 15], [30, 10], [40, 5], [50, 0], [40, -5], [30, -10], [20, -15], [10, -20], [0, -25], [-10, -30], [-20, -35], [-15, -30], [-10, -25], [-5, -20], [0, -15], [5, -10], [10, -5], [15, 0], [20, 5], [25, 10], [30, 15], [35, 20], [30, 25], [25, 30], [20, 35], [-20, 35]]
  ],
  american: [
    [[-170, 65], [-160, 60], [-150, 55], [-140, 50], [-130, 45], [-120, 40], [-110, 35], [-100, 30], [-90, 25], [-80, 20], [-70, 15], [-60, 10], [-50, 5], [-40, 0], [-35, -5], [-30, -10], [-35, -15], [-40, -20], [-45, -25], [-50, -30], [-55, -35], [-60, -40], [-65, -45], [-70, -50], [-75, -55], [-70, -60], [-65, -65], [-60, -70], [-55, -75], [-60, -80], [-70, -75], [-80, -70], [-90, -65], [-100, -60], [-110, -55], [-120, -50], [-130, -45], [-140, -40], [-150, -35], [-160, -30], [-170, -25], [-180, -20]]
  ],
  indoaustralian: [
    [[70, -10], [80, -5], [90, 0], [100, 5], [110, 10], [120, 15], [130, 20], [140, 25], [150, 30], [160, 35], [170, 40], [180, 45], [170, 50], [160, 55], [150, 60], [140, 65], [130, 70], [120, 75], [110, 80], [100, 75], [90, 70], [80, 65], [70, 60], [60, 55], [50, 50], [40, 45], [30, 40], [20, 35], [30, 30], [40, 25], [50, 20], [60, 15], [70, 10], [70, -10]]
  ]
}

const initChart = async () => {
  if (!chartRef.value) return
  
  loading.value = true
  chart = echarts.init(chartRef.value)
  
  if (props.data && props.data.length > 0) {
    chartData.value = props.data
  } else {
    try {
      const response = await axios.get('/api/earthquake-distribution?limit=1000')
      if (response.data.success) {
        chartData.value = response.data.data
      }
    } catch (error) {
      console.error('加载板块图数据失败:', error)
    }
  }
  
  updateChart()
  loading.value = false
  window.addEventListener('resize', handleResize)
}

const updateChart = () => {
  if (!chart) return
  
  let filteredData = chartData.value
  if (selectedPlate.value !== 'all' && plateBoundaries[selectedPlate.value]) {
    filteredData = chartData.value.filter(() => {
      return true
    })
  }
  
  const scatterData = filteredData.map(item => [
    item.longitude,
    item.latitude,
    item.magnitude
  ])
  
  const series = [
    {
      name: '地震分布',
      type: 'scatter',
      coordinateSystem: 'cartesian2d',
      data: scatterData,
      symbolSize: (val) => Math.max(4, Math.min(15, val[2] * 2)),
      itemStyle: {
        color: new echarts.graphic.RadialGradient(0.5, 0.5, 0.5, [
          { offset: 0, color: '#ff6b6b' },
          { offset: 1, color: '#c92a2a' }
        ]),
        opacity: 0.75,
        shadowBlur: 6,
        shadowColor: 'rgba(201, 42, 42, 0.3)'
      },
      emphasis: {
        scale: 1.5,
        itemStyle: {
          opacity: 1,
          shadowBlur: 15,
          shadowColor: 'rgba(201, 42, 42, 0.6)'
        }
      },
      progressive: 200,
      progressiveThreshold: 500
    }
  ]
  
  if (selectedPlate.value === 'all') {
    Object.keys(plateBoundaries).forEach((plateName, index) => {
      const colors = ['#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#dfe6e9']
      plateBoundaries[plateName].forEach(boundary => {
        series.push({
          name: plateName + '边界',
          type: 'line',
          data: boundary,
          lineStyle: {
            color: colors[index % colors.length],
            width: 2,
            type: 'solid'
          },
          symbol: 'none',
          silent: true
        })
      })
    })
  } else if (plateBoundaries[selectedPlate.value]) {
    plateBoundaries[selectedPlate.value].forEach(boundary => {
      series.push({
        name: '板块边界',
        type: 'line',
        data: boundary,
        lineStyle: {
          color: '#4ecdc4',
          width: 3,
          type: 'solid'
        },
        symbol: 'none',
        silent: true
      })
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
        if (params.seriesType === 'scatter') {
          const lon = params.value[0]
          const lat = params.value[1]
          const mag = params.value[2]
          const lonDir = lon >= 0 ? '东经' : '西经'
          const latDir = lat >= 0 ? '北纬' : '南纬'
          return `<div style="font-weight: bold; margin-bottom: 10px; font-size: 14px; color: #1e293b;">地震信息</div>
            <div style="padding: 2px 0;">${lonDir}: <span style="font-weight: bold;">${Math.abs(lon).toFixed(2)}°</span></div>
            <div style="padding: 2px 0;">${latDir}: <span style="font-weight: bold;">${Math.abs(lat).toFixed(2)}°</span></div>
            <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #e2e8f0;">
              震级: <span style="font-weight: bold; color: #f56c6c;">M${mag.toFixed(1)}</span>
            </div>`
        }
        return null
      }
    },
    legend: {
      data: selectedPlate.value === 'all' 
        ? ['地震分布', '太平洋板块', '欧亚板块', '非洲板块', '美洲板块', '印澳板块']
        : ['地震分布', '板块边界'],
      bottom: 0,
      itemWidth: 20,
      itemHeight: 12,
      textStyle: {
        color: axisTheme.color.axisLabel,
        fontSize: axisTheme.fontSize.label
      }
    },
    grid: {
      left: '8%',
      right: '5%',
      bottom: '18%',
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
    series: series
  }
  
  chart.setOption(option, true)
}

const handleResize = () => chart?.resize()

onMounted(initChart)
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})

watch(selectedPlate, updateChart)

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
