"""
B站高质量视频爬虫

功能：
1. 爬取B站各分类排行榜数据
2. 计算视频点赞率（点赞数/播放数）
3. 筛选点赞率>0.1的高质量视频
4. 保存到CSV文件，支持25个分类

作者: GitHub Copilot
创建时间: 2025-08-20
"""

import pandas as pd
import requests
import time
import random
import os
import glob

def get_bilibili_ranking_data(tid, category_name, target_count=10):
    """
    获取B站排行榜数据，只保留点赞率>0.1的高质量视频
    """
    url = f'https://api.bilibili.com/x/web-interface/ranking/v2?rid={tid}&type=all'
    
    # 更完整的headers，模拟真实浏览器
    headers = {
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
    
    print(f"正在爬取: {category_name}")
    
    try:
        # 添加session来保持连接
        session = requests.Session()
        session.headers.update(headers)
        
        # 首先访问首页建立session
        session.get('https://www.bilibili.com/', timeout=10)
        time.sleep(1)
        
        # 然后请求API
        response = session.get(url, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code != 200:
            print(f"HTTP错误: {response.status_code}")
            return None
            
        json_data = response.json()
        
        # 检查API返回状态
        if json_data.get('code') != 0:
            print(f"API返回错误: code={json_data.get('code')}, message={json_data.get('message')}")
            if json_data.get('code') == -352:
                print("触发反爬虫机制，建议增加延时或更换IP")
            return None
            
        # 检查数据结构
        if 'data' not in json_data or 'list' not in json_data['data']:
            print(f"数据结构异常: {json_data}")
            return None
            
        video_list = json_data['data']['list']
        print(f"获取到 {len(video_list)} 条数据")
        
        # 解析数据，计算点赞率并过滤高质量视频
        data_rows = []
        high_quality_count = 0
        
        for video in video_list:
            view_count = video.get('stat', {}).get('view', 0)
            like_count = video.get('stat', {}).get('like', 0)
            
            # 避免除零错误，播放数为0时跳过
            if view_count == 0:
                continue
                
            # 计算点赞率
            like_rate = like_count / view_count
            
            # 只保留点赞率>0.1的高质量视频
            if like_rate > 0.1:
                row = {
                    '视频标题': video.get('title', ''),
                    '视频地址': f"https://www.bilibili.com/video/{video.get('bvid', '')}",
                    '作者': video.get('owner', {}).get('name', ''),
                    '播放数': view_count,
                    '弹幕数': video.get('stat', {}).get('danmaku', 0),
                    '投币数': video.get('stat', {}).get('coin', 0),
                    '点赞数': like_count,
                    '分享数': video.get('stat', {}).get('share', 0),
                    '收藏数': video.get('stat', {}).get('favorite', 0),
                    '点赞率': round(like_rate, 4)  # 保留4位小数
                }
                data_rows.append(row)
                high_quality_count += 1
                
                # 达到目标数量就停止
                if high_quality_count >= target_count:
                    break
        
        print(f"筛选出 {len(data_rows)} 条高质量数据（点赞率>0.1）")
        return data_rows
        
    except requests.exceptions.Timeout:
        print(f"请求超时")
        return None
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return None
    except ValueError as e:
        print(f"JSON解析失败: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None

def main():
    # 分类配置 - 根据提供的完整信息扩充
    categorys = [{
        "name": "全站",
        "tid": 0,
        "slug": "all"
    }, {
        "name": "国产动画",
        "type": "bangumi",
        "tid": 168,
        "slug": "guochan",
        "season_type": 4
    }, {
        "name": "国创相关",
        "tid": 168,
        "slug": "guochuang"
    }, {
        "name": "纪录片",
        "type": "cinema",
        "slug": "documentary",
        "tid": 177,
        "season_type": 3
    }, {
        "name": "动画",
        "tid": 1,
        "slug": "douga"
    }, {
        "name": "音乐",
        "tid": 3,
        "slug": "music"
    }, {
        "name": "舞蹈",
        "tid": 129,
        "slug": "dance"
    }, {
        "name": "游戏",
        "tid": 4,
        "slug": "game"
    }, {
        "name": "知识",
        "tid": 36,
        "slug": "knowledge"
    }, {
        "name": "科技",
        "tid": 188,
        "slug": "tech"
    }, {
        "name": "运动",
        "tid": 234,
        "slug": "sports"
    }, {
        "name": "汽车",
        "tid": 223,
        "slug": "car"
    }, {
        "name": "生活",
        "tid": 160,
        "slug": "life"
    }, {
        "name": "美食",
        "tid": 211,
        "slug": "food"
    }, {
        "name": "动物圈",
        "tid": 217,
        "slug": "animal"
    }, {
        "name": "鬼畜",
        "tid": 119,
        "slug": "kichiku"
    }, {
        "name": "时尚",
        "tid": 155,
        "slug": "fashion"
    }, {
        "name": "娱乐",
        "tid": 5,
        "slug": "ent"
    }, {
        "name": "影视",
        "tid": 181,
        "slug": "cinephile"
    }]
    
    # 先清空之前的CSV文件
    print("🧹 正在清空之前的CSV文件...")
    import os
    import glob
    
    # 确保data目录存在
    if not os.path.exists("data"):
        os.makedirs("data")
    
    csv_files = glob.glob("data/B站TOP*-*.csv")
    for csv_file in csv_files:
        try:
            os.remove(csv_file)
            print(f"✅ 删除文件: {csv_file}")
        except Exception as e:
            print(f"❌ 删除文件失败 {csv_file}: {e}")
    
    print(f"\n{'='*60}")
    print("🎯 开始爬取高质量视频数据（点赞率>0.1，每个分类10个）")
    print(f"{'='*60}")
    
    successful_categories = 0
    failed_categories = 0
    
    for category in categorys:
        category_name = category["name"]
        tid = category["tid"]
        
        print(f"\n📂 正在处理分类: {category_name} (tid={tid})")
        
        # 获取数据
        data_rows = get_bilibili_ranking_data(tid, category_name, target_count=10)
        
        if data_rows and len(data_rows) > 0:
            # 创建DataFrame
            df = pd.DataFrame(data_rows)
            
            # 保存到CSV
            filename = f'data/B站TOP-{category_name}-高质量.csv'
            df.to_csv(filename, index=False, encoding='utf_8_sig')
            successful_categories += 1
            print(f'✅ 写入成功: {filename}，共 {len(df)} 条高质量数据')
            
            # 显示数据统计
            avg_like_rate = df['点赞率'].mean()
            max_like_rate = df['点赞率'].max()
            print(f"📊 平均点赞率: {avg_like_rate:.4f}, 最高点赞率: {max_like_rate:.4f}")
            
            # 显示前3条数据
            print("🔍 前3条数据预览:")
            for i, row in df.head(3).iterrows():
                print(f"  {i+1}. {row['视频标题'][:25]}... - {row['作者']} - 点赞率:{row['点赞率']:.4f}")
        else:
            failed_categories += 1
            print(f"❌ {category_name} 未找到符合条件的高质量数据")
        
        # 添加延时避免请求过于频繁
        if category != categorys[-1]:  # 不是最后一个
            delay = random.uniform(2, 4)
            print(f"⏰ 等待 {delay:.1f} 秒...")
            time.sleep(delay)
    
    print(f"\n{'='*60}")
    print(f"🎉 数据爬取完成！")
    print(f"✅ 成功: {successful_categories} 个分类")
    print(f"❌ 失败: {failed_categories} 个分类")
    print(f"📁 生成的CSV文件保存在 data/ 目录")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
