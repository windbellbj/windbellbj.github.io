---
layout: post
title: "claude-mem 使用说明书：给 AI 编程助手装上跨会话持久记忆"
subtitle: "自动记录 Claude Code 等 Agent 的会话要点，压缩后注入下一次会话，Java 后端也能快速试用"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - MCP服务
news_category: mcp
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/thedotmack/claude-mem
- Stars：99742
- 语言：TypeScript
- 创建时间：2025-08-31
- 最近更新：2026-10-11
- 官方简介：Persistent Context Across Sessions for Every Agent –  Captures everything your agent does during sessions, compresses it with AI, and injects relevant context back into future sessions. Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More

---

> claude-mem 是一个开源的「持久记忆压缩系统」：它自动捕获 AI 编程 Agent 在会话中的工具调用与关键结论，用 AI 压缩成结构化记忆，再在后续会话中把相关上下文注入回去。最适合那些长期用 Claude Code / Codex / Cursor 等 Agent 写代码、又厌倦每次重开会话都要重新交代项目背景的开发者。

## 它到底解决什么问题

AI 编程助手最大的痛点之一是「失忆」：一次会话结束后，之前讨论过的架构决策、踩过的坑、修过的 bug，下一次全部归零。claude-mem 的思路是把这些内容从聊天记录里抽出来，变成独立于会话的结构化笔记，并在新会话开始时按需注入。

官方把它描述为「为 Claude Code 打造的持久记忆压缩系统」，同时声明可配合 Claude Code、OpenClaw、Codex、Gemini、Hermes、Copilot、OpenCode 等多种 Agent 使用。官网首页的定位语是「All your context. Everywhere. All at once.」——让上一次会话中的决策、发现和修复，能被下一次会话、另一台机器、另一个工具直接使用。

典型适用场景：

- 项目周期长、上下文多，每次新开会话都要重新解释项目结构和技术选型。
- 团队里多人用 Agent 协作，希望关键决策有据可查。
- 需要在多台电脑之间延续同一项目的记忆。
- 想用自然语言检索「当时为什么这么改」。

## 核心概念与工作原理

claude-mem 由几个部件组成，理解它们有助于判断它是否适合你的工作流：

| 组件 | 作用 |
| --- | --- |
| 生命周期钩子 | 在会话开始、用户提交提示、工具调用后、停止、会话结束等时机自动捕获内容 |
| Worker 服务 | 本地 HTTP API，提供 Web 查看界面与搜索端点，由 Bun 管理 |
| SQLite 数据库 | 存储会话、观察记录与摘要 |
| mem-search 技能 | 用自然语言查询项目历史，支持渐进式披露 |
| Chroma 向量数据库 | 混合语义 + 关键词检索，用于智能召回上下文 |
| MCP 搜索工具 | 通过 4 个 MCP 工具按「3 层工作流」检索记忆，控制 token 消耗 |

工作流可以概括为：**捕获 → 压缩 → 存储 → 召回**。会话进行时钩子持续记录；会话结束后由 AI 压缩成结构化观察记录；新会话开始时，系统把与当前任务相关的记忆注入上下文。官网强调「渐进式召回」——先让 Agent 找到一条笔记的索引，需要时再读取详情，从而避免把整段对话塞回上下文。

隐私方面，官方提供 `<private>` 标签，可以把敏感内容排除在存储之外；另有自动脱敏（Auto-Redaction）相关文档。

## 环境与前置依赖

- **Node.js**：官方徽章标注 `>=20.0.0`。
- **Bun 与 uv**：安装器会检查这两项运行时依赖。
- **操作系统**：官方文档未限定平台，Windows 用户可参考下述 PowerShell 步骤；如遇脚本类问题，可优先考虑在 WSL 中执行。
- **账号（可选）**：默认安装流程会引导登录 claude-mem 账号（邮箱魔法链接，无需信用卡），并附带 30 天免费试用。若不想登录，可显式指定 `--provider`、设置 `CLAUDE_MEM_ONLINEOPTIN=false`，或在 CI/非交互式终端中运行，安装器会跳过账号交互。

> 注意：`npm install -g claude-mem` 只安装 SDK/库，不会注册插件钩子，也不会启动 Worker 服务。官方明确要求通过 `npx claude-mem install` 或插件市场命令安装。

## 安装与配置（Windows + PowerShell）

### 第一步：确认 Node 版本

在 PowerShell 中执行 `node -v`，确认输出不低于 v20。若版本过低，先升级 Node.js。

### 第二步：执行安装

在 PowerShell 中运行 `npx claude-mem install`。安装器分三个阶段：

1. **选择 Agent 并安装运行时**：自动预选检测到的 Agent（含 OpenCode、OMP、Cursor、Codex CLI 等），检查 Bun 与 uv，把插件文件复制到市场目录、注册插件并安装依赖。
2. **登录**：启动 OAuth 配对，打印形如 `XXXX-XXXX` 的设备码，并在浏览器打开授权地址，轮询直到认证完成。若选择 `--provider claude`（使用自己的 Anthropic 套餐），此步跳过。
3. **选择记忆提供方**：默认预选 CMEM Pro（托管记忆），也可选择自己的 OpenRouter、Gemini、Anthropic 套餐，或 `--provider host`（本地回环观察器）。选择后写入 `~/.claude-mem/settings.json` 并重启 Worker。

### 第三步：按目标 Agent 选择安装参数

- Claude Code：`npx claude-mem install`，或在 Claude Code 内执行 `/plugin marketplace add thedotmack/claude-mem` 后再执行 `/plugin install claude-mem`，然后重启 Claude Code。
- OpenCode：`npx claude-mem install --ide opencode`，要求 OpenCode 1.3.4 及以上（含 OpenCode 2），安装后重启 OpenCode。
- T3 Code：`npx claude-mem install --ide t3code`，安装器会识别已启用的提供方并注册原生插件，重启后按提示信任钩子并新建线程。
- Antigravity CLI：`npx claude-mem install --ide antigravity`。
- OMP：`npx claude-mem install --ide omp`。
- Pi / DeepSeek Harness：`npx claude-mem install --ide pi` 或 `npx claude-mem install --ide dsh --dsh-profile tui`。
- Grok Bot：`npx claude-mem install --ide grok-bot`，默认使用 CMEM Pro，本地观察器需显式加 `--provider host`。
- OpenClaw 网关：官方提供一键脚本 `curl -fsSL https://install.cmem.ai/openclaw.sh | bash`（该命令为官方给出的 shell 形式，Windows 下建议在 WSL 或 Git Bash 中执行）。

### 第四步：融入 Trae Work 与 Java / Spring 工作流

这里需要说清楚一件事：**官方未提供与 Trae Work 的直接集成方式，也未提供 Java / Spring 的 SDK 或 HTTP 集成路径。** 官方列出的集成对象是 Claude Code、OpenCode、T3 Code、Cursor、Codex、Grok Bot、Antigravity、OMP、Pi、DeepSeek Harness、OpenClaw 等，Trae Work 不在其中。

因此对 Java 后端开发者而言，现实可行的路径是：

1. **把 claude-mem 当作独立的记忆服务使用**：安装后它会启动本地 Worker 服务并提供 HTTP API 与 Web 查看界面。你可以在 Trae Work 中让 AI 助手通过 HTTP 调用该服务来检索历史记忆——但这属于自行接线，官方未提供现成配置。
2. **把 MCP 搜索工具接入支持 MCP 的客户端**：claude-mem 提供 4 个 MCP 搜索工具。若你的 Trae Work 版本支持自定义 MCP 服务，可尝试把 claude-mem 的 MCP 端点加入配置；具体端点与配置格式官方未在公开资料中给出针对 Trae Work 的说明。
3. **在终端中作为 CLI 使用**：安装后可在 PowerShell 中通过 `npx claude-mem` 相关子命令与记忆交互，适合脚本化或手动查询。
4. **Java / Spring 项目本身无需改动**：claude-mem 不侵入你的代码库，它记录的是 Agent 的会话行为，而不是你的 Java 源码。你可以在 Spring 项目目录下正常使用已支持的 Agent，记忆会按项目维度沉淀。

> 如果你的核心诉求是「在 Trae Work 里直接获得跨会话记忆」，目前需要自行验证可行性；官方公开资料中没有 Trae Work 集成章节。

## 快速上手

1. 在 PowerShell 中执行 `npx claude-mem install`，按提示选择 Agent、完成登录、选择记忆提供方。
2. 重启你选择的 Agent（例如 Claude Code 或 OpenCode）。
3. 正常开始一次编码会话，让 Agent 读代码、改代码、做决策。
4. 结束会话，重新开一个会话，观察是否自动带入了此前的上下文。
5. 需要主动检索时，使用 mem-search 技能或 MCP 搜索工具，用自然语言提问，例如「我们为什么把重试限制在三次」。

## 如何确认安装成功

官方文档给出了一组安装后验证动作，可逐项检查：

1. **依赖自动安装**：安装器应自动完成依赖安装，无报错。
2. **插件注册**：确认插件已注册到对应 Agent 的市场目录。
3. **数据目录**：确认数据目录已生成，记忆数据落盘。
4. **Worker 日志**：检查 Worker 服务日志，确认服务已启动。
5. **上下文检索测试**：发起一次检索，确认能返回历史观察记录。
6. **CMEM Pro / 同步**：若使用托管记忆，确认同步状态正常。

启动时 Worker 会打印访问地址，浏览器打开即可看到实时记忆流界面。

## 费用与授权

- **开源引擎免费**：本地 claude-mem 引擎是开源的，许可证为 Apache 2.0。
- **CMEM Pro 付费**：托管观察、云同步和私有 MCP 连接属于付费服务，30 天免费试用，之后官网标注为每月 30 美元。
- **TeamBrain 试点**：面向团队共享记忆，官方表示试点范围与入驻方式需双方商定，公开的团队定价尚未公布。
- **不影响其他订阅价格**：官网说明 CMEM Pro 不会改变其他订阅的价格或额度；托管观察把记忆生成从主 Agent 的订阅上移走，对 token 消耗的影响取决于工作负载和提供方。

## 局限与风险

- **捕获范围有限**：官网明确说明并非所有工具的所有内容都会被捕获，捕获取决于所安装的工具与集成方式。MCP 连接只提供召回；连接 ChatGPT 不会自动捕获 ChatGPT 对话。
- **Trae Work 无官方支持**：如前所述，官方未提供 Trae Work 集成，Java / Spring 也没有官方 SDK。
- **平台差异**：官方文档未针对 Windows 给出专门说明，部分安装脚本（如 OpenClaw 的一键脚本）为 shell 形式，Windows 下可能需要 WSL 或 Git Bash。
- **数据敏感性**：记忆会被压缩并存储，涉及密钥、客户数据时应使用 `<private>` 标签或自动脱敏功能。
- **成熟度**：项目创建于 2025-08-31，迭代非常活跃（仓库元信息显示最近更新为 2026-10-11，版本号 13.35.0），但快速迭代也意味着配置项和行为可能变化。
- **版本号口径不一**：仓库徽章标注版本 13.35.0，而第三方插件目录页面显示为 11.0.1，两者不一致，使用时以实际安装版本为准。

## 社区评价

Hacker News 上关于 AI 记忆的讨论热度很高。在《Claude Memory》话题下（559 points，312 条评论），以及《Show HN: Recall: Give Claude memory with Redis-backed persistent context》（171 points，93 条评论）中，社区观点呈现明显分歧：

- 有用户担心「旧代码渗进新代码」，认为对话式记忆更适合增强「Claude 懂你」的体验，而不适合编码场景。
- 也有用户表示「不想要旧代码污染新代码，但很想要对话之间的记忆」。
- 有实际使用者反馈，使用后上下文问题变少，在上下文压缩（context compact）之后也能轻松召回。
- 还有人质疑：为什么不用 `.md` 形式的上下文文件，例如 SpecKit 项目的做法。

这些讨论并非针对 claude-mem 本身，但反映了「AI 记忆」这一类工具共同的争议点：记忆的边界控制与注入精度，决定了它是助力还是噪音。

## 一句话建议

如果你主力使用 Claude Code、OpenCode、Codex 等官方支持的 Agent，且项目周期长、上下文负担重，claude-mem 值得花半小时装来试试；如果你坚持在 Trae Work 里完成全部工作，目前需要自行探索 HTTP 或 MCP 接线，官方没有现成答案。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring 后端项目，技术栈是 Spring Boot + MyBatis + MySQL，日常用 AI 助手读代码、改接口、排查线上问题。我听说 claude-mem 能给 AI 编程助手加跨会话持久记忆，但官方没有 Trae Work 集成说明。

目标：帮我在不破坏现有项目的前提下，评估并尝试把 claude-mem 接入我的工作流，让它能记住项目里的架构决策、踩坑记录和修复方案。

具体要求：
1. 先帮我确认本机 Node 版本是否满足 claude-mem 要求的 >=20，并列出需要预装的运行时依赖（Bun、uv）。
2. 给出在 Windows PowerShell 中安装 claude-mem 的完整步骤，包括 npx claude-mem install 的交互流程说明，以及如何跳过登录、如何选择本地观察器。
3. 分析 claude-mem 的本地 Worker HTTP API 和 4 个 MCP 搜索工具，判断我的 Trae Work 版本能否通过自定义 MCP 配置接入；如果不能，给出替代方案（例如在终端用 CLI 查询记忆）。
4. 说明如何验证安装成功：插件注册、数据目录、Worker 日志、上下文检索测试分别怎么检查。
5. 提醒我哪些内容不应该被记忆捕获，以及如何用 <private> 标签保护敏感信息。
6. 最后给我一个最小试用计划：用一周时间在 Spring 项目上记录哪些类型的决策，如何评估记忆召回是否真的提升了效率。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
