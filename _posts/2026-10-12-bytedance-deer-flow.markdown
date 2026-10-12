---
layout: post
title: "DeerFlow 2.0 使用说明书：字节开源的 SuperAgent 运行壳"
subtitle: "一个自带沙箱、记忆、技能与子智能体的长任务智能体运行壳，Java 后端也能把它当 MCP 服务接进 Trae Work"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - Agent Harness
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/bytedance/deer-flow
- Stars：83699
- 语言：Python
- 创建时间：2025-05-07
- 最近更新：2026-10-11
- 官方简介：An open-source long-horizon SuperAgent harness that researches, codes, and creates. With the help of sandboxes, memories, tools, skill, subagents and message gateway, it handles different levels of tasks that could take minutes to hours.

---

> DeerFlow 2.0 是字节跳动开源的「SuperAgent 运行壳」（harness）：它把子智能体、长期记忆、Docker/K8s 沙箱、技能与消息网关编排在一起，用来跑几分钟到几小时的长任务（深度调研、写代码、产出报告）。最适合想在自己机器上跑一个「能动手干活」的智能体中枢、并愿意用 Docker 起服务的开发者；如果你只想在 IDE 里补全代码，它不是同类工具。

## 它到底是什么

DeerFlow 全称 **D**eep **E**xploration and **E**fficient **R**esearch **Flow**，官方定位是「开源的长时程 SuperAgent 运行壳」，借助沙箱、记忆、工具、技能、子智能体与消息网关，处理从几分钟到几小时的不同量级任务。

需要先分清两件事：

- **DeerFlow 2.0 是一次彻底重写**，与 1.x 不共享代码。1.x 是早期的 Deep Research 框架，仍在 `main-1.x` 分支维护；活跃开发已全部转到 2.0。
- 2.0 的形态更接近「运行时」而不是「框架库」。第三方评测（SOTAAZ Lab）把它和 LangGraph、CrewAI、AutoGen 对比后给出的说法是：CrewAI、AutoGen 更像组装套件，DeerFlow 更像一台配齐装备的工作站——沙箱、持久记忆、技能系统、消息网关都是内置的，而其他框架需要你自己搭。

社区热度方面，官方说明称 2026 年 2 月 28 日 DeerFlow 在 2.0 发布后登上 GitHub Trending 第一名；第三方评测称其 24 小时内登顶 Trending、不到一个月突破 4 万 star。仓库当前显示约 8.3 万 star，两个数字口径不同，以仓库页面为准即可。

## 核心概念与工作原理

### 两层架构

- **Harness（核心引擎）**：可发布的核心运行时，第三方评测提到其包名为 `deerflow-harness`。负责智能体编排（基于 LangGraph StateGraph）、工具系统、沙箱、记忆、技能、MCP 连接。
- **App（应用层）**：包住 harness 的服务层。第三方评测给出的端口分布是：LangGraph Server `2024`、Gateway API（FastAPI）`8001`、前端（Next.js）`3000`、Nginx `80`。

### 多智能体工作流

第三方评测称 2.0 基于 LangGraph StateGraph 构建了 9 个专用节点，包括 Supervisor（分析任务、生成结构化计划、派发子任务）、Researcher（带引用的深度检索）、Coder（在沙箱里执行 Python/Bash）、Reporter（汇总成交付物）、Analyst、Planner、Human Feedback（通过 `interrupt()` 暂停等待人工确认）、Background Investigation、Podcast Generator。

官方对「子智能体」的描述是：由主智能体派生、各自承担一段独立工作的执行单元；「技能」是可扩展的能力包，官方支持**导出自定义技能**，并提供 **Claude Code 集成**。

### 工具来源与沙箱

- 工具从 **5 个来源**加载（第三方评测口径），并支持 **MCP** 接入外部工具服务器。
- 沙箱支持 **Local / Docker / Kubernetes** 三种模式，官方推荐 Docker。
- 记忆为**持久化存储**，第三方评测称其基于 JSON 实现，支持跨会话学习。

### 其他能力（官方说明）

私有知识检索（RAGFlow）、聊天归档、会话目标、手动上下文压缩、智能体浏览器控制、上下文工程、长期记忆、项目与文档架、定时任务（cron）、终端工作台（TUI）、嵌入式 Python 客户端。

<!-- asset:blog-1 start -->
![两层架构与端口分布](/img/ai-news/bytedance-deer-flow/blog-1.png)

*图：两层架构与端口分布*
<!-- asset:blog-1 end -->


## 适用场景与它解决的问题

| 场景 | DeerFlow 提供什么 |
| --- | --- |
| 需要跑几十分钟以上的调研/写作任务 | 多节点编排 + 子智能体 + 人工反馈中断 |
| 需要让智能体真的执行代码 | 内置 Docker/K8s 沙箱，隔离执行 Python/Bash |
| 需要跨会话记住偏好与结论 | 内置持久记忆 |
| 需要接外部工具 | MCP 服务接入 |
| 需要从 IM 触发任务 | 消息网关（第三方评测列出 Slack / Telegram / 飞书） |
| 需要定时跑任务 | 定时任务（cron），并可通过 API 预览 cron 触发时间 |

反过来，如果你的需求只是「在 IDE 里补全 Java 代码」，DeerFlow 属于重型方案，起一套 Docker 服务的成本明显高于收益。

<!-- asset:blog-2 start -->
![DeerFlow 适用场景](/img/ai-news/bytedance-deer-flow/blog-2.png)

*图：DeerFlow 适用场景*
<!-- asset:blog-2 end -->


## 环境与前置依赖

| 项目 | 要求 | 来源 |
| --- | --- | --- |
| Python | 3.12+ | 官方徽章 |
| Node.js | 22+ | 官方徽章 |
| 内存 | 最低 4GB，推荐 8GB | 第三方评测 |
| 磁盘 | 2GB+ | 第三方评测 |
| 包管理器 | uv（Python）、pnpm（前端） | 第三方评测 |
| 容器 | Docker（官方推荐路径） | 官方说明 |
| 许可证 | MIT | 官方徽章 |

**推荐模型**：官方强烈推荐使用 Doubao-Seed-2.0-Code、DeepSeek v3.2 与 Kimi 2.5 来运行 DeerFlow，并给出了字节火山引擎 Coding Plan 的入口（中国大陆开发者有单独链接）。

## 在 Windows + Trae Work 环境下的安装与配置

> 官方未提供与 Trae Work / Java 的集成方式。以下步骤是通用安装流程在 Windows PowerShell 下的写法；与 Trae Work 的结合方式见本节最后一段。

### 第一步：准备基础环境

1. 安装 Python 3.12 或更高版本，并确认 `python --version` 输出符合要求。
2. 安装 Node.js 22 或更高版本，确认 `node --version`。
3. 安装 Docker Desktop for Windows 并启动，确认 `docker version` 能正常返回。
4. 安装 uv（Python 包管理器）。官方与第三方给出的安装脚本是 Unix 写法（`curl -LsSf https://astral.sh/uv/install.sh | sh`），在 PowerShell 中请改用官方 Windows 安装方式或 `pip install uv`，安装后确认 `uv --version`。
5. 安装 pnpm（前端依赖），确认 `pnpm --version`。

### 第二步：获取代码

在 PowerShell 中执行：

1. `git clone https://github.com/bytedance/deer-flow.git`
2. `cd deer-flow`

### 第三步：运行配置向导

在项目根目录（`deer-flow/`）执行 `make setup`。

官方说明：这会启动一个交互式向导，引导你选择 LLM 提供方、可选的网页搜索，以及执行/安全偏好（沙箱模式、bash 访问、文件写入工具等），生成一份最小化的 `config.yaml` 并把密钥写入 `.env`，大约耗时 2 分钟。向导也允许你配置可选的网页搜索提供方，或先跳过。

> Windows 上若没有 `make`，可先安装 GNU Make（例如通过 Chocolatey 或 MSYS2），或参照向导脚本手动完成同样的配置项。官方未公开说明 Windows 原生无 make 时的替代命令。

配置完成后，随时可以运行 `make doctor` 校验环境并获得可执行的修复提示。如果准备提 GitHub issue，官方建议先运行 `make support-bundle`，它会打印上报步骤，并写出一个 `*-issue-summary.md` 文件供粘贴到 issue 中。

### 第四步：启动应用

官方给出两条路径：

- **Docker（推荐）**：按官方 Quick Start 的 Docker 路径启动整套服务。
- **本地开发**：按 Local Development 路径分别起后端与前端。

启动模式（Startup Modes）与 LangGraph Studio（可选）在官方说明中单列小节；生产部署另有 Docker Production Deployment 一节。

### 第五步：可选能力配置

- **沙箱模式**：Local / Docker / Kubernetes。
- **MCP Server**：官方在 Advanced 下设有 MCP Server 小节，用于把外部工具服务器接进来。
- **IM 通道**：官方在 Advanced 下设有 IM Channels 小节。
- **链路追踪**：支持 LangSmith、Langfuse、Monocle 三种追踪，以及请求链路关联（Request Trace Correlation）。
- **多提供方**：支持同时使用多个模型提供方（Using Multiple Providers）。
- **个人访问令牌**：Personal Access Tokens。

### 关于 Trae Work 与 Java 项目

官方未提供与 Trae Work / Java 的集成方式，也没有公开的 Java SDK。可确认的接入面是：DeerFlow 自身提供 **Gateway API（FastAPI，第三方评测称端口 8001）** 与 **嵌入式 Python 客户端**，并支持作为 **MCP 服务** 对外提供能力。

因此对 Java 后端而言，现实路径只有两条：一是把 DeerFlow 当作独立服务跑起来，Java/Spring 侧通过 HTTP 调用它的 Gateway API；二是如果它暴露 MCP 端点，再考虑在支持 MCP 的客户端里挂载。**具体端点路径、鉴权方式与 MCP 挂载配置，官方未公开说明，请以启动后服务的实际暴露情况为准，不要凭猜测填写配置。**

<!-- asset:code-1 start -->
```powershell
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
make setup
make doctor
make support-bundle
```
<!-- asset:code-1 end -->


## 如何确认安装成功

1. `make doctor` 无阻断性报错，并给出可执行的修复提示（若有）。
2. Docker 路径下，`docker ps` 能看到 DeerFlow 相关容器处于运行状态。
3. 浏览器访问前端端口（第三方评测口径为 `3000`），能看到 Web UI。
4. 访问 Gateway API 端口（第三方评测口径为 `8001`），服务有响应。
5. 在 Web UI 里跑一个最小任务（例如让它做一次简单检索并输出结论），观察是否有节点流转与最终产出。

> 端口号来自第三方评测，官方说明中未逐条列出端口，实际以你本机启动日志为准。

## 快速上手：跑通第一个任务

1. 打开 Web UI。
2. 在输入框里给一个**边界清晰、可验证**的任务，例如「检索某开源项目最近的发布说明，整理成一份带来源链接的简报」。
3. 观察 Supervisor 拆解计划、Researcher/Coder 分工执行、Reporter 汇总的过程。
4. 若流程触发 Human Feedback 中断，按提示确认或修正后继续。
5. 任务结束后，检查产出物与沙箱中生成的文件。

官方官网（deerflow.tech）提供了多个真实案例回放，包括「埃菲尔铁塔与最高建筑的高度对比」（会用 Python 计算倍数）、「GitHub 上最热门的仓库」（使用 MCP 服务识别并用搜索引擎整理）、「南京传统菜肴」（图文并茂）、「小户型出租房如何装修」、「《这个杀手不太冷》介绍」、「如何看待中国的外卖大战」（中文）、「超加工食品是否与健康相关」、「你会为你的 AI 分身投保吗」。这些案例以白名单只读形式展示，无需登录即可打开，适合先看效果再决定是否安装。

## 局限与风险

### 安全

官方设有专门的 Security Notice 章节，明确几条：

- **部署不当会引入安全风险**。
- **Gateway 管理员权限等同于代码执行权限**。
- 外部聊天消息的角色需要谨慎处理。
- 部署默认值需要按官方安全建议逐条核对。

此外，官方在配置说明中要求：自托管的 Browserless、Crawl4AI、Firecrawl、fastCRW 抓取后端，必须在设置 `network_isolation_confirmed: true` 之前完成对私有、回环、链路本地与云元数据网络的出站隔离；DeerFlow 默认拒绝私有或无法验证的后端，因为这些服务自行处理重定向、DNS 解析与子资源。`allow_private_addresses` 只允许有意的内部目标 URL，不会绕过后端检查。`make doctor` 会报告会被拒绝的后端配置。

### 成熟度与版本

- 2.0 是彻底重写，与 1.x 无代码共享，生态与文档仍在快速演进。
- 仓库创建于 2025-05-07，最近更新 2026-10-11，迭代节奏很快，升级前建议先看官方 Upgrade Notes。

### 费用

- 软件本身为 MIT 许可，可商用。
- 但运行成本取决于你选的模型提供方与用量；官方推荐 Doubao-Seed-2.0-Code、DeepSeek v3.2、Kimi 2.5，并链接到火山引擎 Coding Plan。
- 官方提到可选的 `request_admission` 用于按模型对请求限速，以控制在提供方的每分钟请求上限内；默认关闭。启用后会关闭已暴露的 SDK 重试以及 Claude、Codex 适配器的内部重试循环。
- 官方还提到 Jina 抓取支持可选的 `max_retries`（默认 `0`）与 `retry_budget_seconds`（默认 `30`），并明确提示**重试可能增加上游请求与成本**。

### 其他已知约束

- InfoQuest 的 reader、web search、image search 使用 **30 秒**的 HTTP 连接/读取空闲超时；抓取的 `timeout` 与 `navigation_timeout` 是独立的服务端选项，不控制本地 HTTP 超时。
- Jina 抓取可选的 `max_response_bytes` 会在抽取前拦截超大解码响应，不产生部分成功也不重试；4096 字符的输出上限不变，且不限制 HTTPX 解压分配或线路带宽。

## 社区评价（来自 Hacker News 讨论）

本次可用的公开资料中，未包含 Hacker News 讨论的具体内容，因此暂无来自该渠道的社区评价可引用。

## 一句话结论

如果你想要一个**能自己动手、能记住事、能跑长任务**的智能体中枢，并且不介意在 Windows 上多装一套 Docker + Python + Node 环境，DeerFlow 2.0 值得花半小时试一次；如果你只想在 Trae Work 里补全 Java 代码，先别装它。

```text
背景：我在 Windows 上用 Trae Work 开发 Java / Spring 后端项目，想试用字节开源的 DeerFlow 2.0（一个 SuperAgent 运行壳，自带沙箱、记忆、技能与子智能体）。

目标：在不破坏我现有 Java 项目的前提下，把 DeerFlow 在本机跑起来，并让我能用 Java 侧调用它。

具体要求：
1. 先检查我的环境：Python 是否 3.12+、Node.js 是否 22+、Docker Desktop 是否可用、uv 与 pnpm 是否已安装。缺什么就告诉我 Windows PowerShell 下的安装命令。
2. 用 PowerShell 命令帮我完成：git clone https://github.com/bytedance/deer-flow.git，进入目录，运行 make setup 配置向导。如果 Windows 上没有 make，请给出可行的替代做法，不要编造不存在的命令。
3. 配置向导里我需要选择 LLM 提供方、是否启用网页搜索、沙箱模式与文件写入权限。请用表格列出每个选项的含义与推荐值，并说明安全影响。
4. 启动后，告诉我如何验证安装成功：包括 make doctor 的输出该怎么看、docker ps 该看到什么、Web UI 与 Gateway API 分别在哪个端口。端口号如果不确定，请说明以启动日志为准，不要猜。
5. 给我一个最小可验证任务，让我在 Web UI 里跑通一次，并说明怎么判断它是真的执行了而不是只输出了一段文字。
6. 最后回答：DeerFlow 官方是否提供 Java SDK 或与 Trae Work 的集成方式？如果没有，请明确说没有，并给出通过 HTTP 调用其 Gateway API 的可行思路（只写思路，不要编造端点路径和鉴权方式）。
7. 全程不要修改我现有 Java 项目的任何文件。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
