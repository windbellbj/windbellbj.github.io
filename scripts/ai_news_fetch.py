#!/usr/bin/env python3
# AI 新资讯抓取脚本：每条目独立成文；抓取 README/正文后调用大模型生成中文介绍，失败时退回规则提取
# 仅依赖 Python 标准库
import argparse
import json
import os
import re
import sys
import time
import http.client
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib import parse, request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CST = timezone(timedelta(hours=8))

PROJECT_CONTEXT = (
    "读者环境：Windows 10/11 本地开发机，已安装 Python 3.12 与 Ruby；"
    "项目本身是 Jekyll 3.9.5 静态博客（GitHub Pages 部署，仓库 windbellbj/windbellbj.github.io），"
    "含 Python 标准库编写的 scripts/ 自动化脚本与 GitHub Actions 工作流。"
)


def log(msg):
    print("[ai-news] " + msg, file=sys.stderr, flush=True)


def http_request(url, headers=None, payload=None, timeout=25, retries=2, raw=False):
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
                try:
                    content = resp.read()
                except http.client.IncompleteRead as incomplete:
                    content = incomplete.partial
                if raw:
                    return content.decode("utf-8", errors="replace")
                return json.loads(content.decode("utf-8"))
        except Exception as e:
            last_err = e
            time.sleep(2 * (i + 1))
    raise last_err


def http_json(url, **kwargs):
    return http_request(url, **kwargs)


def http_text(url, headers=None, timeout=25, retries=1):
    return http_request(url, headers=headers, timeout=timeout, retries=retries, raw=True)


def github_headers(accept=None):
    headers = {"Accept": accept or "application/vnd.github+json"}
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
            data = http_json(url, headers=github_headers())
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
                "oid": oid,
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
            data = http_json(url, headers=github_headers())
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
            "language": data.get("language") or "-",
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
    cutoff = (datetime.now(CST) - timedelta(days=days)).strftime("%Y-%m-%d")
    state["seen"] = {u: d for u, d in state["seen"].items() if d >= cutoff}


def slugify(text, max_len=50):
    text = re.sub(r"[^a-z0-9]+", "-", (text or "").lower())
    text = text.strip("-")
    return (text[:max_len].rstrip("-")) or "item"


def safe_code(text):
    return (text or "").replace("```", "'''")


def fetch_readme(full_name, limit):
    url = "https://api.github.com/repos/%s/readme" % full_name
    try:
        text = http_text(url, headers=github_headers("application/vnd.github.raw"), retries=1)
    except Exception as e:
        log("README 获取失败(%s)：%s" % (full_name, e))
        return ""
    if len(text) > limit:
        text = text[:limit] + "\n\n（README 较长，已截取前 %d 字符）" % limit
    return text


SECTION_RE = re.compile(r"^(#{1,4})\s*(.+?)\s*#*\s*$")
SECTION_KEYWORDS = re.compile(
    r"install|installation|setup|getting started|quick ?start|usage|use|how to|安装|使用|快速开始|接入|配置",
    re.I,
)


def extract_readme_sections(readme, max_chars=8000):
    lines = (readme or "").splitlines()
    headings = []
    for i, line in enumerate(lines):
        m = SECTION_RE.match(line)
        if m:
            headings.append((i, len(m.group(1))))
    picked = []
    for idx, (lineno, level) in enumerate(headings):
        title = lines[lineno].lstrip("#").strip()
        if not SECTION_KEYWORDS.search(title):
            continue
        end = len(lines)
        for lineno2, level2 in headings[idx + 1:]:
            if level2 <= level:
                end = lineno2
                break
        block = "\n".join(lines[lineno:end]).strip()
        if block:
            picked.append(block)
    text = "\n\n".join(picked)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n（章节内容较长，已截取）"
    return text


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        if tag in ("p", "div", "br", "li", "h1", "h2", "h3", "tr"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "tr"):
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def html_to_text(html, limit=6000):
    parser = _TextExtractor()
    try:
        parser.feed(html or "")
    except Exception:
        pass
    text = "".join(parser.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) > limit:
        text = text[:limit] + "\n（网页正文较长，已截取）"
    return text


def _collect_comments(node, out):
    for child in node.get("children") or []:
        text = child.get("text")
        if text:
            pts = child.get("points")
            out.append({"points": pts if isinstance(pts, int) else 0, "text": text})
        _collect_comments(child, out)


def fetch_hn_material(item, limit=20000):
    parts = []
    oid = item["oid"]
    try:
        data = http_json(
            "https://hn.algolia.com/api/v1/items/%s" % oid, timeout=40, retries=1
        )
    except Exception as e:
        log("HN 条目获取失败(%s)：%s" % (oid, e))
        data = None
    if data:
        if data.get("text"):
            parts.append("【原文正文(HN 自帖)】\n" + html_to_text(data["text"], 3000))
        comments = []
        _collect_comments(data, comments)
        comments.sort(key=lambda c: -c["points"])
        blocks = [
            "（%d points）\n%s" % (c["points"], html_to_text(c["text"], 1200))
            for c in comments[:8]
        ]
        if blocks:
            parts.append("【HN 高赞评论】\n" + "\n\n---\n\n".join(blocks))
    if item.get("url") and "news.ycombinator.com" not in item["url"]:
        try:
            page = http_text(item["url"], timeout=20, retries=0)
            page_text = html_to_text(page, 6000)
            if page_text:
                parts.append("【原文网页文本】\n" + page_text)
        except Exception as e:
            log("原文网页抓取失败：%s" % e)
    text = "\n\n".join(parts)
    if len(text) > limit:
        text = text[:limit] + "\n\n（素材较长，已截取）"
    return text


TOOL_SECTIONS = ["解决什么问题", "核心概念", "前置依赖", "安装与配置", "最小可用示例",
                 "验证方法", "风险与注意事项", "替代方案"]

TOOL_SYSTEM = (
    "你是一名资深工程师，负责把一个开源 AI 工具/技能的官方 README 读透，用中文写出可直接落地的介绍文章。\n"
    "硬性要求：\n"
    "1. 全文使用中文；所有事实只能来自用户给出的 README 原文与仓库元信息，README 未提及的内容写“README 未提供”，"
    "严禁编造版本号、命令或结论。\n"
    "2. 输出严格使用以下 8 个二级标题，顺序不变，不多不少："
    + " / ".join("## " + s for s in TOOL_SECTIONS) + "。\n"
    "3. 「安装与配置」必须结合读者实际项目环境给步骤；若该工具与读者项目没有直接集成点（如独立应用、在线服务或其他语言生态），"
    "必须先写一句“本工具不直接作用于 Jekyll 博客站点本身”，再给出在读者环境中试用的步骤。\n"
    "4. 「最小可用示例」中必须包含且只能包含一个 ```text 代码块，块内是读者可整段复制给任意 AI 编程助手的落地指令"
    "（含背景、目标、要求）。\n"
    "   特别强调：全文有且仅有这一个围栏代码块（即全文只能出现一次开头的 ```text 与一次结尾的 ```）；"
    "「安装与配置」等章节中的命令一律改用行内代码（反引号）或编号普通文本步骤表达，"
    "严禁使用 ```bash、```shell、```json 等任何围栏代码块，即使命令很多也不允许例外。\n"
    "5. 「验证方法」给可执行步骤；「风险与注意事项」「替代方案」基于 README 事实撰写，README 没有就写“README 未提供”。\n"
    "6. title 需包含项目名称且不超过 40 字，subtitle 不超过 60 字。\n"
    "7. 只输出 JSON，不要输出 JSON 以外的任何文字，格式："
    "{\"title\":\"...\",\"subtitle\":\"...\",\"markdown\":\"完整文章正文(Markdown，注意转义换行与引号)\"}。\n"
    + PROJECT_CONTEXT
)

NEWS_SYSTEM = (
    "你是一名资深技术编辑，负责把一条 Hacker News 热门话题的原文与讨论读透，用中文写一篇简短资讯。\n"
    "硬性要求：\n"
    "1. 全文中文；事实只能来自用户给出的素材，素材不足处写“素材中未提供”，严禁编造。\n"
    "2. 严格使用 3 个二级标题，顺序不变：## 是什么 / ## 为什么重要 / ## 发给 AI 的落地指令。\n"
    "3. 第三节给出一个且仅一个 ```text 代码块，块内是读者可整段复制给 AI 助手的跟进/评估指令；其他位置不得出现代码块。\n"
    "4. title 不超过 40 字、subtitle 不超过 60 字。\n"
    "5. 只输出 JSON：{\"title\":\"...\",\"subtitle\":\"...\",\"markdown\":\"...\"}，不要输出 JSON 以外的文字。\n"
)


def call_llm(cfg, system_prompt, user_prompt):
    key = os.environ.get("LLM_API_KEY")
    if not key:
        log("未设置 LLM_API_KEY，跳过 AI 生成，使用兜底")
        return None
    llm = cfg["llm"]
    payload = {
        "model": llm["model"],
        "temperature": 0.3,
        "max_tokens": llm.get("max_tokens", 16000),
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if llm.get("disable_thinking", False):
        payload["thinking"] = {"type": "disabled"}
    url = llm["base_url"].rstrip("/") + "/chat/completions"
    try:
        data = http_json(
            url,
            headers={"Authorization": "Bearer " + key},
            payload=payload,
            timeout=llm.get("timeout", 120),
            retries=1,
        )
        content = data["choices"][0]["message"]["content"].strip()
        # 仅当响应整体被代码围栏包裹时才剥离，避免误吃正文 markdown 中的 ```text 块
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content).strip()
        parsed = json.loads(content)
        markdown = (parsed.get("markdown") or "").strip()
        if not markdown:
            raise ValueError("返回 JSON 缺少 markdown 字段")
        return {
            "title": (parsed.get("title") or "").strip(),
            "subtitle": (parsed.get("subtitle") or "").strip(),
            "markdown": markdown,
        }
    except Exception as e:
        log("AI 生成失败，将使用兜底：%s" % e)
        return None


def tool_prompt_block(item):
    return safe_code(
        "你是一名资深工程师助手。我想在当前项目中了解并评估下面这个 AI 工具/技能：\n\n"
        "名称：%s\n链接：%s\n官方简介：%s\nStars：%s\n\n"
        "请先阅读它的 README 与官方文档，然后：\n"
        "1. 用中文说明它解决什么问题、核心概念与前置依赖；\n"
        "2. 结合我的环境（Windows + Python 3.12 + Ruby + Jekyll 静态博客）给出安装、配置步骤和最小可用示例；\n"
        "3. 给出验证方法，并指出风险与替代方案；\n"
        "4. 关键信息缺失时先列出需要我确认的问题，不要擅自假设。"
        % (item["name"], item["url"], item.get("desc") or "（仓库未提供描述）", item.get("stars", "-"))
    )


def fallback_tool(item, readme):
    sections = extract_readme_sections(readme)
    subtitle = (item.get("desc") or "GitHub 热门 AI 项目")[:60]
    lines = [
        "> AI 生成服务本次不可用，以下内容由脚本按规则从 README 提取，可能不完整。",
        "",
        "## 解决什么问题",
        "",
        item.get("desc") or "README 未提供项目描述，请直接查阅仓库。",
        "",
        "## 核心概念",
        "",
        "README 未提供专门的概念说明，请结合官方文档确认。",
        "",
        "## 前置依赖",
        "",
        "见下方 README 安装章节，或让 AI 助手协助确认。",
        "",
        "## 安装与配置",
        "",
    ]
    if sections:
        lines += [sections, ""]
    else:
        lines += ["README 未提供标准安装章节，请参考仓库：%s" % item["url"], ""]
    lines += [
        "## 最小可用示例",
        "",
        "将下面指令整段复制给任意 AI 助手，让它结合你的环境给出可执行步骤：",
        "",
        "```text",
        tool_prompt_block(item),
        "```",
        "",
        "## 验证方法",
        "",
        "按安装章节执行后，以 README 中的用法示例运行验证；也可让 AI 助手根据你的实际环境给出验证命令。",
        "",
        "## 风险与注意事项",
        "",
        "新项目可能存在 API 变动、依赖冲突或安全风险，引入前请审查仓库与许可证。",
        "",
        "## 替代方案",
        "",
        "README 未提供替代方案对比，可让 AI 助手基于同类工具给出。",
        "",
    ]
    return item["name"], subtitle, "\n".join(lines), False


def build_tool_article(cfg, item):
    max_material = cfg["llm"].get("max_material_chars", 30000)
    readme = fetch_readme(item["name"], max_material)
    user_prompt = (
        "项目名称：%s\n仓库链接：%s\n官方简介：%s\nStars：%s\n主语言：%s\n\n"
        "以下是该仓库 README 原文（可能已截断）：\n\n===== README 开始 =====\n%s\n===== README 结束 =====\n\n"
        "请按系统提示要求输出 JSON。"
    ) % (
        item["name"], item["url"], item.get("desc") or "（仓库未提供描述）",
        item.get("stars", "-"), item.get("language", "-"),
        readme or "（README 获取失败，请基于仓库元信息生成，并在不确定处明确标注）",
    )
    result = call_llm(cfg, TOOL_SYSTEM, user_prompt)
    if result:
        return result["title"][:40] or item["name"], result["subtitle"][:60], result["markdown"], True
    return fallback_tool(item, readme)


def fallback_news(item):
    lines = [
        "> AI 生成服务本次不可用，以下为规则生成的简讯。",
        "",
        "## 是什么",
        "",
        item["name"],
        "",
        "## 为什么重要",
        "",
        "该话题在 Hacker News 获得 %s points 讨论，详细观点素材本次未能获取，请直接浏览讨论区。"
        % item.get("points", 0),
        "",
        "## 发给 AI 的落地指令",
        "",
        "```text",
        safe_code(
            "你是一名资深工程师助手。我在 Hacker News 看到热门话题：%s\n原文：%s\n讨论：%s（%s points）\n"
            "请阅读原文与高赞评论后，用中文概括它是什么、为什么重要、社区评价的优缺点，"
            "并结合我的环境（Windows + Python 3.12 + Ruby + Jekyll 静态博客）给出评估与试用建议；信息不足处先列出确认问题。"
            % (item["name"], item["url"], item["discussion"], item.get("points", 0))
        ),
        "```",
        "",
    ]
    return item["name"], "Hacker News 热门话题", "\n".join(lines), False


def build_news_article(cfg, item):
    material = fetch_hn_material(item, cfg["llm"].get("max_material_chars", 30000))
    user_prompt = (
        "话题标题：%s\n原文链接：%s\nHN 讨论：%s（%s points）\n\n"
        "以下是抓取到的素材（可能为空或已截断）：\n\n%s"
    ) % (
        item["name"], item["url"], item["discussion"], item.get("points", 0),
        material or "（素材抓取失败，请基于标题谨慎生成，不足处标注“素材中未提供”）",
    )
    result = call_llm(cfg, NEWS_SYSTEM, user_prompt)
    if result:
        return result["title"][:40] or item["name"], result["subtitle"][:60], result["markdown"], True
    return fallback_news(item)


def build_ph_article(item):
    body = "\n".join([
        "## 是什么",
        "",
        item.get("desc") or "（Product Hunt 未提供简介）",
        "",
        "- 链接：%s" % item["url"],
        "- Product Hunt 票数：%s" % item.get("votes", 0),
        "",
        "## 为什么值得关注",
        "",
        "该产品为本期 Product Hunt 上的 AI 相关新品，建议访问官网评估是否适合自己的工作流。",
        "",
        "## 发给 AI 的落地指令",
        "",
        "```text",
        safe_code(
            "你是一名资深工程师助手。我在 Product Hunt 发现 AI 产品：%s（%s），链接：%s。\n"
            "请帮我调研它的功能、适用场景、接入方式、收费与隐私风险，结合我的环境"
            "（Windows + Python 3.12 + Ruby + Jekyll 静态博客）给出试用建议；信息不足处先列出确认问题。"
            % (item["name"], item.get("desc") or "无简介", item["url"])
        ),
        "```",
        "",
    ])
    return item["name"], "Product Hunt AI 新品", body, False


def yaml_quote(text):
    text = (text or "").replace('"', "'").replace("\n", " ").replace("\r", " ")
    return '"' + text + '"'


def render_post(cfg, item, title, subtitle, body, ai_used, now):
    if item["kind"] in ("github", "community"):
        meta = "\n".join([
            "- 仓库：%s" % item["url"],
            "- Stars：%s" % item.get("stars", "-"),
            "- 语言：%s" % item.get("language", "-"),
            "- %s：%s" % ("最近推送" if item["kind"] == "community" else "创建时间",
                          item.get("pushed") or item.get("created", "-")),
            "- 官方简介：%s" % (item.get("desc") or "（仓库未提供描述）"),
        ])
        source = "GitHub README"
    elif item["kind"] == "hn":
        meta = "\n".join([
            "- 原文链接：%s" % item["url"],
            "- HN 讨论：%s（%s points）" % (item["discussion"], item.get("points", 0)),
        ])
        source = "Hacker News 原文与讨论"
    else:
        meta = "\n".join([
            "- 链接：%s" % item["url"],
            "- Product Hunt 票数：%s" % item.get("votes", 0),
            "- 官方简介：%s" % (item.get("desc") or "（无简介）"),
        ])
        source = "Product Hunt"
    if ai_used:
        note = "本文由 AI 阅读官方素材（%s）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。" % source
    else:
        note = "本文 AI 生成服务本次不可用，由脚本规则提取/兜底生成，详情请查阅来源：%s。" % source
    lines = [
        "---",
        "layout: post",
        "title: %s" % yaml_quote(title),
        "subtitle: %s" % yaml_quote(subtitle),
        "date: %s" % now.strftime("%Y-%m-%d %H:%M:%S +0800"),
        'author: ""',
        'header-img: "%s"' % cfg["header_img"],
        "tags:",
        "    - %s" % cfg["post_tag"],
        "---",
        "",
        meta,
        "",
        "---",
        "",
        body.rstrip(),
        "",
        "---",
        "",
        "> " + note,
        "",
    ]
    return "\n".join(lines)


def post_slug(item):
    if item["kind"] == "hn":
        return "hn-" + slugify(item["name"], 44) + "-" + item["oid"][-6:]
    if item["kind"] == "ph":
        return "ph-" + slugify(item["name"], 50)
    return slugify(item["name"], 60)


def main():
    parser = argparse.ArgumentParser(description="抓取近期热门 AI 项目/话题，每个条目独立生成一篇文章")
    parser.add_argument("--config", default=os.path.join(ROOT, "scripts", "ai_news_config.json"))
    parser.add_argument("--lookback", type=int, default=None, help="回溯天数，覆盖配置文件")
    parser.add_argument("--dry-run", action="store_true", help="只打印计划，不写文件、不更新去重状态")
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

    now = datetime.now(CST)
    since = now - timedelta(days=lookback)

    fetched = [
        ("github", fetch_github(cfg, since)),
        ("community", fetch_community(cfg, since)),
        ("hn", fetch_hackernews(cfg, since)),
        ("ph", fetch_producthunt(cfg, since)),
    ]

    state_path = os.path.join(ROOT, cfg["state_file"])
    state = load_state(state_path)
    prune_state(state)
    today = now.strftime("%Y-%m-%d")

    seen_urls = set()
    candidates = []
    for kind, items in fetched:
        for item in items:
            url = item.get("url")
            if not url or url in state["seen"] or url in seen_urls:
                continue
            seen_urls.add(url)
            candidates.append(item)

    if not candidates:
        log("本周期没有新条目，不生成文章")
        return

    if args.dry_run:
        for item in candidates:
            log("计划生成：[%s] %s（%s）" % (item["kind"], item["name"], item["url"]))
        log("dry-run：共 %d 篇，未写入文件、未更新去重状态" % len(candidates))
        return

    posts_dir = os.path.join(ROOT, cfg["posts_dir"])
    os.makedirs(posts_dir, exist_ok=True)
    generated = 0
    for item in candidates:
        if item["kind"] in ("github", "community"):
            title, subtitle, body, ai_used = build_tool_article(cfg, item)
        elif item["kind"] == "hn":
            title, subtitle, body, ai_used = build_news_article(cfg, item)
        else:
            title, subtitle, body, ai_used = build_ph_article(item)
        filename = "%s-%s.markdown" % (now.strftime("%Y-%m-%d"), post_slug(item))
        post_path = os.path.join(posts_dir, filename)
        if os.path.exists(post_path):
            log("文件已存在，跳过：%s" % filename)
            continue
        markdown = render_post(cfg, item, title, subtitle, body, ai_used, now)
        with open(post_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(markdown)
        state["seen"][item["url"]] = today
        save_state(state_path, state)
        generated += 1
        log("已生成（%s）：%s" % ("AI" if ai_used else "兜底", filename))
        time.sleep(2)
    log("完成，新生成 %d 篇文章" % generated)


if __name__ == "__main__":
    main()