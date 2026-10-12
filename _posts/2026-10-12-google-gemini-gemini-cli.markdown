---
layout: post
title: "Gemini CLI 使用说明书：把 Gemini 装进 Windows 终端"
subtitle: "免费额度、MCP 扩展、GEMINI.md 上下文，Java 后端在 Trae Work 旁多开一个终端 Agent"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - 编码Agent
news_category: agent-cli
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/google-gemini/gemini-cli
- Stars：107286
- 语言：TypeScript
- 创建时间：2025-04-17
- 最近更新：2026-10-10
- 官方简介：An open-source AI agent that brings the power of Gemini directly into your terminal.

---

> Gemini CLI 是 Google 开源的终端 AI Agent，把 Gemini 模型直接接进命令行，能读写代码库、跑 shell、联网搜索、通过 MCP 扩展能力；最适合习惯命令行、想用免费额度快速试水 AI 编码 Agent 的开发者。

## 它解决什么问题

日常写 Java / Spring 时，很多活儿其实不需要离开终端：查一个陌生依赖的用法、批量改包名、解释一段遗留代码、跑一遍 Maven 测试再根据报错定位。Gemini CLI 的定位就是「从提示词到模型的最短路径」——在项目根目录敲一个 `gemini`，它就能读到当前代码库，并调用内置工具去读文件、执行命令、联网查资料。

官方列出的典型能力包括：

| 能力 | 说明 |
| --- | --- |
| 代码理解与生成 | 查询和编辑大型代码库；用多模态能力从 PDF、图片、草图生成新应用；用自然语言调试排错 |
| 自动化与集成 | 自动处理查询 PR、复杂 rebase 等运维任务；通过 MCP 服务器接入新能力；在脚本中非交互式运行 |
| 进阶能力 | 内置 Google Search 做实时信息 grounding；会话检查点（checkpointing）保存与恢复；用 `GEMINI.md` 定制项目上下文 |
| GitHub 集成 | 通过 Gemini CLI GitHub Action 做 PR 自动评审、Issue 分类、在 Issue/PR 中 @gemini-cli 求助 |

## 核心概念

- **终端优先的 Agent**：不是补全插件，而是一个能自主调用工具的会话式 Agent。
- **内置工具**：文件系统操作、shell 命令、网页抓取与搜索，开箱即用。
- **MCP（Model Context Protocol）**：通过 MCP 服务器挂载自定义工具，例如官方提到的用 Imagen、Veo、Lyria 做媒体生成。
- **`GEMINI.md` 上下文文件**：放在项目里，为该项目提供持久上下文，相当于给 Agent 一份长期记忆的项目说明。
- **检查点（Checkpointing）**：保存并恢复复杂会话。
- **非交互模式**：`-p` 直接拿文本结果，`--output-format json` 拿结构化输出，`--output-format stream-json` 拿逐行 JSON 事件流，适合脚本与监控。

## 环境与前置依赖

- **Node.js 20 或更高版本**（官方系统要求）。
- 支持 **macOS、Linux 或 Windows**。
- 需要一个 Google 账号、Gemini API Key 或 Vertex AI 凭据之一。

> 关于模型版本，不同渠道说法不一致：仓库说明与官网当前页面写的是 **Gemini 3 模型**、100 万 token 上下文窗口；较早的第三方介绍页面写的是 **Gemini 2.5 Pro**、同样 100 万 token 上下文。以你安装时实际可选的模型为准。

## 安装（Windows PowerShell）

### 方式一：免安装直接跑

1. 打开 PowerShell。
2. 执行 `npx @google/gemini-cli`。

适合先试一口再决定要不要常驻。

### 方式二：全局安装（推荐）

1. 确认 Node 版本：`node -v`，需为 20 或以上。
2. 执行 `npm install -g @google/gemini-cli`。
3. 安装完成后执行 `gemini` 启动。

### 发布通道

官方每周二发布，分三条通道，用 npm tag 切换：

| 通道 | 发布时间（UTC） | 安装命令 |
| --- | --- | --- |
| Preview | 每周二 23:59 | `npm install -g @google/gemini-cli@preview` |
| Stable | 每周二 20:00 | `npm install -g @google/gemini-cli@latest` |
| Nightly | 每天 00:00 | `npm install -g @google/gemini-cli@nightly` |

> Preview 与 Nightly 未经完整验证，可能带回归问题，生产环境建议用 `latest`。

## 认证配置

三条路线，按需选一条：

**路线一：用 Google 账号登录（个人开发者首选）**

1. 执行 `gemini` 启动。
2. 在提示中选择 *Sign in with Google*，按浏览器流程完成授权。
3. 免费额度为每分钟 60 次请求、每天 1000 次请求。
4. 若使用组织发放的付费 Code Assist 许可，需先设置云项目：在 PowerShell 中执行 `$env:GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"`，再执行 `gemini`。

**路线二：Gemini API Key**

1. 到 `https://aistudio.google.com/apikey` 取 Key。
2. 在 PowerShell 中执行 `$env:GEMINI_API_KEY="YOUR_API_KEY"`。
3. 执行 `gemini`。

**路线三：Vertex AI（企业/生产）**

1. 在 PowerShell 中执行 `$env:GOOGLE_API_KEY="YOUR_API_KEY"`。
2. 再执行 `$env:GOOGLE_GENAI_USE_VERTEXAI=true`。
3. 执行 `gemini`。

> 官方示例用的是 `export`（macOS/Linux 写法），Windows PowerShell 下对应 `$env:变量名="值"`。若希望长期生效，可用系统环境变量界面或 `setx` 持久化。

## 融入 Trae Work + Java / Spring 的日常工作流

先说结论：**官方未提供与 Trae Work 的集成方式**，也没有针对 Java / Spring 的专用 SDK 或插件。它是以「终端里的独立 Agent」形态存在的，因此最自然的用法是**与 Trae Work 并行**：Trae Work 负责 IDE 内的编辑与重构，Gemini CLI 在旁边的 PowerShell 里做代码库问答、批量脚本、跑构建与测试。

可落地的几种接法：

1. **终端 CLI 调用（最直接）**：在 Spring 项目根目录打开 PowerShell，执行 `gemini`，让它读当前代码库。多模块项目可加目录：`gemini --include-directories ../lib,../docs`。
2. **指定模型**：`gemini -m gemini-2.5-flash`（模型名以你账号实际可选为准）。
3. **脚本化 / CI 辅助**：`gemini -p "Explain the architecture of this codebase"` 拿纯文本；加 `--output-format json` 拿结构化结果；加 `--output-format stream-json` 拿逐行 JSON 事件流，便于监控长任务。
4. **MCP 服务接入**：在 `~/.gemini/settings.json` 中配置 MCP 服务器来扩展工具。配置好后可在会话里用 `@github`、`@slack`、`@database` 这类前缀调用，例如 `@database Run a query to find inactive users`。具体字段格式请以官方 MCP Server Integration 文档为准。
5. **项目上下文**：在 Spring 项目根目录放一个 `GEMINI.md`，写清模块划分、构建命令、代码规范，让 Agent 每次进入项目都带着这份背景。
6. **GitHub 侧**：接入 Gemini CLI GitHub Action，做 PR 自动评审与 Issue 分类；在 Issue / PR 里 @gemini-cli 触发按需协助。

> 注意：Gemini CLI 不是 Trae Work 的插件，也不会出现在 Trae Work 的侧边栏里。把它当成「另一个窗口里的结对程序员」来用，而不是 IDE 内的功能。

## 快速上手

1. 在 Spring 项目根目录打开 PowerShell。
2. 执行 `gemini` 进入交互会话。
3. 首次使用按提示完成 Google 账号登录。
4. 直接提问，例如让它总结昨天以来的改动、解释某个 Service 的调用链、或根据报错定位问题。
5. 需要一次性答案时改用 `gemini -p "你的问题"`。
6. 会话复杂时用检查点保存，下次恢复继续。

## 如何确认安装成功

- `gemini` 能正常启动并进入交互界面，说明安装与认证都通了。
- 在会话里发一条简单指令（例如让它总结当前目录结构），能返回合理结果，说明模型与工具链正常。
- 用 `gemini -p "hello"` 能拿到纯文本输出，说明非交互模式可用。
- 遇到问题可在会话内用 `/bug` 命令直接上报。

## 局限与风险

**许可证与费用**

- 开源协议为 **Apache License 2.0**。
- 免费额度：个人 Google 账号每分钟 60 次请求、每天 1000 次请求；API Key 路线为每天 1000 次请求（Gemini 3，flash 与 pro 混合）。超出后按各路线规则计费或受限。

**成熟度与生命周期（重要）**

- 官网当前挂出提示：**未付费层级与 Google One 用户，Gemini CLI 已于 2026 年 6 月 18 日被 Antigravity CLI 取代**。
- Hacker News 上有一篇《Gemini CLI will stop working from June 18, 2026》的讨论（406 points、209 条评论），社区在讨论迁移到 Antigravity CLI，以及「未来可能需要转向基于 MCP 的变通方案」。
- 这意味着：如果你属于上述用户群，现在上手前要先确认自己是否还能用；企业/付费路线的情况请以官方公告为准。

**安全风险**

- Hacker News 上有一篇《I watched Gemini CLI hallucinate and delete my files》的讨论（304 points、365 条评论），标题即结论：Agent 误判可能造成文件被删。
- 官方提供了沙箱（Sandboxing & Security）与受信任文件夹（Trusted Folders）机制来控制执行策略，建议在重要仓库中启用，并保持版本控制可回滚。

**社区评价（来自 Hacker News 讨论）**

- 首发讨论《Gemini CLI》热度很高（1428 points、788 条评论），社区对免费额度与终端形态反应积极。
- 有评论提到内置彩蛋，例如输入 `/corgi` 可激活 corgi 模式。
- 也有评论认为，随着各家 CLI Agent 林立，未来可能更多依赖 MCP 这类通用协议来做跨工具编排。

**其他已知边界**

- 官方未公开说明与 Trae Work 的集成方式，也无 Java / Spring 专用 SDK。
- 与 Java 项目的结合主要靠「在项目目录里跑 CLI + 写 `GEMINI.md` + 用 MCP 挂工具」这三件事。

## 一段可直接交给 Trae Work 的落地指令

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 多模块项目，项目根目录已安装并登录 Gemini CLI（命令为 gemini）。

目标：把 Gemini CLI 变成我日常开发流程里的一个固定环节，而不是偶尔试一次。

请帮我完成以下事情，并给出可直接执行的 Windows PowerShell 命令：
1. 为当前 Spring 项目起草一份 GEMINI.md，内容包括：模块划分与职责、常用构建与测试命令（Maven）、代码规范要点、禁止修改的目录、以及我希望 Agent 默认遵守的回答风格。
2. 设计 3 个我每天都会用到的非交互式调用场景，并写出对应命令，要求覆盖：解释某个包/类的调用链、根据一段报错定位可能原因、总结最近一次提交以来的改动。
3. 说明如何在本机配置 MCP 服务器（给出 settings.json 的字段结构说明即可，不要编造不存在的字段），并给出一个对 Java 后端有用的 MCP 使用示例。
4. 列出在重要仓库中使用 Gemini CLI 时应当开启的安全设置（沙箱、受信任文件夹），并解释各自作用。
5. 最后给出一份「每天 5 分钟」的试用清单，让我能在一周内判断它是否值得长期留在我的工作流里。

约束：所有命令必须是 Windows PowerShell 写法；不确定的地方明确标注「需查阅官方文档确认」，不要编造版本号、路径或参数。
```

## 卸载

官方提供独立的卸载指南，按其中的步骤移除即可；若只是临时试用，用 `npx @google/gemini-cli` 的方式运行则无需卸载。

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
