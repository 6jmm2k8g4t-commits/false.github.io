#!/usr/bin/env python3
"""
PythonAnywhere 自动化部署脚本
运行方式：在 PythonAnywhere Bash 控制台中执行
    python deploy_pythonanywhere.py
"""

import os
import sys
import subprocess

def run_command(cmd, description=""):
    """运行命令并输出结果"""
    if description:
        print(f"\n{'='*60}")
        print(f"📋 {description}")
        print(f"{'='*60}")
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"⚠️  {result.stderr}")
    return result.returncode == 0

def main():
    print("🚀 开始 PythonAnywhere 自动部署")
    print("=" * 60)
    
    # 1. 检查当前目录
    current_dir = os.getcwd()
    print(f"\n📁 当前目录: {current_dir}")
    
    # 2. 检查已安装的包
    print("\n📦 检查已安装的 Python 包...")
    run_command("pip list | grep -i flask", "Flask 相关包")
    run_command("pip list | grep -i pandas", "Pandas 相关包")
    
    # 3. 尝试安装依赖（如果失败则跳过）
    print("\n📦 尝试安装依赖...")
    print("   如果失败，请手动在 PythonAnywhere 的 'Consoles' 页面安装")
    
    # 设置临时目录
    os.environ['TMPDIR'] = os.path.expanduser('~/tmp')
    os.makedirs(os.environ['TMPDIR'], exist_ok=True)
    
    # 尝试安装，但失败不退出
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True,
        env={**os.environ, 'TMPDIR': os.environ['TMPDIR']}
    )
    if result.returncode == 0:
        print("✅ 依赖安装成功")
    else:
        print("⚠️  依赖安装失败（可能已安装或权限问题）")
        print("   错误信息:", result.stderr[:200] if result.stderr else "无")
    
    # 4. 检查数据文件
    data_file = os.environ.get('DATA_FILE_PATH', 'earthquake_dataset.csv')
    if os.path.exists(data_file):
        size_mb = os.path.getsize(data_file) / (1024 * 1024)
        print(f"\n✅ 数据文件存在: {data_file} ({size_mb:.1f} MB)")
    else:
        print(f"\n⚠️  数据文件不存在: {data_file}")
        print("   请上传数据文件到项目目录")
    
    # 5. 检查后端代码
    if os.path.exists('backend/app.py'):
        print("✅ 后端代码存在")
    else:
        print("❌ 后端代码不存在")
        return False
    
    # 6. 测试导入
    print("\n🧪 测试后端导入...")
    try:
        sys.path.insert(0, current_dir)
        from backend.app import app
        print("✅ 后端导入成功")
    except Exception as e:
        print(f"❌ 后端导入失败: {e}")
        print("\n可能的解决方案：")
        print("1. 在 PythonAnywhere 的 'Consoles' 页面手动运行: pip install flask flask-cors pandas numpy matplotlib")
        print("2. 检查是否有缺失的依赖包")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 部署检查完成！")
    print("=" * 60)
    print("\n下一步操作：")
    print("1. 在 Web 标签页中 Reload 应用")
    print("2. 访问您的域名查看是否正常运行")
    print("3. 检查日志排查问题")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
