---
layout: post
title: "harness-anything：AI Agent 全栈操控办公与设计"
subtitle: "47 个 CLI 命令 + 27 个学术 Skill，让 AI 直接驱动 WPS、Office、PS 与 Zotero"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: harness
---

- 来源：重点跟踪清单
- 仓库：https://github.com/yb2460/harness-anything
- Stars：2245
- 语言：Python
- 创建时间：2026-05-27
- 最近更新：2026-10-09
- 官方简介：Harness Anything - AI agent control hub: WPS, MS Office, Zotero, Photoshop, 47 CLI commands, 27 academic skills, SVG-to-PPTX

---

## 解决什么问题

README 显示，harness-anything（仓库内主项目名为 cli-anything-wps）要解决的是「AI Agent 只能聊天、不能真正动手操作桌面软件」的问题。它把 WPS / Microsoft Office、Adobe Illustrator、Adobe Photoshop、Zotero 这些日常生产力软件，通过 Windows COM 自动化接口暴露成 CLI 命令，让 AI Agent 可以直接创建文档、画图、排版、导出、检索文献。

README 给出的能力清单包括：

- cli-anything-wps：47 个 CLI 命令，操控 WPS Office 或 Microsoft Office（Word/Excel/PowerPoint），覆盖 Writer 段落/标题/列表/表格/图片/查找替换/字体样式，Calc 工作表管理/单元格读写/公式/合并/批量填充，Impress 幻灯片增删改/文本框/形状/背景/导出，以及 DOCX/XLSX/PPTX/PDF/TXT/HTML/CSV/RTF 导出。
- cli-anything-zotero：文献管理 + 27 个学术 Skill 集成，写综述、写论文、审稿、做图表一站式。
- Illustrator Harness：通过 COM 操控 Adobe Illustrator，让 AI Agent 创建和编辑矢量图形。
- Photoshop Harness：通过 COM 操控 Adobe Photoshop，让 AI Agent 创建和编辑位图图像。
- WPS PPT 自动化生成：JSON 数据驱动 + 元素类型路由 + WPS COM 即时生成，README 给出了 5 所高校招生数据全景的示例项目。
- pptengine：通用 WPS PPT 生成引擎，路径无关、开箱即用，代码驱动或 JSON 驱动，素材自生成，落盘校验。

对 Java 后端程序员来说，它的价值在于把「写文档、做汇报 PPT、整理图表」这类非编码工作也纳入 AI Agent 的可执行范围，而不是只停留在生成文本。

## 核心概念

- **CLI 命令**：README 中所有能力最终都以命令行形式暴露，例如 `cli-anything-wps`、`cli-anything-zotero`、`cli-anything-illustrator`、`cli-anything-photoshop`。
- **COM 自动化接口**：README 明确说明这些工具通过 Windows COM 自动化接口操控目标软件，并指出「COM 接口与 Microsoft Office VBA 兼容。如需操控 MS Office，将 ProgID 改为 `PowerPoint.Application` / `Word.Application` / `Excel.Application` 即可」。
- **Skill 与 pipeline**：cli-anything-zotero 提供 27 个学术 Skill，分为 search（3）、research（4）、writing（5）、review（5）、visualization（4）、analysis（3）、pipeline（2）七大类；README 给出 `skills list`、`skills pipeline original_article`、`skills pipeline meta_analysis`、`skills journal "Nature"` 等用法。
- **Harness**：Illustrator Harness 与 Photoshop Harness 的链路在 README 中描述为「CLI 命令 → Click CLI → Core 模块 → COM Bridge → 应用引擎」。
- **PPT 设计系统**：README 提到 4 套预设 + 14 种布局 + 5 维度质量审查；WPS PPT 自动化生成部分列出 13 种元素类型，如 `text` / `image` / `table` / `cards_2x3` / `cards_1x4_info` / `card_list_wide` / `tagline_bar` / `timeline_horiz` 等。
- **pptengine 原语**：README 示例中出现 `Deck` 与 `el.*` 原语，以及 `ensure_default_assets()`、`deck.add_slide()`、`el.header(...)`、`el.grad_bar(...)`、`deck.save(...)`。
- **已内置规避的 WPS COM 坑**：README 列出 7 项，包括 `Adjustments.Item(1)=` 语法错误、`Bold=False` 异常、`WordWrap` 与居中冲突、多行居中上浮、`AddTable` 边框不稳、`SaveAs` 静默失败、中文字体方块。

## 前置依赖

README「系统要求」一节给出的依赖为：

- Windows 10/11
- WPS Office 2019+ 或 Microsoft Office 2016+ / Zotero 7+
- Adobe Illustrator 2023+（可选）/ Adobe Photoshop 2023+（可选）
- Python 3.10+ + pywin32

各子项目另有说明：

- Illustrator Harness 前置条件：Windows 10/11 + Adobe Illustrator 2023+ + Python 3.10+ + pywin32 + click。
- Photoshop Harness 前置条件：Windows 10/11 + Adobe Photoshop 2023+ + Python 3.10+ + pywin32。
- pptengine 需要安装 `requirements.txt` 中的依赖（README 未逐项列出具体包名）。

README 未提供与 Trae Work / Java 的集成方式。

## 安装与配置

以下步骤按「Windows + Java 后端程序员 + Trae Work」的视角整理，命令均来自 README 原文。

1. 确认环境：Windows 10/11，安装 Python 3.10+，并安装 pywin32。
2. 安装 WPS 办公能力：在终端执行 `pip install git+https://github.com/yb2460/cli-anything-wps.git`。
3. 安装 Illustrator Harness：进入 `illustrator-harness/agent-harness` 目录后执行 `pip install -e .`。
4. 安装 Photoshop Harness：进入 `photoshop-harness/agent-harness` 目录后执行 `pip install -e .`。
5. 安装 pptengine 依赖：进入 `WPS/ppt-engine` 目录后执行 `pip install -r requirements.txt`。
6. 准备目标软件：按需安装 WPS Office 2019+ 或 Microsoft Office 2016+、Zotero 7+、Adobe Illustrator 2023+、Adobe Photoshop 2023+。
7. 如果要用 MS Office 而不是 WPS，按 README 说明把 ProgID 改为 `PowerPoint.Application` / `Word.Application` / `Excel.Application`。

关于融入 Trae Work 日常工作流：README 未提供与 Trae Work / Java 的集成方式，也没有说明可作为 MCP 服务接入、可作为 Skill 放入技能目录、可在 Trae Work 终端中作为 CLI 调用，或在 Java/Spring 项目中通过 SDK/HTTP 集成。因此这里不给出任何配置路径或命令，建议先按上面的通用安装步骤在本机把 CLI 跑通，再自行决定如何在 Trae Work 中调用。

## 最小可用示例

把下面这段指令整段复制给 Trae Work 等 AI 编程助手，让它先在本机把 harness-anything 的 WPS 能力跑通，再结合你的 Java 项目产出汇报材料。

```text
背景：我在 Windows 10/11 上做 Java / Spring 后端开发，日常用 Trae Work。我已经在本机安装了 Python 3.10+ 和 pywin32，也装了 WPS Office。我想试用 harness-anything（cli-anything-wps）这套 AI Agent 工具集，用它把项目里的接口清单和模块结构自动整理成一份汇报 PPT。

目标：
1. 先帮我确认本机是否已安装 cli-anything-wps，如果没有，执行 pip install git+https://github.com/yb2460/cli-anything-wps.git 完成安装。
2. 用 cli-anything-wps 新建一个 impress 类型的演示文档，套用 academic 预设（参考 README 中的 cli-anything-wps preset apply academic --talk-type defense）。
3. 把我提供的 Java 项目信息（我会贴出 Controller 列表、核心 Service 名称和一张模块依赖关系）整理成 5 到 8 页幻灯片：封面、项目背景、模块划分、核心接口清单表格、调用链路示意、后续计划。
4. 正文文字不小于 22pt，标题居中，每页至少包含一种图表或表格。
5. 最后导出为 PPTX 和 PDF 两个文件，并把生成的文件路径告诉我。

要求：
- 所有命令都通过 cli-anything-wps 执行，不要手写 python-pptx 之类的替代脚本。
- 如果某一步命令报错，把原始报错信息完整贴出来，并说明你打算怎么改。
- 不要编造 README 里没有的命令参数；不确定的参数先问我。
```

## 验证方法

README 提供了可直接执行的验证路径：

1. 验证 WPS 办公链路：执行 `cli-anything-wps document new --type impress --name "演示"`，再执行 `cli-anything-wps preset apply academic --talk-type defense`，最后执行 `cli-anything-wps export render output.pptx -p pptx`，检查是否生成 output.pptx。
2. 验证 Zotero 学术 Skill：执行 `cli-anything-zotero skills list` 查看 Skill 列表；执行 `cli-anything-zotero skills pipeline original_article` 或 `cli-anything-zotero skills pipeline meta_analysis` 验证流程；执行 `cli-anything-zotero journal "Nature"` 验证期刊图表规范；执行 `cli-anything-zotero catalog search "machine learning"` 验证检索。
3. 验证 Illustrator Harness：依次执行 `cli-anything-illustrator project new logo.ai -w 500 -h 500`、`cli-anything-illustrator text add "Brand" --x 100 --y 100 --font "Arial" --size 72`、`cli-anything-illustrator shapes rect --x 50 --y 50 --w 200 --h 100`、`cli-anything-illustrator export svg output.svg`，检查 output.svg 是否生成。
4. 验证 Photoshop Harness：依次执行 `cli-anything-photoshop project new poster.psd -w 1920 -h 1080`、`cli-anything-photoshop text add --content "Hello World" --font "Arial" --size 72`、`cli-anything-photoshop export png --output result.png`，检查 result.png 是否生成。
5. 验证 pptengine：进入 `WPS/ppt-engine/examples` 后执行 `python build_demo.py` 应生成 `out/demo.pptx`（+PDF），执行 `python build_from_json.py` 应生成 `out/from_json.pptx`。
6. 验证 WPS PPT 自动化生成示例：进入 `WPS/南科大` 后执行 `python build_sustech.py`，README 说明会「WPS可见生成 → PPTX + PDF」。

## 风险与注意事项

- 平台限制：README 明确要求 Windows 10/11，非 Windows 环境无法按 README 方式使用。
- 软件依赖较重：需要本机安装 WPS Office 2019+ 或 Microsoft Office 2016+ / Zotero 7+，Illustrator 与 Photoshop 部分还需要 Adobe Illustrator 2023+ / Adobe Photoshop 2023+。
- COM 自动化会真实操作本机软件：README 描述的是通过 COM 接口操控 WPS、Office、Illustrator、Photoshop，属于对真实桌面应用的自动化，README 未提供沙箱、回滚或权限隔离说明。
- README 已列出 7 个 WPS COM 坑（如 `SaveAs` 静默失败、中文字体方块等），说明该链路存在已知不稳定点；pptengine 声称已内置规避，但其他子项目 README 未说明是否同样处理。
- 关于数据安全、隐私、并发调用、错误重试、版本兼容矩阵等内容，README 未提供。
- 关于与 Trae Work / Java 的集成方式，README 未提供。

## 替代方案

README 未提供替代方案。README 中唯一可视为「同类替代」的说明是：COM 接口与 Microsoft Office VBA 兼容，如需操控 MS Office，将 ProgID 改为 `PowerPoint.Application` / `Word.Application` / `Excel.Application` 即可——即在 WPS 与 MS Office 之间切换。除此之外，README 未提及任何其他替代工具或方案。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
