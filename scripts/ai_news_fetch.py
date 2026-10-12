#!/usr/bin/env python3
# AI 新资讯抓取脚本：面向 Java + Trae Work 开发者，三条来源（GitHub 近期爆火 / 重点跟踪清单 / Show HN）
# 规则关键词粗筛 -> LLM 按读者画像精判 -> 每个保留条目独立成文；AI 失败时退回规则提取
# 仅依赖 Python 标准库
import argparse
import json
import os
import re
import sys
import time
import glob
import http.client
from datetime import datetime, timedelta, timezone
from html import unescape as html_unescape
from html.parser import HTMLParser
from urllib import parse, request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CST = timezone(timedelta(hours=8))

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

READER_CONTEXT = (
    "读者画像：Java 后端程序员，日常在 Windows 上使用 Trae Work（AI IDE）开发，技术栈以 Java / Spring 为主；"
    "关注能直接提升开发效率的 AI 新品：AI 编程助手与 CLI、Trae/Claude Skill、MCP 服务与客户端、"
    "Agent Harness（智能体运行壳/控制中枢）、编码 Agent、AI IDE 插件，希望快速安装试用并融入日常 Trae Work 工作流。"
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


def repo_item(repo, kind, order=None):
    return {
        "kind": kind,
        "name": repo["full_name"],
        "url": repo["html_url"],
        "desc": (repo.get("description") or "").strip(),
        "stars": repo["stargazers_count"],
        "language": repo.get("language") or "-",
        "topics": repo.get("topics") or [],
        "created": (repo.get("created_at") or "")[:10],
        "pushed": (repo.get("pushed_at") or "")[:10],
        "homepage": (repo.get("homepage") or "").strip(),
        "order": order,
    }


def fetch_trending(cfg, since):
    # 近期爆火：近 N 天有推送、星标达标，按星标排序（可召回老仓近期爆发的新品）
    tcfg = cfg["trending"]
    since_str = since.strftime("%Y-%m-%d")
    queries = tcfg["queries"]
    authenticated = bool(os.environ.get("GITHUB_TOKEN"))
    items = {}
    for idx, q in enumerate(queries):
        url = "https://api.github.com/search/repositories?" + parse.urlencode({
            "q": "%s pushed:>=%s stars:>=%d" % (q, since_str, tcfg["min_stars"]),
            "sort": "stars",
            "order": "desc",
            "per_page": tcfg.get("per_query", 20),
        })
        try:
            data = http_json(url, headers=github_headers())
        except Exception as e:
            log("GitHub 爆火查询失败(%s)：%s" % (q, e))
            continue
        for repo in data.get("items", []):
            if repo["stargazers_count"] < tcfg["min_stars"]:
                continue
            items.setdefault(repo["full_name"], repo_item(repo, "trending"))
        if idx < len(queries) - 1:
            time.sleep(3 if authenticated else 8)
    ranked = sorted(items.values(), key=lambda x: -x["stars"])
    return ranked[: tcfg.get("fetch_cap", 40)]


def fetch_watchlist(cfg):
    # 重点跟踪清单：首次出现即成文，之后靠 state 去重；不看近期是否有推送
    items = []
    for idx, repo_name in enumerate(cfg.get("watchlist", {}).get("repos", [])):
        try:
            data = http_json(
                "https://api.github.com/repos/" + repo_name.strip("/"),
                headers=github_headers(),
            )
        except Exception as e:
            log("重点清单仓库获取失败(%s)：%s" % (repo_name, e))
            continue
        items.append(repo_item(data, "watchlist", idx))
        time.sleep(1)
    return items


def fetch_show_hn(cfg, since):
    # 只取 Show HN（标签 story,show_hn），按热度排序
    scfg = cfg["show_hn"]
    since_ts = int(since.timestamp())
    items = {}
    for q in scfg["queries"]:
        url = "https://hn.algolia.com/api/v1/search?" + parse.urlencode({
            "query": q,
            "tags": "story,show_hn",
            "numericFilters": "created_at_i>%d,points>=%d" % (since_ts, scfg["min_points"]),
            "hitsPerPage": scfg.get("per_query", 15),
        })
        try:
            data = http_json(url)
        except Exception as e:
            log("Show HN 查询失败(%s)：%s" % (q or "全部", e))
            continue
        for hit in data.get("hits", []):
            oid = hit.get("objectID")
            if not oid or oid in items:
                continue
            discussion = "https://news.ycombinator.com/item?id=" + oid
            title = re.sub(r"^show hn:\s*", "", hit.get("title") or oid, flags=re.I)
            items[oid] = {
                "kind": "hn",
                "name": title,
                "url": hit.get("url") or discussion,
                "discussion": discussion,
                "points": hit.get("points") or 0,
                "created": (hit.get("created_at") or "")[:10],
                "oid": oid,
            }
        time.sleep(1)
    ranked = sorted(items.values(), key=lambda x: -x["points"])
    return ranked[: scfg.get("fetch_cap", 20)]


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
        text = text[:limit] + "\n\n（官方仓库说明较长，已截取前 %d 字符）" % limit
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
            parts.append("【原文正文(Show HN 自帖)】\n" + html_to_text(data["text"], 3000))
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
        text = text[:limit] + "\n\n（讨论内容较长，已截取前 %d 字符）" % limit
    return text


# ---------- 多源调研：官网正文 + DuckDuckGo 搜索深抓 + HN 社区讨论（全部免密钥，失败静默跳过） ----------

_SKIP_DOMAINS = (
    "duckduckgo.com", "github.com", "news.ycombinator.com", "youtube.com",
    "twitter.com", "x.com", "reddit.com", "facebook.com", "login.",
)


def _is_candidate_url(url):
    low = (url or "").lower()
    if not low.startswith("http"):
        return False
    return not any(d in low for d in _SKIP_DOMAINS)


def fetch_page_text(url, limit):
    try:
        html = http_text(
            url,
            headers={"User-Agent": BROWSER_UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"},
            timeout=20, retries=0,
        )
    except Exception:
        return ""
    return html_to_text(html, limit)


def ddg_search(query, max_results=4):
    # DuckDuckGo HTML/Lite 免密钥端点；解析 /l/?uddg= 跳转链接还原真实 URL，任一失败静默返回空
    endpoints = [
        "https://html.duckduckgo.com/html/?q=",
        "https://lite.duckduckgo.com/lite/?q=",
    ]
    for base in endpoints:
        hrefs = []
        try:
            html = http_text(
                base + parse.quote(query),
                headers={"User-Agent": BROWSER_UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"},
                timeout=20, retries=0,
            )
        except Exception:
            continue
        for raw in re.findall(r'href="([^"]*(?:uddg=|/l/\?)[^"]*)"', html):
            href = html_unescape(raw)
            if href.startswith("//"):
                href = "https:" + href
            target = ""
            if "uddg=" in href:
                target = (parse.parse_qs(parse.urlparse(href).query).get("uddg") or [""])[0]
            elif href.startswith("http"):
                target = href
            if target and _is_candidate_url(target) and target not in hrefs:
                hrefs.append(target)
            if len(hrefs) >= max_results:
                break
        if hrefs:
            return hrefs[:max_results]
        time.sleep(1)
    return []


def _squash(text):
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


# 常见通用词：仅凭标题里出现这些词不能判定讨论的是该项目
_GENERIC_HN_NAMES = {
    "skill", "skills", "mcp", "agent", "agents", "harness", "cli", "ide",
    "code", "codes", "opencode", "tool", "tools", "plugin", "plugins", "ecc",
}

# 标题只命中产品名时，还需命中 AI 编程领域词，避免 superpowers 这类通用词误匹配
_DOMAIN_RE = re.compile(
    r"\b(agent|agents|ai|llm|mcp|skill|skills|harness|coding|code|claude|"
    r"copilot|cursor|trae|codex|cli|ide)\b",
    re.I,
)


def _story_matches(name, hit):
    title = (hit.get("title") or "").lower()
    url = (hit.get("url") or "").lower()
    owner, _, short = name.partition("/")
    if "github.com/" + name.lower() in url:
        return True
    # 标题命中但链接指向其他 owner 的 GitHub 仓库，按同名异物排除
    if "github.com/" in url and owner.lower() not in url:
        return False
    if name.lower() in title:
        return True
    title_sq = _squash(title)
    if owner.lower() in title and _squash(short) in title_sq:
        return True
    short_sq = _squash(short)
    if (
        len(short_sq) >= 6
        and short_sq not in _GENERIC_HN_NAMES
        and short_sq in title_sq
        and _DOMAIN_RE.search(hit.get("title") or "")
    ):
        return True
    return False


def fetch_hn_discussions(name, story_cap=3, limit=5000):
    # 按项目名搜 HN story，取热门讨论的标题与高赞评论
    queries = [name]
    short = name.split("/")[-1]
    if short and short != name:
        queries.append(short.replace("-", " "))
    hits = {}
    for q in queries:
        url = "https://hn.algolia.com/api/v1/search?" + parse.urlencode({
            "query": q, "tags": "story", "hitsPerPage": 8,
        })
        try:
            data = http_json(url, timeout=20, retries=0)
        except Exception:
            continue
        for h in data.get("hits", []):
            if (h.get("points") or 0) >= 10 and h.get("objectID") and _story_matches(name, h):
                hits[h["objectID"]] = h
        time.sleep(0.5)
    top = sorted(hits.values(), key=lambda h: -(h.get("points") or 0))[:story_cap]
    if not top:
        return ""
    parts = []
    for h in top:
        parts.append(
            "- 《%s》：%s points，%s 条评论，%s"
            % (
                h.get("title") or "",
                h.get("points") or 0,
                h.get("num_comments") or 0,
                h.get("url") or ("https://news.ycombinator.com/item?id=" + h["objectID"]),
            )
        )
    for h in top[:2]:
        try:
            thread = http_json(
                "https://hn.algolia.com/api/v1/items/%s" % h["objectID"], timeout=30, retries=0
            )
        except Exception:
            continue
        comments = []
        _collect_comments(thread, comments)
        comments.sort(key=lambda c: -c["points"])
        tops = [
            "  （%d points）%s" % (c["points"], html_to_text(c["text"], 700))
            for c in comments[:3]
        ]
        if tops:
            parts.append("  高赞评论：\n" + "\n".join(tops))
        time.sleep(0.5)
    text = "\n".join(parts)
    return text[:limit]


def research_tool(item, rcfg):
    # 汇总官网正文、第三方介绍评测、HN 讨论；任何渠道失败都不影响其他渠道
    blocks = []
    homepage = (item.get("homepage") or "").strip()
    if homepage and "github.com" not in homepage.lower():
        text = fetch_page_text(homepage, rcfg.get("homepage_chars", 4000))
        if text and len(text) >= 200:
            blocks.append("【官网/文档正文】来源：%s\n%s" % (homepage, text))
            time.sleep(1)
    web_cap = rcfg.get("web_result_count", 2)
    picked = 0
    visited = {homepage.rstrip("/").lower()}
    queries = [item["name"], item["name"].split("/")[-1].replace("-", " ")]
    for q in queries:
        if picked >= web_cap:
            break
        for target in ddg_search(q, max_results=web_cap * 2):
            if picked >= web_cap:
                break
            norm = target.rstrip("/").lower()
            if norm in visited:
                continue
            visited.add(norm)
            text = fetch_page_text(target, rcfg.get("web_result_chars", 4000))
            if not text or len(text) < 200:
                continue
            blocks.append("【第三方介绍/评测】来源：%s\n%s" % (target, text))
            picked += 1
            time.sleep(1)
    hn = fetch_hn_discussions(
        item["name"], rcfg.get("hn_story_count", 3), rcfg.get("hn_chars", 5000)
    )
    if hn:
        blocks.append("【Hacker News 社区讨论】\n" + hn)
    return "\n\n".join(blocks)

TOOL_SYSTEM = (
    "你是一名资深工程师兼技术文档作者，要为一个开源 AI 开发工具/技能撰写一份中文「使用说明书」，"
    "读者看完能快速判断它值不值得用、并完成安装试用。\n"
    "一、事实与措辞\n"
    "1. 全文使用中文。用户会给出仓库元信息、官方仓库说明、官网/文档正文、第三方介绍评测、Hacker News 社区讨论等多渠道资料，"
    "事实只能来自这些资料；可交叉印证、互相补充。\n"
    "2. 严禁编造版本号、命令、路径、指标；不同渠道说法冲突时，用一句话并列两种说法，不要自行裁决；"
    "确无公开信息时，自然地写「官方未公开说明」或「暂无公开资料」。\n"
    "3. 成文中严禁出现「README」「素材」「抓取」「资料中未提供」这类暴露信息来源方式的字眼，"
    "不要写「根据 README」「官方文档指出」式的转述句，直接以产品说明书口吻陈述事实。\n"
    "二、结构与排版（不要套固定模板）\n"
    "4. 开头先用一个引用块（> ）给出一句话定位：这个产品是什么、解决什么问题、最适合谁用。\n"
    "5. 后续标题按产品自身特点自由组织，禁止千篇一律套同一套标题；但以下内容必须覆盖到"
    "（可合并、可换标题名、可调整顺序，没有相关内容的部分可不写）：适用场景与解决的问题、"
    "核心概念或工作原理、环境与前置依赖、安装与配置、快速上手、如何确认安装/运行成功、"
    "局限与风险（许可证、费用、成熟度、安全，有依据时）。\n"
    "6. 安装与配置必须写成读者可照做的步骤：读者在 Windows 上用 Trae Work 开发、技术栈 Java / Spring。"
    "除通用安装外，必须明确该产品如何融入其日常工作流（作为 MCP 服务接入、Skill 放入技能目录、"
    "终端中作为 CLI 调用、或 Java/Spring 项目里以 SDK/HTTP 集成）；命令用 Windows PowerShell 写法；"
    "官方确实没有该接入路径时，直接写「官方未提供与 Trae Work / Java 的集成方式」，严禁编造配置路径或命令。\n"
    "7. 排版要清晰、重点突出：善用二/三级标题切分长文；关键结论、命令、注意事项用加粗；"
    "提示与警告用引用块；成组的平行信息（版本要求、常用命令、优点与局限、不同渠道的评价）用表格；"
    "操作步骤用有序列表。避免大段没有信息增量的套话。\n"
    "8. 内容要详细准确：命令、参数、路径原样保留并解释作用；社区讨论中的真实评价可写入「社区评价」类小节，"
    "并注明来自 Hacker News 讨论。\n"
    "三、代码块硬约束\n"
    "9. 全文末尾保留唯一一个 ```text 围栏块：块内是读者可整段复制给 Trae Work 等 AI 编程助手的落地指令，"
    "包含背景、目标、具体要求，贴合 Java 程序员的试用场景。\n"
    "10. 除该块外，允许再出现围栏代码块（仅限 ```powershell、```json、```yaml），"
    "用于把成组的安装命令或配置写成读者可照做的形式，但必须同时满足："
    "(1) 最多 2 块、每块不超过 15 行；(2) 每条命令、每个配置项都必须能在给出的资料中找到原文依据，"
    "严禁改写参数、拼接或补全，资料没有就不写；(3) 命令用 Windows PowerShell 写法；"
    "(4) 零散单条命令仍用行内反引号，不要为凑块拆碎叙述。\n"
    "四、输出\n"
    "11. title 需包含项目名称、不超过 50 字；subtitle 不超过 80 字；面向想第一时间试用新品的开发者，不要公文腔。\n"
    "12. category 按项目最主要形态归类，只能取六个英文标识之一："
    "skill（AI 技能/Skill 包）、mcp（MCP 服务与客户端）、harness（Agent Harness/智能体运行壳）、"
    "agent-cli（编码 Agent 与命令行 AI 编程工具）、ide-plugin（AI IDE 插件/扩展）、other（以上都不是）。\n"
    "13. 只输出 JSON："
    "{\"title\":\"...\",\"subtitle\":\"...\",\"category\":\"六个标识之一\",\"markdown\":\"完整正文 Markdown（注意转义换行与引号）\"}，"
    "不要输出 JSON 以外的任何文字。\n"
    + READER_CONTEXT
)

NEWS_SYSTEM = (
    "你是一名资深技术编辑，要把一条 Hacker News「Show HN」新品的自帖、项目网页与社区讨论，"
    "写成一份中文「新品说明书」短文，让读者快速看懂并能上手试。\n"
    "硬性要求：\n"
    "1. 全文中文；事实只能来自用户给出的资料，严禁编造；没有公开信息的内容写「官方未公开说明」或「暂无公开资料」；"
    "成文中不得出现「README」「素材」「抓取」等字眼。\n"
    "2. 开头用引用块给一句话定位（是什么、适合谁）；正文结构按产品特点自由组织，不要套固定模板，"
    "但必须讲清：它是什么、解决什么问题/为什么值得试、社区怎么评价（有讨论时）、怎么开始试用；"
    "站在 Java 程序员、Windows 上日常用 Trae Work 的视角判断价值；若与 AI 辅助软件开发无关，直接如实说明读者可跳过。\n"
    "3. 排版重点突出：善用加粗、引用块、列表，成组信息可用表格。\n"
    "4. 文末必须有一个且仅一个 ```text 围栏块：读者可整段复制给 Trae Work 等 AI 助手的试用/评估指令"
    "（含背景、目标、要求）；全文只能出现这一个围栏代码块，其他命令用行内代码或编号步骤。\n"
    "5. title 不超过 50 字、subtitle 不超过 80 字，简洁直接。\n"
    "6. category 只能取六个英文标识之一："
    "skill（AI 技能/Skill 包）、mcp（MCP 服务与客户端）、harness（Agent Harness/智能体运行壳）、"
    "agent-cli（编码 Agent 与命令行 AI 编程工具）、ide-plugin（AI IDE 插件/扩展）、"
    "other（以上都不是，或与 AI 辅助开发无关）。\n"
    "7. 只输出 JSON：{\"title\":\"...\",\"subtitle\":\"...\",\"category\":\"六个标识之一\",\"markdown\":\"...\"}，"
    "不要输出 JSON 以外的文字。\n"
    + READER_CONTEXT
)

JUDGE_SYSTEM = (
    "你是一名技术资讯编辑，为特定读者从候选条目中筛出值得推送的 AI 开发新品。\n"
    + READER_CONTEXT + "\n"
    "保留标准（需同时满足）：\n"
    "1. 是可安装、可试用的软件产品/工具/框架（GitHub 仓库或 Show HN 发布的新品），或面向开发者的重大新版本；\n"
    "2. 与 AI 辅助软件开发直接相关，读者有现实使用场景（AI 编程助手/CLI、Skill、MCP、Agent Harness、编码 Agent、AI IDE 插件、开发者自动化）；\n"
    "3. 优先近约 6 个月内创建、或近期爆发/发布重大更新的项目；创建超过一年且已广为人知的成熟项目丢弃。\n"
    "丢弃：观点/讨论/资讯文章、论文、模型权重、榜单/书单/资源合集、渗透测试/黑产工具、硬件固件、"
    "量化交易/炒股、与软件开发无关的通用消费应用、游戏娱乐、纯设计/画图/视频类产品、明显刷星或描述夸张失实的仓库。\n"
    "判定要克制：拿不准是否与读者开发工作流相关的，一律丢弃。\n"
    "只输出 JSON：{\"decisions\":[{\"url\":\"与输入完全一致\",\"keep\":true,\"reason\":\"一句中文理由\"}]}，"
    "每个输入条目都必须给出一条判定，不得遗漏。"
)


def call_llm(cfg, system_prompt, user_prompt, max_tokens=None):
    key = os.environ.get("LLM_API_KEY")
    if not key:
        log("未设置 LLM_API_KEY，跳过 AI 调用")
        return None
    llm = cfg["llm"]
    payload = {
        "model": llm["model"],
        "temperature": 0.3,
        "max_tokens": max_tokens or llm.get("max_tokens", 16000),
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
        return json.loads(content)
    except Exception as e:
        log("AI 调用失败：%s" % e)
        return None


def llm_judge(cfg, items):
    # 返回 {url: (keep: bool, reason: str)}；无 key 或调用失败时返回 None（调用方按规则粗筛结果放行）
    if not os.environ.get("LLM_API_KEY"):
        return None
    decisions = {}
    batch_size = max(1, cfg.get("judge_batch_size", 25))
    for start in range(0, len(items), batch_size):
        batch = items[start:start + batch_size]
        rows = []
        for it in batch:
            if it["kind"] == "hn":
                rows.append({
                    "url": it["url"],
                    "来源": "Show HN",
                    "名称": it["name"],
                    "points": it.get("points", 0),
                    "发布时间": it.get("created", "-"),
                })
            else:
                rows.append({
                    "url": it["url"],
                    "来源": "GitHub 近期爆火",
                    "名称": it["name"],
                    "简介": it.get("desc") or "",
                    "stars": it.get("stars", 0),
                    "语言": it.get("language", "-"),
                    "topics": it.get("topics", []),
                    "创建时间": it.get("created", "-"),
                    "最近更新": it.get("pushed", "-"),
                })
        user_prompt = (
            "以下是候选条目（JSON 数组）：\n"
            + json.dumps(rows, ensure_ascii=False, indent=1)
            + "\n\n请按系统提示逐条判定，严格只输出要求的 JSON。"
        )
        parsed = call_llm(
            cfg, JUDGE_SYSTEM, user_prompt,
            max_tokens=cfg["llm"].get("judge_max_tokens", 4000),
        )
        if not parsed or not isinstance(parsed.get("decisions"), list):
            log("AI 精判本批返回异常，该批 %d 条全部放行" % len(batch))
            for it in batch:
                decisions[it["url"]] = (True, "精判不可用，放行")
            continue
        got = {}
        for d in parsed["decisions"]:
            if isinstance(d, dict) and d.get("url"):
                got[d["url"]] = (bool(d.get("keep")), str(d.get("reason") or ""))
        for it in batch:
            # 漏判的条目放行，避免模型漏输出导致条目丢失
            decisions[it["url"]] = got.get(it["url"], (True, "模型未返回判定，放行"))
        time.sleep(2)
    return decisions


def rule_filter(cfg, item):
    # 关键词粗筛：返回 (通过, 原因)
    fcfg = cfg.get("filter", {})
    if item["kind"] == "hn":
        text = (item.get("name", "") + " " + item.get("url", "")).lower()
    else:
        text = " ".join(
            [item.get("name", ""), item.get("desc", ""), " ".join(item.get("topics", []))]
        ).lower()
    for kw in fcfg.get("exclude_keywords", []):
        if kw in text:
            return False, "命中排除词「%s」" % kw
    if item["kind"] != "hn":
        kws = fcfg.get("include_keywords", [])
        if kws and not any(k in text for k in kws):
            return False, "未命中任何包含关键词"
    return True, ""


CATEGORIES = ["skill", "mcp", "harness", "agent-cli", "ide-plugin", "other"]

# 类目 slug -> 子 tag 中文短名（与站点子页一一对应）
CATEGORY_TAGS = {
    "skill": "AI技能",
    "mcp": "MCP服务",
    "harness": "Agent Harness",
    "agent-cli": "编码Agent",
    "ide-plugin": "AI IDE插件",
    "other": "其他",
}

# 规则兜底归类：顺序即优先级，命中即归（LLM 未返回合法 category 时使用）
CATEGORY_RULES = [
    ("harness", ["harness"]),
    ("skill", ["skill", "skills", "技能"]),
    ("mcp", ["mcp"]),
    ("ide-plugin", ["plugin", "extension", "插件", "vscode", "vs code", "jetbrains", "intellij"]),
    ("agent-cli", ["agent", "cli", "copilot", "cursor", "codex", "code assistant", "命令行"]),
]


def rule_category(item):
    text = " ".join([
        item.get("name", ""), item.get("desc", ""), " ".join(item.get("topics", []))
    ]).lower()
    for cat, kws in CATEGORY_RULES:
        if any(k in text for k in kws):
            return cat
    return "other"


def pick_category(parsed, item):
    cat = (parsed or {}).get("category") if parsed else None
    return cat if cat in CATEGORIES else rule_category(item)


def tool_prompt_block(item):
    return safe_code(
        "你是一名资深工程师助手。我想了解并评估下面这个 AI 开发工具/技能：\n\n"
        "名称：%s\n链接：%s\n官方简介：%s\nStars：%s\n\n"
        "请查阅它的官方仓库、官网文档与公开评测，然后：\n"
        "1. 用中文说明它解决什么问题、核心概念与前置依赖；\n"
        "2. 结合我的环境（Windows、Java/Spring 技术栈、日常使用 Trae Work 开发）给出安装、配置步骤，"
        "并说明它如何融入我的 Trae Work 工作流（MCP 接入 / Skill 安装 / 终端 CLI / Java 集成等）；\n"
        "3. 给出最小可用示例与验证方法，并指出风险与替代方案；\n"
        "4. 关键信息缺失时先列出需要我确认的问题，不要擅自假设。"
        % (item["name"], item["url"], item.get("desc") or "（仓库未提供描述）", item.get("stars", "-"))
    )


TITLE_HARD_LIMIT = 50
SUBTITLE_HARD_LIMIT = 80


def clip_text(text, limit):
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    window = text[:limit]
    cut = max(window.rfind(" "), window.rfind("/"), window.rfind("，"))
    if cut >= limit - 10:
        window = window[:cut]
    return window.rstrip(" /，") + "…"


def fallback_tool(item, readme):
    sections = extract_readme_sections(readme)
    subtitle = clip_text(item.get("desc") or "近期值得关注的 AI 开发工具", SUBTITLE_HARD_LIMIT)
    lines = [
        "> %s：%s" % (item["name"], item.get("desc") or "近期值得关注的 AI 开发工具"),
        "",
        "## 它是什么",
        "",
        item.get("desc") or "官方暂无公开的项目描述，建议直接查看仓库：%s。" % item["url"],
        "",
        "## 安装与试用",
        "",
    ]
    if sections:
        lines += [sections, ""]
    else:
        lines += ["公开资料中未提取到标准安装章节，请参考仓库：%s。" % item["url"], ""]
    lines += [
        "## 发给 AI 的落地指令",
        "",
        "把下面指令整段复制给 Trae Work 等 AI 助手，让它结合你的环境给出可执行步骤：",
        "",
        "```text",
        tool_prompt_block(item),
        "```",
        "",
        "## 注意事项",
        "",
        "- AI 生成服务本次不可用，以上安装信息由脚本从项目公开资料中按规则提取，可能不完整，关键命令请以官方文档为准。",
        "- 新项目可能存在版本变动、依赖冲突或安全风险，引入前请审查仓库与许可证。",
        "",
    ]
    return item["name"], subtitle, "\n".join(lines), False, rule_category(item)


def build_tool_article(cfg, item):
    total_budget = cfg["llm"].get("max_material_chars", 30000)
    rcfg = cfg.get("research", {})
    research = research_tool(item, rcfg)
    research_cap = (
        rcfg.get("homepage_chars", 4000)
        + rcfg.get("web_result_count", 2) * rcfg.get("web_result_chars", 4000)
        + rcfg.get("hn_chars", 5000)
    )
    readme_budget = max(6000, total_budget - research_cap)
    readme = fetch_readme(item["name"], readme_budget)
    blocks = [
        "项目名称：%s\n仓库链接：%s\n官方简介：%s\nStars：%s\n主语言：%s\n创建时间：%s\n最近更新：%s"
        % (
            item["name"], item["url"], item.get("desc") or "（仓库未提供描述）",
            item.get("stars", "-"), item.get("language", "-"),
            item.get("created", "-"), item.get("pushed", "-"),
        ),
        "【官方仓库说明】\n"
        + (readme or "（官方仓库说明获取失败，请仅依据仓库元信息与其他渠道资料撰写，不确定处明确写「官方未公开说明」）"),
    ]
    if research:
        blocks.append(research)
    user_prompt = "\n\n".join(blocks) + "\n\n请按系统提示要求输出 JSON。"
    parsed = call_llm(cfg, TOOL_SYSTEM, user_prompt)
    markdown = (parsed or {}).get("markdown", "").strip() if parsed else ""
    if markdown:
        return clip_text(parsed.get("title") or item["name"], TITLE_HARD_LIMIT) or item["name"], \
               clip_text(parsed.get("subtitle") or "", SUBTITLE_HARD_LIMIT), markdown, True, pick_category(parsed, item)
    return fallback_tool(item, readme)


def fallback_news(item):
    lines = [
        "> AI 生成服务本次不可用，以下为规则生成的简讯。",
        "",
        "## 是什么",
        "",
        item["name"],
        "",
        "## 为什么值得试",
        "",
        "该产品在 Hacker News「Show HN」获得 %s points 讨论，详细观点本次未能获取，请直接浏览项目页与讨论区。"
        % item.get("points", 0),
        "",
        "## 发给 AI 的落地指令",
        "",
        "```text",
        safe_code(
            "你是一名资深工程师助手。我在 Hacker News「Show HN」看到新品：%s\n"
            "项目链接：%s\n讨论：%s（%s points）\n"
            "请阅读项目页与高赞评论后，用中文概括它是什么、解决什么问题、社区评价的优缺点，"
            "并结合我的环境（Windows、Java/Spring 技术栈、日常使用 Trae Work 开发）判断它对我的开发工作流是否有用、给出试用建议；"
            "信息不足处先列出确认问题。"
            % (item["name"], item["url"], item["discussion"], item.get("points", 0))
        ),
        "```",
        "",
    ]
    return item["name"], "Show HN 新品", "\n".join(lines), False, rule_category(item)


def build_news_article(cfg, item):
    material = fetch_hn_material(item, cfg["llm"].get("max_material_chars", 30000))
    user_prompt = (
        "产品标题：%s\n项目链接：%s\nHN 讨论：%s（%s points）\n\n"
        "以下是该产品的项目页原文与 Hacker News 社区讨论（可能为空或已截断）：\n\n%s"
    ) % (
        item["name"], item["url"], item["discussion"], item.get("points", 0),
        material or "（项目页与讨论内容本次均未获取到，请仅依据标题谨慎生成，没有公开依据的内容写「官方未公开说明」）",
    )
    parsed = call_llm(cfg, NEWS_SYSTEM, user_prompt)
    markdown = (parsed or {}).get("markdown", "").strip() if parsed else ""
    if markdown:
        return clip_text(parsed.get("title") or item["name"], TITLE_HARD_LIMIT) or item["name"], \
               clip_text(parsed.get("subtitle") or "", SUBTITLE_HARD_LIMIT), markdown, True, pick_category(parsed, item)
    return fallback_news(item)


def yaml_quote(text):
    text = (text or "").replace('"', "'").replace("\n", " ").replace("\r", " ")
    return '"' + text + '"'


def render_post(cfg, item, title, subtitle, body, ai_used, category, now):
    if item["kind"] in ("trending", "watchlist"):
        source_label = "重点跟踪清单" if item["kind"] == "watchlist" else "GitHub 近期爆火"
        meta = "\n".join([
            "- 来源：%s" % source_label,
            "- 仓库：%s" % item["url"],
            "- Stars：%s" % item.get("stars", "-"),
            "- 语言：%s" % item.get("language", "-"),
            "- 创建时间：%s" % item.get("created", "-"),
            "- 最近更新：%s" % item.get("pushed", "-"),
            "- 官方简介：%s" % (item.get("desc") or "（仓库未提供描述）"),
        ])
        source = "官方仓库、项目官网与第三方公开资料"
    else:
        meta = "\n".join([
            "- 来源：Hacker News Show HN",
            "- 项目链接：%s" % item["url"],
            "- HN 讨论：%s（%s points）" % (item["discussion"], item.get("points", 0)),
        ])
        source = "Show HN 原帖与社区讨论"
    if ai_used:
        note = "本文由 AI 综合%s撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。" % source
    else:
        note = "本文 AI 生成服务本次不可用，由脚本按规则提取公开资料生成，详情请查阅来源：%s。" % source
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
        "    - %s" % CATEGORY_TAGS[category],
        "news_category: %s" % category,
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
    return slugify(item["name"], 60)


def rewrite_existing(cfg):
    # 按去重名单重抓多源资料并重写存量文章：覆盖原文件、保留原日期，不抓取新条目、不更新去重状态
    state_path = os.path.join(ROOT, cfg["state_file"])
    state = load_state(state_path)
    posts_dir = os.path.join(ROOT, cfg["posts_dir"])
    watchlist = {x.lower() for x in cfg.get("watchlist", {}).get("repos", [])}

    # 以「- 仓库：URL」行建立旧文件索引，并取出原始 date
    index = {}
    for path in glob.glob(os.path.join(posts_dir, "*.markdown")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        m_url = re.search(r"^- 仓库：(\S+)\s*$", text, re.M)
        m_date = re.search(r"^date:\s*(.+?)\s*$", text, re.M)
        if m_url and m_date:
            index[m_url.group(1)] = (path, m_date.group(1).strip().strip('"'))

    done = 0
    for url, day in sorted(state.get("seen", {}).items(), key=lambda kv: (kv[1], kv[0])):
        hit = index.get(url)
        if not hit:
            log("未找到旧文件，跳过：%s" % url)
            continue
        path, date_str = hit
        if "github.com" not in url:
            log("--rewrite 暂不支持非仓库条目，跳过：%s" % url)
            continue
        full_name = parse.urlparse(url).path.strip("/")
        try:
            repo = http_json(
                "https://api.github.com/repos/" + full_name, headers=github_headers()
            )
        except Exception as e:
            log("仓库信息获取失败(%s)：%s" % (full_name, e))
            continue
        item = repo_item(repo, "watchlist" if full_name.lower() in watchlist else "trending")
        title, subtitle, body, ai_used, category = build_tool_article(cfg, item)
        try:
            old_now = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S +0800")
        except ValueError:
            old_now = datetime.strptime(day + " 01:00:00 +0800", "%Y-%m-%d %H:%M:%S +0800")
        markdown = render_post(cfg, item, title, subtitle, body, ai_used, category, old_now)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(markdown)
        done += 1
        log("已重写（%s）：%s" % ("AI" if ai_used else "兜底", os.path.basename(path)))
        time.sleep(2)
    log("重写完成，共 %d 篇，去重状态未改动" % done)


def main():
    parser = argparse.ArgumentParser(description="抓取面向 Java + Trae Work 开发者的 AI 新品，每个条目独立生成一篇文章")
    parser.add_argument("--config", default=os.path.join(ROOT, "scripts", "ai_news_config.json"))
    parser.add_argument("--lookback", type=int, default=None, help="回溯天数，覆盖配置文件中的各来源窗口")
    parser.add_argument("--dry-run", action="store_true", help="只打印抓取与筛选结果，不写文件、不更新去重状态")
    parser.add_argument("--rewrite", action="store_true", help="不抓取新条目，按去重名单重抓资料并重写存量文章，覆盖原文件并保留原日期")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if args.rewrite:
        rewrite_existing(cfg)
        return

    override = args.lookback
    if override is None and os.environ.get("LOOKBACK_DAYS"):
        override = int(os.environ["LOOKBACK_DAYS"])
    now = datetime.now(CST)
    trending_since = now - timedelta(days=override or cfg["trending"]["lookback_days"])
    hn_since = now - timedelta(days=override or cfg["show_hn"]["lookback_days"])

    # 重点清单排在最前，保证同 URL 去重时以清单条目为准
    fetched = (
        [("watchlist", fetch_watchlist(cfg))]
        + [("trending", fetch_trending(cfg, trending_since))]
        + [("hn", fetch_show_hn(cfg, hn_since))]
    )
    log("抓取完成：重点清单 %d 条，近期爆火 %d 条，Show HN %d 条"
        % (len(fetched[0][1]), len(fetched[1][1]), len(fetched[2][1])))

    state_path = os.path.join(ROOT, cfg["state_file"])
    state = load_state(state_path)
    prune_state(state)

    seen_urls = set()
    watchlist, rest = [], []
    for kind, items in fetched:
        for item in items:
            url = item.get("url")
            if not url or url in state["seen"] or url in seen_urls:
                continue
            seen_urls.add(url)
            (watchlist if kind == "watchlist" else rest).append(item)

    kept, dropped = [], []
    for item in rest:
        ok, reason = rule_filter(cfg, item)
        if ok:
            kept.append(item)
        else:
            dropped.append((item, "规则粗筛：" + reason))

    decisions = llm_judge(cfg, kept)
    judged = []
    if decisions is None:
        log("AI 精判不可用，规则粗筛通过的 %d 条全部进入生成" % len(kept))
        judged = kept
    else:
        for item in kept:
            keep, reason = decisions[item["url"]]
            if keep:
                judged.append(item)
            else:
                dropped.append((item, "AI 精判：" + reason))

    # 顺序：重点清单（按配置顺序）-> 爆火（星标降序）-> Show HN（热度降序）
    trending_kept = sorted(
        [x for x in judged if x["kind"] == "trending"], key=lambda x: -x["stars"]
    )
    hn_kept = sorted(
        [x for x in judged if x["kind"] == "hn"], key=lambda x: -x["points"]
    )
    watchlist.sort(key=lambda x: x.get("order") or 0)
    candidates = (watchlist + trending_kept + hn_kept)[: cfg["max_items_total"]]

    for item, reason in dropped:
        log("丢弃[%s] %s：%s" % (item["kind"], item["name"], reason))
    if decisions is not None:
        for item in judged:
            if item in candidates:
                log("保留[%s] %s（%s）" % (item["kind"], item["name"], item["url"]))
    log("筛选结果：重点清单 %d，近期爆火 %d，Show HN %d；丢弃 %d 条；本期计划成文 %d 篇"
        % (len(watchlist), len(trending_kept), len(hn_kept), len(dropped), len(candidates)))

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
    today = now.strftime("%Y-%m-%d")
    generated = 0
    for item in candidates:
        if item["kind"] == "hn":
            title, subtitle, body, ai_used, category = build_news_article(cfg, item)
        else:
            title, subtitle, body, ai_used, category = build_tool_article(cfg, item)
        filename = "%s-%s.markdown" % (now.strftime("%Y-%m-%d"), post_slug(item))
        post_path = os.path.join(posts_dir, filename)
        if os.path.exists(post_path):
            log("文件已存在，跳过：%s" % filename)
            continue
        markdown = render_post(cfg, item, title, subtitle, body, ai_used, category, now)
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
