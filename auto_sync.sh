#!/bin/bash
# 新闻生成后自动同步到 GitHub
# 供定时任务调用

set -e

# 同步到 GitHub
/root/my-blog/sync_to_github.sh

echo "新闻已同步到 GitHub: https://github.com/shentsung/my-blog"