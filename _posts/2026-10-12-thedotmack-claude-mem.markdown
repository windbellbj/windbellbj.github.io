---
layout: post
title: "claude-mem 上手：给编码 Agent 装上跨会话记忆"
subtitle: "自动捕获会话、AI 压缩、下次会话注入上下文，Java 程序员也能快速试用"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/thedotmack/claude-mem
- Stars：99687
- 语言：TypeScript
- 创建时间：2025-08-31
- 最近更新：2026-10-11
- 官方简介：Persistent Context Across Sessions for Every Agent –  Captures everything your agent does during sessions, compresses it with AI, and injects relevant context back into future sessions. Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More

---

## 解决什么问题

README 指出，Claude-Mem 是一个为 Claude Code 打造的持久记忆压缩系统（Persistent memory compression system built for Claude Code）。它要解决的核心问题是：Agent 在会话结束后会丢失上下文。

按 README 描述，Claude-Mem 会自动捕获工具使用观察（tool usage observations）、生成语义摘要（semantic summaries），并让这些内容在未来的会话中可用，从而让 Claude 在会话结束或重连之后，仍能保持对项目的知识连续性。

官方简介也写明：它捕获 Agent 在会话中做的一切，用 AI 压缩，再把相关上下文注入到未来的会话中，支持 Claude Code、OpenClaw、Codex、Gemini、Hermes、Copilot、OpenCode 等。

## 核心概念

README 列出的核心组件包括：

- 5 个生命周期 Hook：SessionStart、UserPromptSubmit、PostToolUse、Stop、SessionEnd（共 6 个 hook 脚本）。
- Smart Install：缓存式依赖检查器（pre-hook 脚本，不是生命周期 hook）。
- Worker Service：本地 HTTP API，带 Web 查看器 UI 和搜索端点，由 Bun 管理。
- SQLite 数据库：存储 sessions、observations、summaries。
- mem-search Skill：自然语言查询，配合渐进式披露（progressive disclosure）。
- Chroma 向量数据库：语义 + 关键词的混合搜索，用于智能上下文检索。

README 还提到 4 个 MCP 搜索工具，遵循省 token 的 3 层工作流：

1. `search`：拿到带 ID 的紧凑索引（约 50-100 tokens/条结果）。
2. `timeline`：查看感兴趣结果前后的时间线上下文。
3. `get_observations`：只对筛选后的 ID 拉取完整详情（约 500-1,000 tokens/条结果）。

README 称这种“先过滤再取详情”的方式可节省约 10 倍 token。

## 前置依赖

README 的 System Requirements 写明：

- Node.js：20.0.0 或更高版本。
- Claude Code：带插件支持的最新版本。
- Bun：JavaScript 运行时与进程管理器（缺失时自动安装）。
- uv：用于向量搜索的 Python 包管理器（缺失时自动安装）。
- SQLite 3：用于持久化存储（已内置）。

Windows 相关：README 的 Windows Setup Notes 提到，如果出现 `npm : The term 'npm' is not recognized as the name of a cmdlet` 这类错误，需要确认 Node.js 和 npm 已安装并加入 PATH，从 https://nodejs.org 下载最新 Node.js 安装包，安装后重启终端。

## 安装与配置

README 给出的通用安装方式（在终端中执行）：

1. 最简安装：运行 `npx claude-mem install`。README 说明安装器会先完成全部配置，然后要求你在浏览器中登录 claude-mem（邮箱 magic link，无需信用卡）。登录会为你的账号分配 memory key，并解锁带 30 天免费试用的 claude-mem observer。免费试用结束后，除非订阅，记忆会自动回退到你的 Anthropic plan。登录后需要选择记忆提供方：claude-mem observer、你自己的 OpenRouter 或 Gemini key，或你的 Anthropic plan。
2. 想跳过登录：传入显式 `--provider` 参数、设置 `CLAUDE_MEM_ONLINE_OPTIN=false`，或在 CI/非交互式 shell 中运行，安装器会在无账号交互的情况下完成。
3. 在 Claude Code 内从插件市场安装：先执行 `/plugin marketplace add thedotmack/claude-mem`，再执行 `/plugin install claude-mem`，然后重启 Claude Code。README 称上一个会话的上下文会自动出现在新会话中。
4. 其他 IDE 的安装命令（README 列出）：`npx claude-mem install --ide grok-bot`、`npx claude-mem install --ide opencode`（需 OpenCode 1.3.4 或更高，含 OpenCode 2，安装后重启 OpenCode）、`npx claude-mem install --ide t3code`、`npx claude-mem install --ide antigravity`、`npx claude-mem install --ide omp`、`npx claude-mem install --ide pi`、`npx claude-mem install --ide dsh --dsh-profile tui`。
5. OpenClaw 网关：执行 `curl -fsSL https://install.cmem.ai/openclaw.sh | bash`。

README 特别提醒：Claude-Mem 也发布在 npm 上，但 `npm install -g claude-mem` 只安装 SDK/库，不会注册插件 hook，也不会搭建 worker 服务。始终应通过 `npx claude-mem install` 或上面的 `/plugin` 命令安装。

配置方面，README 说明设置保存在 `~/.claude-mem/settings.json`（首次运行时自动创建默认值），可配置 AI 模型、worker 端口、数据目录、日志级别和上下文注入设置。若要在 Claude Code 和 Codex 的 SessionStart 上下文中包含来自所有 harness 的观察，在该文件中设置 `"CLAUDE_MEM_SESSION_START_INCLUDE_ALL_SOURCES": "true"`，或在查看器设置中开启 “Include all sources at session start”；默认是 `"false"`，即只包含当前 harness。

模式与语言：通过 `CLAUDE_MEM_MODE` 设置，同时控制工作流行为（如 code、chill、investigation）和生成观察所用语言。在 `~/.claude-mem/settings.json` 中写入 `"CLAUDE_MEM_MODE": "code--zh"` 即可使用简体中文模式。README 说明 `code--zh` 已内置，无需额外安装或更新插件；修改模式后需重启 Claude Code。可用模式可用 `ls ~/.claude/plugins/marketplaces/thedotmack/plugin/modes/` 在本地查看。

关于融入你的日常工作流：README 未提供与 Trae Work / Java 的集成方式。README 中提到的接入形态是 Claude Code 插件、各 IDE 的 `--ide` 安装参数、OpenClaw 网关脚本，以及 MCP 搜索工具（`search`、`timeline`、`get_observations`），但未说明如何在 Trae Work 中作为 MCP 服务接入、作为 Skill 放入技能目录、在 Trae Work 终端中作为 CLI 调用，或在 Java/Spring 项目中通过 SDK/HTTP 集成。这些接入路径 README 未提供，请勿自行假设配置路径或命令。

## 最小可用示例

下面这段指令可以直接整段复制给 Trae Work 等 AI 编程助手，用于在 Java 项目里试用 claude-mem 的记忆能力：

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 后端项目，日常用 Maven 构建、JUnit 5 写测试。我了解到 claude-mem 是一个为编码 Agent 提供跨会话持久记忆的工具，会自动捕获会话中的工具使用观察、生成语义摘要，并在后续会话注入相关上下文。

目标：帮我在本机把 claude-mem 跑起来，并验证它确实能在两次会话之间保留项目上下文。

要求：
1. 先检查我的环境：Node.js 是否 >= 20.0.0，npm 是否在 PATH 中（Windows 上如果报 'npm 不是可识别的命令'，先帮我确认 Node.js 安装与 PATH）。
2. 只使用 claude-mem README 中明确给出的安装方式：npx claude-mem install，或 Claude Code 内的 /plugin marketplace add thedotmack/claude-mem 与 /plugin install claude-mem。不要使用 npm install -g claude-mem，README 说明它只装 SDK/库，不会注册 hook 和 worker。
3. 安装过程中如果需要登录或选择记忆提供方，把选项和影响解释给我听，让我决定；如果我想跳过登录，告诉我可以用显式 --provider 参数或 CLAUDE_MEM_ONLINE_OPTIN=false。
4. 安装后帮我确认 settings.json 的位置（README 说是 ~/.claude-mem/settings.json），并把 CLAUDE_MEM_MODE 设为 code--zh，让生成的观察使用简体中文。
5. 告诉我如何验证：README 提到启动时会打印 worker URL，可以用 Web 查看器 UI 看实时记忆流；也提到有 mem-search skill 和 search / timeline / get_observations 三个 MCP 工具。请按 README 的说法指导我验证，不要编造 README 里没有的命令或路径。
6. 最后明确告诉我：claude-mem 与 Trae Work 的集成方式 README 未提供，所以不要假设它已经接入 Trae Work，只把它当作独立安装并验证。
```

## 验证方法

README 中可用于验证的事实点：

1. 安装完成后重启对应工具。README 在 Claude Code 插件安装路径下写明“Restart Claude Code. Context from previous sessions will automatically appear in new sessions.”；在 OpenCode 路径下写明安装后重启 OpenCode。
2. 查看 worker 的 Web 查看器 UI。README 在 Key Features 中写明 “Web Viewer UI - Real-time memory stream at the worker URL printed on startup”，即启动时会打印 worker URL，可在该地址看到实时记忆流。
3. 使用 mem-search skill 查询项目历史。README 在 Key Features 中写明 “Skill-Based Search - Query your project history with mem-search skill”。
4. 使用 MCP 搜索工具。README 说明有 `search`、`timeline`、`get_observations` 三个可用 MCP 工具，并给出示例用法：先 `search(query="authentication bug", type="bugfix", limit=10)`，再根据索引中的 ID（如 #123、#456）调用 `get_observations(ids=[123, 456])`。
5. 排查问题：README 的 Troubleshooting 说明，把问题描述给 Claude，troubleshoot skill 会自动诊断并给出修复方案。

## 风险与注意事项

- 安装方式陷阱：README 明确警告 `npm install -g claude-mem` 只安装 SDK/库，不会注册插件 hook，也不会搭建 worker 服务，必须用 `npx claude-mem install` 或 `/plugin` 命令。
- 账号与计费：README 说明安装器会引导登录 claude-mem（邮箱 magic link，无需信用卡），登录后解锁带 30 天免费试用的 claude-mem observer；试用结束后，除非订阅，记忆会自动回退到你的 Anthropic plan。
- 隐私：README 提到可用 `<private>` 标签把敏感内容排除在存储之外。
- 默认上下文范围：`CLAUDE_MEM_SESSION_START_INCLUDE_ALL_SOURCES` 默认为 `"false"`，即启动上下文只包含当前 harness；设为 `"true"` 才会包含所有 harness 的观察。
- 模式切换需重启：README 说明修改 `CLAUDE_MEM_MODE` 后需要重启 Claude Code 才能生效。
- Windows 环境：README 提示若出现 `npm` 不是可识别命令的错误，需确认 Node.js 与 npm 已安装并加入 PATH，安装后重启终端。
- 与 Trae Work / Java 的集成风险：README 未提供与 Trae Work / Java 的集成方式，因此无法基于 README 判断在 Trae Work 工作流中的兼容性与配置方式。
- 版本与更新：README 徽章显示版本 13.35.0、Node >= 20.0.0；仓库元信息显示最近更新时间为 2026-10-11。除此之外的版本细节 README 未提供。

## 替代方案

README 未提供替代方案的相关说明。

README 中与“替代”最接近的内容是：安装时可选择不同的记忆提供方——claude-mem observer、你自己的 OpenRouter 或 Gemini key，或你的 Anthropic plan；以及可通过 `--provider` 参数或 `CLAUDE_MEM_ONLINE_OPTIN=false` 跳过登录。这些是同一工具内的提供方选择，不是替代产品。

README 还提到 Claude-Mem 采用 Apache-2.0 许可，理由是“durable agentic memory should be easy to embed in developer tools, local agents, MCP servers, enterprise systems, robotics stacks, and production agent harnesses”，但未列出具体的替代项目。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
