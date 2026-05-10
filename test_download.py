import requests

# 测试 GitHub Releases 下载链接
url = 'https://github.com/6jmm2k8g4t-commits/false.github.io/releases/download/v1.0/earthquake_dataset.csv.gz'

print(f"测试下载：{url}")
print("发送请求...")

response = requests.get(url, timeout=30, stream=True)
print(f"状态码：{response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Content-Length: {response.headers.get('Content-Length')} bytes")

# 下载前 1KB 检查内容
downloaded = 0
content_preview = b''
for chunk in response.iter_content(chunk_size=1024):
    content_preview += chunk
    downloaded += len(chunk)
    if downloaded >= 1024:
        break

print(f"\n前 1KB 内容预览：")
print(content_preview[:200])

# 检查是否是 Git LFS 指针
if b'version https://git-lfs.github.com' in content_preview:
    print("\n❌ 这是 Git LFS 指针文件！")
else:
    print("\n✅ 这是真实的文件！")
