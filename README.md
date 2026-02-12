# 个人博客系统

一个简约风格的 Markdown 个人博客。

## 📁 文件结构

```
my-blog/
├── index.html      # 主页面
├── style.css       # 样式文件
├── app.js          # JavaScript 逻辑
├── posts/          # 博客文章目录
│   └── welcome.md  # 示例文章
└── README.md       # 说明文档
```

## ✨ 功能特点

- ✅ 简约设计风格
- ✅ Markdown 编辑支持
- ✅ 侧边栏按日期排序显示
- ✅ 响应式设计（支持手机）
- ✅ 数据保存在本地（LocalStorage）
- ✅ 无需服务器，直接浏览器打开

## 🚀 使用方法

### 方法一：直接打开（推荐）

1. 进入 `my-blog` 目录
2. 双击打开 `index.html`
3. 开始写博客！

### 方法二：本地服务器

```bash
cd my-blog
python3 -m http.server 8000
```

然后访问：http://localhost:8000

## 📝 使用指南

### 1. 新建文章

点击页面顶部的"➕ 新建文章"按钮。

### 2. 编辑文章

- 输入文章标题
- 使用 Markdown 编写内容
- 支持：标题、列表、代码、链接等

### 3. 保存文章

点击"💾 保存文章"按钮。

### 4. 阅读文章

点击侧边栏的文章标题即可阅读。

## 🔧 技术栈

- HTML5 + CSS3
- Vanilla JavaScript
- Marked.js（Markdown 渲染）
- LocalStorage（数据存储）

## 📱 响应式设计

博客完美支持手机、平板和桌面电脑访问。

## ⚠️ 注意

- 文章数据保存在浏览器本地，清理缓存会丢失
- 如需长期保存，建议定期备份数据
- 不支持图片上传（仅支持图片链接）

## 📄 License

MIT License