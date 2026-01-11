# 财经新闻自动爬取生成系统

## 项目简介

这是一个财经新闻自动爬取生成系统，每天定时从多个财经网站爬取最新新闻，自动关联相关基金信息，并生成符合微信公众号格式的HTML文件。生成的文件可以直接复制到微信公众号编辑器中发布，无需额外格式调整。

## 技术栈

- **开发语言**：Python 3.10+
- **爬虫技术**：requests + BeautifulSoup
- **HTML生成**：纯HTML + 内联CSS
- **自动部署**：GitHub Actions

## 爬取平台

- **东方财富网**：https://finance.eastmoney.com/
- **新浪财经**：https://finance.sina.com.cn/
- **每日经济新闻**：https://money.nbd.com.cn/columns/440/
- **同花顺财经**：https://m.10jqka.com.cn/fund/jjzx_list/
- **基金速查网**：https://www.dayfund.cn/news/

## 设计原理

### 1. 模块化设计

项目采用类结构设计，将功能模块化，便于维护和扩展：

- **NewsFetcher**：负责从多个来源爬取财经新闻
- **NewsProcessor**：负责新闻数据的处理和基金关联
- **NewsGenerator**：负责生成符合微信公众号格式的HTML

### 2. 多来源新闻获取

- 从多个财经网站爬取新闻，提高新闻的多样性和全面性
- 支持自定义添加更多新闻来源
- 实现了请求频率控制，避免被服务器封禁

### 3. 智能基金关联

- 根据新闻内容自动关联相关基金，确保基金与新闻主题在同一行业内
- 支持10种基金类型：AI、云计算、大数据、芯片、金融科技、高股息、医药、新能源、汽车、游戏
- 每条新闻至少关联2个基金
- 优化的基金匹配算法，提高关联准确性



### 5. 微信公众号兼容

- 生成纯HTML + 内联CSS格式
- 所有字体大小统一为16px
- 每条新闻之间只空1行
- 摘要和关联基金加粗显示
- 核心提示每句换行分段
- 摘要长度严格控制在150-400字之间
- 摘要内容完整显示，无省略号
- 摘要与标题内容不同，提供丰富的详细信息

## 功能特性

1. **自动爬取**：每天定时从多个财经网站爬取最新新闻
2. **基金关联**：自动关联相关基金信息，确保基金与新闻主题匹配
3. **格式兼容**：生成符合微信公众号的HTML格式
4. **新旧区分**：标记新旧新闻，便于识别
5. **易于部署**：支持GitHub Actions自动部署
6. **摘要优化**：摘要长度严格控制在150-400字之间，内容完整且与标题不同，**所有摘要均为爬取的真实内容，不生成任何内容**
7. **多源获取**：从5个财经网站获取新闻，确保新闻数量充足
8. **关联基金不重复**：10条新闻的关联基金组合不重复，确保内容多样性

## 快速开始

### 本地运行

1. **克隆项目**

```bash
git clone https://github.com/your-username/finance-news-crawler.git
cd finance-news-crawler
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **运行程序**

```bash
python app.py
```

4. **查看结果**

生成的HTML文件为：`index.html`

### 部署到GitHub

1. **创建GitHub仓库**

在GitHub上创建一个新的仓库，命名为`finance-news-crawler`或其他名称。

2. **推送代码**

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/finance-news-crawler.git
git push -u origin main
```

3. **启用GitHub Actions**

GitHub Actions配置文件已经包含在项目中：`.github/workflows/update-finance-news.yml`

GitHub会自动检测到该配置文件，无需额外设置。

4. **配置自动更新**

GitHub Actions会每天晚上8点（上海时间）自动运行，生成最新的`index.html`文件。

## 项目结构

```
finance-news-crawler/
├── .github/
│   └── workflows/
│       └── update-finance-news.yml  # GitHub Actions配置
├── app.py                           # 主程序
├── requirements.txt                  # 依赖列表
├── README.md                        # 项目说明
└── index.html                       # 生成的HTML文件（运行后生成）
```

## 核心配置

### 1. 基金关联配置

在`app.py`中可以修改基金关联规则：

- **FUND_KEYWORDS**：基金类型与关键词映射
- **FUND_CODES**：基金类型与基金代码映射

### 2. 定时运行配置

在`.github/workflows/update-finance-news.yml`中可以修改定时运行时间：

```yaml
# 每天晚上8点运行（上海时间）
schedule:
  - cron: '0 12 * * *'  # UTC时间12:00，对应上海时间20:00
```

### 3. 新闻来源配置

在`app.py`的`NewsFetcher`类中可以添加或修改新闻来源：

- `fetch_eastmoney_news`：东方财富网
- `fetch_sina_finance_news`：新浪财经
- `fetch_nbd_news`：每日经济新闻
- `fetch_10jqka_news`：同花顺财经
- `fetch_dayfund_news`：基金速查网

## 使用说明

1. **查看生成的HTML文件**

运行程序后，生成的HTML文件为`index.html`，可以直接在浏览器中打开查看。

2. **复制到微信公众号**

- 在浏览器中打开`index.html`
- 按`Ctrl+A`全选内容
- 按`Ctrl+C`复制
- 粘贴到微信公众号编辑器中
- 直接发布，无需额外格式调整

3. **自定义配置**

- 可以修改`app.py`中的基金关联规则
- 可以修改生成的HTML格式
- 可以添加更多新闻来源

## 注意事项

1. **爬虫频率**

- 程序已实现请求频率控制，避免被服务器封禁
- 不要频繁手动运行，以免触发反爬机制

2. **微信公众号格式**

- 生成的HTML格式已优化，兼容微信公众号编辑器
- 如果遇到格式问题，可以调整`app.py`中的HTML生成逻辑

3. **自动更新**

- 确保GitHub Actions已启用
- 自动生成的`index.html`会覆盖旧文件
- 可以在GitHub Actions页面查看运行记录

## 常见问题

### 1. 为什么生成的新闻数量不足10条？

- 爬虫可能没有获取到足够的新新闻
- 程序从5个新闻来源获取新闻，通常能保证10条以上
- 可以调整`app.py`中的`get_finance_news`方法，增加获取的新闻数量

### 2. 为什么基金关联不正确？

- 基金关联基于关键词匹配，确保基金与新闻主题在同一行业内
- 可以修改`app.py`中的`FUND_KEYWORDS`和`FUND_CODES`配置
- 增加更多关键词可以提高关联准确性
- 已优化基金匹配算法，提高关联准确性

### 3. 如何添加新的新闻来源？

- 在`NewsFetcher`类中添加新的方法
- 参考现有的`fetch_eastmoney_news`和`fetch_sina_finance_news`方法
- 在`get_finance_news`方法中调用新的方法

## 许可证

本项目采用MIT许可证，可自由使用和修改。

## 贡献

欢迎提交Issue和Pull Request，共同改进项目。

## 更新日志

- **v1.0**：初始版本，支持基本的新闻爬取和HTML生成
- **v1.1**：添加基金关联功能
- **v1.2**：支持多来源新闻
- **v1.3**：添加新旧新闻区分
- **v1.4**：优化微信公众号格式
- **v1.5**：添加自动部署和定时更新
- **v1.6**：
  - 优化摘要生成逻辑，摘要长度严格控制在150-400字之间
  - 改进基金关联算法，确保基金与新闻主题匹配
  - 增加新闻来源至5个，确保新闻数量充足
  - 优化摘要内容，确保摘要与标题不同且完整显示
  - 移除默认新闻，所有新闻均来自网站爬取
- **v1.7**：
  - 移除所有摘要生成逻辑，**所有摘要均为爬取的真实内容，不生成任何内容**
  - 优化新闻去重逻辑，将内容重复的新闻合并
  - 确保10条新闻的关联基金组合不重复
  - 确保所有新闻数据均为爬取当天的数据，保证数据准确性
- **v1.8**：
  - 将自动更新时间调整为上海时间每天晚上8点
  - 更新GitHub Actions配置，使用UTC时间12:00运行（对应上海时间20:00）
  - 更新README文档，统一使用上海时间描述
- **v1.9**：
  - 修复上一个交易日日期显示问题，添加交易日计算逻辑，确保标题显示正确的上一个交易日新闻
  - 修改index.html文件保存位置，从output文件夹改为项目根目录，便于GitHub Pages部署
  - 修复GitHub Actions推送失败的403权限问题，添加permissions配置
  - 优化新闻排序逻辑，根据发布时间排序，确保最新新闻排在前面
  - 改进交易日计算逻辑，支持处理周一和周末的特殊情况

## 联系方式

如有问题或建议，欢迎联系项目维护者。
