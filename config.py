# B站高质量视频爬虫配置文件

# 数据质量阈值
LIKE_RATE_THRESHOLD = 0.1  # 点赞率阈值，大于此值认为是高质量视频

# 爬取设置
TARGET_COUNT_PER_CATEGORY = 100  # 每个分类爬取的目标视频数量
TARGET_COUNT_POPULAR = 500  # 热门页面爬取的目标视频数量
MAX_EMPTY_PAGES = 5  # 连续空页数阈值，超过此数停止爬取
REQUEST_DELAY_MIN = 2  # 请求间隔最小秒数
REQUEST_DELAY_MAX = 4  # 请求间隔最大秒数
REQUEST_TIMEOUT = 10   # 请求超时时间（秒）

# 文件路径
DATA_DIR = "data"  # 数据保存目录
RANKING_DIR = "data/ranking"  # 分类排行榜数据目录
POPULAR_DIR = "data/popular"   # 热门页面数据目录
CSV_PREFIX = "B站TOP"  # CSV文件名前缀

# API设置
BASE_URL = "https://api.bilibili.com"
RANKING_API = "/x/web-interface/ranking/v2"  # 排行榜API
POPULAR_API = "/x/web-interface/popular"     # 热门API
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}
