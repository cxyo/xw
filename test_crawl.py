import requests
from bs4 import BeautifulSoup

# 测试东方财富网
def test_eastmoney():
    print("测试东方财富网...")
    url = "https://finance.eastmoney.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        print(f"状态码: {response.status_code}")
        print(f"响应长度: {len(response.text)} 字符")
        
        # 尝试获取一些链接
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True, limit=20)
        print(f"找到 {len(links)} 个链接")
        for i, link in enumerate(links[:5]):
            title = link.get_text(strip=True)
            href = link['href']
            print(f"{i+1}. {title}: {href}")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    test_eastmoney()