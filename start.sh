#!/bin/bash
# 博客启动脚本

cd "$(dirname "$0")"
nohup python blog.py > /var/log/blog.log 2>&1 &
echo "博客服务已启动，访问 http://localhost:5000"