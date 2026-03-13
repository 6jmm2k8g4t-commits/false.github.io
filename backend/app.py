#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地震数据可视化应用 - 支持可切换功能
"""

from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import warnings
import gzip
import json
import time
from functools import wraps
warnings.filterwarnings('ignore')

try:
    from statsmodels.tsa.arima.model import ARIMA
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    STATSMODELS_AVAILABLE = True
    print("✅ statsmodels 已成功安装并导入")
except ImportError as e:
    STATSMODELS_AVAILABLE = False
    print(f"⚠️ statsmodels 未安装，将使用模拟预测。错误：{e}")

try:
    from scipy.stats import gaussian_kde
    from scipy.spatial import cKDTree
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("⚠️ scipy 未安装，核密度估计将使用简化算法")

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("⚠️ prophet 未安装，Prophet 模型将使用模拟预测")

app = Flask(__name__)
CORS(app)

app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# 健康检查接口
@app.route('/api/health')
def health_check():
    """健康检查接口"""
    from datetime import datetime
    return jsonify({
        'status': 'ok',
        'message': 'Earthquake API is running',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'version': '2.0.0'
    })

# 根路由测试
@app.route('/')
def root():
    """根路由"""
    return jsonify({
        'message': 'Welcome to Earthquake API',
        'endpoints': {
            'health': '/api/health',
            'stats': '/api/stats',
            'time-series': '/api/time-series',
            'high-risk-regions': '/api/high-risk-regions'
        }
    })

df = None
df_filtered_cache = {}
_high_risk_regions_cache = None

def gzip_response(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        if isinstance(response, Response):
            content = response.get_data()
            if len(content) > 1024:
                gzip_buffer = gzip.compress(content)
                response.set_data(gzip_buffer)
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Content-Length'] = len(gzip_buffer)
        return response
    return decorated_function

def get_location_name(lat, lon):
    """根据经纬度生成位置描述"""
    if lat >= 25 and lat <= 45 and lon >= 130 and lon <= 145:
        return "日本"
    elif lat >= 35 and lat <= 42 and lon >= -125 and lon <= -115:
        return "美国加利福尼亚"
    elif lat >= -40 and lat <= -30 and lon >= -75 and lon <= -65:
        return "智利"
    elif lat >= -10 and lat <= 10 and lon >= 95 and lon <= 140:
        return "印度尼西亚"
    elif lat >= 35 and lat <= 45 and lon >= 25 and lon <= 45:
        return "土耳其"
    elif lat >= 20 and lat <= 55 and lon >= 70 and lon <= 140:
        return "中国"
    elif lat >= -5 and lat <= 10 and lon >= 115 and lon <= 130:
        return "菲律宾"
    elif lat >= -50 and lat <= -10 and lon >= 110 and lon <= 155:
        return "澳大利亚"
    elif lat >= 50 and lat <= 70 and lon >= 160 and lon <= 180:
        return "俄罗斯远东"
    elif lat >= -40 and lat <= -20 and lon >= 165 and lon <= 180:
        return "新西兰"
    elif lat >= 15 and lat <= 30 and lon >= -100 and lon <= -80:
        return "墨西哥"
    elif lat >= -10 and lat <= 5 and lon >= -85 and lon <= -70:
        return "秘鲁/厄瓜多尔"
    elif lat >= 50 and lat <= 60 and lon >= -10 and lon <= 5:
        return "英国"
    elif lat >= 35 and lat <= 45 and lon >= -10 and lon <= 5:
        return "西班牙/葡萄牙"
    elif lat >= 35 and lat <= 50 and lon >= 5 and lon <= 20:
        return "意大利/希腊"
    elif lat >= -5 and lat <= 5 and lon >= 30 and lon <= 45:
        return "东非"
    else:
        return f"海域 ({lat:.1f}°N, {lon:.1f}°E)"

def load_data():
    """加载地震数据"""
    global df
    try:
        # 支持从 URL 下载数据文件（用于云部署）
        data_url = os.environ.get('DATA_FILE_URL', 'https://raw.githubusercontent.com/6jmm2k8g4t-commits/false.github.io/main/earthquake_dataset.csv')
        data_file = os.environ.get('DATA_FILE_PATH', '/data/earthquake_dataset.csv')
        
        # 如果文件不存在，尝试从 GitHub 下载
        if not os.path.exists(data_file):
            print(f"数据文件不存在，正在从 GitHub 下载：{data_url}")
            import requests
            response = requests.get(data_url, timeout=60)
            response.raise_for_status()
            
            # 保存到本地
            os.makedirs(os.path.dirname(data_file), exist_ok=True)
            with open(data_file, 'wb') as f:
                f.write(response.content)
            print(f"✅ 数据文件已下载到：{data_file} ({len(response.content)} bytes)")
        
        full_path = data_file
        
        # 如果相对路径找不到，尝试绝对路径
        if not os.path.exists(full_path) and os.path.exists(data_file):
            full_path = data_file
            
        if os.path.exists(full_path):
            usecols = ['time', 'latitude', 'longitude', 'depth', 'magnitude']
            df = pd.read_csv(full_path, usecols=usecols)
            df['time'] = pd.to_datetime(df['time'], format='mixed', utc=True)
            df['year'] = df['time'].dt.year
            df['month'] = df['time'].dt.to_period('M').astype(str)
            df['quarter'] = df['time'].dt.to_period('Q').astype(str)
            print(f"✅ 加载 {len(df)} 条数据")
            
            # 预计算高风险区域数据
            print("🔄 预计算高风险区域数据...")
            _high_risk_regions_cache = _compute_high_risk_regions()
            print("✅ 高风险区域数据预计算完成")
        else:
            print("⚠️ 数据文件不存在")
            df = None
    except Exception as e:
        print(f"⚠️ 加载失败：{e}")
        import traceback
        print(traceback.format_exc())
        df = None

# 在模块加载时立即加载数据（用于云平台部署）
print("🔄 开始加载地震数据...")
load_data()

@app.route('/')
def index():
    """服务 Vue3 前端"""
    try:
        vue_index = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist', 'index.html')
        if os.path.exists(vue_index):
            with open(vue_index, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # 回退到旧版本
            dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard_with_switches.html')
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        return f"<h1>错误</h1><p>无法加载页面：{e}</p>", 500

@app.route('/<path:path>')
def serve_static(path):
    """服务 Vue3 静态文件"""
    try:
        dist_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
        file_path = os.path.join(dist_path, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory(dist_path, path)
        else:
            # 对于前端路由，返回 index.html
            vue_index = os.path.join(dist_path, 'index.html')
            with open(vue_index, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        return f"<h1>错误</h1><p>无法加载资源：{e}</p>", 404

# ... 其余代码保持不变 ...

if __name__ == '__main__':
    print('=' * 60)
    print('🌍 地震数据可视化应用 - 可切换版本')
    print('=' * 60)
    load_data()
    
    # 支持云平台的 PORT 环境变量
    port = int(os.environ.get('PORT', 8090))
    
    print(f'📍 访问地址：http://localhost:{port}')
    print('✨ 功能特性:')
    print('   - 主题切换 (浅色/深色)')
    print('   - 视图切换 (图表/列表)')
    print('   - 数据筛选 (震级/时间)')
    print('   - 状态持久化 (localStorage)')
    print('=' * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
