---
layout: post
title: "DeerFlow 2.0 上手：字节开源的超级智能体运行壳"
subtitle: "用沙箱、记忆、子智能体和技能，把分钟级到小时级任务交给它跑"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/bytedance/deer-flow
- Stars：83693
- 语言：Python
- 创建时间：2025-05-07
- 最近更新：2026-10-11
- 官方简介：An open-source long-horizon SuperAgent harness that researches, codes, and creates. With the help of sandboxes, memories, tools, skill, subagents and message gateway, it handles different levels of tasks that could take minutes to hours.

---

## 解决什么问题

DeerFlow（**D**eep **E**xploration and **E**fficient **R**esearch **Flow**）是一个开源的 **super agent harness**（超级智能体运行壳），它编排 **sub-agents（子智能体）**、**memory（记忆）** 和 **sandboxes（沙箱）**，并依靠**可扩展的技能（extensible skills）**来完成几乎任何任务。

README 明确说明它处理的是「不同层级的任务，耗时可能从几分钟到几小时」（handles different levels of tasks that could take minutes to hours）。也就是说，它面向的不是单轮问答，而是长周期（long-horizon）的调研、编码与创作类任务。

需要特别注意：**DeerFlow 2.0 是一次彻底重写（ground-up rewrite），与 v1 不共享任何代码**。如果你要找最初的 Deep Research 框架，它在 `1.x` 分支上维护，但活跃开发已经转移到 2.0。

## 核心概念

README 中反复出现、构成这套 harness 的关键概念包括：

- **Super Agent Harness**：整个项目的自我定位，负责编排各类能力去完成长周期任务。
- **Sub-Agents（子智能体）**：README 目录中单列了 Sub-Agents 章节，说明它是任务分解与并行执行的核心机制。
- **Sandbox & File System（沙箱与文件系统）**：提供隔离的执行环境与文件操作能力。
- **Skills & Tools（技能与工具）**：可扩展的技能体系，README 还提到「Exporting Custom Skills」（导出自定义技能）与「Claude Code Integration」（Claude Code 集成）。
- **Long-Term Memory（长期记忆）** 与 **DeerMem extraction prompts**：记忆与上下文工程的一部分。
- **Context Engineering（上下文工程）**、**Manual Context Compaction（手动上下文压缩）**、**Current Task Notes（当前任务笔记）**：用于管理长任务的上下文窗口。
- **Agentic Browser Control（智能体浏览器控制）**：让智能体操作浏览器。
- **MCP Server**：README 的 Advanced 章节列出了 MCP Server。
- **IM Channels（IM 渠道）** 与 **message gateway**：官方简介提到 message gateway，README 中有 IM Channels 章节。
- **Scheduled Tasks（定时任务）**：支持 cron 形式的计划任务。
- **Terminal Workbench (TUI)**：终端工作台。
- **Projects（项目）**：包含 Project instructions、Document shelf、Archive read semantics、Trash 等子概念。
- **Private Knowledge Retrieval (RAGFlow)**：私有知识检索。
- **Embedded Python Client**：嵌入式 Python 客户端。

## 前置依赖

根据 README 顶部的徽章与说明，可以确认的依赖要求是：

- **Python 3.12+**（徽章链接指向 `./backend/pyproject.toml`）
- **Node.js 22+**（徽章链接指向 `./Makefile`）
- **License: MIT**

README 中提到的运行方式包括 Docker（推荐）与本地开发（Local Development），因此 Docker 是可选但被推荐的环境。

README 未提供关于操作系统支持范围的完整说明，也未提供针对 Windows 的专门依赖清单。

## 安装与配置

README 提供了「One-Line Agent Setup」和「Quick Start」两条路径。

**路径一：把安装交给编码智能体（README 原文方式）**

README 说明，如果你使用 Claude Code、Codex、Cursor、Windsurf 或其他编码智能体，可以用一句话把安装说明交给它。README 给出的原句是让智能体在需要时克隆 DeerFlow，然后按照 `https://raw.githubusercontent.com/bytedance/deer-flow/main/Install.md` 引导本地开发环境；该提示词面向编码智能体，会告诉智能体在需要时克隆仓库、在可用时选择 Docker，并在最后停下来给出确切的下一步命令以及用户仍需提供的缺失配置。

**路径二：手动 Quick Start**

1. 克隆 DeerFlow 仓库：`git clone https://github.com/bytedance/deer-flow.git`，然后 `cd deer-flow`。
2. 在项目根目录（`deer-flow/`）运行 `make setup`。README 说明这会启动一个交互式向导，引导你选择 LLM provider、可选的 web search，以及执行/安全偏好（例如 sandbox mode、bash access、file-write tools）。它会生成一个最小的 `config.yaml` 并把你的密钥写入 `.env`，大约耗时 2 分钟。向导也允许你配置可选的 web search provider，或者暂时跳过。
3. 随时运行 `make doctor` 来验证配置并获得可操作的修复提示。
4. 如果你更愿意直接编辑 `config.yaml`，README 建议改为运行 `make config` 来复制完整模板；完整参考见 `config.example.yaml`。

**运行应用**

README 的 Running the Application 章节给出两种方式：

- **Option 1: Docker（推荐）**
- **Option 2: Local Development（本地开发）**

此外还有 Startup Modes、LangGraph Studio（可选）、Docker Production Deployment 等小节。README 还提到 `make dev` 这一命令（在讨论相对路径解析时提及「as in `make dev`」）。

**关于 Trae Work 与 Java 的集成**

README 未提供与 Trae Work / Java 的集成方式。README 中提到的集成相关内容仅有：Claude Code Integration、MCP Server、IM Channels、Embedded Python Client，以及可配置的 CLI-backed providers（Codex CLI、Claude Code OAuth）与 ACP agents（例如 MiniMax Code 的 `mcode`）。README 未提供任何 Trae Work 技能目录、Trae Work MCP 配置路径或 Java/Spring SDK 的说明。

**Windows 相关提示（README 中确有提及的部分）**

README 在 ACP agent 部分提到，裸命令或绝对路径的 ACP agent `command` 会在 agent 启动前解析，因此 npm 安装的启动器在 Windows 上也能工作：`npx` 或 `mcode` 会被作为 `npx.cmd`/`mcode.cmd` shim 启动，而不是报 command-not-found；像 `C:\Users\me\AppData\Roaming\npm\mcode` 这样的绝对路径会解析到 npm 无扩展名 shell 脚本旁边的 `mcode.cmd` shim，而不是报 `WinError 193`。这是 README 中唯一明确涉及 Windows 的说明。

**模型配置要点**

- README 强烈推荐使用 Doubao-Seed-2.0-Code、DeepSeek v3.2 和 Kimi 2.5 来运行 DeerFlow。
- 管理员可以打开 **Settings → Models**，在不编辑 `config.yaml` 的情况下添加、编辑、测试和启用/禁用共享的 OpenAI-compatible Chat Completions 模型。需要填写唯一名称、base URL、model ID 和可选 API key；保存后会刷新 chat model 列表。连接测试会发送一个短的流式 tool-call 请求，可能产生 provider 费用。
- 官方 DeepSeek 模型（`https://api.deepseek.com` 或 `https://api.deepseek.com/v1`）会自动使用 DeerFlow 的 DeepSeek adapter。
- 加密的 catalog 和生成的本地加密密钥存放在 `$DEER_FLOW_HOME/managed-models/`（默认 `.deer-flow/managed-models/`）。

## 最小可用示例

下面这段指令可以直接整段复制给 Trae Work 等 AI 编程助手，用于在你的 Windows + Java/Spring 环境里试用 DeerFlow。

```text
背景：我是 Java 后端程序员，日常在 Windows 上用 Trae Work 开发，技术栈以 Java / Spring 为主。我想试用字节开源的 DeerFlow 2.0（https://github.com/bytedance/deer-flow），它是一个 super agent harness，用子智能体、记忆和沙箱处理从几分钟到几小时的长周期任务。

目标：在我的 Windows 机器上把 DeerFlow 2.0 跑起来，并完成一次最小验证。

要求：
1. 先阅读仓库 README 和 Install.md，确认前置依赖（README 标注 Python 3.12+、Node.js 22+），并检查我本机是否满足；不满足的地方逐条告诉我怎么装。
2. 按 README 的 Quick Start 走：克隆仓库后运行 make setup，向导里帮我选择 LLM provider、可选的 web search，以及 sandbox mode、bash access、file-write tools 这些执行/安全偏好。
3. 运行 make doctor 验证配置，把它的输出和修复建议解释给我听。
4. 运行应用时优先用 README 推荐的 Docker 方式；如果 Docker 不可用，再走本地开发方式，并说明两者的差别。
5. 全程用中文解释每一步在做什么，遇到 Windows 特有的问题（例如命令解析、路径问题）要指出原因。
6. 如果 README 没有提供某个信息（例如与 Trae Work 或 Java/Spring 的集成方式），直接告诉我 README 未提供，不要自行编造配置路径或命令。
```

## 验证方法

README 中给出的可执行验证手段：

1. **运行 `make doctor`**：README 明确说明「Run `make doctor` at any time to verify your setup and get actionable fix hints」，即随时运行它来验证配置并获得可操作的修复提示。
2. **运行 `make support-bundle`**：如果你要开 GitHub issue 反馈本地配置或运行时问题，README 说明该命令会打印 reporter 的后续步骤，写出一个 `*-issue-summary.md` 文件用于粘贴到 issue，一个 `*-issue-draft.md` 文件用于 AI 辅助提 issue，以及在 `.deer-flow/support-bundles/` 下可选的证据 zip。README 强调如果由 AI 助手提 issue，要从 draft 出发并替换每一个 REQUIRED 占位符，而不是编造缺失的事实；只有在维护者要求、或 summary 本身不够时才附上 zip。
3. **模型连接测试**：在 **Settings → Models** 中保存模型时会做连接测试，发送一个短的流式 tool-call 请求。README 提醒这可能产生 provider 费用，并且它不保存草稿、也不验证图片支持。
4. **DeepSeek 真实 provider 回归测试**：在环境中设置 `DEEPSEEK_TEST_API_KEY`，然后在 `backend/` 下运行 `DEER_FLOW_RUN_LIVE_TESTS=1 uv run --no-sync pytest tests/test_managed_deepseek_live.py -q`。README 说明这些测试会向 DeepSeek 发送短请求并可能产生费用，使用临时状态、绝不把凭据保存到部署 catalog，且在 CI 中会被跳过。可选地用 `DEEPSEEK_TEST_MODEL` 选择不同的 DeepSeek 模型 ID（默认 `deepseek-flash`）。
5. **官方 Demo**：README 提到可以在官网 deerflow.tech 查看 real demos，落地页的案例研究以 allowlisted、只读的 showcase 形式打开，无需登录。

## 风险与注意事项

README 专门设有 **⚠️ Security Notice** 章节，其中列出的要点包括：

- **不当部署可能引入安全风险（Improper Deployment May Introduce Security Risks）**。
- **Gateway Admin 等价于代码执行（Gateway Admin Is Equivalent to Code Execution）**。
- **外部聊天消息角色（External Chat Message Roles）**。
- **部署默认值（Deployment Defaults）**。
- **安全建议（Security Recommendations）**。

其他 README 中明确提到的风险与限制：

- **自托管 fetch 后端需要出站隔离**：自托管的 Browserless、Crawl4AI、Firecrawl 和 fastCRW fetch 后端，在给每个工具设置 `network_isolation_confirmed: true` 之前，需要与私有、loopback、link-local 和云元数据网络做出站隔离。DeerFlow 默认拒绝私有或无法验证的后端，因为这些服务自己处理重定向、DNS 解析和子资源。`allow_private_addresses` 允许有意的内部目标 URL，但不会绕过后端检查。
- **重试可能增加成本**：Jina fetch 支持通过 `max_retries`（默认 `0`）和 `retry_budget_seconds`（默认 `30`）选择性开启有界重试。README 明确提醒「Retries may increase upstream requests and cost」。
- **模型连接测试可能产生费用**，且不验证图片支持。
- **DeepSeek 实时测试可能产生费用**。
- **托管模型的加密密钥风险**：本地密钥由文件系统权限保护；加密并不能防止能同时读取两个文件的人。丢失密钥需要从备份恢复。catalog 无法解密时读写会失败，而不是替换它。
- **禁用模型的影响**：禁用一个模型会把它从未来的选择/解析中移除，因此在禁用前要更新任何显式引用它的自定义 agent 或定时任务定义。
- **定价货币必须统一**：可选的按模型定价必须在所有已定价模型中使用同一种货币。当货币混用时，DeerFlow 会禁用 Console 成本估算，而不是给出无效的聚合值。
- **ACP agent 超时**：每个 ACP agent 的 `timeout_seconds`（默认 1800）是初始化、会话创建和 prompt 共享的一个预算，从子进程启动后开始计算。超时后 DeerFlow 会中止调用并在返回错误前关闭子进程。
- **`auto_approve_permissions`**：对不可信任务应保持 `false`；只有当 mcode 必须编辑文件或运行命令且你信任该任务时才启用。

README 未提供关于数据合规、许可证之外的商业使用限制等方面的额外说明。

## 替代方案

README 中提到的相关或可替代项目与路径：

- **DeerFlow 1.x**：README 说明 2.0 是彻底重写，与 v1 不共享代码；如果你要找最初的 Deep Research 框架，它在 `1.x` 分支（`main-1.x`）上维护，仍然欢迎贡献，但活跃开发已转移到 2.0。
- **LLM Space**：README 的 Sister Projects 中列出，描述为 DeerFlow 背后的秘密武器——一个桌面工具，用于原型化 agent 想法、检查每个 harness 步骤、重放失败并做性能基准测试。
- **InfoQuest**：README 说明 DeerFlow 新集成了 BytePlus 独立开发的智能搜索与爬取工具集 InfoQuest，支持免费在线体验。
- **RAGFlow**：README 的 Core Features 中列出 Private Knowledge Retrieval (RAGFlow)，作为私有知识检索方案。
- **CLI-backed providers**：README 提到 Codex CLI、Claude Code OAuth 等 CLI 支持的 provider，以及 MiniMax Code（`mcode`）这类直接讲 ACP 的 agent。

README 未提供与其他 agent harness 或编码智能体的横向对比说明。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
