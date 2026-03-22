# 鱼塘主的博客

基于 Flask 的个人博客系统，展示 AI 行业新闻和机器人行业新闻。

## 技术栈

- **后端**: Flask (Python)
- **模板引擎**: Jinja2
- **Markdown 渲染**: mistune
- **样式**: 内置 CSS（深色主题）

## 目录结构

```
my-blog/
├── blog.py          # Flask 主程序
├── posts/           # Markdown 文章目录
│   ├── AI行业新闻-*.md
│   └── 机器人行业新闻-*.md
├── start.sh         # 启动脚本
└── README.md
```

## 运行

```bash
# 安装依赖
pip install flask mistune

# 启动服务
python blog.py
# 或
./start.sh

# 访问
# http://localhost:5000
```

## 文章分类

- 🤖 AI 新闻：每日 AI 行业动态
- ⚙️ 机器人行业：机器人领域新闻

## 自动更新

博客文章每天自动更新并推送到 GitHub。

---

*由小龙虾 🦞 维护*