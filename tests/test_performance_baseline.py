"""
性能基准测试 - 优化前
用于记录优化前的性能指标，作为对比基准
"""
import time
import psutil
import requests
import json
from datetime import datetime
import statistics

class PerformanceBaseline:
    """性能基准测试类"""
    
    def __init__(self, base_url="http://localhost:8090"):
        self.base_url = base_url
        self.results = {}
        
    def test_api_response_time(self, endpoint, params=None, iterations=10):
        """测试API响应时间"""
        times = []
        url = f"{self.base_url}{endpoint}"
        
        for i in range(iterations):
            start = time.time()
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                end = time.time()
                times.append((end - start) * 1000)  # 转换为毫秒
            except Exception as e:
                print(f"请求失败: {e}")
                times.append(None)
        
        # 过滤掉失败的请求
        valid_times = [t for t in times if t is not None]
        
        if valid_times:
            return {
                'endpoint': endpoint,
                'iterations': len(valid_times),
                'avg_ms': statistics.mean(valid_times),
                'min_ms': min(valid_times),
                'max_ms': max(valid_times),
                'median_ms': statistics.median(valid_times),
                'p95_ms': sorted(valid_times)[int(len(valid_times) * 0.95)] if len(valid_times) >= 20 else max(valid_times)
            }
        return None
    
    def test_memory_usage(self):
        """测试内存使用情况"""
        process = psutil.Process()
        mem_info = process.memory_info()
        
        return {
            'rss_mb': mem_info.rss / 1024 / 1024,
            'vms_mb': mem_info.vms / 1024 / 1024,
            'percent': process.memory_percent()
        }
    
    def run_all_tests(self):
        """运行所有基准测试"""
        print("=" * 60)
        print("性能基准测试 - 优化前")
        print("=" * 60)
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试URL: {self.base_url}")
        print("=" * 60)
        
        # 测试内存使用
        print("\n1. 内存使用情况")
        memory = self.test_memory_usage()
        self.results['memory'] = memory
        print(f"   RSS: {memory['rss_mb']:.2f} MB")
        print(f"   VMS: {memory['vms_mb']:.2f} MB")
        print(f"   内存占用: {memory['percent']:.2f}%")
        
        # 测试API响应时间
        print("\n2. API响应时间测试")
        
        # 测试统计数据接口
        print("   测试 /api/stats ...")
        result = self.test_api_response_time('/api/stats')
        if result:
            self.results['api_stats'] = result
            print(f"   平均响应: {result['avg_ms']:.2f}ms")
            print(f"   P95响应: {result['p95_ms']:.2f}ms")
        
        # 测试时序数据接口 - 年度
        print("   测试 /api/time-series (yearly) ...")
        result = self.test_api_response_time('/api/time-series', {'granularity': 'yearly', 'magnitude': 'all'})
        if result:
            self.results['api_time_series_yearly'] = result
            print(f"   平均响应: {result['avg_ms']:.2f}ms")
            print(f"   P95响应: {result['p95_ms']:.2f}ms")
        
        # 测试时序数据接口 - 季度
        print("   测试 /api/time-series (quarterly) ...")
        result = self.test_api_response_time('/api/time-series', {'granularity': 'quarterly', 'magnitude': 'all'})
        if result:
            self.results['api_time_series_quarterly'] = result
            print(f"   平均响应: {result['avg_ms']:.2f}ms")
            print(f"   P95响应: {result['p95_ms']:.2f}ms")
        
        # 测试时序数据接口 - 月度
        print("   测试 /api/time-series (monthly) ...")
        result = self.test_api_response_time('/api/time-series', {'granularity': 'monthly', 'magnitude': 'all'})
        if result:
            self.results['api_time_series_monthly'] = result
            print(f"   平均响应: {result['avg_ms']:.2f}ms")
            print(f"   P95响应: {result['p95_ms']:.2f}ms")
        
        # 测试高风险区域接口
        print("   测试 /api/high-risk-regions ...")
        result = self.test_api_response_time('/api/high-risk-regions')
        if result:
            self.results['api_high_risk_regions'] = result
            print(f"   平均响应: {result['avg_ms']:.2f}ms")
            print(f"   P95响应: {result['p95_ms']:.2f}ms")
        
        # 测试预测接口
        print("   测试 /api/prediction ...")
        result = self.test_api_response_time('/api/prediction', {'model': 'arima', 'granularity': 'monthly', 'horizon': 12})
        if result:
            self.results['api_prediction'] = result
            print(f"   平均响应: {result['avg_ms']:.2f}ms")
            print(f"   P95响应: {result['p95_ms']:.2f}ms")
        
        # 保存结果
        self.save_results()
        
        print("\n" + "=" * 60)
        print("基准测试完成")
        print("=" * 60)
        
        return self.results
    
    def save_results(self):
        """保存测试结果"""
        filename = f"performance_baseline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'base_url': self.base_url,
                'results': self.results
            }, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {filename}")

if __name__ == '__main__':
    # 创建基准测试实例
    baseline = PerformanceBaseline()
    
    # 运行所有测试
    results = baseline.run_all_tests()
