<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>📈 地震时序趋势分析</h3>
      <div class="chart-controls">
        <el-radio-group v-model="timeGranularity" size="small" @change="handleGranularityChange">
          <el-radio-button value="yearly">年度</el-radio-button>
          <el-radio-button value="quarterly">季度</el-radio-button>
          <el-radio-button value="monthly">月度</el-radio-button>
        </el-radio-group>
      </div>
    </div>
    <div ref="chartRef" class="chart-content"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const chartRef = ref(null)
let chart = null
const timeGranularity = ref('monthly')
const rawData = ref({ categories: [], frequency: [], magnitude: [] })

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

// 时间格式化函数 - 根据当前粒度动态格式化
const formatTimeLabel = (val, granularity) => {
  if (!val) return String(val)
  
  const strVal = String(val)
  
  switch (granularity) {
    case 'yearly':
      // 处理纯数字年份或字符串年份
      if (/^\d{4}$/.test(strVal)) return `${strVal}年`
      // 处理月份格式 2020-01
      if (/^\d{4}-\d{2}$/.test(strVal)) return strVal.slice(0, 4) + '年'
      // 处理季度格式 2020Q1
      if (/^\d{4}Q\d$/.test(strVal)) return strVal.slice(0, 4) + '年'
      return strVal
      
    case 'quarterly':
      // 处理季度格式 2020Q1
      if (/^\d{4}Q(\d)$/.test(strVal)) {
        const match = strVal.match(/(\d{4})Q(\d)/)
        return `${match[1]}年第${match[2]}季度`
      }
      // 处理月份格式 2020-05 -> 转换为季度
      if (/^\d{4}-\d{2}$/.test(strVal)) {
        const year = strVal.slice(0, 4)
        const month = parseInt(strVal.slice(5))
        const quarter = Math.ceil(month / 3)
        return `${year}年第${quarter}季度`
      }
      return strVal
      
    case 'monthly':
    default:
      // 处理月份格式 2020-05
      if (/^\d{4}-\d{2}$/.test(strVal)) {
        return `${strVal.slice(0, 4)}年${parseInt(strVal.slice(5))}月`
      }
      return strVal
  }
}

const granularityConfig = computed(() => {
  const dataLength = rawData.value.categories.length
  const granularity = timeGranularity.value
  
  const configs = {
    yearly: {
      rotate: 0,
      interval: 0,
      xAxisTitle: '年份',
      barWidth: Math.min(60, Math.max(30, 800 / Math.max(dataLength, 1))),
      defaultZoomEnd: 100,
      labelFormat: (val) => formatTimeLabel(val, 'yearly')
    },
    quarterly: {
      rotate: 45,
      interval: Math.floor(dataLength / 20),
      xAxisTitle: '季度',
      barWidth: Math.min(40, Math.max(15, 800 / Math.max(dataLength, 1))),
      defaultZoomEnd: Math.min(100, Math.max(50, (36 / Math.max(dataLength, 1)) * 100)),
      labelFormat: (val) => formatTimeLabel(val, 'quarterly')
    },
    monthly: {
      rotate: 45,
      interval: Math.floor(dataLength / 15),
      xAxisTitle: '月份',
      barWidth: Math.min(20, Math.max(8, 600 / Math.max(dataLength, 1))),
      defaultZoomEnd: Math.min(100, Math.max(20, (24 / Math.max(dataLength, 1)) * 100)),
      labelFormat: (val) => formatTimeLabel(val, 'monthly')
    }
  }
  return configs[granularity]
})

const handleGranularityChange = () => {
  // 清空数据强制重新加载
  rawData.value = { categories: [], frequency: [], magnitude: [] }
  if (chart) {
    chart.clear()
  }
  loadData()
}

const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  loadData()
  
  window.addEventListener('resize', handleResize)
}

const handleResize = () => {
  chart?.resize()
}

const calculateYAxisRange = (data, padding = 0.1) => {
  if (!data || data.length === 0) return { min: 0, max: 100 }
  
  const min = Math.min(...data)
  const max = Math.max(...data)
  const range = max - min || 1
  const pad = range * padding
  
  return {
    min: Math.max(0, Math.floor((min - pad) / 100) * 100),
    max: Math.ceil((max + pad) / 100) * 100
  }
}

const loadData = async () => {
  try {
    // 添加时间戳防止缓存
    const timestamp = new Date().getTime()
    const response = await axios.get(`/api/time-series?granularity=${timeGranularity.value}&magnitude=all&_t=${timestamp}`)
    
    if (response.data.success && response.data.data) {
      let data = response.data.data
      
      // 前端补全数据到2026年当前季度
      data = completeDataTo2026(data, timeGranularity.value)
      
      rawData.value = data
      console.log('加载数据:', timeGranularity.value, rawData.value.categories.slice(0, 5), '...', rawData.value.categories.slice(-3))
      updateChart()
    }
  } catch (error) {
    console.error('加载图表数据失败:', error)
  }
}

// 补全数据到2026年当前季度
const completeDataTo2026 = (data, granularity) => {
  console.log('completeDataTo2026 输入:', granularity, data.categories.slice(-3))
  
  const categories = [...data.categories]
  const frequency = [...data.frequency]
  const magnitude = [...data.magnitude]
  const completeness = [...data.completeness]
  
  const now = new Date()
  const currentYear = now.getFullYear()
  const currentMonth = now.getMonth() + 1
  const currentQuarter = Math.ceil(currentMonth / 3)
  
  console.log('当前时间:', currentYear, '年', currentMonth, '月', 'Q', currentQuarter)
  
  // 获取最后一个数据点的时间
  const lastCategory = categories[categories.length - 1]
  console.log('最后一个数据:', lastCategory)
  
  if (granularity === 'quarterly') {
    // 解析最后一个季度 - 支持 2020Q1 或 2020-03 格式
    let match = lastCategory.match(/(\d{4})Q(\d)/)
    
    // 如果不是 Q 格式，尝试从月份格式转换
    if (!match) {
      const monthMatch = lastCategory.match(/(\d{4})-(\d{2})/)
      if (monthMatch) {
        const year = monthMatch[1]
        const month = parseInt(monthMatch[2])
        const quarter = Math.ceil(month / 3)
        match = [null, year, String(quarter)]
        console.log('从月份格式转换:', lastCategory, '->', year + 'Q' + quarter)
      }
    }
    
    if (match) {
      let lastYear = parseInt(match[1])
      let lastQuarter = parseInt(match[2])
      
      console.log('开始补全季度:', lastYear, 'Q', lastQuarter, '->', currentYear, 'Q', currentQuarter)
      
      // 生成从最后一个季度到2026年当前季度的所有季度
      let count = 0
      while (lastYear < currentYear || (lastYear === currentYear && lastQuarter < currentQuarter)) {
        lastQuarter++
        if (lastQuarter > 4) {
          lastQuarter = 1
          lastYear++
        }
        const newCategory = `${lastYear}Q${lastQuarter}`
        categories.push(newCategory)
        frequency.push(0)
        magnitude.push(0)
        // 2026年的数据标记为不完整
        completeness.push(lastYear !== currentYear)
        count++
      }
      console.log('补全了', count, '个季度, 最终:', categories.slice(-3))
    } else {
      console.log('无法解析最后一个季度格式:', lastCategory)
    }
  } else if (granularity === 'monthly') {
    // 解析最后一个月份
    const match = lastCategory.match(/(\d{4})-(\d{2})/)
    if (match) {
      let lastYear = parseInt(match[1])
      let lastMonth = parseInt(match[2])
      
      // 生成从最后一个月份到2026年当前月的所有月份
      while (lastYear < currentYear || (lastYear === currentYear && lastMonth < currentMonth)) {
        lastMonth++
        if (lastMonth > 12) {
          lastMonth = 1
          lastYear++
        }
        const newCategory = `${lastYear}-${String(lastMonth).padStart(2, '0')}`
        categories.push(newCategory)
        frequency.push(0)
        magnitude.push(0)
        // 2026年的数据标记为不完整
        completeness.push(lastYear !== currentYear)
      }
    }
  } else if (granularity === 'yearly') {
    // 解析最后一年
    const lastYear = parseInt(lastCategory)
    
    // 生成从最后一年到2026年的所有年份
    for (let y = lastYear + 1; y <= currentYear; y++) {
      categories.push(String(y))
      frequency.push(0)
      magnitude.push(0)
      // 2026年标记为不完整
      completeness.push(y !== currentYear)
    }
  }
  
  return {
    categories,
    frequency,
    magnitude,
    completeness
  }
}

const updateChart = () => {
  if (!chart || !rawData.value.categories.length) return
  
  const data = rawData.value
  const config = granularityConfig.value
  const granularity = timeGranularity.value
  const dataLength = data.categories.length
  
  const freqRange = calculateYAxisRange(data.frequency, 0.15)
  
  // 根据粒度调整显示参数
  const isYearly = granularity === 'yearly'
  const isQuarterly = granularity === 'quarterly'
  const isMonthly = granularity === 'monthly'
  
  const option = {
    animation: true,
    animationDuration: 800,
    animationEasing: 'cubicOut',
    tooltip: {
      trigger: 'axis',
      axisPointer: { 
        type: 'cross',
        crossStyle: {
          color: '#999'
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
        // 使用当前选择的时间粒度来格式化时间
        const timeValue = params[0].axisValue
        const formattedTime = formatTimeLabel(timeValue, granularity)
        
        let result = `<div style="font-weight: bold; margin-bottom: 10px; font-size: 14px; color: #1e293b;">${formattedTime}</div>`
        params.forEach(param => {
          const value = param.seriesName === '地震频次' 
            ? param.value.toLocaleString() + ' 次'
            : 'M' + param.value.toFixed(2)
          result += `<div style="display: flex; justify-content: space-between; gap: 20px; padding: 4px 0;">
            <span>${param.marker} ${param.seriesName}</span>
            <span style="font-weight: bold;">${value}</span>
          </div>`
        })
        return result
      }
    },
    legend: {
      data: ['地震频次', '平均震级'],
      bottom: 0,
      itemWidth: 20,
      itemHeight: 12,
      textStyle: {
        color: axisTheme.color.axisLabel,
        fontSize: axisTheme.fontSize.label
      }
    },
    grid: {
      left: '5%',
      right: '5%',
      bottom: isMonthly ? '18%' : '12%',
      top: '12%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: true,
      data: data.categories,
      name: config.xAxisTitle,
      nameLocation: 'middle',
      nameGap: 35,
      nameTextStyle: {
        color: axisTheme.color.axisTitle,
        fontSize: axisTheme.fontSize.title,
        fontWeight: 'bold',
        padding: [0, 0, 0, 0]
      },
      axisLine: {
        show: true,
        lineStyle: {
          color: axisTheme.color.axisLine,
          width: 1.5
        }
      },
      axisTick: {
        show: true,
        alignWithLabel: true,
        lineStyle: {
          color: axisTheme.color.axisLine,
          width: 1
        }
      },
      axisLabel: {
        color: axisTheme.color.axisLabel,
        fontSize: axisTheme.fontSize.label,
        rotate: config.rotate,
        interval: config.interval,
        margin: 12,
        overflow: 'truncate',
        width: isYearly ? 60 : 80,
        formatter: (val) => formatTimeLabel(val, granularity)
      },
      splitLine: {
        show: false
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '地震频次 (次)',
        nameLocation: 'middle',
        nameGap: 50,
        nameTextStyle: {
          color: axisTheme.color.axisTitle,
          fontSize: axisTheme.fontSize.title,
          fontWeight: 'bold',
          padding: [0, 0, 0, 0]
        },
        min: freqRange.min,
        max: freqRange.max,
        interval: Math.ceil((freqRange.max - freqRange.min) / 5),
        axisLine: {
          show: true,
          lineStyle: {
            color: axisTheme.color.axisLine,
            width: 1.5
          }
        },
        axisTick: {
          show: true,
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
            if (value >= 1000) return (value / 1000).toFixed(1) + 'K'
            return value
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
      {
        type: 'value',
        name: '平均震级 (M)',
        nameLocation: 'middle',
        nameGap: 45,
        nameTextStyle: {
          color: axisTheme.color.axisTitle,
          fontSize: axisTheme.fontSize.title,
          fontWeight: 'bold',
          padding: [0, 0, 0, 0]
        },
        min: 0,
        max: 10,
        interval: 2,
        axisLine: {
          show: true,
          lineStyle: {
            color: axisTheme.color.axisLine,
            width: 1.5
          }
        },
        axisTick: {
          show: true,
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
          show: false
        }
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
        zoomOnMouseWheel: true,
        moveOnMouseMove: true
      },
      {
        type: 'slider',
        show: true,
        height: 20,
        bottom: 50,
        start: 0,
        end: 100,
        borderColor: 'transparent',
        backgroundColor: '#f1f5f9',
        fillerColor: 'rgba(102, 126, 234, 0.2)',
        handleStyle: {
          color: '#667eea',
          borderColor: '#667eea'
        },
        textStyle: {
          color: '#64748b',
          fontSize: 11
        },
        labelFormatter: (value) => {
          const idx = Math.floor(value / 100 * (dataLength - 1))
          const category = data.categories[Math.min(idx, dataLength - 1)]
          return formatTimeLabel(category, granularity)
        }
      }
    ],
    series: [
      {
        name: '地震频次',
        type: 'bar',
        data: data.frequency,
        barWidth: config.barWidth,
        barMaxWidth: isYearly ? 60 : isQuarterly ? 40 : 20,
        barMinWidth: isYearly ? 30 : isQuarterly ? 15 : 5,
        barGap: isYearly ? '20%' : '10%',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#667eea' },
            { offset: 0.5, color: '#764ba2' },
            { offset: 1, color: '#8b5cf6' }
          ]),
          borderRadius: isYearly ? [8, 8, 0, 0] : [4, 4, 0, 0]
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#764ba2' },
              { offset: 1, color: '#667eea' }
            ]),
            shadowBlur: 10,
            shadowColor: 'rgba(102, 126, 234, 0.5)'
          }
        }
      },
      {
        name: '平均震级',
        type: 'line',
        yAxisIndex: 1,
        data: data.magnitude,
        smooth: true,
        symbol: isYearly ? 'circle' : isQuarterly ? 'circle' : 'none',
        symbolSize: isYearly ? 12 : isQuarterly ? 8 : 4,
        showAllSymbol: isYearly || isQuarterly,
        itemStyle: {
          color: '#f5576c',
          borderColor: '#fff',
          borderWidth: 2
        },
        lineStyle: {
          width: isYearly ? 4 : isQuarterly ? 3 : 2,
          shadowColor: 'rgba(245, 87, 108, 0.3)',
          shadowBlur: 10,
          shadowOffsetY: 5
        },
        areaStyle: isYearly ? {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(245, 87, 108, 0.3)' },
            { offset: 1, color: 'rgba(245, 87, 108, 0.05)' }
          ])
        } : null,
        emphasis: {
          scale: 1.5,
          itemStyle: {
            shadowBlur: 15,
            shadowColor: 'rgba(245, 87, 108, 0.6)'
          }
        }
      }
    ]
  }
  
  chart.setOption(option, true)
}

onMounted(() => {
  initChart()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
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
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.chart-content {
  height: 400px;
  width: 100%;
}
</style>
