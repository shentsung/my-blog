#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将新闻写入博客并自动同步到 GitHub
"""

import os
import sys
import subprocess
from datetime import datetime

# 博客文章目录 (my-blog 项目)
POSTS_DIR = '/root/my-blog/posts'
MY_BLOG_DIR = '/root/my-blog'
os.makedirs(POSTS_DIR, exist_ok=True)

def sync_to_github():
    """同步到 GitHub"""
    try:
        # 切换到 my-blog 目录
        os.chdir(MY_BLOG_DIR)
        
        # 先拉取远程更新
        result = subprocess.run(
            ['git', 'pull', 'origin', 'main', '--rebase'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # 检查是否有更改
        result = subprocess.run(
            ['git', 'diff', '--quiet'],
            capture_output=True
        )
        staged_result = subprocess.run(
            ['git', 'diff', '--staged', '--quiet'],
            capture_output=True
        )
        
        if result.returncode == 0 and staged_result.returncode == 0:
            print("ℹ️ 没有需要提交的更改")
            return True
        
        # 添加所有更改
        subprocess.run(['git', 'add', '-A'], check=True)
        
        # 提交
        date_str = datetime.now().strftime('%Y-%m-%d')
        subprocess.run(
            ['git', 'commit', '-m', f'更新博客文章 - {date_str}'],
            check=True
        )
        
        # 推送到 GitHub
        result = subprocess.run(
            ['git', 'push', 'origin', 'main'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ 已同步到 GitHub")
            return True
        else:
            print(f"❌ 推送失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Git 操作超时")
        return False
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return False

def save_news_to_blog(news_content, title=None, category="机器人行业"):
    """将新闻内容保存为博客文章"""
    
    if title is None:
        title = f"{category}新闻 - {datetime.now().strftime('%Y-%m-%d')}"
    
    # 生成文件名
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"{category}新闻-{date_str}.md"
    filepath = os.path.join(POSTS_DIR, filename)
    
    # 构建 Markdown 内容
    content = f"""# {title}

> *发布时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*

{news_content}

---
*📰 每日行业新闻自动更新*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

if __name__ == '__main__':
    # 从命令行参数或 stdin 获取新闻内容
    if len(sys.argv) > 1:
        # 第一个参数可能是分类
        if len(sys.argv) > 2 and sys.argv[1] in ['AI', '机器人']:
            category = sys.argv[1]
            news_content = ' '.join(sys.argv[2:])
        else:
            category = "机器人行业"
            news_content = ' '.join(sys.argv[1:])
    else:
        # 从 stdin 读取
        category = "机器人行业"
        news_content = sys.stdin.read()
    
    if news_content.strip():
        filepath = save_news_to_blog(news_content, category=category)
        print(f"✅ 新闻已保存到: {filepath}")
        
        # 同步到 GitHub
        sync_to_github()
    else:
        print("❌ 没有新闻内容")
        sys.exit(1)