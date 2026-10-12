---
layout: post
title: "CC Switch：一键切换 Claude Code/Codex 供应商的桌面管理器"
subtitle: "跨平台 Tauri 桌面工具，集中管理 AI 编程工具的 API 供应商、MCP、Skills 与提示词，免去手改配置文件"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - MCP服务
news_category: mcp
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/farion1231/cc-switch
- Stars：142792
- 语言：Rust
- 创建时间：2025-08-04
- 最近更新：2026-10-11
- 官方简介：A cross-platform desktop All-in-One assistant for Claude Code, Codex, OpenCode, OpenClaw, Grok Build & Hermes Agent. Only official website: ccswitch.io

---

> CC Switch 是一款基于 Tauri 2 的跨平台桌面应用，把 Claude Code、Codex、Gemini CLI、OpenCode、OpenClaw、Grok Build、Hermes Agent 等一众 AI 编程工具的 API 供应商切换、MCP 服务器、Skills 与提示词集中到一个图形界面里管理，让你不再手写 JSON / TOML / YAML 配置。最适合同时使用多个 AI 编码工具、手里握着好几家 API 中转或官方 Key、又懒得反复改配置文件的开发者。

## 它到底解决什么问题

日常用 AI 编程工具的人几乎都会遇到同一类麻烦：

- **供应商切换靠手改文件**。想从官方 API 换到中转站，得翻出 `~/.claude/settings.json`、Codex 的 TOML、Gemini CLI 的 YAML，逐个改 base URL 和 Key，改错一个字段工具就报错。
- **MCP 服务器配置分散**。每个工具各有一套 MCP 配置格式，同一个 MCP 服务要在多个工具里重复登记。
- **Skills 与提示词无处安放**。写好的提示词、技能包散落在各个目录，换工具就丢。
- **用量与花费看不清**。多个供应商轮着用，月底不知道钱花在哪。

CC Switch 把这些统一收进一个桌面窗口：**一键切换供应商**，**集中管理 MCP / Skills / Prompts**，并附带会话查看、用量看板、备份同步等能力。

<!-- asset:blog-2 start -->
![CC Switch 解决的四个痛点](/img/ai-news/farion1231-cc-switch/blog-2.png)

*图：CC Switch 解决的四个痛点*
<!-- asset:blog-2 end -->


## 核心概念与工作原理

从公开的架构信息看，CC Switch 的组成大致如下：

| 层次 | 作用 |
| --- | --- |
| 桌面界面（Tauri + React） | 供应商管理、MCP 管理、Skills 管理、提示词库、会话读取、用量看板等页面 |
| Tauri 命令层 | 前端通过 API 绑定调用原生能力，统一分发管理操作 |
| 供应商模式控制与实时配置更新 | 切换供应商时改写目标客户端的配置文件，并做增量补丁 |
| 本地代理（Local Proxy） | 请求可经本地代理转发到所选供应商，由路由上下文挑选供应商 |
| 持久化与洞察 | SQLite 存配置与会话记录，备份同步服务负责配置备份 |

一句话概括工作方式：**你在图形界面里选好供应商，CC Switch 去改写对应 AI 工具的配置文件（或经本地代理转发请求），让该工具立刻用上新的 API 端点。**

<!-- asset:blog-1 start -->
![CC Switch 工作方式示意](/img/ai-news/farion1231-cc-switch/blog-1.png)

*图：CC Switch 工作方式示意*
<!-- asset:blog-1 end -->


## 支持的工具与平台

- **平台**：Windows、macOS、Linux（官方徽章标注三平台）。
- **管理的 AI 工具**：Claude Code、Claude Desktop、Codex、Gemini CLI、Grok Build、OpenCode、OpenClaw、Hermes Agent、Pi、MiniMax Code 等（不同渠道列举略有出入，官方简介与仓库标题的清单并不完全一致）。
- **官方唯一官网**：ccswitch.io。仓库明确强调只有这一个官网，其余站点均非官方。

## 环境与前置依赖

- **操作系统**：Windows / macOS / Linux 桌面环境。
- **运行时**：作为 Tauri 2 打包的桌面应用分发，普通用户下载安装包即可，无需自行准备 Rust 或 Node 环境。
- **被管理的工具**：需要你先在本机装好对应的 AI 编程工具（例如 Claude Code、Codex CLI），CC Switch 才有配置文件可改。
- **网络**：切换到的供应商需可访问；若使用中转服务，按其要求配置。

> 官方未公开说明具体的最低系统版本、内存占用等硬性指标，安装前可先看 Releases 页面的安装包说明。

## 安装与配置（Windows）

### 第一步：下载安装包

1. 打开官方 Releases 页面：`https://github.com/farion1231/cc-switch/releases/latest`。
2. 在 Assets 中下载 Windows 安装包（通常为 `.msi` 或 `.exe`，以页面实际提供的文件名为准）。
3. 双击安装，按向导完成。若 SmartScreen 弹窗提示，选择「更多信息」→「仍要运行」。

### 第二步：确认安装成功

1. 从开始菜单启动 CC Switch，能看到主界面窗口即安装成功。
2. 在「供应商管理」页面能看到已识别的本机 AI 工具及其当前配置。
3. 若某个工具未被识别，说明该工具尚未安装或配置路径不在默认位置。

### 第三步：配置第一个供应商

1. 在供应商管理页选择目标工具（例如 Claude Code）。
2. 新增一个供应商条目，填入名称、API Base URL、API Key 等字段。
3. 保存后点击切换，CC Switch 会改写该工具的配置文件。
4. 回到终端运行该工具，确认请求走的是新供应商。

### 第四步：管理 MCP 与 Skills

1. 进入 MCP 管理页，添加 MCP 服务器（名称、命令、参数、环境变量）。
2. 进入 Skills 管理页，把技能包放入对应位置并在界面中登记。
3. 进入提示词库，沉淀常用提示词，供各工具复用。

## 如何融入 Trae Work + Java / Spring 工作流

需要先说清楚一件事：**CC Switch 管理的是 Claude Code、Codex、Gemini CLI 这类命令行/桌面 AI 工具，官方未提供与 Trae Work 的集成方式，也未提供 Java / Spring 的 SDK 或 HTTP 集成方式。** 它不是一个可以 `import` 进 Spring 项目的库，也不是一个 MCP 服务端。

因此在你的日常环境里，合理的用法是**并行使用**，而不是把 CC Switch 嵌进 Trae Work：

1. **用 CC Switch 管好终端侧的 AI 工具**。你在 Windows PowerShell 里跑 Claude Code 或 Codex 时，供应商切换、MCP 登记、提示词复用都交给 CC Switch。
2. **Trae Work 侧保持独立配置**。Trae Work 自身的模型与 MCP 设置在其 IDE 设置里维护，与 CC Switch 互不干扰。
3. **MCP 配置可手工对齐**。如果你希望 Trae Work 和终端工具用同一批 MCP 服务，可在 CC Switch 里查看到 MCP 的启动命令与参数，再手工填进 Trae Work 的 MCP 配置中。这一步是手工搬运，不是自动同步。
4. **Java / Spring 项目本身不受影响**。CC Switch 不参与构建、不注入依赖，`pom.xml` / `build.gradle` 无需任何改动。

> 若后续官方补充了与 IDE 或 MCP 客户端的对接能力，以官方文档为准；当前没有可照做的集成路径。

## 常用操作速查

| 场景 | 做法 |
| --- | --- |
| 换 API 供应商 | 供应商管理页选中条目 → 切换 |
| 新增供应商 | 供应商管理页 → 新增 → 填 Base URL 与 Key → 保存 |
| 登记 MCP 服务 | MCP 管理页 → 添加 → 填命令、参数、环境变量 |
| 管理技能包 | Skills 管理页 → 导入/登记 |
| 沉淀提示词 | 提示词库 → 新建 → 保存 |
| 查看用量 | 用量看板页 |
| 备份配置 | 备份与同步功能 |
| 查看会话 | 会话读取页 |

## 社区评价

来自 Hacker News 讨论的反馈集中在几点：

- **正面**：省去手改配置文件的痛点被反复提及，多供应商来回切换的场景下体验提升明显；Tauri 打包的桌面应用体积和启动速度获得认可。
- **质疑**：有讨论者担心把 API Key 集中交给一个第三方桌面应用保管的安全性，以及本地代理转发请求带来的额外信任面。
- **中立**：也有人认为如果只用一家供应商，这类工具的价值有限。

第三方评测站点 beamforai 给出的速度评分为 1.37/10，归类为 stable，并统计到约 134k stars、9.3k forks、239 位贡献者、最近一次提交约 19 天前。该站点的评分口径与仓库元信息中的 star 数并不一致，两处数据并列供参考。

## 局限与风险

- **许可证**：官方未公开说明具体开源许可证类型，商用前请自行到仓库确认。
- **成熟度**：项目创建于 2025-08-04，迭代活跃，但属于较新的工具；第三方评测将其归为 stable，速度评分偏低。
- **安全**：应用需要读写各 AI 工具的配置文件，并可能持有 API Key、经本地代理转发请求。请只从官方 Releases 与官网 ccswitch.io 获取安装包，警惕仿冒站点。
- **费用**：CC Switch 本身免费，但你配置的各家 API 供应商按各自计费规则收费；仓库中大量赞助商为中转服务商，选择时请自行评估其可靠性与合规性。
- **集成边界**：官方未提供与 Trae Work、Java / Spring 的集成方式，不要期待它能作为 SDK 或 MCP 服务嵌入你的工程。

## 值不值得试

如果你在 Windows 上同时用着 Claude Code、Codex 等多个 AI 编程工具，并且经常在官方 API 与中转服务之间切换，CC Switch 能实打实省下改配置文件的时间，值得装一个试试。如果你只用 Trae Work 一家、且不碰终端里的 AI 工具，它的价值有限，可以先观望。

```text
背景：我是 Java / Spring 后端工程师，在 Windows 上用 Trae Work 做日常开发，同时在 PowerShell 里使用 Claude Code 和 Codex 等命令行 AI 工具。我装了 CC Switch 这个桌面管理器，想用它统一管理这些工具的 API 供应商、MCP 服务器和提示词。

目标：帮我把 CC Switch 用起来，并和我现有的 Java / Spring 开发流程衔接好。

具体要求：
1. 先带我确认 CC Switch 已正确安装并能识别本机的 Claude Code 与 Codex，告诉我该看界面上的哪些位置。
2. 指导我新增两个供应商条目（一个官方 API、一个中转服务），字段包括名称、Base URL、API Key，并说明每个字段的作用和常见填错方式。
3. 演示一次供应商切换，并告诉我切换后如何在 PowerShell 里验证 Claude Code 实际走的是新供应商。
4. 指导我在 CC Switch 里登记一个 MCP 服务器，并说明如何把同样的启动命令与参数手工填进 Trae Work 的 MCP 配置，让两边用同一批 MCP 服务。
5. 说明 CC Switch 与 Java / Spring 项目的关系：确认它不需要改动 pom.xml 或 build.gradle，也不作为 SDK 或 MCP 服务嵌入工程。
6. 提醒我安全注意事项：只从官方 Releases 和 ccswitch.io 下载，API Key 的存放位置，以及本地代理转发带来的信任面。
7. 全程命令用 Windows PowerShell 写法，路径用 Windows 风格。

输出形式：分步骤的操作清单，每步说明做什么、在哪里做、做完如何确认成功。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
