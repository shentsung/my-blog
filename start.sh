#!/bin/bash
# 启动博客服务器

cd "$(dirname "$0")"
echo "Starting blog server at http://localhost:8000"
echo "Press Ctrl+C to stop"
python3 -m http.server 8000