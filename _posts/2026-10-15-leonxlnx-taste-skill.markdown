---
layout: post
title: "Taste Skill：让编码 Agent 告别 AI 味前端的技能包"
subtitle: "给 Cursor、Claude Code、Codex 等 Agent 装上艺术指导、真实配图与浏览器自检，专治千篇一律的落地页"
date: 2026-10-15 04:23:58 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI技能
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/Leonxlnx/taste-skill
- Stars：96319
- 语言：JavaScript
- 创建时间：2026-02-19
- 最近更新：2026-10-14
- 官方简介：Agent skills that give coding agents taste: art direction, reference images and a browser check instead of generic AI pages

---

> Taste Skill 是一组 Agent Skills，让编码 Agent 像设计师一样做网站，而不是拼出千篇一律的落地页——它给 Agent 一套艺术方向、真实图片和真实浏览器自检能力。最适合需要产出面向公众的落地页、营销站、作品集与产品页的前端/全栈开发者。

## 它解决什么问题

一个模型生成的页面，通常看起来像它见过的所有页面的平均值：居中标题占三行、上面一个小标签、一排图标卡片、一层柔和渐变、几条细线和一个等宽字体说明。里面没有一处是错的，也没有一处是被决定过的。

Taste Skill 用四种方式把这些默认值替换成真正的决策：

- **方向由脚本发牌、你来选**：让模型凭空发明一个外观，它每次都会选品类默认值。`scripts/draw.mjs` 从 20 个经过研究的方向里发三张牌，你挑出最贴合主题的那一个，脚本再从 247 个真实站点提炼出的库里发出它的字体系统、配色、首屏与分节构图。
- **创意来自主题本身**：在研究中，最好的站点与最容易被遗忘的站点之间的差别，是概念取自事物本身，而不是取自样式。
- **无装饰的自家风格，由真实浏览器度量**：`scripts/inspect.mjs` 在真实浏览器里检查规则，让规则是被验证的，而不是被期望的。
- **你要亲眼看自己做了什么**：三个宽度下的截图、一份评审评分表、修复、再看一遍。

## 适用场景

| 你的情况 | 建议使用的技能 |
| --- | --- |
| 从零做一个新的公开页面 | **taste-skill**（默认，v2） |
| 改进一个已经存在的页面 | **redesign-skill** |
| 视觉方向已经定了 | **soft-skill**、**minimalist-skill** 或 **brutalist-skill** |
| 想先出图、再写代码 | 图像生成类技能，或一步到位的 **image-to-code-skill** |
| Agent 总是把输出写一半就收尾 | 加上 **output-skill** |

需要注意：默认技能面向**面向公众的页面**，不适用于仪表盘和应用内界面；产品 UI 请改用 **minimalist-skill** 或 **soft-skill**。它支持 React、Vue、Svelte、纯 HTML——规则是关于设计的，与框架无关。

## 核心概念与工作原理

默认技能基于对 247 个精选站点的研究构建，一次构建分六步：

1. 读取需求简报，列出只有这个客户才有的东西。
2. 一个脚本从 20 个经过研究的方向里发三张牌，Agent 从中选一个。
3. 找到创意：用一句话把客户自己的素材与那个方向绑在一起。
4. 用开放图库里的真实图片和影像来构建，并标注出处。
5. 在真实浏览器里以三个宽度检查页面，不合格就判失败。
6. 看自己的截图，修掉最严重的三个问题，最多三轮。

一次构建大约需要 **30 到 45 分钟**，消耗几十万 token。

### 技能清单

每个技能只做一件事，你不需要全部安装。**安装名**是传给 `--skill` 的值。

| 技能 | 安装名 | 作用 |
| --- | --- | --- |
| taste-skill | `design-taste-frontend` | v2。任意技术栈的落地页、营销站、作品集与产品页的艺术指导 |
| redesign-skill | `redesign-existing-projects` | 已有项目：先审计 UI，再修布局、间距、层级与样式 |
| image-to-code-skill | `image-to-code` | 先生成站点参考图，分析后再把前端实现成匹配的样子 |
| gpt-tasteskill | `gpt-taste` | 面向 GPT 与 Codex 的更严格变体：更强的布局变化与动效方向 |
| soft-skill | `high-end-visual-design` | 平静、精致的 UI：柔和对比、留白、弹簧动效 |
| minimalist-skill | `minimalist-ui` | 编辑感的产品 UI，克制的配色与清晰的结构 |
| brutalist-skill | `industrial-brutalist-ui` | 硬朗的机械语言：瑞士字体、锐利对比、实验性布局 |
| stitch-skill | `stitch-design-taste` | 面向 Google Stitch 的规则，可选导出 `DESIGN.md` |
| output-skill | `full-output-enforcement` | 当模型交付半成品时使用：完整输出，不留占位注释 |

另有三个图像生成技能（只出设计图、不出代码）：`imagegen-frontend-web`（网站稿：首屏、落地页、多分节）、`imagegen-frontend-mobile`（iOS、Android 与跨平台的移动端界面与流程）、`brandkit`（品牌套件板：logo 方向、配色、字体、应用示例）。

### 旧版本

| 技能 | 安装名 | 说明 |
| --- | --- | --- |
| taste-skill-v2-experimental | `design-taste-frontend-v2-experimental` | v2 之前作为默认的单文件、旋钮驱动重写版 |
| taste-skill-v1 | `design-taste-frontend-v1` | 最初的版本 |

这两个旧版本在文件顶部各有三个 1 到 10 的旋钮：**DESIGN_VARIANCE**（从居中干净到非对称）、**MOTION_INTENSITY**（从仅悬停到滚动驱动）、**VISUAL_DENSITY**（从疏朗到密集）。v2 没有旋钮，它的方向来自发牌，它的边界来自检查器。

<!-- asset:blog-1 start -->
![一次构建的六步流程](/img/ai-news/leonxlnx-taste-skill/blog-1.png)

*图：一次构建的六步流程*
<!-- asset:blog-1 end -->


## 环境与前置依赖

- **Node 22 或更高版本**（默认技能用它运行脚本）。
- 已安装的 **Chrome、Edge 或 Chromium**（用于真实浏览器检查）。
- 它不安装任何东西，也不需要 API key。
- 只有找图片时需要网络访问。

> 图片来自 Wikimedia Commons、Openverse、Met 等开放图库，只提供公有领域、CC0、CC BY 与 CC BY-SA 的文件，技能会把出处标注在页面上。拿到自己的图后请替换掉它们。

## 安装与配置

### 通用安装

安装仓库里的全部技能：

```powershell
npx skills add https://github.com/Leonxlnx/taste-skill
```

只装其中一个，传入它的安装名：

```powershell
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

已经装过？再跑一次安装命令即可。安装名没有变，旧版本仍以各自的名字保留可用。

### 从克隆安装（软链接而非复制）

`./install.sh` 会把技能软链接进 Claude Code（`--codex` 用于 Codex，`--all-agents` 用于两者），这样一次 `git pull` 就能就地更新它们。`./install.sh --list` 会列出所有安装名。

### 在 Trae Work 中接入

Taste Skill 的形态是 **Agent Skill**：每个技能就是一个 `SKILL.md`，Agent 在动 UI 之前先读它。官方说明它可插入任何会读取 `SKILL.md` 文件的工具，官网列出的适配对象包括 Cursor、Claude Code、Codex、Gemini CLI、v0、Lovable、OpenCode 等。

**官方未提供与 Trae Work 的集成方式**，也未提供与 Java / Spring 的集成方式。它不通过 MCP 服务接入，也没有 Java SDK 或 HTTP 接口，因此无法作为 MCP 服务或 SDK 集成进 Java / Spring 项目。

如果你的 Trae Work 支持读取 `SKILL.md` 形式的技能目录，可以按上面的通用安装命令安装后，将技能文件放入 Trae Work 的技能目录试用；具体目录路径官方未公开说明，请以 Trae Work 自身文档为准。

### Claude Code 插件

在 Claude Code 内运行以下命令。每个技能都归在 `taste-skill:` 命名空间下，不会与你的其他技能冲突：

```text
/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill@taste-skill
```

之后用 `/plugin update` 升级。

### Codex 插件

```powershell
codex plugin marketplace add Leonxlnx/taste-skill
codex plugin add taste-skill@taste-skill
```

之后请新开一个 Codex 会话，让技能被加载。

<!-- asset:code-1 start -->
```powershell
npx skills add https://github.com/Leonxlnx/taste-skill
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```
<!-- asset:code-1 end -->


## 快速上手

1. 确认本机有 Node 22+ 与 Chrome / Edge / Chromium。
2. 在 PowerShell 中执行 `npx skills add https://github.com/Leonxlnx/taste-skill`，或只装默认技能：`npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"`。
3. 在你的编码 Agent 里新开一个会话，让它读取技能。
4. 给出一份页面需求简报，让 Agent 按技能的六步流程构建。
5. 构建过程中，脚本会发出三个方向供你选择；挑出最贴合主题的那一个。
6. 构建完成后，查看三个宽度下的截图，按评审评分表让 Agent 修掉最严重的问题。

## 如何确认安装成功

- 安装命令执行后，技能被写入你的 Agent 技能目录；`./install.sh --list` 会列出所有安装名，可用来核对。
- 在 Claude Code 中，技能归在 `taste-skill:` 命名空间下，可在插件列表中看到。
- 在 Codex 中，新开会话后技能应被加载。
- 触发一次构建时，若 Agent 开始执行「读取简报 → 发牌选方向 → 找创意 → 用真实图片构建 → 浏览器三宽度检查 → 看截图修复」的流程，说明技能已生效。

## 局限与风险

- **成熟度**：v2 是实验性的，且已经是默认版本。安装名保持稳定，规则措辞会在 2.0 之前继续调整。如果你的项目依赖 v1 的确切行为，请改用 `design-taste-frontend-v1`。
- **适用范围**：默认技能面向公开页面，不适合仪表盘和应用内界面。
- **成本**：一次构建约 30 到 45 分钟、几十万 token，不适合轻量改动。
- **图片版权**：图片来自开放图库，仅限公有领域、CC0、CC BY、CC BY-SA，技能会在页面上标注出处；正式项目建议替换为自有素材。
- **许可证**：MIT。
- **安全**：第三方技能目录显示其通过 Gen Agent Trust Hub、Socket、Snyk 三项安全审计。
- **接入限制**：官方未提供与 Trae Work、Java / Spring 的集成方式，也没有 MCP 服务形态。

<!-- asset:blog-2 start -->
![使用前需注意的几点](/img/ai-news/leonxlnx-taste-skill/blog-2.png)

*图：使用前需注意的几点*
<!-- asset:blog-2 end -->


## 社区评价

来自 Hacker News 讨论的反馈：社区关注点集中在「反 AI 味」这一诉求上，认为把设计规则固化成 Agent 可读的技能文件、并用真实浏览器做自检，是比单纯调提示词更可复现的做法；同时也有讨论提到 v2 的构建耗时与 token 消耗偏高，以及实验性版本作为默认版本带来的稳定性顾虑。

```text
背景：我在 Windows 上用 Trae Work 开发，技术栈是 Java / Spring，需要为项目做一个面向公众的产品落地页。

目标：用 Taste Skill 的默认技能 design-taste-frontend，产出一个不像模板的落地页前端。

具体要求：
1. 先确认本机已安装 Node 22+ 与 Chrome / Edge / Chromium。
2. 在 PowerShell 中执行：npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
3. 安装后新开一个会话，读取该技能，然后按技能的六步流程构建页面：读取简报、从脚本发出的三个方向中选一个、用一句话把主题与方向绑定、用开放图库的真实图片构建并标注出处、在真实浏览器里以三个宽度检查、看截图修掉最严重的三个问题。
4. 页面是公开的营销/产品页，不要做成仪表盘或应用内界面。
5. 技术栈用纯 HTML/CSS/JS 或你判断合适的前端方案，规则与框架无关；后端接口按 Spring 的常规方式预留。
6. 构建完成后，把三个宽度的截图和评审结论给我，并说明你修掉了哪三个问题。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
