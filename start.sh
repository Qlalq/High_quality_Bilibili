#!/bin/bash
# B站高质量视频爬虫 - 一键启动脚本
# 支持分类排行榜和热门页面两种模式

echo "🔥 B站高质量视频爬虫 v2.0"
echo "=================================="
echo ""
echo "请选择爬取模式："
echo "1) 分类排行榜模式 (20个分类，每类最多100个视频)"
echo "2) 热门页面模式 (不限分类，可获取更多视频)"
echo "3) 同时运行两种模式"
echo ""
read -p "请输入选择 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "🎯 启动分类排行榜爬虫..."
        python3 bilibili_crawler.py
        ;;
    2)
        echo ""
        read -p "请输入目标视频数量 (默认500): " target_count
        target_count=${target_count:-500}
        echo "🌟 启动热门页面爬虫，目标数量: $target_count"
        python3 popular_crawler.py $target_count
        ;;
    3)
        echo ""
        echo "🚀 同时运行两种模式..."
        echo ""
        echo "📊 第一步：运行分类排行榜爬虫..."
        python3 bilibili_crawler.py
        
        echo ""
        echo "🌟 第二步：运行热门页面爬虫..."
        read -p "请输入热门页面目标数量 (默认500): " target_count
        target_count=${target_count:-500}
        python3 popular_crawler.py $target_count
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "📁 查看生成的数据文件："
echo "分类排行榜数据:"
ls -la data/ranking/*.csv | tail -5
echo "热门页面数据:"
ls -la data/popular/*.csv | tail -5

echo ""
echo "🎉 爬取任务完成！"
echo "💡 提示：热门页面模式可以获取更多视频数据，突破排行榜100视频限制"
