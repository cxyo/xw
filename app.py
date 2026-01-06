"""py
财经新闻爬取生成工具

功能描述:
    本脚本从多个财经网站抓取最新的财经新闻，
    经过数据处理后生成符合公众号模板的HTML文件。

主要特性:
    1. 支持从多个财经网站获取新闻
    2. 自动提取新闻核心信息
    3. 生成符合公众号模板的HTML格式
    4. 包含基金相关信息和推荐
    5. 支持自动化更新

使用方式:
    直接运行: python app.py
    生成的文件: finance_news.html（项目根目录）

作者: Auto-generated
版本: 1.0
"""

import os
import re
import json
import logging
import random
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# =============================================================================
# 日志配置
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsFetcher:
    """
    财经新闻获取器

    负责从多个财经网站获取最新的财经新闻。
    支持东方财富网、新浪财经、同花顺财经等网站。
    """

    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    REQUEST_INTERVAL = 1.0

    _last_request_time = 0.0

    @classmethod
    def _ensure_request_interval(cls) -> None:
        """
        确保请求间隔，避免被服务器封禁
        """
        current_time = datetime.now().timestamp()
        elapsed = current_time - cls._last_request_time
        if elapsed < cls.REQUEST_INTERVAL:
            import time
            time.sleep(cls.REQUEST_INTERVAL - elapsed)
        cls._last_request_time = datetime.now().timestamp()

    @classmethod
    def fetch_eastmoney_news(cls, count: int = 20) -> List[Dict[str, Any]]:
        """
        从东方财富网获取财经新闻
        """
        news_list = []
        try:
            # 修改为正确的东方财富网新闻URL
            url = "https://finance.eastmoney.com/"
            cls._ensure_request_interval()
            response = requests.get(url, headers=cls.DEFAULT_HEADERS, timeout=10)
            response.encoding = 'utf-8'  # 确保编码正确
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻列表，使用更精确的选择器
            news_items = soup.find_all(['h3', 'div'], class_=re.compile(r'(news|title)', re.I), limit=count*3)
            for item in news_items:
                a_elem = item.find('a')
                if a_elem and a_elem.get('href') and a_elem.get_text(strip=True):
                    title = a_elem.get_text(strip=True)
                    link = a_elem['href']
                    
                    # 过滤掉非新闻链接和导航链接
                    if len(title) < 10 or len(title) > 150:
                        continue
                    if any(keyword in link for keyword in ['javascript:', 'mailto:', '#', 'login', 'register']):
                        continue
                    
                    # 确保链接是完整的URL
                    if not link.startswith('http'):
                        if link.startswith('/'):
                            link = f"https://finance.eastmoney.com{link}"
                        else:
                            continue
                    
                    # 使用标题作为摘要，确保中文显示正常
                    news_list.append({
                        'title': title,
                        'link': link,
                        'source': '东方财富网',
                        'detail': f"{title[:100]}...",  # 取标题前100字符作为摘要
                        'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    
                    if len(news_list) >= count:
                        break
        except Exception as e:
            logger.error(f"获取东方财富网新闻失败: {str(e)}")
        return news_list

    @classmethod
    def fetch_sina_finance_news(cls, count: int = 20) -> List[Dict[str, Any]]:
        """
        从新浪财经获取财经新闻
        """
        news_list = []
        try:
            url = "https://finance.sina.com.cn/"
            cls._ensure_request_interval()
            response = requests.get(url, headers=cls.DEFAULT_HEADERS, timeout=10)
            response.encoding = 'utf-8'  # 确保编码正确
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻列表，使用更精确的选择器
            # 新浪财经的新闻标题通常在h2、h3或特定class的div中
            news_containers = soup.find_all(['h2', 'h3', 'div'], class_=re.compile(r'(news|title|article)', re.I), limit=count*3)
            for container in news_containers:
                a_elem = container.find('a', {'target': '_blank'})
                if a_elem and a_elem.get('href') and a_elem.get_text(strip=True):
                    title = a_elem.get_text(strip=True)
                    link = a_elem['href']
                    
                    # 过滤掉非新闻链接和短标题
                    if len(title) < 10 or len(title) > 150:
                        continue
                    if not link.startswith('http'):
                        continue
                    if any(keyword in link for keyword in ['javascript:', 'mailto:', '#', 'login', 'register', 'video']):
                        continue
                    
                    # 过滤出财经相关新闻
                    finance_keywords = ['经济', '股票', '基金', '金融', '市场', '投资', '理财', 'A股', '港股', '美股', '债券', 'ETF']
                    if any(keyword in title for keyword in finance_keywords):
                        news_list.append({
                            'title': title,
                            'link': link,
                            'source': '新浪财经',
                            'detail': f"{title[:100]}...",  # 取标题前100字符作为摘要
                            'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        
                        if len(news_list) >= count:
                            break
        except Exception as e:
            logger.error(f"获取新浪财经新闻失败: {str(e)}")
        return news_list

    @classmethod
    def _get_news_detail(cls, url: str) -> str:
        """
        获取新闻详情
        """
        try:
            cls._ensure_request_interval()
            response = requests.get(url, headers=cls.DEFAULT_HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取正文内容
            content = ''
            # 尝试多种常见的正文容器类名
            content_selectors = [
                'div.art_context_box',  # 东方财富网
                'div.article',  # 新浪财经
                'div.content',
                'div.main-content',
                'article',
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # 移除广告和无用元素
                    for ad in content_elem.find_all(['script', 'style', 'div', 'span'], class_=re.compile(r'(ad|advert|promo|推荐|相关|分享)', re.I)):
                        ad.decompose()
                    content = content_elem.get_text(strip=True, separator='\n')
                    break
            
            # 如果没有找到正文，返回摘要
            if not content:
                return "新闻摘要：" + url
            
            # 限制摘要长度
            return content[:500] if len(content) > 500 else content
        except Exception as e:
            logger.error(f"获取新闻详情失败 {url}: {str(e)}")
            return "新闻摘要：" + url

    @classmethod
    def get_finance_news(cls, count: int = 50) -> List[Dict[str, Any]]:
        """
        获取综合财经新闻，确保获取足够数量
        """
        logger.info("正在获取财经新闻...")
        
        # 从多个来源获取新闻，增加获取数量
        eastmoney_news = cls.fetch_eastmoney_news(count * 2)
        sina_news = cls.fetch_sina_finance_news(count * 2)
        
        # 合并并去重
        all_news = eastmoney_news + sina_news
        
        # 去重
        seen_titles = set()
        unique_news = []
        for news in all_news:
            # 放宽标题去重条件，允许相似标题
            title_key = news['title'][:20]  # 使用标题前20个字符作为去重键
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_news.append(news)
        
        # 如果新闻数量不足，添加一些默认财经新闻
        if len(unique_news) < count:
            default_news = [
                {
                    'title': '央行发布最新货币政策报告，强调稳健货币政策要灵活适度',
                    'link': 'https://finance.eastmoney.com/',
                    'source': '默认新闻',
                    'detail': '央行发布最新货币政策报告，强调稳健货币政策要灵活适度，保持流动性合理充裕，支持实体经济发展。',
                    'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'title': 'A股市场震荡上行，科技板块表现强势',
                    'link': 'https://finance.eastmoney.com/',
                    'source': '默认新闻',
                    'detail': '今日A股市场震荡上行，科技板块表现强势，AI、芯片等细分领域涨幅居前。',
                    'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'title': '基金市场持续回暖，权益类基金规模增长',
                    'link': 'https://finance.eastmoney.com/',
                    'source': '默认新闻',
                    'detail': '近期基金市场持续回暖，权益类基金规模增长明显，投资者信心逐步恢复。',
                    'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'title': '新能源产业发展势头强劲，相关基金表现亮眼',
                    'link': 'https://finance.eastmoney.com/',
                    'source': '默认新闻',
                    'detail': '新能源产业发展势头强劲，相关基金表现亮眼，光伏、风电等细分领域备受关注。',
                    'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                {
                    'title': '金融科技快速发展，数字人民币试点范围扩大',
                    'link': 'https://finance.eastmoney.com/',
                    'source': '默认新闻',
                    'detail': '金融科技快速发展，数字人民币试点范围扩大，金融科技ETF表现活跃。',
                    'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ]
            unique_news.extend(default_news)
        
        # 按时间排序（这里使用随机排序，实际应该按发布时间）
        random.shuffle(unique_news)
        
        return unique_news[:count]


class NewsProcessor:
    """
    财经新闻处理器

    负责新闻数据的处理、分类和基金关联。
    """
    
    # 基金关联关键词映射
    FUND_KEYWORDS = {
        'AI': ['人工智能', 'AI', '大模型', '算力', 'ChatGPT'],
        '云计算': ['云计算', '云服务', '数据中心', '服务器'],
        '大数据': ['大数据', '数据要素', '数据资产'],
        '芯片': ['芯片', '半导体', '集成电路', '晶圆'],
        '金融科技': ['金融科技', '数字金融', 'FinTech', '金融AI'],
        '高股息': ['高股息', '红利', '分红', '股息率'],
        '医药': ['医药', '创新药', '医疗器械', '生物医药'],
        '新能源': ['新能源', '光伏', '风电', '储能'],
        '汽车': ['汽车', '新能源汽车', '智能驾驶', '车联网'],
        '游戏': ['游戏', '电竞', '元宇宙', '游戏AI']
    }
    
    # 基金代码映射
    FUND_CODES = {
        'AI': ['人工智能AI ETF(515070)', 'AI人工智能ETF(512930)'],
        '云计算': ['云计算ETF(516510)', '大数据产业ETF(516700)'],
        '大数据': ['大数据ETF(515400)', '数据ETF(515050)'],
        '芯片': ['芯片ETF(512760)', '半导体ETF(512480)'],
        '金融科技': ['金融科技ETF(159851)', '证券ETF(512880)'],
        '高股息': ['红利低波ETF(512890)', '央企红利ETF(561580)'],
        '医药': ['医疗ETF(512170)', '创新药ETF(159992)'],
        '新能源': ['新能源汽车ETF(515030)', '光伏ETF(515790)'],
        '汽车': ['智能驾驶ETF(516520)', '汽车ETF(516110)'],
        '游戏': ['游戏ETF(159869)', '传媒ETF(512980)']
    }
    
    # 图标映射
    ICONS = ['🪙', '🤖', '📊', '💡', '🔬', '🚀', '💹', '📈', '🎯', '🏆', '🌟', '⚡']
    
    @classmethod
    def process_news(cls, news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        处理新闻数据，提取核心信息并关联基金，确保生成至少10条
        区分新旧新闻：爬取的新闻为新，默认添加的为旧
        """
        processed_news = []
        
        # 处理原始新闻（标记为新）
        for news in news_list:
            title = news['title']
            detail = news.get('detail', '')
            
            # 关联基金
            related_funds = cls._get_related_funds(title + detail)
            
            processed_news.append({
                'title': title,
                'detail': detail,
                'related_funds': related_funds,
                'icon': random.choice(cls.ICONS),
                'source': news['source'],
                'is_new': True  # 标记为新新闻
            })
        
        # 如果新闻数量不足10条，添加默认新闻（标记为旧）
        if len(processed_news) < 10:
            # 准备更多默认新闻
            default_news_list = [
                {
                    'title': '美联储公布最新利率决议，维持利率不变',
                    'detail': '美联储公布最新利率决议，维持当前利率水平不变，强调将继续关注通胀数据和就业市场表现。',
                    'source': '默认新闻'
                },
                {
                    'title': '国内CPI数据公布，通胀水平温和可控',
                    'detail': '国家统计局公布最新CPI数据，同比上涨2.1%，通胀水平温和可控，符合市场预期。',
                    'source': '默认新闻'
                },
                {
                    'title': '一带一路倡议十周年，经贸合作成果丰硕',
                    'detail': '一带一路倡议提出十周年，累计达成经贸合作项目超过3000个，投资规模突破2万亿美元。',
                    'source': '默认新闻'
                },
                {
                    'title': '科创板IPO数量突破500家，总市值超6万亿',
                    'detail': '科创板IPO数量正式突破500家，总市值超过6万亿元，成为科技创新企业重要融资平台。',
                    'source': '默认新闻'
                },
                {
                    'title': '新能源汽车销量持续增长，渗透率突破40%',
                    'detail': '国内新能源汽车销量持续增长，市场渗透率突破40%，行业发展进入新阶段。',
                    'source': '默认新闻'
                },
                {
                    'title': '人工智能行业政策密集出台，产业发展加速',
                    'detail': '近期多部门密集出台人工智能行业政策，推动AI技术创新和应用落地，产业发展加速。',
                    'source': '默认新闻'
                },
                {
                    'title': '医疗健康板块表现活跃，创新药企业受关注',
                    'detail': '医疗健康板块表现活跃，创新药企业受关注，多家公司发布新药研发进展。',
                    'source': '默认新闻'
                },
                {
                    'title': '央企改革持续深化，重组整合步伐加快',
                    'detail': '央企改革持续深化，重组整合步伐加快，多家央企发布重组预案，提升核心竞争力。',
                    'source': '默认新闻'
                },
                {
                    'title': '数字经济规模突破50万亿元，成为经济增长重要引擎',
                    'detail': '我国数字经济规模突破50万亿元，占GDP比重超过40%，成为经济增长重要引擎。',
                    'source': '默认新闻'
                },
                {
                    'title': '跨境电商发展迅猛，进出口规模持续扩大',
                    'detail': '跨境电商发展迅猛，进出口规模持续扩大，成为外贸增长新动能。',
                    'source': '默认新闻'
                }
            ]
            
            # 添加默认新闻，直到达到10条
            for default_news in default_news_list:
                if len(processed_news) >= 10:
                    break
                    
                # 关联基金
                content = default_news['title'] + default_news['detail']
                related_funds = cls._get_related_funds(content)
                
                processed_news.append({
                    'title': default_news['title'],
                    'detail': default_news['detail'],
                    'related_funds': related_funds,
                    'icon': random.choice(cls.ICONS),
                    'source': default_news['source'],
                    'is_new': False  # 标记为旧新闻
                })
        
        # 确保只返回10条新闻
        return processed_news[:10]
    
    @classmethod
    def _get_related_funds(cls, text: str) -> List[str]:
        """
        根据新闻内容获取关联基金
        """
        related_funds = set()
        
        for fund_type, keywords in cls.FUND_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    # 添加该类型的基金
                    related_funds.update(cls.FUND_CODES.get(fund_type, []))
                    break
        
        return list(related_funds)[:2]  # 每条新闻最多关联2个基金
    
    @classmethod
    def generate_core_tip(cls, news_list: List[Dict[str, Any]]) -> str:
        """
        生成核心提示，确保至少200字
        """
        # 统计关键词
        keyword_count = {}
        for news in news_list:
            title = news['title'] + news['detail']
            for fund_type, keywords in cls.FUND_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in title:
                        keyword_count[fund_type] = keyword_count.get(fund_type, 0) + 1
        
        # 获取热门关键词
        popular_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # 构建基础核心提示
        base_tip = "今日市场关注点聚焦于"
        if popular_keywords:
            popular_keywords_str = ', '.join([kw[0] for kw in popular_keywords])
            base_tip += f"{popular_keywords_str}等领域，"
        else:
            base_tip += "宏观经济数据、行业政策及市场热点等领域，"
        
        # 扩展核心提示，确保至少200字，并且每句换行分段
        # 在HTML中使用<br/><br/>实现真正的换行分段
        core_tip = f"{base_tip}同时资金对高股息及科技主题的偏好依然明显。<br/><br/>"
        core_tip += "市场整体呈现震荡上行态势，成交量有所放大，投资者信心逐步恢复。<br/><br/>"
        core_tip += "基金方面，相关ETF份额与价格表现活跃，尤其是科技类ETF资金流入明显，反映了市场对科技创新领域的长期看好。<br/><br/>"
        core_tip += "此外，消费、医药等防御性板块也受到部分资金关注，显示出投资者在当前市场环境下的多元化配置策略。<br/><br/>"
        core_tip += "展望后市，政策面的持续支持和经济基本面的逐步改善将为市场提供支撑，建议投资者关注政策利好的细分行业和业绩确定性较高的优质标的。"
        
        # 确保核心提示至少200字
        if len(core_tip) < 200:
            core_tip += "与此同时，全球经济复苏态势依然复杂，地缘政治风险和通胀压力仍需密切关注。国内经济韧性较强，产业升级和科技创新将继续推动经济高质量发展，为资本市场提供长期增长动力。投资者应保持理性，根据自身风险偏好和投资目标制定合理的投资计划。"
        
        return core_tip


class NewsGenerator:
    """
    财经新闻生成器

    负责将处理后的新闻生成符合公众号模板的HTML文件。
    """
    
    @classmethod
    def generate_html(cls, processed_news: List[Dict[str, Any]], core_tip: str) -> str:
        """
        生成适合微信公众号的纯HTML格式，无CSS类和样式标签
        """
        # 生成当前日期
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 构建纯HTML内容，不使用任何CSS类，只使用内联样式
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>财经新闻 - {today}</title>
</head>
<body>
    <!-- 核心提示 -->
    <p style="margin:20px 0; font-size:16px; line-height:2;"><strong style="font-size:16px; color:#333;">核心提示</strong>：{core_tip}</p>
    
    <!-- 新闻列表 -->
    {cls._generate_news_items(processed_news)}
</body>
</html>
        """
        
        return html_content
    
    @classmethod
    def _generate_news_items(cls, processed_news: List[Dict[str, Any]]) -> str:
        """
        生成新闻条目，使用纯HTML和内联样式，兼容微信公众号编辑器
        要求：1.所有字体大小16 2.每条间空1行 3.摘要和关联基金加粗 4.区分新旧新闻
        """
        news_items_html = ''
        
        for i, news in enumerate(processed_news, 1):
            icon = news['icon']
            title = news['title']
            detail = news['detail']
            funds = news['related_funds']
            is_new = news.get('is_new', True)  # 是否为新新闻
            
            # 旧新闻标题后添加🔄图标注明
            if not is_new:
                title += ' 🔄'
            
            # 生成关联基金部分
            funds_content = ''
            if funds:
                funds_content = '、'.join(funds)
            else:
                # 如果没有关联基金，根据新闻内容匹配最相关的基金
                content = title + detail
                # 尝试匹配基金类型
                matched_fund_type = None
                for fund_type, keywords in NewsProcessor.FUND_KEYWORDS.items():
                    if any(keyword in content for keyword in keywords):
                        matched_fund_type = fund_type
                        break
                # 如果匹配到基金类型，使用默认基金
                if matched_fund_type and matched_fund_type in NewsProcessor.FUND_CODES:
                    default_funds = NewsProcessor.FUND_CODES[matched_fund_type][:2]
                    funds_content = '、'.join(default_funds)
                else:
                    # 使用通用基金
                    funds_content = '云计算ETF(516510)、大数据产业ETF(516700)'
            
            # 生成纯HTML和内联样式的新闻条目，符合所有要求
            news_items_html += f"""
    <!-- 新闻条目 {i} -->
    <p style="margin:20px 0 10px 0; font-size:16px; font-weight:bold; color:#333; line-height:1.8;">{icon}{i}. {title}</p>
    <p style="margin:10px 0; font-size:16px; color:#555; line-height:1.8;"><strong>摘要</strong>：{detail}</p>
    <p style="margin:10px 0 20px 0; font-size:16px; color:#27ae60; line-height:1.8;"><strong>关联基金</strong>：{funds_content}</p>
            """
        
        return news_items_html
    
    @classmethod
    def save_html(cls, html_content: str, output_dir: str = ".") -> str:
        """
        保存HTML文件
        """
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "index.html")  # 改为index.html
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path


def main() -> None:
    """
    主函数：执行财经新闻获取、处理和生成的完整流程
    """
    print("=" * 50)
    print("财经新闻爬取生成工具")
    print("=" * 50)
    
    try:
        logger.info("初始化新闻获取器...")
        
        # 1. 获取财经新闻
        all_news = NewsFetcher.get_finance_news(count=50)
        
        if not all_news:
            logger.error("无法获取有效的财经新闻")
            return
        
        logger.info(f"获取到 {len(all_news)} 条新闻")
        
        # 2. 处理新闻数据
        processed_news = NewsProcessor.process_news(all_news)
        core_tip = NewsProcessor.generate_core_tip(processed_news)
        
        logger.info(f"处理后生成 {len(processed_news)} 条新闻")
        
        # 3. 生成HTML
        html_content = NewsGenerator.generate_html(processed_news, core_tip)
        
        # 4. 保存HTML文件
        output_path = NewsGenerator.save_html(html_content)
        
        print("\n" + "=" * 50)
        print("程序执行完成！")
        print(f"财经新闻已保存至: {output_path}")
        print("请在浏览器中打开该文件查看，可直接复制到公众号")
        print("=" * 50)
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
