#!/usr/bin/env python3
# 博客与小红书配图管线：LLM 规划（assets.json）→ Mermaid CLI / Playwright 渲染 → 回填博客文章。
# 事实约束：图中元素必须有正文依据，代码块每行必须逐字来自正文行内反引号，画不出就 0 张。
# 产物：
#   img/ai-news/<slug>/assets.json、blog-1.png、blog-2.png、blog-*.mmd
#   xhs/<date>/<slug>/cover.png、fig-1.png、fig-2.png、fig-3.png
import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ai_news_fetch as m
import xhs_build as xb

IMG_ROOT = os.path.join(m.ROOT, "img", "ai-news")
POSTS_GLOB = os.path.join(m.ROOT, "_posts", "*.markdown")

ASSETS_SYSTEM = (
    "你是一名技术配图编辑。根据给定的中文技术文章（Markdown）规划博客配图、可溯源代码块和小红书配图。只输出 JSON。\n"
    "铁律：\n"
    "1. 只能使用文章中明确出现的事实；图中每个节点、每条箭头、每句文字都必须在正文中有对应描述。"
    "没有可图形化的结构就输出空数组，严禁编造组件、流程、数据流或数字。\n"
    "2. blog_figures 为 0–2 个：type=mermaid（结构/流程/时序图，用 graph、flowchart 或 sequenceDiagram）"
    "或 type=card（3–4 条并列要点卡）。anchor 必须逐字取自给出的「可用小节标题」，图会放在该小节末尾；"
    "mermaid 总规模不超过 14 行、节点文字用简短中文；caption 不超过 20 字。\n"
    "3. code_blocks 为 0–2 个，把正文中已有的成组行内命令/配置升级为围栏块。content 中每行必须逐字来自正文反引号代码，"
    "只能搬运和排序，禁止改写、补参数、换行拼接；每块不超过 15 行；没有成组命令就输出 []。language 只能取 powershell、json、yaml。\n"
    "4. xhs 描述三张小红书配图：product 为产品名（不超过 18 字，取自文章）；one_liner 为一句话定位（不超过 30 字，取自开头导语）；"
    "figures 必须恰好 2 个（对应第 2、3 张）：type=mermaid 时给 heading（不超过 14 字）和 mermaid（同样禁止编造）；"
    "type=card 时给 heading（不超过 14 字）和 3–4 条 points（每条不超过 20 字，取自正文要点）。\n"
    "5. 只输出 JSON：\n"
    '{"blog_figures":[{"type":"mermaid|card","anchor":"...","caption":"...","mermaid":"...",'
    '"card":{"heading":"...","points":["..."]}}],'
    '"code_blocks":[{"anchor":"...","language":"powershell","content":"..."}],'
    '"xhs":{"product":"...","one_liner":"...","figures":[{"type":"mermaid|card","heading":"...",'
    '"mermaid":"...","card":{"points":["..."]}}]}}'
)

PUP_THEME = {
    "blog": {
        "theme": "base",
        "themeVariables": {
            "fontFamily": "'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif",
            "fontSize": "20px",
            "primaryColor": "#eef2ff", "primaryTextColor": "#1e1b4b",
            "primaryBorderColor": "#4338ca", "lineColor": "#4338ca",
            "secondaryColor": "#cffafe", "tertiaryColor": "#f5f3ff",
        },
    },
    "xhs": {
        "theme": "dark",
        "themeVariables": {
            "darkMode": True, "background": "transparent",
            "fontFamily": "'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif",
            "fontSize": "22px",
            "primaryColor": "#1e2a5e", "primaryTextColor": "#e0e7ff",
            "primaryBorderColor": "#67e8f9", "lineColor": "#67e8f9",
            "secondaryColor": "#241a4d", "tertiaryColor": "#172044",
        },
    },
}

# 小红书深色卡片（1242×1656），与封面同一套品牌视觉
XHS_CARD = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
.canvas {{ position:relative; width:1242px; height:1656px; overflow:hidden;
  font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif; color:#f8fafc;
  background:linear-gradient(135deg,#0a0d1f 0%,#121a3a 50%,#241a4d 100%); }}
.glow {{ position:absolute; border-radius:50%; filter:blur(10px); }}
.g1 {{ width:820px; height:820px; left:-240px; top:-240px;
  background:radial-gradient(circle,rgba(67,56,202,0.45) 0%,rgba(67,56,202,0) 70%); }}
.g2 {{ width:760px; height:760px; right:-240px; bottom:-240px;
  background:radial-gradient(circle,rgba(14,165,233,0.32) 0%,rgba(14,165,233,0) 70%); }}
.in {{ position:absolute; inset:0; display:flex; flex-direction:column;
  padding:104px 88px 92px; }}
.pills {{ display:flex; gap:20px; }}
.pill {{ font-size:32px; font-weight:700; letter-spacing:3px; color:#67e8f9;
  border:2px solid rgba(103,232,249,0.55); padding:12px 30px; border-radius:999px; background:rgba(103,232,249,0.08); }}
.pill.dim {{ color:#a5b4fc; border-color:rgba(165,180,252,0.45); background:rgba(165,180,252,0.06); }}
.foot {{ margin-top:auto; display:flex; align-items:flex-end; justify-content:space-between; }}
.brand {{ font-size:34px; font-weight:700; color:#c7d2fe; letter-spacing:2px; }}
.page {{ font-size:30px; color:#67e8f9; }}
/* intro */
.product {{ font-size:92px; font-weight:800; line-height:1.25; margin:120px 0 56px; }}
.oneliner {{ font-size:46px; line-height:1.6; color:#c7d2fe;
  border-left:10px solid #67e8f9; padding-left:40px; }}
/* keypoints */
.eyebrow {{ margin-top:110px; font-size:30px; letter-spacing:6px; color:#67e8f9; }}
.heading {{ font-size:66px; font-weight:800; line-height:1.3; margin:28px 0 70px; }}
.points {{ display:flex; flex-direction:column; gap:54px; }}
.pt {{ display:flex; align-items:flex-start; gap:34px; }}
.no {{ font-size:40px; font-weight:800; color:#67e8f9; padding-top:6px; }}
.txt {{ font-size:44px; line-height:1.45; color:#e0e7ff; }}
/* mermaid */
.mh {{ margin-top:90px; font-size:60px; font-weight:800; line-height:1.3; }}
.diagram {{ flex:1; display:flex; align-items:flex-start; justify-content:center; padding-top:60px; }}
.diagram img {{ max-width:1060px; max-height:1060px; }}
</style></head><body>
<div class="canvas"><div class="glow g1"></div><div class="glow g2"></div><div class="in">
{body}
</div></div></body></html>
"""

# 博客浅色卡片（1600×900）
BLOG_CARD = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
.canvas {{ width:1600px; height:900px; background:#ffffff;
  font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",sans-serif;
  border-left:18px solid #4338ca; padding:86px 110px; display:flex; flex-direction:column; }}
.heading {{ font-size:58px; font-weight:800; color:#1e1b4b; line-height:1.3; margin-bottom:64px; }}
.points {{ display:flex; flex-direction:column; gap:48px; }}
.pt {{ display:flex; align-items:flex-start; gap:30px; }}
.dot {{ width:22px; height:22px; border-radius:50%; background:#0ea5e9; margin-top:22px; flex:none; }}
.txt {{ font-size:40px; line-height:1.45; color:#334155; }}
</style></head><body>
<div class="canvas">
  <div class="heading">{heading}</div>
  <div class="points">{points}</div>
</div></body></html>
"""


def log(msg):
    m.log("[assets] " + msg)


def has_news_category(path):
    head = open(path, encoding="utf-8").read(2000)
    return bool(re.search(r"^news_category:\s*\S+", head, re.M))


def clip(text, n):
    text = str(text).strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def _char_w(ch):
    # 显示宽度（全角字倍数）：全角 1.0，ASCII 字母数字 0.58，其余半角 0.4，空格 0.32
    if ch == " ":
        return 0.32
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 1.0
    return 0.58 if ch.isalnum() else 0.4


def dwidth(text):
    return sum(_char_w(c) for c in text)


def clip_w(text, width):
    """按显示宽度截断，尽量回退到末尾标点，避免英文标识符被切成残句。"""
    text = str(text).strip()
    if dwidth(text) <= width:
        return text
    out, cur = "", 0.0
    for ch in text:
        cw = _char_w(ch)
        if cur + cw > width - 0.6:
            break
        out, cur = out + ch, cur + cw
    out = re.sub(r"[，、；：,;:\s]+$", "", out)
    return out + "…"


def clean_points(raw, width):
    """清洗 LLM 给的卡片要点：剥条目序号、丢数字脏项与过短项，超宽按显示宽度截断；
    返回去重列表，不足 3 条由调用方弃用整卡。"""
    out = []
    for p in raw or []:
        s = str(p).strip()
        s = re.sub(r"^(?:\d+\s*[.、)]\s*|[（(]\d+[）)]\s*|[-·•]\s*)", "", s).strip()
        if len(s) < 6 or re.fullmatch(r"[\d.\-、)）\s]+", s):
            log("丢弃卡片要点（脏项/过短）：%s" % s[:20])
            continue
        s = clip_w(s, width)
        if s not in out:
            out.append(s)
    return out[:4]


def article_body(body):
    # 截掉参考链接及其后内容，保留导语与正文小节
    return re.split(r"^##\s*(?:相关链接|参考链接)\s*$", body, maxsplit=1, flags=re.M)[0]


def section_titles(text):
    return [ln[3:].strip() for ln in text.splitlines() if re.match(r"^##\s+", ln)]


def plan_assets(cfg, post):
    body = article_body(post["body"])
    titles = section_titles(body)
    user_prompt = (
        "可用小节标题（anchor 只能从这里逐字选）：\n"
        + "\n".join("- " + t for t in titles)
        + "\n\n文章正文：\n" + body
        + "\n\n请按系统提示输出 JSON。"
    )
    plan = m.call_llm(cfg, ASSETS_SYSTEM, user_prompt, max_tokens=4000)
    if not plan:
        time.sleep(3)
        plan = m.call_llm(cfg, ASSETS_SYSTEM, user_prompt, max_tokens=4000)
    return plan


def validate_plan(plan, body):
    """丢弃无正文依据的元素：anchor 不存在、代码块命令非逐字来自行内反引号。"""
    titles = set(section_titles(body))
    spans = [s.strip() for s in re.findall(r"`([^`\n]+)`", body)]
    figs, codes = [], []
    for fig in plan.get("blog_figures") or []:
        if fig.get("type") not in ("mermaid", "card"):
            continue
        if fig.get("anchor") not in titles:
            log("丢弃博客图：anchor 不存在：%s" % fig.get("anchor"))
            continue
        if fig["type"] == "mermaid" and not str(fig.get("mermaid", "")).strip():
            continue
        if fig["type"] == "card":
            pts = clean_points((fig.get("card") or {}).get("points"), 28)
            if len(pts) < 3:
                log("丢弃博客卡片图：有效要点不足 3 条（anchor=%s）" % fig.get("anchor"))
                continue
            fig["card"]["heading"] = clip(fig["card"].get("heading", ""), 24)
            fig["card"]["points"] = pts
        caption = str(fig.get("caption", "")).strip()
        if not caption:
            continue
        fig["caption"] = clip_w(caption, 32)
        figs.append(fig)
        if len(figs) == 2:
            break
    for blk in plan.get("code_blocks") or []:
        anchor, lang = blk.get("anchor"), blk.get("language", "powershell")
        content = str(blk.get("content", "")).strip()
        if anchor not in titles or lang not in ("powershell", "json", "yaml") or not content:
            continue
        bad = None
        for raw in content.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            line = re.sub(r"^(?:PS\s*>|PS>|>\s*|\$\s*)", "", line).strip()
            if len(line) < 8:
                continue
            if not any(line == s or (len(s) >= 8 and (line in s or s in line)) for s in spans):
                bad = line
                break
        if bad:
            log("丢弃代码块（命令在正文行内代码中找不到原文）：%s" % bad[:60])
            continue
        codes.append({"anchor": anchor, "language": lang, "content": content})
        if len(codes) == 2:
            break
    xhs = plan.get("xhs") or {}
    xfigs = []
    for xf in xhs.get("figures") or []:
        t = xf.get("type")
        heading = clip(xf.get("heading", ""), 14)
        if t == "mermaid" and str(xf.get("mermaid", "")).strip() and heading:
            xfigs.append({"type": "mermaid", "heading": heading,
                          "mermaid": str(xf["mermaid"]).strip()})
        elif t == "card" and heading:
            pts = clean_points((xf.get("card") or {}).get("points"), 44)
            if len(pts) >= 3:
                xfigs.append({"type": "card", "heading": heading, "points": pts})
        if len(xfigs) == 2:
            break
    xhs_out = {
        "product": clip(xhs.get("product", ""), 18),
        "one_liner": clip_w(str(xhs.get("one_liner", "")).rstrip("…").strip(), 44),
        "figures": xfigs,
    }
    return {"blog_figures": figs, "code_blocks": codes, "xhs": xhs_out}


def quote_edge_labels(mmd):
    # mermaid 边标签 |...| 内裸用 @、括号等字符会解析失败，统一改成带双引号的安全写法
    return re.sub(r"\|([^|\"\n]+)\|", r'|"\g<1>"|', mmd)


class Renderer:
    def __init__(self, workdir):
        self.workdir = workdir
        npx = shutil.which("npx") or shutil.which("npx.cmd")
        if not npx:
            raise RuntimeError("未找到 npx，请先安装 Node.js")
        self.npx = npx
        self.pup_cfg = os.path.join(workdir, "puppeteer.json")
        with open(self.pup_cfg, "w", encoding="utf-8") as f:
            json.dump({"args": ["--no-sandbox", "--disable-gpu"]}, f)
        from playwright.sync_api import sync_playwright
        self.pw_cm = sync_playwright().start()
        self.browser = self.pw_cm.chromium.launch(args=["--no-sandbox"])

    def close(self):
        self.browser.close()
        self.pw_cm.stop()

    def _theme_file(self, kind):
        p = os.path.join(self.workdir, "theme-%s.json" % kind)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(PUP_THEME[kind], f, ensure_ascii=False)
        return p

    def mermaid(self, src, out_png, kind, width):
        mmd = out_png.rsplit(".", 1)[0] + ".mmd"
        with open(mmd, "w", encoding="utf-8", newline="\n") as f:
            f.write(quote_edge_labels(src))
        cmd = [self.npx, "-y", "@mermaid-js/mermaid-cli", "-i", mmd, "-o", out_png,
               "-b", "white" if kind == "blog" else "transparent",
               "-w", str(width), "-c", self._theme_file(kind), "-p", self.pup_cfg]
        r = subprocess.run(cmd, capture_output=True, timeout=300)
        if r.returncode != 0 or not os.path.exists(out_png):
            log("mermaid 渲染失败：%s" % (r.stderr.decode("utf-8", "ignore")[-400:] or "未知错误"))
            return False
        return True

    def shot(self, html_text, out_png, w, h):
        path = os.path.join(self.workdir, "_page.html")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(html_text)
        page = self.browser.new_page(viewport={"width": w, "height": h})
        page.goto(file_uri(path))
        page.wait_for_load_state("domcontentloaded")
        page.screenshot(path=out_png, clip={"x": 0, "y": 0, "width": w, "height": h})
        page.close()


def file_uri(path):
    # Windows 路径转 file URI
    p = os.path.abspath(path).replace("\\", "/")
    if re.match(r"^[A-Za-z]:", p):
        p = "/" + p
    return "file://" + p


def xhs_intro_html(category_name, product, one_liner, page_no):
    body = (
        '<div class="pills"><span class="pill">{cat}</span><span class="pill dim">AI 新资讯</span></div>'
        '<div class="product">{product}</div>'
        '<div class="oneliner">{line}</div>'
    ).format(cat=html.escape(category_name), product=html.escape(product),
             line=html.escape(one_liner))
    return body


def xhs_points_html(heading, points, page_no):
    lis = "".join(
        '<div class="pt"><div class="no">%02d</div><div class="txt">%s</div></div>'
        % (i + 1, html.escape(p)) for i, p in enumerate(points))
    return ('<div class="eyebrow">AI 新资讯</div><div class="heading">%s</div>'
            '<div class="points">%s</div>') % (html.escape(heading), lis)


def xhs_mermaid_html(heading, img_path, page_no):
    return ('<div class="mh">%s</div><div class="diagram"><img src="%s"></div>') % (
        html.escape(heading), file_uri(img_path))


def xhs_wrap(body, page_no):
    foot = ('<div class="foot"><div class="brand">XinLong Li</div>'
            '<div class="page">%d / 3</div></div>') % page_no
    return XHS_CARD.format(body=body + foot)


def blog_card_html(heading, points):
    lis = "".join('<div class="pt"><div class="dot"></div><div class="txt">%s</div></div>'
                  % html.escape(p) for p in points)
    return BLOG_CARD.format(heading=html.escape(heading), points=lis)


def strip_asset_blocks(text):
    text = re.sub(r"<!-- asset:[\w.-]+ start -->.*?<!-- asset:[\w.-]+ end -->\n?",
                  "", text, flags=re.S)
    return re.sub(r"\n{3,}", "\n\n", text)


def backfill(post_path, slug, plan):
    """按规划在指定小节末尾插入图片与代码块（先清旧标记，幂等）。"""
    text = open(post_path, encoding="utf-8").read()
    text = strip_asset_blocks(text)
    lines = text.splitlines()

    inserts = []  # (行号, 块文本)
    for i, fig in enumerate(plan["blog_figures"], 1):
        aid = "blog-%d" % i
        url = "/img/ai-news/%s/%s.png" % (slug, aid)
        cap = clip_w(fig["caption"], 32)
        inner = "![%s](%s)\n\n*图：%s*" % (cap, url, cap)
        inserts.append((fig["anchor"], "<!-- asset:%s start -->\n%s\n<!-- asset:%s end -->"
                        % (aid, inner, aid)))
    for i, blk in enumerate(plan["code_blocks"], 1):
        aid = "code-%d" % i
        inner = "```%s\n%s\n```" % (blk["language"], blk["content"])
        inserts.append((blk["anchor"], "<!-- asset:%s start -->\n%s\n<!-- asset:%s end -->"
                        % (aid, inner, aid)))

    # 计算每个 anchor 小节最后一个有效行
    anchor_rows = {}

    def row_of(anchor):
        if anchor in anchor_rows:
            return anchor_rows[anchor]
        head = re.compile(r"^##\s+" + re.escape(anchor) + r"\s*$")
        start = next((k for k, ln in enumerate(lines) if head.match(ln)), None)
        if start is None:
            anchor_rows[anchor] = -1
            return -1
        end = next((k for k in range(start + 1, len(lines))
                    if re.match(r"^##\s+", lines[k])), len(lines))
        k = end - 1
        while k > start and (lines[k].strip() == "" or lines[k].strip() == "---"):
            k -= 1
        anchor_rows[anchor] = k
        return k

    for anchor, block in sorted(inserts, key=lambda x: row_of(x[0]), reverse=True):
        row = row_of(anchor)
        if row < 0:
            continue
        lines[row + 1: row + 1] = ["", block, ""]

    with open(post_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines).rstrip("\n") + "\n")


def build_one(cfg, renderer, post, force, plan_only):
    slug, date, category = post["slug"], post["date"], post["category"]
    assets_dir = os.path.join(IMG_ROOT, slug)
    xhs_dir = os.path.join(xb.XHS_ROOT, date, slug)
    os.makedirs(assets_dir, exist_ok=True)
    plan_path = os.path.join(assets_dir, "assets.json")

    if os.path.exists(plan_path) and not force:
        plan = json.load(open(plan_path, encoding="utf-8"))
        log("复用已有规划：%s" % slug)
    else:
        raw = plan_assets(cfg, post)
        if not raw:
            log("规划失败（LLM 无返回）：%s" % slug)
            return False
        plan = validate_plan(raw, article_body(post["body"]))
        with open(plan_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        log("规划完成：%s（博客图 %d，代码块 %d，小红书图类型 %s）" % (
            slug, len(plan["blog_figures"]), len(plan["code_blocks"]),
            [f["type"] for f in plan["xhs"]["figures"]]))
    if plan_only:
        return True

    # 清理旧产物后重新渲染
    for pat in ("blog-*.png", "blog-*.mmd"):
        for p in glob.glob(os.path.join(assets_dir, pat)):
            os.remove(p)
    for p in glob.glob(os.path.join(xhs_dir, "fig-*.png")):
        os.remove(p)

    # 博客图
    for i, fig in enumerate(plan["blog_figures"], 1):
        out = os.path.join(assets_dir, "blog-%d.png" % i)
        if fig["type"] == "mermaid":
            if not renderer.mermaid(fig["mermaid"], out, "blog", 1600):
                fig["_render_failed"] = True
                continue
        else:
            c = fig["card"]
            renderer.shot(blog_card_html(c["heading"], c["points"][:4]), out, 1600, 900)

    # 小红书封面（xhs_build 已产出 cover.html）
    cover_html = os.path.join(xhs_dir, "cover.html")
    if os.path.exists(cover_html):
        renderer.shot(open(cover_html, encoding="utf-8").read(),
                      os.path.join(xhs_dir, "cover.png"), 1242, 1656)
    else:
        log("缺 cover.html，跳过封面截图：%s（先跑 xhs_build.py）" % slug)

    # 小红书三张配图
    cat_name = xb.CATEGORY_NAMES.get(category, "其他")
    x = plan["xhs"]
    pages = [("intro", None)]
    for xf in x["figures"]:
        pages.append((xf["type"], xf))
    ok = [False, False, False]
    for idx, (kind, xf) in enumerate(pages):
        out = os.path.join(xhs_dir, "fig-%d.png" % (idx + 1))
        if idx == 0:
            if not x["product"] or not x["one_liner"]:
                log("缺 product/one_liner，跳过 fig-1：%s" % slug)
                continue
            body_html = xhs_intro_html(cat_name, x["product"], x["one_liner"], idx + 1)
        elif kind == "mermaid":
            tmp_png = os.path.join(renderer.workdir, "xhs-diagram-%d.png" % (idx + 1))
            if not renderer.mermaid(xf["mermaid"], tmp_png, "xhs", 1800):
                continue
            body_html = xhs_mermaid_html(xf["heading"], tmp_png, idx + 1)
        else:
            body_html = xhs_points_html(xf["heading"], xf["points"], idx + 1)
        renderer.shot(xhs_wrap(body_html, idx + 1), out, 1242, 1656)
        ok[idx] = True
        if kind == "mermaid":
            os.remove(tmp_png)
    if not all(ok):
        log("小红书配图不完整：%s（缺第 %s 张）" % (
            slug, "、".join(str(i + 1) for i, v in enumerate(ok) if not v)))

    # 回填博客（渲染失败的图不插）
    eff = [f for f in plan["blog_figures"] if not f.get("_render_failed")]
    plan_eff = dict(plan)
    plan_eff["blog_figures"] = eff
    backfill(post["path"], slug, plan_eff)
    # 渲染失败信息回写 assets.json
    if eff != plan["blog_figures"]:
        plan["blog_figures"] = eff
        with open(plan_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="处理全部 AI 新资讯文章")
    ap.add_argument("--slug", help="只处理指定 slug")
    ap.add_argument("--force", action="store_true", help="忽略 assets.json 重新调 LLM 规划")
    ap.add_argument("--plan-only", action="store_true", help="只生成规划不渲染、不回填")
    args = ap.parse_args()

    cfg = json.load(open(os.path.join(m.ROOT, "scripts", "ai_news_config.json"), encoding="utf-8"))
    paths = [p for p in glob.glob(POSTS_GLOB) if has_news_category(p)]
    posts = [p for p in (xb.parse_post(x) for x in paths) if p]
    if args.slug:
        targets = [p for p in posts if p["slug"] == args.slug]
    elif args.all:
        targets = sorted(posts, key=lambda p: (p["date"], p["slug"]))
    else:
        latest = max(p["date"] for p in posts)
        targets = sorted((p for p in posts if p["date"] == latest), key=lambda p: p["slug"])
    if not targets:
        log("没有找到待处理文章")
        return

    renderer = None
    if not args.plan_only:
        workdir = tempfile.mkdtemp(prefix="assets_build_")
        try:
            renderer = Renderer(workdir)
        except Exception as e:
            log("渲染环境初始化失败：%s\n需要 Node.js 与 `pip install playwright` 且已安装 chromium" % e)
            sys.exit(2)
    failed = []
    try:
        for post in targets:
            try:
                if not build_one(cfg, renderer, post, args.force, args.plan_only):
                    failed.append("%s/%s" % (post["date"], post["slug"]))
            except Exception as e:
                import traceback
                log("处理异常：%s → %s\n%s" % (post["slug"], e, traceback.format_exc()))
                failed.append("%s/%s" % (post["date"], post["slug"]))
            time.sleep(1)
    finally:
        if renderer:
            renderer.close()
    log("配图管线完成：%d 篇，失败 %d 篇" % (len(targets), len(failed)))
    if failed:
        log("失败清单：" + "、".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
