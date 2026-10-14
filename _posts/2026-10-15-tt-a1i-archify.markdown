---
layout: post
title: "Archify 使用说明：把想法和代码库变成可交互架构图"
subtitle: "一个面向 Claude Code、Codex、Cursor 的 Agent Skill，用一句话生成可探索、可验证、可分享的 HTML 图"
date: 2026-10-15 04:23:58 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI技能
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/tt-a1i/archify
- Stars：83477
- 语言：JavaScript
- 创建时间：2026-04-15
- 最近更新：2026-10-14
- 官方简介：Turn any idea, plan, or codebase into a beautiful interactive diagram. An agent skill for Claude Code, Codex, and more.

---

> Archify 是一个 Agent Skill：你向 AI 编程助手用自然语言描述系统、计划或代码库，它生成一张自包含、可交互、经过校验的 HTML 图（架构 / 工作流 / 时序 / 数据流 / 生命周期等）。最适合已经在用 Claude Code、Codex、Cursor、OpenCode 等编码 Agent，希望把「讲清楚一个系统」这件事从画图软件里解放出来的开发者。

## 它到底解决什么问题

写文档、做评审、给同事讲清楚一次请求怎么走，往往比写代码还费时间。Archify 的定位是：**把「描述」直接变成「可探索的图」**。

- 你不需要打开绘图工具，也不需要手写 Mermaid 再调样式。
- 输出是**单个 HTML 文件**，内联 SVG，自带深色 / 浅色主题，可分享、可离线打开。
- 图不是「画得像」，而是**先经过校验再交付**：schema、布局、HTML/SVG、路由、标签与路由间距都要通过检查，产物才会替换上一次已知良好的输出。

官方给出的能力边界很明确：**它不是通用绘图编辑器**，也不是数字图表 / 仪表盘工具。它擅长的是「有步骤、有部件、有关系、有状态」的东西——既包括微服务拓扑、API 调用链、缓存回退、CI/CD 流水线，也包括年假怎么排、求职进度到哪一步、房租怎么流转这类日常主题。

## 核心概念与工作原理

理解下面几个词，基本就理解 Archify 了。

| 概念 | 含义 |
|---|---|
| Agent Skill | Archify 以「技能」形式挂载到编码 Agent 上，由 Agent 调用它的 CLI 与规则来生成图 |
| 类型化 JSON IR | 每张图先落成有 schema 的 JSON 中间表示，再渲染成 HTML，因此可复现、可比较 |
| 校验（validate） | 交付前的原子化检查，失败时返回稳定的规则代码、精确对象和实测证据，而不是一堆堆栈 |
| 上次良好状态 | 预览只在新候选通过全部关卡后才刷新；保存不完整或无效时继续显示上一张已验证的图 |
| 源证据（SRC n） | 基于证据的架构节点会标记来源，可打开固定到某个公开提交的文件与行范围；普通产物不带源 |

支持的图表类型官方口径为十种：**Architecture、Workflow、Sequence、Dataflow、Lifecycle、ERD、Class、Tree、Timeline、Waterfall**。官网把前五种作为「选哪个图」的推荐起点：

| 类型 | 回答的问题 | 提示里应包含 |
|---|---|---|
| Architecture | 它由什么组成？ | 范围、核心组件、主要路径 |
| Workflow | 接下来发生什么？ | 参与者、顺序、分支、异常 |
| Sequence | 谁在什么时候说了什么？ | 调用方、被调用方、返回、时序 |
| Data Flow | 东西都流到哪去了？ | 数据源、转换、存储、边界 |
| Lifecycle | 现在处于什么状态？ | 状态、事件、重试和取消路径 |

<!-- asset:blog-1 start -->
![五个核心概念](/img/ai-news/tt-a1i-archify/blog-1.png)

*图：五个核心概念*
<!-- asset:blog-1 end -->


## 环境与前置依赖

- **运行环境**：需要一个支持 Skill 的编码 Agent。官方明确列出 **Claude Code、Codex CLI、Cursor、OpenCode**，官网另标注支持 **Copilot**；赞助商页面提到 **Kimi Work** 插件商店中以「Interactive Architecture Diagram」形式提供。
- **Node.js**：安装与本地 CLI 通过 `npx` / `node` 调用，因此本机需要可用的 Node 环境。
- **零运行时依赖**：官方强调产物本身 **0 runtime dependencies**，生成的 HTML 不依赖外部服务即可打开。
- **许可证**：MIT。
- **版本**：官方仓库徽章与官网均标注稳定版 **v3.1.0**（更新日期 2026-10-14）；第三方评测页面在介绍时写的是 **v2.13.0**，两处说法不一致，以官方渠道的 v3.1.0 为准更稳妥。

> 关于 Stars：仓库元信息显示 83477，第三方技能站显示 81929，两者口径不同，此处并列供参考。

## 安装

Archify 的安装本质是「把技能装进你的 Agent」。官方给出的通用命令是：

```powershell
npx skills add tt-a1i/archify -g
```

`-g` 表示全局安装，装好后在你任意项目目录里都能调用这个技能。

如果你用的是 Cursor，官方提供了一个显式、非交互式的安装写法：

```powershell
npx -y skills add tt-a1i/archify --skill archify --agent cursor --global --copy --yes
```

只想临时试一下、不想永久安装，可以用：

```powershell
npx skills use tt-a1i/archify@archify --agent codex
```

这个切换器支持 `cursor`、`codex`、`claude-code` 和 `opencode` 四个目标。

> **关于 Trae Work 与 Java/Spring 集成**：官方公开资料中列出的集成目标是 Claude Code、Codex、Cursor、OpenCode、Copilot 以及 Kimi Work 插件商店，**官方未提供与 Trae Work 的集成方式，也未提供 Java/Spring 的 SDK 或 HTTP 接入方式**。因此不存在可照抄的 Trae 配置路径或 Maven 依赖，请不要自行编造。

## 快速上手

### 第一步：装好技能

在 Windows PowerShell 里执行上面的 `npx skills add tt-a1i/archify -g`，等待安装完成。

### 第二步：向 Agent 提一个明确限定的请求

官方推荐的第一个例子是描述一次 Web 请求：

```text
Use Archify to diagram a web request: Browser calls the API,
the API checks Redis, and a cache miss queries PostgreSQL and fills the cache.
```

对于真实代码库，官方建议这样提：

```text
Analyze this repository, then use archify to create a high-level runtime architecture diagram.
Show 8–12 core components, one primary path, external dependencies, and trust boundaries.
Put supporting detail in cards instead of adding more edges.
```

对 Java 后端来说，把「Web App → API → Redis → PostgreSQL」换成你自己的链路即可，例如网关、鉴权、服务层、缓存、数据库、消息队列。

### 第三步：在对话里持续细化

生成后不需要重新描述，直接追加聚焦指令，例如 `add Redis`、`move auth to the left`、`highlight the rollback path`。Archify 会保留输入的源，便于做有针对性的迭代。

### 第四步：导出与分享

导出菜单支持把 PNG 复制到剪贴板，并下载静态或动态格式（PNG / JPEG / WebP / SVG / WebM）。需要给文档、发布或社交帖子配一张规范的 **1200×630** 图时，用「复制分享卡片」；追踪某条路径后，用「导出 → 路径分享卡片」把该路径下载为 1200×630 PNG，并保留完整图表作为上下文。

## 如何确认安装与运行成功

- 安装命令执行后没有报错，且 Agent 能识别 `archify` 这个技能名。
- 向 Agent 发出上面的示例请求后，工作目录下会出现 `.archify/<type>-<slug>-<YYYYMMDD-HHMMSS>/` 文件夹，里面包含 `candidate.json` 与 `<slug>.html`。
- 用浏览器打开生成的 HTML，能看到可交互的图，并且深色 / 浅色主题可以切换。
- 官方还提供了一个零依赖 CLI 用来确认工具链可用，例如让它推荐图表类型：

```powershell
node archify/bin/archify.mjs guide "Show an API request with Redis cache miss"
```

> 注意：命令里的 `archify/bin/archify.mjs` 需要替换成你实际安装位置的绝对路径，或相对于当前工作目录的路径；输入输出路径都从该工作目录解析。

<!-- asset:code-1 start -->
```powershell
node archify/bin/archify.mjs guide "Show an API request with Redis cache miss"
```
<!-- asset:code-1 end -->


## 进阶用法

### 对比架构变更（适合 PR / 设计评审）

Architecture Delta 可以把经过验证的 Before / Delta / After 快照做比较，并给出机器凭证：

```powershell
node archify/bin/archify.mjs compare architecture base.json head.json architecture-delta.html --json
```

官方强调它**只做查看，不推断影响、风险或合并安全性**。

### 生产部署评审的严格模式

Architecture 可以启用 `deployment-ownership` 工程配置。当缺少负责人、单区域部署、私有数据库范围或具名边界跨越时，它会**拒绝通过（fail closed）**。它不会被静默启用，并且校验的是人工编写的事实，而非实时基础设施。

### 失败时怎么排查

`validate --json` 和 `deliver --json` 会返回稳定的规则代码、精确的对象、测量到的证据，并且只提供受支持的修复控制，而不是 Node 堆栈或非结构化的重试猜测。

## 局限与风险

- **不是通用绘图编辑器**，也不是数字图表 / 仪表盘工具；需要精确数值可视化时它不合适。
- **不声称运行时影响**：交互、路径追踪、角色比较都基于已编写的节点和关系，不会凭空发明拓扑。
- **源证据需要显式请求**：只有基于证据的 Architecture 节点才会标记 `SRC n` 并打开固定到单个公开提交的文件与行范围。
- **第三方服务与付费计划**：官方声明 Archify 本身免费开源，第三方在线服务与付费计划由其各自提供方运营，不代表 Archify。
- **版本口径不一致**：官方渠道为 v3.1.0，第三方评测页面写作 v2.13.0，安装前建议以官方渠道为准。
- **与 Trae Work / Java 无官方集成**：如前所述，官方未提供相关接入方式。

<!-- asset:blog-2 start -->
![使用前需知的边界](/img/ai-news/tt-a1i-archify/blog-2.png)

*图：使用前需知的边界*
<!-- asset:blog-2 end -->


## 社区评价

来自 Hacker News 讨论的反馈集中在两点：一是「输出是单个自包含 HTML」这一点被认为很实用，便于直接丢进文档或分享；二是「先校验再交付、保留上次良好状态」的机制被评价为比一次性生成更可靠。也有讨论提到，它更适合表达结构与关系，而不是替代专业绘图工具做精细排版。

## 一句话总结

如果你日常在编码 Agent 里工作，又经常需要把「一个系统 / 一个流程 / 一个计划」讲清楚，Archify 值得花五分钟装上试一次；如果你需要的是精细排版的通用绘图工具，或者想在 Trae Work 里直接调用，它目前并不对口。

```text
背景：我在 Windows 上用 Trae Work 开发 Java / Spring 后端项目，希望把一次典型的 API 请求链路讲清楚，用于团队评审和文档。
目标：用 Archify 生成一张可交互的架构图，覆盖网关、鉴权、服务层、Redis 缓存、PostgreSQL 数据库，并标出缓存未命中时的回退路径。
具体要求：
1. 先确认 Archify 技能是否已安装；如果未安装，给出在 Windows PowerShell 下的安装命令。
2. 如果 Archify 官方不支持 Trae Work，请直接说明，不要编造配置路径或命令。
3. 用自然语言描述这条请求链路，生成 Architecture 类型的图，核心组件控制在 8–12 个，只保留一条主路径，把细节放进卡片而不是增加连线。
4. 生成后把缓存未命中路径设为次要路径，并高亮出来。
5. 输出为单个自包含 HTML 文件，确认深色 / 浅色主题可切换，并说明如何导出 1200×630 分享卡片。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
