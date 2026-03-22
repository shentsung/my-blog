# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Blog

This is a Flask-based server-side blog.

```bash
# Install dependencies
pip install flask mistune

# Run locally
python blog.py

# Or use the start script (runs in background, logs to /var/log/blog.log)
./start.sh

# Access at http://localhost:5000
```

## Architecture

**Flask monolithic application** - Single-file server with inline templates.

- **blog.py**: Flask application with routes, templates, and logic in one file
- **posts/**: Markdown files for blog content (auto-created on first run)
- **start.sh**: Production startup script (background process)

## Tech Stack

- **Framework**: Flask (Python 3)
- **Template**: Jinja2 (inline via `render_template_string`)
- **Markdown Parser**: mistune (with strikethrough, table, task_lists plugins)
- **Styling**: Dark theme CSS (inline in template)
- **Authentication**: Flask session-based (hardcoded password in `BLOG_PASSWORD`)

## Data Model

Posts are stored as `.md` files in `posts/` directory with naming convention:
- `AI行业新闻-{YYYY-MM-DD}.md` → categorized as AI
- `机器人行业新闻-{YYYY-MM-DD}.md` → categorized as Robotics

Each post has a metadata line for publish date:
```markdown
> 发布时间：{YYYY-MM-DD HH:MM}
```

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home with post list, filtered by `?category=ai\|robotics` |
| `/post/<filename>` | Full article view |
| `/login` | Admin authentication |
| `/admin` | Post management (requires login) |
| `/admin/new` | Create new post (requires login) |
| `/admin/delete/<filename>` | Delete post (requires login) |
| `/logout` | Clear session |

## File Naming & Category Detection

Category is determined by filename substring (case-insensitive):
- Contains `"ai"` → AI category
- Contains `"机器人"` → Robotics category

When creating posts via `/admin/new`, filename is auto-generated based on category selection.
