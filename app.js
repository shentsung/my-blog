// 博客应用 JavaScript

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    loadPosts();
});

// 加载所有文章
function loadPosts() {
    const posts = getAllPosts();
    
    // 按日期排序（最新的在前）
    posts.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    // 渲染侧边栏列表
    renderPostList(posts);
    
    // 如果有文章，显示第一篇
    if (posts.length > 0) {
        displayPost(posts[0]);
    }
}

// 渲染文章列表
function renderPostList(posts) {
    const list = document.getElementById('post-list');
    list.innerHTML = '';
    
    posts.forEach(post => {
        const li = document.createElement('li');
        li.innerHTML = `
            ${post.title}
            <span class="post-date">${formatDate(post.date)}</span>
        `;
        li.onclick = () => displayPost(post);
        list.appendChild(li);
    });
}

// 显示文章内容
function displayPost(post) {
    document.getElementById('post-content').innerHTML = `
        <h1>${post.title}</h1>
        <div class="post-meta">📅 ${formatDate(post.date)}</div>
        <div class="markdown-body">${marked.parse(post.content)}</div>
    `;
    
    // 更新侧边栏高亮
    document.querySelectorAll('#post-list li').forEach(li => {
        li.classList.remove('active');
    });
    
    // 显示编辑器部分（用于新建）
    document.getElementById('viewer-section').style.display = 'block';
    document.getElementById('editor-section').style.display = 'none';
}

// 显示编辑器
function showEditor() {
    document.getElementById('editor-section').style.display = 'block';
    document.getElementById('viewer-section').style.display = 'none';
    document.getElementById('post-title').value = '';
    document.getElementById('markdown-content').value = '';
    document.getElementById('post-title').focus();
}

// 取消编辑
function cancelEdit() {
    document.getElementById('editor-section').style.display = 'none';
    document.getElementById('viewer-section').style.display = 'block';
}

// 保存文章
function savePost() {
    const title = document.getElementById('post-title').value.trim();
    const content = document.getElementById('markdown-content').value.trim();
    
    if (!title || !content) {
        alert('请填写标题和内容！');
        return;
    }
    
    const post = {
        id: Date.now().toString(),
        title: title,
        content: content,
        date: new Date().toISOString()
    };
    
    savePostToStorage(post);
    
    // 重新加载
    loadPosts();
    
    // 显示新文章
    displayPost(post);
    
    alert('文章保存成功！🎉');
}

// LocalStorage 操作
function getAllPosts() {
    const posts = localStorage.getItem('blog_posts');
    return posts ? JSON.parse(posts) : [];
}

function savePostToStorage(post) {
    const posts = getAllPosts();
    posts.push(post);
    localStorage.setItem('blog_posts', JSON.stringify(posts));
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 添加示例文章（如果没有任何文章）
function addSamplePost() {
    const posts = getAllPosts();
    if (posts.length === 0) {
        const samplePost = {
            id: '1',
            title: '欢迎来到我的博客',
            content: `# 欢迎！

这是一个使用 Markdown 的简单博客。

## 功能特点

- ✏️ 简单编辑
- 📅 自动按日期排序
- 🎨 简约设计
- 💾 本地存储

祝你使用愉快！`,
            date: new Date().toISOString()
        };
        savePostToStorage(samplePost);
    }
}

// 初始化示例文章
addSamplePost();