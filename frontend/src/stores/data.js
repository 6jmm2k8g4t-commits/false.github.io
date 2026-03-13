import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useDataStore = defineStore('data', () => {
  // 状态
  const stats = ref({
    total_count: 0,
    max_magnitude: 0,
    avg_depth: 0,
    high_risk_areas: 0
  })
  const timeSeriesData = ref(null)
  const globeData = ref(null)
  const scatterData = ref(null)
  const heatmapData = ref(null)
  const listData = ref([])
  const loading = ref(false)
  const error = ref(null)
  
  // 计算属性
  const hasData = computed(() => stats.value.total_count > 0)
  
  // 获取统计数据
  const fetchStats = async () => {
    try {
      loading.value = true
      const response = await axios.get('/api/stats')
      if (response.data.success) {
        stats.value = response.data.data
      }
    } catch (err) {
      error.value = err.message
      console.error('获取统计数据失败:', err)
    } finally {
      loading.value = false
    }
  }
  
  // 获取时序数据
  const fetchTimeSeries = async (granularity = 'monthly', magnitude = 'all') => {
    try {
      loading.value = true
      const response = await axios.get(`/api/time-series?granularity=${granularity}&magnitude=${magnitude}`)
      if (response.data.success) {
        timeSeriesData.value = response.data.data
        return response.data.data
      }
      return null
    } catch (err) {
      error.value = err.message
      console.error('获取时序数据失败:', err)
      return null
    } finally {
      loading.value = false
    }
  }
  
  // 获取全球分布数据
  const fetchGlobeData = async (magnitude = 'all') => {
    try {
      loading.value = true
      const response = await axios.get(`/api/globe-data?magnitude=${magnitude}`)
      if (response.data.success) {
        globeData.value = response.data.data
      }
    } catch (err) {
      error.value = err.message
      console.error('获取全球分布数据失败:', err)
    } finally {
      loading.value = false
    }
  }
  
  // 获取散点图数据
  const fetchScatterData = async (magnitude = 'all') => {
    try {
      loading.value = true
      const response = await axios.get(`/api/scatter?magnitude=${magnitude}`)
      if (response.data.success) {
        scatterData.value = response.data.data
      }
    } catch (err) {
      error.value = err.message
      console.error('获取散点图数据失败:', err)
    } finally {
      loading.value = false
    }
  }
  
  // 获取热力图数据
  const fetchHeatmapData = async (magnitude = 'all') => {
    try {
      loading.value = true
      const response = await axios.get(`/api/heatmap?magnitude=${magnitude}`)
      if (response.data.success) {
        heatmapData.value = response.data.data
      }
    } catch (err) {
      error.value = err.message
      console.error('获取热力图数据失败:', err)
    } finally {
      loading.value = false
    }
  }
  
  // 获取列表数据
  const fetchListData = async (params = {}) => {
    try {
      loading.value = true
      const queryParams = new URLSearchParams(params)
      const response = await axios.get(`/api/list-data?${queryParams}`)
      if (response.data.success) {
        listData.value = response.data.data
      }
    } catch (err) {
      error.value = err.message
      console.error('获取列表数据失败:', err)
    } finally {
      loading.value = false
    }
  }
  
  // 加载所有数据
  const loadAllData = async (magnitude = 'all') => {
    await Promise.all([
      fetchStats(),
      fetchTimeSeries('monthly', magnitude),
      fetchGlobeData(magnitude),
      fetchScatterData(magnitude),
      fetchHeatmapData(magnitude),
      fetchListData({ magnitude })
    ])
  }
  
  return {
    stats,
    timeSeriesData,
    globeData,
    scatterData,
    heatmapData,
    listData,
    loading,
    error,
    hasData,
    fetchStats,
    fetchTimeSeries,
    fetchGlobeData,
    fetchScatterData,
    fetchHeatmapData,
    fetchListData,
    loadAllData
  }
})
