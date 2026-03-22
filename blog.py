#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客系统 - 带侧边栏布局
"""

import os
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, flash, session
import mistune

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

BLOG_PASSWORD = 'xixi1314'
POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')
os.makedirs(POSTS_DIR, exist_ok=True)

CATEGORIES = {
    'ai': {'name': 'AI 新闻', 'icon': '🤖'},
    'robotics': {'name': '机器人行业', 'icon': '⚙️'},
    '': {'name': '全部文章', 'icon': '📝'}
}

markdown = mistune.create_markdown(plugins=['strikethrough', 'table', 'task_lists'])

@app.context_processor
def inject_session():
    return dict(session=session)

# 页面模板
PAGE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - 鱼塘主的博客</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🦞</text></svg>">
    <style>
        :root {
            --bg-primary: #0f0f23;
            --bg-secondary: #1a1a2e;
            --bg-card: #16213e;
            --bg-sidebar: #1a1a2e;
            --accent: #00d9ff;
            --accent-glow: rgba(0, 217, 255, 0.15);
            --accent-secondary: #7c3aed;
            --text-primary: #e2e8f0;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border: #2d3748;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.7;
            min-height: 100vh;
            background-image: 
                radial-gradient(ellipse at 20% 0%, rgba(0, 217, 255, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 100%, rgba(124, 58, 237, 0.06) 0%, transparent 50%),
                url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%232d3748' fill-opacity='0.15'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        }
        .layout { max-width: 1200px; margin: 0 auto; padding: 30px 20px; display: grid; grid-template-columns: 1fr 300px; gap: 30px; }
        @media (max-width: 900px) { .layout { grid-template-columns: 1fr; } .sidebar { order: -1; } }
        .main-content { min-width: 0; }
        header { margin-bottom: 30px; animation: fadeInDown 0.6s ease-out; }
        @keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
        .site-title { font-family: 'Noto Serif SC', serif; font-size: 1.6rem; font-weight: 600; background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 6px; }
        .subtitle { color: var(--text-muted); font-size: 0.85rem; }
        nav { display: flex; gap: 8px; margin-top: 20px; flex-wrap: wrap; }
        nav a { padding: 8px 18px; color: var(--text-secondary); text-decoration: none; border-radius: 100px; font-size: 0.85rem; font-weight: 500; transition: all 0.3s; border: 1px solid transparent; }
        nav a:hover { color: var(--text-primary); background: var(--bg-card); transform: translateY(-2px); }
        nav a.active { background: linear-gradient(135deg, var(--accent), var(--accent-secondary)); color: white; box-shadow: 0 4px 20px var(--accent-glow); }
        .sidebar { display: flex; flex-direction: column; gap: 20px; }
        .sidebar-card { background: var(--bg-sidebar); border: 1px solid var(--border); border-radius: 16px; padding: 24px; animation: fadeInUp 0.5s ease-out backwards; }
        .sidebar-card:nth-child(1) { animation-delay: 0.1s; }
        .sidebar-card:nth-child(2) { animation-delay: 0.2s; }
        .sidebar-card:nth-child(3) { animation-delay: 0.3s; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .sidebar-card h3 { font-family: 'Noto Serif SC', serif; font-size: 1rem; margin-bottom: 16px; color: var(--text-primary); display: flex; align-items: center; gap: 8px; }
        .profile-card { text-align: center; }
        .avatar { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, var(--accent), var(--accent-secondary)); margin: 0 auto 16px; display: flex; align-items: center; justify-content: center; font-size: 36px; box-shadow: 0 0 40px var(--accent-glow); }
        .profile-name { font-family: 'Noto Serif SC', serif; font-size: 1.1rem; font-weight: 600; margin-bottom: 4px; }
        .profile-bio { color: var(--text-muted); font-size: 0.8rem; line-height: 1.5; }
        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .stat-item { background: var(--bg-card); border-radius: 12px; padding: 16px; text-align: center; }
        .stat-value { font-size: 1.4rem; font-weight: 700; color: var(--accent); margin-bottom: 4px; }
        .stat-label { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
        .category-list { display: flex; flex-direction: column; gap: 8px; }
        .category-item { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; background: var(--bg-card); border-radius: 10px; text-decoration: none; color: var(--text-secondary); transition: all 0.2s; }
        .category-item:hover { transform: translateX(4px); background: var(--bg-primary); }
        .category-item .icon { font-size: 1.2rem; margin-right: 10px; }
        .category-item .name { flex: 1; font-size: 0.9rem; }
        .category-item .count { background: var(--bg-primary); padding: 2px 10px; border-radius: 100px; font-size: 0.75rem; color: var(--text-muted); }
        .post { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin-bottom: 16px; transition: all 0.3s ease; animation: fadeInUp 0.5s ease-out backwards; }
        .post:hover { transform: translateY(-4px); border-color: var(--accent); box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3), 0 0 0 1px var(--accent-glow); }
        .post h2 { font-family: 'Noto Serif SC', serif; font-size: 1.2rem; font-weight: 600; margin-bottom: 12px; }
        .post h2 a { color: var(--text-primary); text-decoration: none; transition: color 0.2s; }
        .post h2 a:hover { color: var(--accent); }
        .post-meta { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; font-size: 0.8rem; color: var(--text-muted); }
        .category-tag { padding: 4px 12px; border-radius: 100px; font-size: 0.75rem; font-weight: 500; }
        .category-ai { background: rgba(99, 102, 241, 0.2); color: #818cf8; }
        .category-robotics { background: rgba(236, 72, 153, 0.2); color: #f472b6; }
        .post-content { color: var(--text-secondary); font-size: 0.9rem; }
        .read-more { display: inline-flex; align-items: center; gap: 6px; margin-top: 14px; color: var(--accent); text-decoration: none; font-size: 0.85rem; font-weight: 500; transition: gap 0.2s; }
        .read-more:hover { gap: 10px; }
        .empty { text-align: center; padding: 60px 20px; color: var(--text-muted); }
        .empty-icon { font-size: 48px; margin-bottom: 16px; opacity: 0.5; }
        .login-container { max-width: 380px; margin: 80px auto; }
        .login-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px; padding: 40px; text-align: center; }
        .login-card h2 { font-family: 'Noto Serif SC', serif; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group input { width: 100%; padding: 14px 18px; background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; color: var(--text-primary); font-size: 1rem; }
        .form-group input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }
        .btn { display: inline-block; padding: 14px 32px; background: linear-gradient(135deg, var(--accent), var(--accent-secondary)); color: white; border: none; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.3s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px var(--accent-glow); }
        .category-header { background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin-bottom: 24px; display: flex; align-items: center; gap: 16px; }
        .category-header .icon { font-size: 32px; }
        .category-header h2 { font-family: 'Noto Serif SC', serif; font-size: 1.4rem; margin: 0; }
        .article-content { background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px; padding: 40px; }
        .article-content h1 { font-family: 'Noto Serif SC', serif; font-size: 1.8rem; margin-bottom: 16px; }
        .article-content h2 { font-family: 'Noto Serif SC', serif; font-size: 1.4rem; margin: 32px 0 16px; }
        .article-content code { background: var(--bg-secondary); padding: 3px 8px; border-radius: 6px; font-size: 0.9em; }
        .article-content pre { background: var(--bg-secondary); padding: 20px; border-radius: 12px; overflow-x: auto; margin: 16px 0; }
        .article-content pre code { background: none; padding: 0; }
        .article-content blockquote { border-left: 3px solid var(--accent); padding-left: 20px; margin: 20px 0; color: var(--text-secondary); font-style: italic; }
        .article-content img { max-width: 100%; border-radius: 12px; margin: 16px 0; }
        .back-link { display: inline-flex; align-items: center; gap: 8px; color: var(--text-secondary); text-decoration: none; margin-top: 30px; padding: 10px 20px; background: var(--bg-card); border-radius: 100px; transition: all 0.2s; }
        .back-link:hover { color: var(--accent); gap: 12px; }
        .new-post-container { max-width: 600px; margin: 0 auto; }
        .new-post-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px; padding: 40px; }
        .new-post-card h2 { font-family: 'Noto Serif SC', serif; margin-bottom: 30px; text-align: center; }
        .form-group label { display: block; margin-bottom: 8px; color: var(--text-secondary); font-size: 0.9rem; }
        .form-group select, .form-group textarea { width: 100%; padding: 14px 18px; background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; color: var(--text-primary); font-size: 0.95rem; font-family: inherit; resize: vertical; }
        .form-group textarea { min-height: 300px; }
        .form-group select:focus, .form-group textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }
        .form-actions { display: flex; gap: 12px; justify-content: center; margin-top: 24px; }
        .flash { padding: 14px 20px; border-radius: 12px; margin-bottom: 20px; }
        .flash-success { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .flash-error { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
        footer { text-align: center; padding: 30px 20px; color: var(--text-muted); font-size: 0.8rem; margin-top: 40px; border-top: 1px solid var(--border); }
    </style>
</head>
<body>
    <div class="layout">
        <div class="main-content">{{ content|safe }}</div>
        <aside class="sidebar">
            <div class="sidebar-card profile-card">
                <div class="avatar">🦞</div>
                <div class="profile-name">鱼塘主</div>
                <div class="profile-bio">探索AI与机器人前沿<br>记录每日行业动态</div>
            </div>
            <div class="sidebar-card">
                <h3>📊 数据统计</h3>
                <div class="stats-grid">
                    <div class="stat-item"><div class="stat-value">{{ stats.total_posts }}</div><div class="stat-label">文章</div></div>
                    <div class="stat-item"><div class="stat-value">{{ stats.ai_posts }}</div><div class="stat-label">AI</div></div>
                    <div class="stat-item"><div class="stat-value">{{ stats.robotics_posts }}</div><div class="stat-label">机器人</div></div>
                    <div class="stat-item"><div class="stat-value">{{ stats.total_days }}</div><div class="stat-label">天数</div></div>
                </div>
            </div>
            <div class="sidebar-card">
                <h3>🏷️ 文章分类</h3>
                <div class="category-list">
                    <a href="/" class="category-item"><span class="icon">📝</span><span class="name">全部文章</span><span class="count">{{ stats.total_posts }}</span></a>
                    <a href="/?category=ai" class="category-item"><span class="icon">🤖</span><span class="name">AI 新闻</span><span class="count">{{ stats.ai_posts }}</span></a>
                    <a href="/?category=robotics" class="category-item"><span class="icon">⚙️</span><span class="name">机器人行业</span><span class="count">{{ stats.robotics_posts }}</span></a>
                </div>
            </div>
        </aside>
    </div>
    <footer><p>🦞 鱼塘主的博客 · 用心记录AI与机器人行业动态</p></footer>
</body>
</html>
'''

def get_stats():
    posts = []
    if os.path.exists(POSTS_DIR):
        for filename in os.listdir(POSTS_DIR):
            if filename.endswith('.md'):
                cat = 'ai' if 'ai' in filename.lower() else 'robotics' if '机器人' in filename else ''
                posts.append({'category': cat})
    
    total = len(posts)
    ai = len([p for p in posts if p['category'] == 'ai'])
    robotics = len([p for p in posts if p['category'] == 'robotics'])
    
    dates = []
    if os.path.exists(POSTS_DIR):
        for f in os.listdir(POSTS_DIR):
            if f.endswith('.md'):
                try:
                    dates.append(f.split('-')[1][:8])
                except:
                    pass
    days = len(set(dates))
    
    return {'total_posts': total, 'ai_posts': ai, 'robotics_posts': robotics, 'total_days': days}


@app.route('/')
def index():
    category = request.args.get('category', '')
    posts = []
    
    if os.path.exists(POSTS_DIR):
        for filename in os.listdir(POSTS_DIR):
            if filename.endswith('.md'):
                filepath = os.path.join(POSTS_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                date = ''
                cat = 'ai' if 'ai' in filename.lower() else 'robotics' if '机器人' in filename else ''
                
                for line in content.split('\n'):
                    if line.startswith('> 发布时间：'):
                        date = line.replace('> 发布时间：', '').strip()
                
                if category and cat != category:
                    continue
                
                title = filename[:-3].replace('AI行业新闻-', 'AI新闻 ').replace('机器人行业新闻-', '机器人 ')
                
                posts.append({
                    'title': title, 'date': date, 'category': cat,
                    'filename': filename
                })
    
    posts.sort(key=lambda x: x['date'], reverse=True)
    stats = get_stats()
    cat_name = CATEGORIES.get(category, {}).get('name', '全部文章')
    cat_icon = CATEGORIES.get(category, {}).get('icon', '📝')
    
    html = f'''
    <header>
        <h1 class="site-title">{cat_name}</h1>
        <p class="subtitle">探索AI与机器人前沿动态</p>
        <nav>
            <a href="/" {"class='active'" if not category else ""}>全部</a>
            <a href="/?category=ai" {"class='active'" if category == 'ai' else ""}>🤖 AI</a>
            <a href="/?category=robotics" {"class='active'" if category == 'robotics' else ""}>⚙️ 机器人</a>
        </nav>
    </header>
    '''
    
    if category:
        html += f'<div class="category-header"><span class="icon">{cat_icon}</span><h2>{cat_name}</h2></div>'
    
    if posts:
        for post in posts:
            cat_class = 'category-ai' if post['category'] == 'ai' else 'category-robotics'
            cat_icon = '🤖' if post['category'] == 'ai' else '⚙️'
            cat_name = 'AI' if post['category'] == 'ai' else '机器人'
            html += f'''
            <article class="post">
                <h2><a href="/post/{post['filename']}">{post['title']}</a></h2>
                <div class="post-meta">
                    <span>📅 {post['date']}</span>
                    <span class="category-tag {cat_class}">{cat_icon} {cat_name}</span>
                </div>
                <a href="/post/{post['filename']}" class="read-more">阅读全文 →</a>
            </article>
            '''
    else:
        html += '<div class="empty"><div class="empty-icon">📭</div><p>暂无文章</p></div>'
    
    return render_template_string(PAGE_TEMPLATE, title=cat_name, content=html, stats=stats)


@app.route('/post/<filename>')
def post(filename):
    filepath = os.path.join(POSTS_DIR, filename)
    if not os.path.exists(filepath):
        return "文章不存在", 404
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title = filename[:-3]
    date = ''
    for line in content.split('\n'):
        if line.startswith('> 发布时间：'):
            date = line.replace('> 发布时间：', '').strip()
    
    html_content = markdown(content)
    
    if 'ai' in filename.lower():
        category, cat_name, cat_icon = 'ai', 'AI 新闻', '🤖'
    elif '机器人' in filename.lower():
        category, cat_name, cat_icon = 'robotics', '机器人行业', '⚙️'
    else:
        category, cat_name, cat_icon = '', '文章', '📝'
    
    cat_class = 'category-ai' if category == 'ai' else 'category-robotics'
    
    html = f'''
    <a href="/" class="back-link">← 返回首页</a>
    <article class="article-content">
        <h1>{title}</h1>
        <div class="post-meta" style="margin-bottom: 30px;">
            <span>📅 {date}</span>
            <span class="category-tag {cat_class}">{cat_icon} {cat_name}</span>
        </div>
        {html_content}
    </article>
    '''
    
    return render_template_string(PAGE_TEMPLATE, title=title, content=html, stats=get_stats())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == BLOG_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('密码错误', 'error')
    
    html = '''
    <div class="login-container">
        <div class="login-card">
            <h2>🔐 管理登录</h2>
            <form method="post">
                <div class="form-group">
                    <input type="password" name="password" placeholder="请输入管理密码" required>
                </div>
                <button type="submit" class="btn">登录</button>
            </form>
        </div>
    </div>
    '''
    return render_template_string(PAGE_TEMPLATE, title='登录', content=html, stats=get_stats())


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    posts = []
    if os.path.exists(POSTS_DIR):
        for filename in sorted(os.listdir(POSTS_DIR), reverse=True):
            if filename.endswith('.md'):
                filepath = os.path.join(POSTS_DIR, filename)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                posts.append({'filename': filename, 'date': mtime.strftime('%Y-%m-%d %H:%M')})
    
    html = f'''
    <header>
        <h1 class="site-title">📝 文章管理</h1>
        <nav>
            <a href="/">🏠 返回首页</a>
            <a href="/admin/new">✏️ 写新文章</a>
            <a href="/logout">🚪 退出登录</a>
        </nav>
    </header>
    '''
    
    for post in posts:
        html += f'''
        <div class="post" style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="font-size: 1rem;">{post['filename']}</h2>
                <div class="post-meta"><span>📅 {post['date']}</span></div>
            </div>
            <a href="/admin/delete/{post['filename']}" style="color: #f87171; text-decoration: none;">🗑️ 删除</a>
        </div>
        '''
    
    return render_template_string(PAGE_TEMPLATE, title='文章管理', content=html, stats=get_stats())


@app.route('/admin/new', methods=['GET', 'POST'])
def new_post():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '')
        category = request.form.get('category', 'ai')
        content = request.form.get('content', '')
        
        if title and content:
            date_str = datetime.now().strftime('%Y-%m-%d')
            filename = f'AI行业新闻-{date_str}.md' if category == 'ai' else f'机器人行业新闻-{date_str}.md'
            
            full_content = f'''# {title}

> 发布时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 新闻摘要

{content}

---
*🤖 每日 AI 行业新闻自动更新*
'''
            
            with open(os.path.join(POSTS_DIR, filename), 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            flash('文章发布成功！', 'success')
            return redirect(url_for('admin'))
    
    html = '''
    <a href="/admin" class="back-link">← 返回管理</a>
    <div class="new-post-container">
        <div class="new-post-card">
            <h2>✏️ 发布新文章</h2>
            <form method="post">
                <div class="form-group">
                    <label>文章标题</label>
                    <input type="text" name="title" placeholder="请输入文章标题" required>
                </div>
                <div class="form-group">
                    <label>分类</label>
                    <select name="category">
                        <option value="ai">🤖 AI 新闻</option>
                        <option value="robotics">⚙️ 机器人行业</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>文章内容 (Markdown)</label>
                    <textarea name="content" placeholder="请输入文章内容" required></textarea>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn">发布文章</button>
                </div>
            </form>
        </div>
    </div>
    '''
    return render_template_string(PAGE_TEMPLATE, title='发布文章', content=html, stats=get_stats())


@app.route('/admin/delete/<filename>')
def delete_post(filename):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    filepath = os.path.join(POSTS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f'已删除 {filename}', 'success')
    
    return redirect(url_for('admin'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
