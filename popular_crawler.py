#!/usr/bin/env python3
"""
B站热门视频高质量爬虫 - 突破排行榜限制
Author: GitHub Copilot
Version: 1.0
"""

import requests
import pandas as pd
import time
import random
import sys
import os
from config import *

class BilibiliPopularCrawler:
    def __init__(self):
        """初始化爬虫"""
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.data_dir = POPULAR_DIR
        
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
    def delay(self):
        """随机延迟"""
        delay_time = random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
        time.sleep(delay_time)
        
    def get_popular_videos(self, target_count=500, max_pages=50):
        """
        获取热门视频数据
        
        Args:
            target_count: 目标视频数量
            max_pages: 最大页数限制
            
        Returns:
            list: 视频数据列表
        """
        all_videos = []
        page = 1
        empty_page_count = 0  # 连续空页计数器
        
        print(f"🚀 开始爬取热门视频，目标数量: {target_count}")
        print(f"⚙️  停止条件: 连续{MAX_EMPTY_PAGES}页无有效数据时停止")
        
        while len(all_videos) < target_count and page <= max_pages:
            print(f"📄 正在爬取第{page}页...")
            
            url = f"{BASE_URL}{POPULAR_API}"
            params = {
                'ps': 20,  # 每页20个视频
                'pn': page
            }
            
            try:
                response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
                
                if response.status_code != 200:
                    print(f"❌ 请求失败，状态码: {response.status_code}")
                    empty_page_count += 1
                    if empty_page_count >= MAX_EMPTY_PAGES:
                        print(f"📭 连续{MAX_EMPTY_PAGES}页请求失败，停止爬取")
                        break
                    page += 1
                    self.delay()
                    continue
                    
                data = response.json()
                
                if data.get('code') != 0:
                    print(f"❌ API错误: {data.get('message')}")
                    empty_page_count += 1
                    if empty_page_count >= MAX_EMPTY_PAGES:
                        print(f"📭 连续{MAX_EMPTY_PAGES}页API错误，停止爬取")
                        break
                    page += 1
                    self.delay()
                    continue
                    
                video_list = data.get('data', {}).get('list', [])
                
                if not video_list:
                    empty_page_count += 1
                    print(f"📭 第{page}页无原始数据，连续空页计数: {empty_page_count}/{MAX_EMPTY_PAGES}")
                    if empty_page_count >= MAX_EMPTY_PAGES:
                        print(f"📭 连续{MAX_EMPTY_PAGES}页无数据，停止爬取")
                        break
                    page += 1
                    self.delay()
                    continue
                    
                # 处理视频数据
                page_videos = []
                for video in video_list:
                    processed_video = self.process_video_data(video)
                    if processed_video:
                        page_videos.append(processed_video)
                
                # 检查是否获取到有效视频
                if not page_videos:
                    empty_page_count += 1
                    print(f"📭 第{page}页无高质量视频（点赞率<{LIKE_RATE_THRESHOLD}），连续空页计数: {empty_page_count}/{MAX_EMPTY_PAGES}")
                    if empty_page_count >= MAX_EMPTY_PAGES:
                        print(f"📭 连续{MAX_EMPTY_PAGES}页无有效视频，停止爬取")
                        break
                else:
                    # 重置连续空页计数器
                    empty_page_count = 0
                
                all_videos.extend(page_videos)
                
                print(f"✅ 第{page}页获取 {len(page_videos)} 个视频，总计: {len(all_videos)}")
                
                page += 1
                self.delay()
                
            except Exception as e:
                print(f"❌ 爬取第{page}页时出错: {e}")
                empty_page_count += 1
                if empty_page_count >= MAX_EMPTY_PAGES:
                    print(f"📭 连续{MAX_EMPTY_PAGES}页出错，停止爬取")
                    break
                page += 1
                self.delay()
        
        print(f"🎉 爬取完成！共获取 {len(all_videos)} 个视频")
        return all_videos
    
    def process_video_data(self, video):
        """
        处理单个视频数据
        
        Args:
            video: 原始视频数据
            
        Returns:
            dict: 处理后的视频数据
        """
        try:
            # 基础信息
            bvid = video.get('bvid', '')
            title = video.get('title', '').strip()
            
            # 作者信息
            owner = video.get('owner', {})
            author = owner.get('name', '')
            
            # 统计数据
            stat = video.get('stat', {})
            view = stat.get('view', 0)
            like = stat.get('like', 0)
            coin = stat.get('coin', 0)
            favorite = stat.get('favorite', 0)
            share = stat.get('share', 0)
            reply = stat.get('reply', 0)
            danmaku = stat.get('danmaku', 0)
            
            # 其他信息
            duration = video.get('duration', 0)
            pubdate = video.get('pubdate', 0)
            pic = video.get('pic', '')
            desc = video.get('desc', '').strip()
            
            # 计算点赞率
            like_rate = like / view if view > 0 else 0
            
            # 只保留高质量视频
            if like_rate < LIKE_RATE_THRESHOLD:
                return None
            
            return {
                'bvid': bvid,
                'title': title,
                'author': author,
                'view': view,
                'like': like,
                'coin': coin,
                'favorite': favorite,
                'share': share,
                'reply': reply,
                'danmaku': danmaku,
                'like_rate': round(like_rate, 4),
                'duration': duration,
                'pubdate': pubdate,
                'pic': pic,
                'desc': desc[:200],  # 限制描述长度
                'url': f'https://www.bilibili.com/video/{bvid}'
            }
            
        except Exception as e:
            print(f"❌ 处理视频数据时出错: {e}")
            return None
    
    def save_to_csv(self, videos, filename):
        """
        保存数据到CSV文件
        
        Args:
            videos: 视频数据列表
            filename: 文件名
        """
        if not videos:
            print("❌ 无数据可保存")
            return
            
        df = pd.DataFrame(videos)
        
        # 按点赞率排序
        df = df.sort_values('like_rate', ascending=False)
        
        # 添加排名
        df['rank'] = range(1, len(df) + 1)
        
        # 重新排列列顺序
        columns = ['rank', 'title', 'author', 'view', 'like', 'like_rate', 
                  'coin', 'favorite', 'share', 'reply', 'danmaku', 
                  'duration', 'url', 'bvid', 'desc']
        df = df[columns]
        
        # 保存文件
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        
        print(f"💾 数据已保存到: {filepath}")
        print(f"📊 共保存 {len(df)} 个高质量视频")
        
        # 显示统计信息
        print(f"\n📈 质量统计:")
        print(f"平均点赞率: {df['like_rate'].mean():.4f}")
        print(f"最高点赞率: {df['like_rate'].max():.4f}")
        print(f"平均播放量: {df['view'].mean():,.0f}")
        print(f"平均点赞数: {df['like'].mean():,.0f}")
    
    def run(self, target_count=None):
        """
        运行爬虫
        
        Args:
            target_count: 目标视频数量，默认使用配置文件值
        """
        if target_count is None:
            target_count = TARGET_COUNT_POPULAR
            
        print(f"🎯 开始爬取B站热门高质量视频...")
        print(f"⚙️  配置: 点赞率阈值 {LIKE_RATE_THRESHOLD}, 目标数量 {target_count}")
        
        # 获取视频数据
        videos = self.get_popular_videos(target_count)
        
        if videos:
            # 保存数据
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"B站热门-高质量-{timestamp}.csv"
            self.save_to_csv(videos, filename)
        else:
            print("❌ 未获取到任何视频数据")

def main():
    """主函数"""
    print("🔥 B站热门视频高质量爬虫 v1.0")
    print("=" * 50)
    
    try:
        crawler = BilibiliPopularCrawler()
        
        # 可以通过命令行参数指定目标数量
        target_count = None
        if len(sys.argv) > 1:
            try:
                target_count = int(sys.argv[1])
                print(f"📋 使用命令行参数，目标数量: {target_count}")
            except ValueError:
                print(f"❌ 无效的数量参数: {sys.argv[1]}")
                sys.exit(1)
        
        crawler.run(target_count)
        print("\n🎉 爬取任务完成！")
        
    except KeyboardInterrupt:
        print("\n⏹️  用户中断爬取")
    except Exception as e:
        print(f"\n❌ 爬取过程中出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
