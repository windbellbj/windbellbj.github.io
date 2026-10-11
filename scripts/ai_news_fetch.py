#!/usr/bin/env python3
# AI 新资讯周刊抓取脚本，仅依赖 Python 标准库
# 来源：GitHub Search API、Hacker News(Algolia)、Product Hunt(可选，需 Token)、社区关注清单
import argparse
import glob
import json
import os
import sys
import time
from datetime import datetime, timedelta
from urllib import parse, request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def log(msg):
    print("[ai-news] " + msg, file=sys.stderr, flush=True)


def http_json(url, headers=None, payload=None, timeout=25, retries=2):
    data = None
    headers = {"User-Agent": "ai-news-bot/1.0", **(headers or {})}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=data, headers=headers)
    last_err = None
    for i in range(retries + 1):
        try:
            with request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            time.sleep(2 * (i + 1))
    raise last_err


def github_headers():
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    return headers


def fetch_github(cfg, since):
    items = {}
    since_str = since.strftime("%Y-%m-%d")
    queries = cfg["github_queries"]
    authenticated = bool(os.environ.get("GITHUB_TOKEN"))
    for idx, q in enumerate(queries):
        url = "https://api.github.com/search/repositories?" + parse.urlencode({
            "q": "%s created:>=%s" % (q, since_str),
            "sort": "stars",
            "order": "desc",
            "per_page": 20,
        })
        try:
            data = http_json(url, github_headers())
        except Exception as e:
            log("GitHub 查询失败(%s)：%s" % (q, e))
            continue
        for repo in data.get("items", []):
            if repo["stargazers_count"] < cfg["min_github_stars"]:
                continue
            items[repo["full_name"]] = {
                "kind": "github",
                "name": repo["full_name"],
                "url": repo["html_url"],
                "desc": (repo.get("description") or "").strip(),
                "stars": repo["stargazers_count"],
                "language": repo.get("language") or "-",
                "created": repo["created_at"][:10],
            }
        if idx < len(queries) - 1:
            time.sleep(3 if authenticated else 8)
    return sorted(items.values(), key=lambda x: -x["stars"])[: cfg["max_items_per_source"]]


def fetch_hackernews(cfg, since):
    items = {}
    since_ts = int(since.timestamp())
    for q in cfg["hn_queries"]:
        url = "https://hn.algolia.com/api/v1/search?" + parse.urlencode({
            "query": q,
            "tags": "story",
            "numericFilters": "created_at_i>%d,points>=%d" % (since_ts, cfg["hn_min_points"]),
            "hitsPerPage": 20,
        })
        try:
            data = http_json(url)
        except Exception as e:
            log("HN 查询失败(%s)：%s" % (q, e))
            continue
        for hit in data.get("hits", []):
            oid = hit.get("objectID")
            if not oid or oid in items:
                continue
            discussion = "https://news.ycombinator.com/item?id=" + oid
            items[oid] = {
                "kind": "hn",
                "name": hit.get("title") or oid,
                "url": hit.get("url") or discussion,
                "discussion": discussion,
                "points": hit.get("points") or 0,
                "created": (hit.get("created_at") or "")[:10],
            }
        time.sleep(1)
    return sorted(items.values(), key=lambda x: -x["points"])[: cfg["max_items_per_source"]]


def fetch_producthunt(cfg, since):
    # Product Hunt GraphQL API 必须配置 Token（仓库 Secret: PRODUCTHUNT_TOKEN），未配置则跳过
    token = os.environ.get("PRODUCTHUNT_TOKEN")
    if not token:
        log("未设置 PRODUCTHUNT_TOKEN，跳过 Product Hunt")
        return []
    query = {
        "query": "query { posts(order: NEWEST, first: 50) { edges { node { "
                 "name tagline url votesCount createdAt } } } }"
    }
    try:
        data = http_json(
            "https://api.producthunt.com/v2/api/graphql",
            headers={"Authorization": "Bearer " + token},
            payload=query,
        )
    except Exception as e:
        log("Product Hunt 查询失败：%s" % e)
        return []
    items = []
    keywords = ("ai", "agent", "mcp", "skill", "llm", "claude", "gpt")
    try:
        edges = data["data"]["posts"]["edges"]
    except (KeyError, TypeError):
        log("Product Hunt 返回结构异常，已跳过：%s" % json.dumps(data, ensure_ascii=False)[:300])
        return []
    for edge in edges:
        node = edge["node"]
        text = ((node.get("name") or "") + " " + (node.get("tagline") or "")).lower()
        if not any(k in text for k in keywords):
            continue
        created = (node.get("createdAt") or "")[:10]
        if created and created < since.strftime("%Y-%m-%d"):
            continue
        items.append({
            "kind": "ph",
            "name": node.get("name") or "",
            "url": node.get("url") or "",
            "desc": (node.get("tagline") or "").strip(),
            "votes": node.get("votesCount") or 0,
            "created": created,
        })
    return sorted(items, key=lambda x: -x["votes"])[: cfg["max_items_per_source"]]


def fetch_community(cfg, since):
    items = []
    since_str = since.strftime("%Y-%m-%d")
    for repo in cfg.get("community_repos", []):
        url = "https://api.github.com/repos/" + repo.strip("/")
        try:
            data = http_json(url, github_headers())
        except Exception as e:
            log("关注清单仓库获取失败(%s)：%s" % (repo, e))
            continue
        pushed = (data.get("pushed_at") or "")[:10]
        if pushed < since_str:
            continue
        items.append({
            "kind": "community",
            "name": data["full_name"],
            "url": data["html_url"],
            "desc": (data.get("description") or "").strip(),
            "stars": data["stargazers_count"],
            "pushed": pushed,
        })
        time.sleep(1)
    return sorted(items, key=lambda x: -x["stars"])[: cfg["max_items_per_source"]]


def load_state(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data.get("seen"), dict):
                return data
    except (FileNotFoundError, ValueError):
        pass
    return {"seen": {}}


def save_state(path, state):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=True)


def prune_state(state, days=180):
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    state["seen"] = {u: d for u, d in state["seen"].items() if d >= cutoff}


def safe(text):
    return (text or "").replace("```", "'''")


def ai_prompt(item):
    if item["kind"] in ("github", "community"):
        return (
            "你是一名资深工程师助手。我想在当前项目中落地下面这个 AI 工具/技能：\n"
            "\n"
            "名称：%s\n"
            "链接：%s\n"
            "官方简介：%s\n"
            "Stars：%s\n"
            "\n"
            "请先通过链接阅读它的 README 与官方文档，然后：\n"
            "1. 用中文说明它解决什么问题、核心概念与前置依赖；\n"
            "2. 给出适配我当前项目的安装、配置步骤和最小可用示例代码；\n"
            "3. 给出验证方法，并指出风险与替代方案；\n"
            "4. 关键信息缺失时先列出需要我确认的问题，不要擅自假设。"
        ) % (item["name"], item["url"], item["desc"] or "（仓库未提供描述）", item["stars"])
    if item["kind"] == "hn":
        return (
            "你是一名资深工程师助手。我在 Hacker News 上看到一个热门话题，想评估并落地：\n"
            "\n"
            "标题：%s\n"
            "原文链接：%s\n"
            "HN 讨论：%s（%s points）\n"
            "\n"
            "请先阅读原文和 HN 讨论中的高价值评论，然后：\n"
            "1. 用中文概括它是什么、解决什么问题、社区评价的优缺点；\n"
            "2. 给出在我当前项目中试用/落地的具体步骤与示例；\n"
            "3. 指出风险、前置依赖和替代方案；\n"
            "4. 关键信息缺失时先列出需要我确认的问题。"
        ) % (item["name"], item["url"], item["discussion"], item["points"])
    return (
        "你是一名资深工程师助手。我在 Product Hunt 上发现一个 AI 产品，想评估并落地：\n"
        "\n"
        "名称：%s\n"
        "链接：%s\n"
        "简介：%s（%s votes）\n"
        "\n"
        "请先通过链接阅读其官网与文档，然后：\n"
        "1. 用中文说明它的功能、适用场景与前置依赖；\n"
        "2. 给出注册/接入/在当前项目中使用的具体步骤与示例；\n"
        "3. 给出收费、隐私与稳定性方面的风险提示和替代方案；\n"
        "4. 关键信息缺失时先列出需要我确认的问题。"
    ) % (item["name"], item["url"], item["desc"] or "（无简介）", item["votes"])


def render_item(idx, item):
    if item["kind"] == "github":
        head = (
            "### %d. %s\n\n"
            "- 链接：%s\n"
            "- Stars：%s ｜ 创建：%s ｜ 语言：%s\n"
            "- 功能说明（原文）：%s\n"
            "- 使用方法：安装与使用步骤见仓库 README：%s\n"
        ) % (idx, item["name"], item["url"], item["stars"], item["created"],
             item["language"], item["desc"] or "（仓库未提供描述）", item["url"])
    elif item["kind"] == "community":
        head = (
            "### %d. %s（关注清单近期更新）\n\n"
            "- 链接：%s\n"
            "- Stars：%s ｜ 最近推送：%s\n"
            "- 功能说明（原文）：%s\n"
            "- 使用方法：安装与使用步骤见仓库 README：%s\n"
        ) % (idx, item["name"], item["url"], item["stars"], item["pushed"],
             item["desc"] or "（仓库未提供描述）", item["url"])
    elif item["kind"] == "hn":
        head = (
            "### %d. %s\n\n"
            "- 原文链接：%s\n"
            "- HN 讨论：%s（%s points，%s）\n"
            "- 功能说明：详见原文与讨论区\n"
            "- 使用方法：阅读原文与高赞评论，按文末指令让 AI 协助落地\n"
        ) % (idx, item["name"], item["url"], item["discussion"],
             item["points"], item["created"])
    else:
        head = (
            "### %d. %s\n\n"
            "- 链接：%s\n"
            "- Votes：%s ｜ 发布：%s\n"
            "- 功能说明（原文）：%s\n"
            "- 使用方法：访问官网注册/接入，按文末指令让 AI 协助落地\n"
        ) % (idx, item["name"], item["url"], item["votes"],
             item["created"], item["desc"] or "（无简介）")
    return head + "\n**发给 AI 的落地指令（整段复制）：**\n\n```text\n" + safe(ai_prompt(item)) + "\n```\n"


def next_issue(posts_dir):
    pattern = os.path.join(ROOT, posts_dir, "*-ai-news-*.markdown")
    return len(glob.glob(pattern)) + 1


def render_post(cfg, groups, since, now):
    total = sum(len(v) for v in groups.values())
    issue = next_issue(cfg["posts_dir"])
    lines = [
        "---",
        'layout: post',
        'title: "AI 新资讯周刊 #%d"' % issue,
        'subtitle: "本周热门 AI Agent / Claude Skills / MCP 工具速览"',
        "date: %s" % now.strftime("%Y-%m-%d %H:%M:%S"),
        'author: ""',
        'header-img: "%s"' % cfg["header_img"],
        "tags:",
        "    - %s" % cfg["post_tag"],
        "---",
        "",
        "本期统计周期：%s ~ %s，共收录 %d 个新项目/话题。条目由脚本自动抓取，描述保留原文，未做翻译。"
        % (since.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"), total),
        "",
    ]
    sections = [
        ("github", "GitHub 热门新仓库"),
        ("hn", "Hacker News 热门讨论"),
        ("ph", "Product Hunt 新品"),
        ("community", "社区关注清单动态"),
    ]
    for kind, title in sections:
        items = groups.get(kind, [])
        if not items:
            continue
        lines += ["## " + title, ""]
        for idx, item in enumerate(items, 1):
            lines.append(render_item(idx, item))
    lines += [
        "---",
        "",
        "> 本文由 GitHub Actions 自动生成，来源：GitHub Search、Hacker News(Algolia)、"
        "Product Hunt、社区关注清单。抓取范围与阈值可在 `scripts/ai_news_config.json` 修改。",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="抓取本周热门 AI Agent/Skills/MCP 并生成周刊文章")
    parser.add_argument("--config", default=os.path.join(ROOT, "scripts", "ai_news_config.json"))
    parser.add_argument("--lookback", type=int, default=None, help="回溯天数，覆盖配置文件")
    parser.add_argument("--dry-run", action="store_true", help="只打印 Markdown，不写文件、不更新去重状态")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    lookback = args.lookback
    if lookback is None and os.environ.get("LOOKBACK_DAYS"):
        lookback = int(os.environ["LOOKBACK_DAYS"])
    if lookback is None:
        lookback = cfg["lookback_days"]

    now = datetime.now()
    since = now - timedelta(days=lookback)

    raw_groups = {
        "github": fetch_github(cfg, since),
        "hn": fetch_hackernews(cfg, since),
        "ph": fetch_producthunt(cfg, since),
        "community": fetch_community(cfg, since),
    }

    state_path = os.path.join(ROOT, cfg["state_file"])
    state = load_state(state_path)
    prune_state(state)
    today = now.strftime("%Y-%m-%d")

    groups = {}
    known_urls = set()
    for kind, items in raw_groups.items():
        groups[kind] = []
        for item in items:
            url = item.get("url")
            if not url or url in state["seen"] or url in known_urls:
                continue
            known_urls.add(url)
            groups[kind].append(item)

    total = sum(len(v) for v in groups.values())
    if total == 0:
        log("本周期没有新条目，不生成文章")
        return

    markdown = render_post(cfg, groups, since, now)
    if args.dry_run:
        print(markdown)
        log("dry-run：未写入文件、未更新去重状态")
        return

    filename = "%s-ai-news-%s.markdown" % (now.strftime("%Y-%m-%d"), now.strftime("%Y%m%d"))
    post_path = os.path.join(ROOT, cfg["posts_dir"], filename)
    with open(post_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(markdown)
    for items in groups.values():
        for item in items:
            state["seen"][item["url"]] = today
    save_state(state_path, state)
    log("已生成文章：%s（%d 个条目）" % (post_path, total))


if __name__ == "__main__":
    main()
