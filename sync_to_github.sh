#!/bin/bash
# 博客文章自动同步脚本
# 在更新文章后运行此脚本，将更改推送到 GitHub

BLOG_DIR="/root/my-blog"

cd "$BLOG_DIR" || exit 1

# 先拉取远程更新，避免冲突
echo "正在拉取远程更新..."
git pull origin main --rebase

# 检查是否有更改
if git diff --quiet && git diff --staged --quiet; then
    echo "没有需要提交的更改"
    exit 0
fi

# 获取当前日期
DATE=$(date +%Y-%m-%d)

# 添加所有更改
git add -A

# 提交
git commit -m "更新博客文章 - $DATE"

# 推送到 GitHub
git push origin main

echo "博客文章已同步到 GitHub"