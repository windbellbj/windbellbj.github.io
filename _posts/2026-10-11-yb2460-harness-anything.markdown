---
layout: post
title: "harness-anything 使用说明：让 AI Agent 直接操控 WPS、Office、Z…"
subtitle: "2246 Star 的 Windows COM 自动化工具集，47 条 CLI 命令 + 27 个学术 Skill，Java 后端也能顺手用"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - Agent Harness
news_category: harness
---

- 来源：重点跟踪清单
- 仓库：https://github.com/yb2460/harness-anything
- Stars：2246
- 语言：Python
- 创建时间：2026-05-27
- 最近更新：2026-10-09
- 官方简介：Harness Anything - AI agent control hub: WPS, MS Office, Zotero, Photoshop, 47 CLI commands, 27 academic skills, SVG-to-PPTX

---

> 一套跑在 Windows 上的 AI Agent 控制中枢：用命令行把 WPS / Microsoft Office、Zotero、Photoshop、Illustrator 变成 Agent 可调用的工具，适合需要批量产出文档、PPT、图表与文献综述的开发者与研究者。

## 它到底解决什么问题

日常开发里最耗时的往往不是写业务代码，而是那些「必须用 Office 点出来」的产物：答辩 PPT、项目汇报、数据表格、论文配图、文献综述。harness-anything 的思路是把这些桌面软件变成 **Agent 可编程的接口**——通过 Windows COM 自动化，把 WPS / Office / Photoshop / Illustrator 的操作封装成 CLI 命令，再交给 AI Agent 编排。

它同时是一个 **Agent Harness（智能体运行壳）**：不只提供单条命令，还提供 27 个学术 Skill、PPT 设计系统、以及一套可复用的 PPT 生成引擎，让 Agent 能按流程完成「检索文献 → 分析 → 写稿 → 出图 → 生成 PPT」这类长链路任务。

**最适合谁用：**

- 在 Windows 上工作、需要频繁产出 PPT / Word / Excel 的开发者
- 做科研、写论文、需要管理 Zotero 文献库的研究者
- 想把设计软件（PS / AI）纳入自动化流水线的工程师
- 正在搭建 Agent 工作流、需要现成「工具层」的 AI 应用开发者

## 包含哪些子项目

仓库并非单一工具，而是多个可独立使用的模块集合：

| 子项目 | 定位 | 关键能力 |
|--------|------|----------|
| cli-anything-wps | WPS / Microsoft Office 操控 | 47 个 CLI 命令，覆盖 Writer / Calc / Impress，支持 8 种导出格式 |
| cli-anything-zotero | 学术研究智能体 | 文献管理 + 27 个学术 Skill，覆盖检索、写作、审稿、可视化、分析、流水线 |
| Illustrator Harness | Adobe Illustrator Agent | 通过 COM 创建/编辑矢量图，支持图层、形状、文字、导出 |
| Photoshop Harness | Adobe Photoshop Agent | 通过 COM 创建/编辑位图，支持图层、选区、滤镜、导出 |
| WPS PPT 自动化生成 | 5 校招生数据全景示例 | JSON 数据驱动 + 元素类型路由，全自动生成高质量 PPT |
| pptengine | 通用 WPS PPT 生成引擎 | 路径无关、开箱即用，代码驱动 + JSON 驱动双模式 |

<!-- asset:blog-2 start -->
![六个可独立使用的模块](/img/ai-news/yb2460-harness-anything/blog-2.png)

*图：六个可独立使用的模块*
<!-- asset:blog-2 end -->


## 核心概念与工作原理

理解三个关键词，就能看懂整个项目：

**1. COM 自动化**

所有 Office / Adobe 操作都走 Windows COM 接口，与 Microsoft Office VBA 兼容。这意味着命令最终调用的是本机已安装的桌面软件，而不是在云端模拟。想操控 MS Office 而非 WPS，把 ProgID 换成 `PowerPoint.Application` / `Word.Application` / `Excel.Application` 即可。

**2. CLI 命令 → 领域操作 → 应用**

调用链是：`CLI 命令 → Click CLI → Core 模块 → COM Bridge → 应用引擎`。每个子项目都有独立的 CLI 入口，命令组按领域划分（如 `project` / `layers` / `shapes` / `text` / `export`）。

**3. Skill 与 Pipeline**

Zotero 部分把学术工作流拆成 27 个 Skill，分 7 大类，并支持把多个 Skill 串成 pipeline（如 `original_article` 论著推荐流程、`meta_analysis` Meta 分析流程）。

| Skill 分类 | 数量 | 能力 |
|-----------|------|------|
| search | 3 | 快速检索 / 系统评价 / 深度文献搜索 |
| research | 4 | 创意生成 / 头脑风暴 / 假设 / 深度研究 |
| writing | 5 | 写论文 / IMRAD 稿件 / 引用 / 大纲 / 修改 |
| review | 5 | 5 人审稿 / 同行评审 / 七轮对抗 / 引用验证 |
| visualization | 4 | 幻灯片 / 示意图 / 海报 / 期刊图表 |
| analysis | 3 | 探索分析 / 统计 / 证据评估 |
| pipeline | 2 | 完整学术流水线 / 研究到论文 |

<!-- asset:blog-1 start -->
![CLI 到应用的调用链](/img/ai-news/yb2460-harness-anything/blog-1.png)

*图：CLI 到应用的调用链*
<!-- asset:blog-1 end -->


## 环境与前置依赖

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows 10 / 11 |
| Python | 3.10+ |
| 办公软件 | WPS Office 2019+ 或 Microsoft Office 2016+ |
| 文献工具 | Zotero 7+（使用学术功能时） |
| 设计软件 | Adobe Illustrator 2023+（可选）、Adobe Photoshop 2023+（可选） |
| Python 依赖 | pywin32、click（设计模块另需 pywin32） |

> **注意：** 该项目强依赖 Windows COM，官方未提供 macOS / Linux 支持。设计模块（Illustrator / Photoshop）必须本机安装对应 Adobe 软件，否则命令无法执行。

## 安装与配置

### 通用安装

1. 确认已安装 Python 3.10 或更高版本，在 PowerShell 中执行 `python --version` 验证。
2. 安装核心依赖：`pip install pywin32 click`。
3. 安装 WPS / Office 操控模块：`pip install git+https://github.com/yb2460/cli-anything-wps.git`。
4. 安装 Illustrator 模块：进入 `illustrator-harness/agent-harness` 目录后执行 `pip install -e .`。
5. 安装 Photoshop 模块：进入 `photoshop-harness/agent-harness` 目录后执行 `pip install -e .`。
6. 安装 pptengine 依赖：进入 `WPS/ppt-engine` 目录后执行 `pip install -r requirements.txt`。

### 在 Trae Work 中接入

官方未提供与 Trae Work / Java 的集成方式，也没有公开的 MCP 服务端、Skill 目录规范或 Java SDK。因此目前可行的接入路径是 **终端调用**：

1. 在 Trae Work 中打开内置终端（PowerShell）。
2. 按上面的通用安装步骤装好 CLI。
3. 在对话中让 Agent 通过终端执行 `cli-anything-wps`、`cli-anything-zotero` 等命令，由 Agent 读取命令输出并决定下一步。
4. 若希望 Agent 自动编排，可在项目根目录放一份说明文件，把常用命令与参数写清楚，供 Agent 参考。

> **提示：** 由于没有官方 MCP 封装，Agent 调用时需要你显式给出命令与参数，无法像标准 MCP 服务那样自动发现工具列表。

### 在 Java / Spring 项目中接入

官方未提供 Java SDK 或 HTTP 服务端。若要在 Spring 项目里触发这些能力，只能通过 `ProcessBuilder` 或 `Runtime.exec` 调用本机 CLI，并解析标准输出。这属于自行封装，官方未公开说明支持方式。

## 快速上手

### WPS 办公

1. 新建演示文档：`cli-anything-wps document new --type impress --name "演示"`
2. 应用学术预设：`cli-anything-wps preset apply academic --talk-type defense`
3. 导出为 PPTX：`cli-anything-wps export render output.pptx -p pptx`

### Zotero 学术

1. 查看全部学术 Skill：`cli-anything-zotero skills list`
2. 运行论著推荐流程：`cli-anything-zotero skills pipeline original_article`
3. 运行 Meta 分析流程：`cli-anything-zotero skills pipeline meta_analysis`
4. 查询期刊图表规范：`cli-anything-zotero skills journal "Nature"`
5. 检索文献库：`cli-anything-zotero catalog search "machine learning"`

### Illustrator 设计

1. 新建文档：`cli-anything-illustrator project new logo.ai -w 500 -h 500`
2. 添加文字：`cli-anything-illustrator text add "Brand" --x 100 --y 100 --font "Arial" --size 72`
3. 绘制矩形：`cli-anything-illustrator shapes rect --x 50 --y 50 --w 200 --h 100`
4. 导出 SVG：`cli-anything-illustrator export svg output.svg`

### Photoshop 设计

1. 新建文档：`cli-anything-photoshop project new poster.psd -w 1920 -h 1080`
2. 添加文字：`cli-anything-photoshop text add --content "Hello World" --font "Arial" --size 72`
3. 导出 PNG：`cli-anything-photoshop export png --output result.png`

### pptengine 生成 PPT

1. 进入示例目录：`cd WPS/ppt-engine/examples`
2. 运行代码驱动示例：`python build_demo.py`，产物在 `out/demo.pptx`
3. 运行 JSON 驱动示例：`python build_from_json.py`，产物在 `out/from_json.pptx`

<!-- asset:code-1 start -->
```powershell
cli-anything-wps document new --type impress --name "演示"
cli-anything-wps preset apply academic --talk-type defense
cli-anything-wps export render output.pptx -p pptx
```
<!-- asset:code-1 end -->


## 如何确认安装成功

- 执行 `cli-anything-wps --help`，能看到命令组列表即安装成功。
- 执行 `cli-anything-zotero skills list`，能列出 27 个学术 Skill 即 Zotero 模块可用。
- 执行 `cli-anything-illustrator --help` 或 `cli-anything-photoshop --help`，能显示命令组即设计模块就绪。
- 运行 `python build_demo.py` 后检查 `out/` 目录是否生成 `demo.pptx`，能打开且排版正常即 pptengine 工作正常。

## 局限与风险

**平台锁定**

强依赖 Windows COM，无法在 macOS / Linux 使用。设计模块还要求本机安装对应 Adobe 软件，且版本需 2023+。

**成熟度**

项目创建于 2026-05-27，最近更新 2026-10-09，属于较新的项目。第三方站点 GitGem.org 显示其被追踪以来约 883 stars、50 forks、3 个 open issues，最近一次提交约在 4 个月前；而仓库元信息显示 2246 stars。两处数据口径不同，可能因统计时间与统计范围差异，建议以 GitHub 页面实时数据为准。

**已知的 COM 坑**

pptengine 文档明确列出已规避 7 个 WPS COM 问题：`Adjustments.Item(1)=` 语法错误、`Bold=False` 异常、`WordWrap` 与居中冲突、多行居中上浮、`AddTable` 边框不稳、`SaveAs` 静默失败、中文字体方块。这说明直接手写 COM 调用容易踩坑，建议优先使用封装好的引擎。

**费用**

项目本身采用 MIT 许可证，可自由使用与修改。但它调用的 WPS Office、Microsoft Office、Adobe Illustrator、Photoshop 均为商业软件，需自行准备合法授权。

**安全**

CLI 会直接操控本机桌面软件并读写文件，Agent 自动执行时可能覆盖或导出文件。建议在受控目录中试用，重要文档先备份。

## 社区评价

Hacker News 讨论中，社区关注点集中在「用 CLI 把桌面软件变成 Agent 工具」这一思路的实用性，以及 COM 自动化在批量文档生成场景下的稳定性。有讨论提到这类方案的价值在于把原本需要人工点击的 Office 流程变成可脚本化、可被 Agent 编排的步骤；也有观点指出其强绑定 Windows 与商业软件，跨平台与开源替代方案有限。

## 一句话总结

如果你在 Windows 上、经常要产出 Office 文档或学术材料、又想让 AI Agent 帮你把这条链路自动化，harness-anything 提供了一套现成的 CLI 工具层与 Skill 体系，装完就能用；但如果你需要跨平台或标准 MCP 集成，目前它还不满足。

```text
背景：我在 Windows 上用 Trae Work 开发 Java / Spring 后端项目，经常需要产出项目汇报 PPT 和 Excel 数据表。
目标：试用 harness-anything，把 WPS 的 PPT 生成能力接入我的日常工作流。
具体要求：
1. 先帮我在 PowerShell 中确认 Python 版本是否 >= 3.10，并安装 pywin32、click。
2. 执行 pip install git+https://github.com/yb2460/cli-anything-wps.git 安装 WPS 模块。
3. 安装完成后运行 cli-anything-wps --help，把输出的命令组列表整理成一张表，说明每组命令的用途。
4. 用 cli-anything-wps document new --type impress --name "测试演示" 新建一个演示文档，再用 cli-anything-wps preset apply academic --talk-type defense 应用学术预设，最后导出为 output.pptx。
5. 检查 output.pptx 是否生成成功、能否正常打开，并告诉我文件路径。
6. 如果过程中报错，请把完整错误信息贴出来，并给出针对 Windows COM 环境的排查建议。
7. 最后评估：这套工具能否通过终端调用方式融入我的 Trae Work 工作流，有哪些限制需要我提前知道。
```

（以上指令可直接整段复制给 Trae Work 等 AI 编程助手执行。）

## 常用命令速查

| 场景 | 命令 |
|------|------|
| 新建 WPS 演示 | `cli-anything-wps document new --type impress --name "演示"` |
| 应用学术预设 | `cli-anything-wps preset apply academic --talk-type defense` |
| 导出 PPTX | `cli-anything-wps export render output.pptx -p pptx` |
| 列出学术 Skill | `cli-anything-zotero skills list` |
| 论著推荐流程 | `cli-anything-zotero skills pipeline original_article` |
| Meta 分析流程 | `cli-anything-zotero skills pipeline meta_analysis` |
| 期刊图表规范 | `cli-anything-zotero skills journal "Nature"` |
| 文献检索 | `cli-anything-zotero catalog search "machine learning"` |
| 新建 AI 文档 | `cli-anything-illustrator project new logo.ai -w 500 -h 500` |
| 新建 PSD | `cli-anything-photoshop project new poster.psd -w 1920 -h 1080` |
| 导出 PNG | `cli-anything-photoshop export png --output result.png` |
| 生成示例 PPT | `python build_demo.py` |
| JSON 驱动生成 | `python build_from_json.py` |

<!-- asset:code-2 start -->
```powershell
cli-anything-zotero skills list
cli-anything-zotero skills pipeline original_article
cli-anything-zotero skills pipeline meta_analysis
cli-anything-zotero skills journal "Nature"
cli-anything-zotero catalog search "machine learning"
```
<!-- asset:code-2 end -->


## 导出格式一览

WPS 模块支持导出：DOCX、XLSX、PPTX、PDF、TXT、HTML、CSV、RTF。

Illustrator 模块支持导出：PNG、JPEG、SVG、PDF、AI。

Photoshop 模块支持导出：PNG、JPEG、WebP、PSD。

## PPT 设计系统

WPS 模块内置一套 PPT 设计系统，包含 4 套预设、14 种布局、5 维度质量审查。pptengine 进一步提供 13 种元素类型，包括 `text`、`image`、`table`、`cards_2x3`、`cards_1x4_info`、`card_list_wide`、`tagline_bar`、`timeline_horiz` 等。

布局规范要求：透明卡片不挡背景、标题居中无装饰线、正文不小于 22pt、每页图表与表格不少于 2 种。

引擎的素材全部由 PIL 绘制，包括渐变横幅、箭头、圆环、背景、科研示意图，不依赖外部图床；落盘后用 PyMuPDF 检查文本溢出并逐页渲染目检。

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
