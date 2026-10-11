# windbellbj.github.io

我的个人博客，基于 Jekyll 构建，托管在 GitHub Pages，通过 https://windbellbj.github.io 访问。

## 板块

- **传统开发**（`/traditional-development/`）：后端、工程实践等传统开发内容，文章打上 `传统开发` 标签即归入该板块。
- **AI 开发**（`/ai-development/`）：AI 辅助编程、LLM 应用、MCP、Agent 等内容，文章打上 `AI开发` 标签即归入该板块。
- **AI 新资讯**（`/ai-news/`）：由 GitHub Actions 定时自动抓取热门 AI Agent、Claude Skills、MCP servers 等新项目，生成周刊文章。每篇资讯含功能说明、链接和一段可整段复制的「发给 AI 的落地指令」，把文章页面发给任意 AI 即可引导它完成该技能的落地。

板块页在 `section/` 目录下，按文章标签聚合，新增板块照此复制一个页面并在 `_includes/nav.html` 加入口即可。

## 本地运行

```bash
bundle install
bundle exec jekyll serve
```

浏览器打开 http://127.0.0.1:4000 。本地 Jekyll 版本通过 Gemfile 锁定为 3.9.x，与 GitHub Pages 保持一致。

## 写文章

Markdown 文件放在 `_posts/`，文件名格式 `YYYY-MM-DD-标题.markdown`，开头 front matter：

```yaml
---
layout: post
title: "文章标题"
subtitle: "副标题（可选）"
date: 2026-10-11 12:00:00
author: "XinLong Li"
header-img: "img/post-bg-hello.svg"
tags:
    - AI开发
---
```

## AI 新资讯自动抓取

抓取脚本：`scripts/ai_news_fetch.py`（仅依赖 Python 3 标准库），配置文件：`scripts/ai_news_config.json`。

数据来源：GitHub Search API（新建热门仓库）、Hacker News（Algolia API）、Product Hunt（需 Token）、配置文件中的社区关注仓库。

- **定时执行**：`.github/workflows/ai-news.yml`，默认每周一北京时间 09:00 运行，自动提交生成的周刊。改频率只需修改 workflow 中的 cron 表达式。
- **手动执行**：GitHub 仓库 Actions 页面 →「AI 新资讯抓取」→ Run workflow，可填回溯天数。
- **本地试跑**：`python scripts/ai_news_fetch.py --dry-run`（只打印不写文件）；正式运行去掉 `--dry-run`。

可调配置（`scripts/ai_news_config.json`）：

| 配置项 | 说明 |
| --- | --- |
| `lookback_days` | 每次抓取回溯天数 |
| `min_github_stars` / `hn_min_points` | GitHub 星标 / HN 点数入选阈值 |
| `max_items_per_source` | 每个来源最多收录条数 |
| `github_queries` / `hn_queries` | 抓取关键词与 topic |
| `community_repos` | 关注的社区仓库列表，有更新时收录 |

说明：

- GitHub Actions 运行时自动注入 `GITHUB_TOKEN`，无 API 限速问题；本地未认证调用 GitHub API 有较低限速，必要时可设置同名环境变量。
- Product Hunt 为可选来源，在仓库 Secrets 配置 `PRODUCTHUNT_TOKEN` 后生效，未配置时自动跳过。
- 已发布过的条目通过 `scripts/ai_news_state.json` 去重，该文件由 Actions 自动提交。

## License

博客内容版权归本人所有；站点代码基于 Apache License 2.0 模板改造，许可证见 [LICENSE](LICENSE)。
