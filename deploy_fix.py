# 修复 GitHub 上代码的脚本
# 请在 GitHub 上手动更新 backend/app.py 的 load_data 函数

完整的 load_data 函数代码如下：

```python
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
```
