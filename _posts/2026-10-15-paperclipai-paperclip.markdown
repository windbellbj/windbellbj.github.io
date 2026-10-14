---
layout: post
title: "Paperclip 使用说明书：把一群 AI Agent 当公司来管"
subtitle: "开源 Agent 编排控制台，自带组织架构、预算与心跳调度，Windows + Trae Work 用户可先跑本地版试试"
date: 2026-10-15 04:23:58 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - Agent Harness
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/paperclipai/paperclip
- Stars：102084
- 语言：TypeScript
- 创建时间：2026-03-02
- 最近更新：2026-10-14
- 官方简介：The open-source app everyone uses to manage agents at work

---

> Paperclip 是一个开源的多 Agent 编排控制台：把 OpenClaw、Claude Code、Codex、Cursor 等不同 Agent 编进一张组织架构图，分配目标、任务与预算，再从一块看板统一盯进度和花费。它最适合已经在同时开好几个编码 Agent、开始管不过来的人和团队。

## 它到底解决什么问题

如果你现在的状态是「开了 20 个 Claude Code 终端，重启后全丢，不知道谁在干什么」，Paperclip 想替代的就是这种散装自动化。官方把它类比成一家公司：**如果 OpenClaw 是员工，Paperclip 就是公司**。

它对外看起来像任务管理器，底层是组织架构、预算、治理、目标对齐和 Agent 协调。官方给出的典型使用路径只有三步：

1. **定义目标**：例如「把 AI 笔记应用做到 100 万美元 MRR」。
2. **招人组队**：CEO、CTO、工程师、设计师、市场，任意 bot、任意供应商。
3. **审批并开跑**：审阅策略、设定预算、点开始，然后在看板上监控。

官方列出的「适合你」清单里，和程序员直接相关的几条是：协调多种 Agent 朝同一目标工作、想让 Agent 7×24 自主运行但仍要能审计和插手、想监控成本并强制预算、想用「像用任务管理器一样」的流程来管 Agent。

<!-- asset:blog-1 start -->
![Paperclip 三步使用路径](/img/ai-news/paperclipai-paperclip/blog-1.png)

*图：Paperclip 三步使用路径*
<!-- asset:blog-1 end -->


## 核心概念：四根支柱

官方把「一支 AI Agent 组织能真正产出」拆成四件事，Paperclip 就围绕这四根支柱构建：

| 支柱 | 面向谁 | 覆盖内容 |
| --- | --- | --- |
| **Agentic Task Manager**（Agent 任务管理器） | 所有人，日常 | 任务、审批与评审关卡；主动型 Agent 同事；可审计的例行流程与工作流；用 diff、截图、测试来验收 |
| **Org Chart for Agents**（Agent 组织架构） | 管理者 | 人类 + Agent 混合组织图；职责、委派、专业化；治理：谁能做什么；限定范围的密钥与公司边界；连接权限与责任人身份 |
| **Agent Employee Training**（Agent 员工培训） | 赋能者 | Skill Studio 与组织级共享技能；评测与保存的测试运行；主动学习循环与质量指标；Agent 绩效评估；保存的测试输入；技能版本历史与回滚；可复用团队模板 |
| **Agentic OS**（Agent 操作系统） | IT 与平台 | 跨供应商运行时：任意模型、任意 Agent；沙箱、集成与 MCP 服务器；SSO、GRC、RBAC 与成本控制；数据隐私、内部追踪采集；个人与共享应用连接；运行历史与可选追踪 |

几个需要先建立直觉的机制：

- **Heartbeats（心跳）**：Agent 按分配的工作、跟进消息或配置的日程被唤醒，委派沿组织架构上下流动。官方原话是「只要能收到心跳，就能被雇佣」。
- **Goal Alignment（目标对齐）**：任务和项目挂到组织目标上，Agent 拿到工作背后的目标上下文。
- **Cost Control（成本控制）**：公司、Agent、项目三级预算，跟踪上报的花费，到阈值告警，到限额暂停工作。
- **Skills & Skill Studio**：安装或编写共享技能，用保存的输入测试、检查结果、恢复早期版本。
- **Apps & Connections**：连接 GitHub、Notion、Railway 等服务，或你自己的 MCP 服务器；网关动作可设为 Allowed、Ask first 或 Off。

<!-- asset:blog-2 start -->
![四根支柱](/img/ai-news/paperclipai-paperclip/blog-2.png)

*图：四根支柱*
<!-- asset:blog-2 end -->


## 支持哪些 Agent

官方明确列出可接入的运行时包括：OpenClaw、Claude Code、Codex、Cursor 与 Cursor Cloud、Gemini CLI、OpenCode、Pi、Hermes 与 Hermes Gateway、Grok Build、Kimi Code。第三方介绍页还提到 Bash 与 HTTP。

自定义流程、HTTP 端点和外部适配器包可以继续扩充名单，官方文档有专门的适配器总览页说明配置与能力。

## 环境与前置依赖

Paperclip 本体是一个 **Node.js 服务 + React UI**，主语言 TypeScript，采用 MIT 许可证。

官方与第三方资料给出的安装形态有两种：

- **本地版 / 自托管**：官网在「加入等待名单」之外，同时提供「install the local version」入口。第三方介绍页描述为「开源、自托管，交互式安装会带你走完数据库、认证和第一家公司，无需 Paperclip 账号」。
- **Paperclip Cloud**：官网提供等待名单注册入口，属于云端形态。

关于具体 Node.js 版本要求、数据库类型与最低硬件配置，**官方未公开说明**，建议以交互式安装过程中的提示为准。

> 注意：官方文档的安装章节标题为「Install Paperclip: Local or Self-Hosted」，说明自托管是官方支持的一等路径，但本文所见的公开资料没有给出完整的依赖清单。

## 安装与配置（Windows PowerShell）

### 第一步：跑交互式安装

第三方介绍页给出的启动命令是：

```powershell
npx paperclipai onboard --yes
```

`npx` 会拉取并执行 `paperclipai` 包，`onboard` 是引导子命令，`--yes` 表示跳过交互确认。官方描述这个流程会带你完成数据库、认证和第一家公司（Company）的创建，不需要 Paperclip 账号。

### 第二步：按引导完成初始化

安装器会依次询问数据库、认证方式，然后引导你创建第一家公司。官方文档的 Quickstart 路径是：

1. Quickstart Path
2. What is Paperclip?
3. Key Concepts
4. Installation
5. Create Your First Company
6. Hire Your First Agent
7. Watching Agents Work
8. Glossary

也就是说，装完之后你的下一步是**创建第一家公司**，再**雇佣第一个 Agent**，然后才是观察 Agent 干活。

### 第三步：接入你已有的 Agent

Paperclip 不自己造 Agent，它编排你已有的 Agent。官方文档在「Agents & Skills」分类下有三篇直接相关的操作指南：

- Bring Your Own Agent
- Connect an Agent to GitHub
- Add an MCP Server to an Agent

对 Java 程序员来说，最值得先做的是把日常在用的编码 Agent 接进来，再给它挂上 GitHub 连接，让它在任务线程里直接产出可评审的 diff。

### 关于 Trae Work 与 Java/Spring 的集成

**官方未提供与 Trae Work / Java 的集成方式。** 公开资料中没有出现 Trae Work 的适配器、插件或配置路径，也没有 Java SDK 或 Spring 集成说明。

Paperclip 与你的 Java 项目发生关系的方式，是通过它支持的连接器与 MCP 能力间接完成的：官方连接器目录里包含 **GitHub**（含连接器设置、评审机器人配置）、**Jira**、**Linear**、**Sentry**、**Postman**、**Railway**、**Supabase**、**Neon**、**ClickHouse** 等，并且支持**自定义 MCP 服务器**与 **MCP 聚合器**。

> 因此，如果你的 Spring 项目托管在 GitHub、缺陷在 Jira、监控在 Sentry，Paperclip 可以通过这些连接器参与进来；但「在 Trae Work 里直接调用 Paperclip」这条路径，公开资料中没有。

<!-- asset:code-1 start -->
```powershell
npx paperclipai onboard --yes
```
<!-- asset:code-1 end -->


## 快速上手：从零到看见 Agent 干活

1. 在 PowerShell 中执行 `npx paperclipai onboard --yes`，按提示完成数据库与认证配置。
2. 创建你的第一家公司（Company），填入一个具体目标，例如「把某服务重构到 Spring Boot 3 并降低 P99 延迟」。
3. 雇佣第一个 Agent，选择它的运行时（Claude Code、Codex、Cursor 等）和模型。
4. 给这个 Agent 设定月度预算，避免无人值守时成本失控。
5. 创建一个任务，把它挂到项目目标上，指派给该 Agent。
6. 打开 Dashboard，观察心跳触发、任务推进和花费累计。

官方文档在「Working Day-to-day」分类下提供了 Dashboard、Command Palette、Issues、Work Modes、Artifacts、Blocked Inbox、Decisions、Approvals、Costs & Budgets、Activity Log、Work Timeline、Feedback & Voting 等日常操作说明，装完之后按这个顺序翻一遍基本就够用了。

## 如何确认安装成功

公开资料没有给出一个明确的「安装成功」判定命令。可依据的间接信号是：

- 交互式安装流程走完，没有报错退出；
- 能进入 Dashboard 并看到你创建的公司；
- 能成功雇佣一个 Agent 并看到它的心跳记录；
- 在 Costs & Budgets 页面能看到该 Agent 的预算条目。

官方文档另有「Verify and Troubleshoot」与「Debug a Stuck Heartbeat」两篇排障文档，遇到心跳不动的情况可以按这两篇排查。

## 命令行与 API

Paperclip 提供 CLI 与 HTTP API 两套接口。官方文档的 CLI 分类下列出的命令组包括：Setup Commands、Test Drive、Service、Dev Environments、Authentication & Tokens、Connect、MCP、Token、Company、Project、Goal、Issue、Agent、Managed Agent、Prompt、Run (Heartbeat)、Routine、Adapter、Connections、Approval、Activity、Dashboard、Cost & Budget、Workspace、Access & Admin、Skills、Teams、Secrets、Cloud、Plugin、Asset、Feedback。

API 分类下则包括 Companies、Agents、Issues、Cases、Attention、Decisions、Approvals、Goals & Projects、Costs、Secrets、Activity、Routines、Adapters、Teams Catalog、Plugins、Tool Gateway、Connection Intents API 等端点。

> 具体命令参数与请求体格式，公开资料中未逐条列出，需查阅官方文档对应页面。

## 局限与风险

| 维度 | 情况 |
| --- | --- |
| **许可证** | MIT，可自由使用与修改 |
| **成熟度** | 仓库创建于 2026-03-02，最近更新 2026-10-14，官网标注最新版本 v2026.1012.0（2026 年 10 月 12 日）。属于快速迭代期项目 |
| **费用** | 软件本身开源免费，但 Agent 运行会消耗各模型供应商的额度；Paperclip 提供预算与限额机制来控制这部分支出 |
| **安全** | 官方提供 Secret Scopes、Secret Folders、Trust & Low-Trust Review、RBAC、SSO 等机制；第三方介绍页提到安全态势由 Superagent 扫描验证。但把 Agent 接入 GitHub 等真实系统意味着需要认真配置连接权限 |
| **实验性功能** | Agent Chat 与 chat/email 连接器（Slack、Discord、Telegram、AgentMail）被官方标注为实验性，需在实例设置中手动开启 |
| **集成缺口** | 官方未提供与 Trae Work / Java 的直接集成方式 |

## 社区评价

以下评价来自官网收录的用户反馈：

- **Numman Ali**：从没见过一个跨所有业务职能运作的 Agent 编排系统，也没见过设计品味和 UX 质量做到 Linear 那种水准的，而且不绑定任何 Agent。
- **John Holloway**：很适合编排一堆 Agent 去做开发、内容、社交、市场、QA、研究、外联，以及自主业务的其他一切。
- **Logan**：刚开始玩 OpenClaw 时，这就是我心目中 Agent 能走到的地方。自己动手做过，但远没有这个精致。
- **Resolver Vicky**：OpenClaw 是员工，Paperclip 是公司。
- **Wi_F_I**：用起来挺简单，它是一个用 AI Agent 组织和运行工作的工具，而不是一堆分散的自动化。组织架构、目标、任务、预算和 Agent 模板都在一个地方，不用从零接线。
- **yash**：有意思的是它的框架。不是「这是一个 AI 工具」，而是 CEO 雇一个 Coder，你来批准。心智模型是你在经营一家公司，而不是在使用一个工具。

> 以上均为产品官网展示的正面反馈，未包含负面评价。Hacker News 上的相关讨论，公开资料中未提供。

## 一句话建议

如果你已经在同时跑多个编码 Agent、开始为「谁在干什么、花了多少钱」头疼，Paperclip 值得花半小时跑一遍本地版；如果你只是偶尔用单个 AI 助手写代码，它现在的复杂度大概率超过你的需求。

```text
背景：我是 Java 后端程序员，日常在 Windows 上用 Trae Work 开发，技术栈是 Java / Spring，项目托管在 GitHub。我想试用 Paperclip 来统一管理我同时运行的多个编码 Agent。

目标：在不影响现有开发流程的前提下，把 Paperclip 跑起来，并接入一个我常用的编码 Agent，让它能围绕我的 Spring 项目目标工作。

具体要求：
1. 先帮我确认本机是否具备运行 Paperclip 的条件（Node.js 环境等），如果缺少依赖，告诉我需要装什么。
2. 给出在 Windows PowerShell 中执行 npx paperclipai onboard --yes 的完整步骤，并解释每一步在做什么。
3. 引导我完成「创建第一家公司」和「雇佣第一个 Agent」，公司目标请围绕一个真实的 Spring Boot 服务重构任务来写。
4. 帮我给这个 Agent 设置一个月度预算，并说明预算触发后会发生什么。
5. 指导我把这个 Agent 连接到我的 GitHub 仓库，说明需要哪些权限、有哪些风险。
6. 告诉我怎么确认 Agent 的心跳正常、任务在推进，以及心跳卡住时该怎么排查。
7. 全程不要编造 Paperclip 的命令、参数或配置路径；如果某个步骤官方没有公开说明，直接告诉我「官方未公开说明」，并建议我去官方文档的哪个章节找。
8. 最后给我一份「哪些工作适合交给 Paperclip 里的 Agent、哪些不适合」的判断清单，结合 Java 后端开发的实际情况。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
