#!/usr/bin/env python3
# 小红书素材生成：把最新一期（或缺素材的全部）AI 新资讯文章改写成小红书笔记文案，
# 并生成与博客头图同风格的 3:4 封面 HTML。仅依赖标准库，与 ai_news_fetch.py 配套在 Actions 运行。
# 产物：xhs/<文章日期>/<slug>/note.json + cover.html
# 封面 PNG 与 3 张配图由 assets_build.py 渲染（CI 在本脚本之后运行）。
import argparse
import glob
import html
import json
import os
import re
import sys
import time
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ai_news_fetch as m

XHS_ROOT = os.path.join(m.ROOT, "xhs")
POSTS_GLOB = os.path.join(m.ROOT, "_posts", "*.markdown")

CATEGORY_NAMES = {
    "skill": "AI技能",
    "mcp": "MCP服务",
    "harness": "Agent Harness",
    "agent-cli": "编码Agent",
    "ide-plugin": "AI IDE插件",
    "other": "其他",
}

XHS_SYSTEM = (
    "你是一名小红书技术博主，粉丝是想提升效率的程序员。把用户提供的 AI 工具长文改写成一篇小红书图文笔记。\n\n"
    "严格要求：\n"
    "1. 标题不超过 20 字，口语化、有点击欲，禁止标题党、夸张承诺和标点堆叠。\n"
    "2. 正文 500–800 字，短段落，每段不超过 3 行；第一句必须是能勾住人的痛点或结论。\n"
    "3. 在 3–5 个关键行的行首点缀 emoji（如 ⚡️🎯🧩✅⚠️），总量不超过 6 个，不堆砌。\n"
    "4. 内容只讲：这工具解决什么痛点、核心能力、适合谁、上手门槛/费用、值不值得试；不讲安装命令和操作步骤。\n"
    "5. 不允许出现任何网址、仓库地址、仓库名堆砌；不允许出现 README、官方仓库、综合资料、抓取、本文由 AI 等暴露来源的措辞。\n"
    "6. 结尾用一句话引导：完整版图文教程在我主页。\n"
    "7. 输出 3–6 个话题标签，必须包含一个品类大词（如 #AI编程 #AI工具 #openai 等），其余贴具体主题；每个标签以 # 开头。\n"
    "8. 只输出 JSON：{\"title\": \"...\", \"body\": \"...\", \"tags\": [\"#AI编程\", \"...\"]}，不要输出任何解释。"
)

COVER_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>cover</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  .canvas {{
    position: relative;
    width: 1242px; height: 1656px;
    overflow: hidden;
    font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
    background: linear-gradient(135deg, #0a0d1f 0%, #121a3a 50%, #241a4d 100%);
    color: #f8fafc;
  }}
  .glow {{ position: absolute; border-radius: 50%; filter: blur(10px); }}
  .glow1 {{ width: 900px; height: 900px; left: -260px; top: -260px;
            background: radial-gradient(circle, rgba(67,56,202,0.45) 0%, rgba(67,56,202,0) 70%); }}
  .glow2 {{ width: 820px; height: 820px; right: -240px; bottom: -240px;
            background: radial-gradient(circle, rgba(14,165,233,0.35) 0%, rgba(14,165,233,0) 70%); }}
  .nodes {{ position: absolute; inset: 0; width: 100%; height: 100%; opacity: 0.9; }}
  .content {{
    position: absolute; inset: 0;
    display: flex; flex-direction: column; justify-content: space-between;
    padding: 110px 96px 110px;
  }}
  .label {{ display: inline-flex; align-items: center; gap: 18px; }}
  .pill {{
    font-size: 34px; font-weight: 700; letter-spacing: 4px;
    color: #67e8f9; border: 2px solid rgba(103,232,249,0.55);
    padding: 14px 34px; border-radius: 999px;
    background: rgba(103,232,249,0.08);
  }}
  .pill.dim {{ color: #a5b4fc; border-color: rgba(165,180,252,0.45); background: rgba(165,180,252,0.06); }}
  .title {{
    font-size: 96px; font-weight: 800; line-height: 1.3; letter-spacing: 2px;
    text-shadow: 0 8px 40px rgba(10,13,31,0.6);
    display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
  }}
  .title mark {{ background: none; color: #67e8f9; }}
  .footer {{ display: flex; align-items: flex-end; justify-content: space-between; }}
  .brand {{ font-size: 38px; font-weight: 700; color: #c7d2fe; letter-spacing: 2px; }}
  .brand small {{ display: block; margin-top: 12px; font-size: 28px; font-weight: 400; color: #818cf8; }}
  .hint {{ font-size: 30px; color: #67e8f9; border: 1px solid rgba(103,232,249,0.4);
           padding: 12px 26px; border-radius: 12px; background: rgba(103,232,249,0.07); }}
</style>
</head>
<body>
<div class="canvas">
  <div class="glow glow1"></div>
  <div class="glow2"></div>
  <svg class="nodes" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">
    <g stroke="#67e8f9" stroke-opacity="0.22" stroke-width="1.5">
      <line x1="180" y1="200" x2="420" y2="320"/><line x1="180" y1="200" x2="380" y2="560"/>
      <line x1="420" y1="320" x2="700" y2="240"/><line x1="420" y1="320" x2="680" y2="480"/>
      <line x1="380" y1="560" x2="680" y2="480"/><line x1="700" y1="240" x2="980" y2="360"/>
      <line x1="680" y1="480" x2="980" y2="360"/><line x1="680" y1="480" x2="960" y2="660"/>
      <line x1="980" y1="360" x2="1260" y2="280"/><line x1="980" y1="360" x2="1240" y2="540"/>
      <line x1="960" y1="660" x2="1240" y2="540"/><line x1="1260" y1="280" x2="1450" y2="430"/>
      <line x1="1240" y1="540" x2="1450" y2="430"/><line x1="380" y1="560" x2="520" y2="780"/>
      <line x1="960" y1="660" x2="780" y2="800"/><line x1="520" y1="780" x2="780" y2="800"/>
    </g>
    <g fill="#67e8f9">
      <circle cx="180" cy="200" r="7"/><circle cx="420" cy="320" r="9"/>
      <circle cx="380" cy="560" r="8"/><circle cx="700" cy="240" r="10"/>
      <circle cx="680" cy="480" r="11"/><circle cx="980" cy="360" r="12"/>
      <circle cx="960" cy="660" r="9"/><circle cx="1260" cy="280" r="9"/>
      <circle cx="1240" cy="540" r="10"/><circle cx="1450" cy="430" r="8"/>
      <circle cx="520" cy="780" r="7"/><circle cx="780" cy="800" r="8"/>
    </g>
  </svg>
  <div class="content">
    <div class="label">
      <span class="pill">{category}</span>
      <span class="pill dim">AI 新资讯</span>
    </div>
    <div class="title">{title}</div>
    <div class="footer">
      <div class="brand">XinLong Li<small>程序员的 AI 效率观察</small></div>
      <div class="hint">完整版长文 → 主页</div>
    </div>
  </div>
</div>
</body>
</html>
"""


def parse_post(path):
    text = open(path, encoding="utf-8").read()
    mt = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not mt:
        return None
    front, body = mt.group(1), mt.group(2)
    md = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", front, re.M)
    mc = re.search(r"^news_category:\s*(\S+)\s*$", front, re.M)
    if not md or not mc:
        return None
    slug = os.path.basename(path)[11:].rsplit(".", 1)[0]
    return {
        "path": path,
        "date": md.group(1),
        "slug": slug,
        "category": mc.group(1),
        "body": body,
    }


def strip_body(markdown):
    # 去掉代码围栏（落地指令块）与参考链接段、元信息、AI 尾注，只留导语与正文小节
    text = re.sub(r"```.*?```", "", markdown, flags=re.S)
    text = re.split(r"^##\s*参考链接\s*$", text, maxsplit=1, flags=re.M)[0]
    kept = []
    for line in text.splitlines():
        s = line.strip()
        if s in ("---", ""):
            continue
        if re.match(r"^-\s*(来源|仓库|项目链接|Stars|语言|创建时间|最近更新|官方简介|HN 讨论)", s):
            continue
        if s.startswith("> 本文由 AI") or s.startswith("> AI 生成服务本次不可用"):
            continue
        kept.append(line)
    return "\n".join(kept).strip()


def normalize_tags(tags):
    out = []
    for t in tags or []:
        t = str(t).strip().lstrip("#").strip()
        if not t:
            continue
        t = "#" + t
        if t not in out:
            out.append(t)
    return out[:6]


COVER_TITLE_FONT = 96   # 封面标题字号 px
COVER_CONTENT_W = 1050  # 封面内容区宽度 px（1242 - 左右各 96 留白）


def _char_w(ch):
    # 按字号倍数估算字符宽度：全角 1.0，ASCII 字母数字 0.58，其余半角 0.4，空格 0.32
    if ch == " ":
        return 0.32
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 1.0
    return 0.58 if ch.isalnum() else 0.4


def split_cover_title(title):
    """标题一行放不下时按显示宽度近似均分成两行，避免浏览器随机断行出现孤字。
    返回 (line1, line2)；不超长时 line2 为 None。"""
    n = len(title)
    widths = [_char_w(c) for c in title]

    def fits(i, j):
        chars = j - i
        if chars <= 0:
            return False
        return sum(widths[i:j]) * COVER_TITLE_FONT + (chars - 1) * 2 <= COVER_CONTENT_W

    if n <= 1 or fits(0, n):
        return title, None
    total = sum(widths)
    best = None
    for k in range(1, n):
        if not (fits(0, k) and fits(k, n)):
            continue
        # 选最接近等宽的断点；断点落在空格附近时小幅优先，落在连续英文词中间时惩罚
        score = abs(sum(widths[:k]) - total / 2)
        if title[k - 1] == " " or title[k] == " ":
            score -= 0.5
        if title[k - 1].isascii() and title[k].isascii() \
                and title[k - 1].isalnum() and title[k].isalnum():
            score += total
        if best is None or score < best[0]:
            best = (score, k)
    if best is None:
        return title, None
    k = best[1]
    return title[:k].strip(), title[k:].strip()


def build_one(cfg, post):
    out_dir = os.path.join(XHS_ROOT, post["date"], post["slug"])
    note_path = os.path.join(out_dir, "note.json")
    if os.path.exists(note_path):
        m.log("跳过（素材已存在）：%s/%s" % (post["date"], post["slug"]))
        return True
    content = strip_body(post["body"])
    user_prompt = content + "\n\n请按系统提示要求输出 JSON。"
    parsed = m.call_llm(cfg, XHS_SYSTEM, user_prompt, max_tokens=2000)
    if not parsed or not parsed.get("title") or not parsed.get("body"):
        # call_llm 内部已重试一次网络错误，这里对空结果再补一次
        time.sleep(3)
        parsed = m.call_llm(cfg, XHS_SYSTEM, user_prompt, max_tokens=2000)
    if not parsed or not parsed.get("title") or not parsed.get("body"):
        m.log("改写失败：%s/%s" % (post["date"], post["slug"]))
        return False
    note = {
        "title": str(parsed["title"]).strip()[:20],
        "body": str(parsed["body"]).strip(),
        "tags": normalize_tags(parsed.get("tags")),
        "category": post["category"],
        "category_name": CATEGORY_NAMES.get(post["category"], "其他"),
        "slug": post["slug"],
        "date": post["date"],
    }
    line1, line2 = split_cover_title(note["title"])
    title_html = html.escape(line1) + ("<br>" + html.escape(line2) if line2 else "")
    cover = COVER_TEMPLATE.format(
        title=title_html,
        category=html.escape(note["category_name"]),
    )
    os.makedirs(out_dir, exist_ok=True)
    with open(note_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(note, f, ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, "cover.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(cover)
    m.log("已生成素材：%s/%s（%s）" % (post["date"], post["slug"], note["title"]))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="为所有缺素材的历史文章补生成")
    ap.add_argument("--slug", help="只处理指定 slug 的文章")
    args = ap.parse_args()

    cfg = json.load(open(os.path.join(m.ROOT, "scripts", "ai_news_config.json"), encoding="utf-8"))
    posts = [p for p in (parse_post(x) for x in glob.glob(POSTS_GLOB)) if p]
    if args.slug:
        targets = [p for p in posts if p["slug"] == args.slug]
    elif args.all:
        targets = sorted(posts, key=lambda p: (p["date"], p["slug"]))
    else:
        latest = max(p["date"] for p in posts)
        targets = sorted((p for p in posts if p["date"] == latest), key=lambda p: p["slug"])
    if not targets:
        m.log("没有找到待处理文章")
        return

    failed = []
    for post in targets:
        if not build_one(cfg, post):
            failed.append("%s/%s" % (post["date"], post["slug"]))
        time.sleep(1)
    m.log("小红书素材生成完成：%d 篇，失败 %d 篇" % (len(targets), len(failed)))
    if failed:
        m.log("失败清单：" + "、".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
