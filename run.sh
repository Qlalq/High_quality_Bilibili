#!/bin/bash

# B站高质量视频爬虫启动脚本

echo "🚀 启动B站高质量视频爬虫..."
echo "================================================"

cd "$(dirname "$0")"

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到Python环境"
    exit 1
fi

# 检查依赖
python -c "import pandas, requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  缺少依赖，正在安装..."
    pip install pandas requests
fi

# 运行爬虫
echo "🎯 开始爬取高质量视频数据..."
python bilibili_crawler.py

echo ""
echo "================================================"
echo "🎉 爬取完成！数据保存在 data/ 目录中"
echo "📊 查看数据: ls -la data/"
echo "📖 项目说明: cat README.md"
