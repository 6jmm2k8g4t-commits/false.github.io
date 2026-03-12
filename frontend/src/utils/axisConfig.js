/**
 * ECharts 坐标轴通用配置
 * 统一管理所有图表的坐标轴样式，确保一致性和专业性
 */

export const axisTheme = {
  color: {
    axisLine: '#8c9bb0',
    axisLabel: '#4a5568',
    axisTitle: '#2d3748',
    splitLine: '#e2e8f0',
    minorSplitLine: '#f1f5f9'
  },
  fontSize: {
    title: 14,
    label: 12,
    small: 11
  },
  fontWeight: {
    title: 'bold',
    label: 'normal'
  }
}

export const baseXAxis = {
  type: 'category',
  boundaryGap: false,
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
    fontWeight: axisTheme.fontWeight.label,
    margin: 12,
    interval: 'auto',
    rotate: 0,
    overflow: 'truncate',
    width: 80
  },
  splitLine: {
    show: true,
    lineStyle: {
      color: axisTheme.color.splitLine,
      type: 'dashed',
      width: 1,
      opacity: 0.6
    }
  },
  minorSplitLine: {
    show: false,
    lineStyle: {
      color: axisTheme.color.minorSplitLine,
      type: 'dotted',
      width: 0.5
    }
  }
}

export const baseYAxis = {
  type: 'value',
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
    fontWeight: axisTheme.fontWeight.label,
    margin: 12,
    formatter: null
  },
  splitLine: {
    show: true,
    lineStyle: {
      color: axisTheme.color.splitLine,
      type: 'dashed',
      width: 1,
      opacity: 0.6
    }
  },
  minorSplitLine: {
    show: false,
    lineStyle: {
      color: axisTheme.color.minorSplitLine,
      type: 'dotted',
      width: 0.5
    }
  }
}

export const createXAxis = (options = {}) => ({
  ...baseXAxis,
  ...options,
  axisLine: {
    ...baseXAxis.axisLine,
    ...(options.axisLine || {})
  },
  axisTick: {
    ...baseXAxis.axisTick,
    ...(options.axisTick || {})
  },
  axisLabel: {
    ...baseXAxis.axisLabel,
    ...(options.axisLabel || {})
  },
  splitLine: {
    ...baseXAxis.splitLine,
    ...(options.splitLine || {})
  }
})

export const createYAxis = (options = {}) => ({
  ...baseYAxis,
  ...options,
  axisLine: {
    ...baseYAxis.axisLine,
    ...(options.axisLine || {})
  },
  axisTick: {
    ...baseYAxis.axisTick,
    ...(options.axisTick || {})
  },
  axisLabel: {
    ...baseYAxis.axisLabel,
    ...(options.axisLabel || {})
  },
  splitLine: {
    ...baseYAxis.splitLine,
    ...(options.splitLine || {})
  }
})

export const createValueXAxis = (options = {}) => createXAxis({
  type: 'value',
  ...options
})

export const createValueYAxis = (options = {}) => createYAxis({
  type: 'value',
  ...options
})

export const createCategoryXAxis = (options = {}) => createXAxis({
  type: 'category',
  ...options
})

export const createCategoryYAxis = (options = {}) => createYAxis({
  type: 'category',
  ...options
})

export const createLogYAxis = (options = {}) => createYAxis({
  type: 'log',
  ...options
})

export const gridConfig = {
  standard: {
    left: '5%',
    right: '5%',
    bottom: '12%',
    top: '10%',
    containLabel: true
  },
  compact: {
    left: '3%',
    right: '3%',
    bottom: '8%',
    top: '5%',
    containLabel: true
  },
  wide: {
    left: '8%',
    right: '8%',
    bottom: '15%',
    top: '12%',
    containLabel: true
  },
  withLegend: {
    left: '5%',
    right: '5%',
    bottom: '18%',
    top: '10%',
    containLabel: true
  }
}

export const createAxisTitle = (text, options = {}) => ({
  text,
  color: axisTheme.color.axisTitle,
  fontSize: axisTheme.fontSize.title,
  fontWeight: axisTheme.fontWeight.title,
  padding: [0, 0, 8, 0],
  ...options
})

export const numberFormatter = {
  integer: (value) => Math.round(value).toLocaleString(),
  decimal1: (value) => value.toFixed(1),
  decimal2: (value) => value.toFixed(2),
  percent: (value) => (value * 100).toFixed(1) + '%',
  scientific: (value) => {
    if (Math.abs(value) >= 10000 || (Math.abs(value) < 0.01 && value !== 0)) {
      return value.toExponential(2)
    }
    return value.toFixed(2)
  },
  compact: (value) => {
    if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
    if (value >= 1000) return (value / 1000).toFixed(1) + 'K'
    return value.toFixed(0)
  }
}

export const createIntervalConfig = (min, max, splitNumber = 5) => {
  const step = (max - min) / splitNumber
  return {
    min,
    max,
    interval: step,
    splitNumber
  }
}

export const autoInterval = (data, splitNumber = 5) => {
  if (!data || data.length === 0) return { min: 0, max: 100, interval: 20 }
  
  const min = Math.min(...data)
  const max = Math.max(...data)
  const range = max - min
  const padding = range * 0.1
  
  const adjustedMin = Math.floor((min - padding) / 10) * 10
  const adjustedMax = Math.ceil((max + padding) / 10) * 10
  const interval = Math.ceil((adjustedMax - adjustedMin) / splitNumber / 10) * 10
  
  return {
    min: adjustedMin,
    max: adjustedMax,
    interval,
    splitNumber
  }
}

export default {
  axisTheme,
  baseXAxis,
  baseYAxis,
  createXAxis,
  createYAxis,
  createValueXAxis,
  createValueYAxis,
  createCategoryXAxis,
  createCategoryYAxis,
  createLogYAxis,
  gridConfig,
  createAxisTitle,
  numberFormatter,
  createIntervalConfig,
  autoInterval
}
