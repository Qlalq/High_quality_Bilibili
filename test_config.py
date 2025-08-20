#!/usr/bin/env python3
"""测试配置导入的小程序"""

from config import *
import bilibili_crawler

def test_config():
    print("📋 配置测试")
    print(f"点赞率阈值: {LIKE_RATE_THRESHOLD}")
    print(f"每分类目标数量: {TARGET_COUNT_PER_CATEGORY}")
    print(f"请求延时范围: {REQUEST_DELAY_MIN}-{REQUEST_DELAY_MAX}秒")
    print(f"数据目录: {DATA_DIR}")
    print(f"CSV前缀: {CSV_PREFIX}")
    print(f"API地址: {BASE_URL}")
    
    print("\n🧪 测试单个分类爬取...")
    # 测试音乐分类
    data_rows = bilibili_crawler.get_bilibili_ranking_data(3, "音乐测试", 3)
    if data_rows:
        print(f"✅ 成功获取 {len(data_rows)} 条数据")
        for i, row in enumerate(data_rows):
            print(f"  {i+1}. {row['视频标题'][:20]}... - 点赞率: {row['点赞率']}")
    else:
        print("❌ 获取数据失败")

if __name__ == "__main__":
    test_config()
