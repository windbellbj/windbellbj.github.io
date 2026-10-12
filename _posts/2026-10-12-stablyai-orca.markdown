---
layout: post
title: "Orca 使用说明书：并行跑一队编码 Agent 的 ADE"
subtitle: "Windows 上装好 Orca，把 Claude Code、Codex 等 CLI Agent 塞进独立 worktree 并行干活，再决定要不要长期用"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - Agent Harness
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/stablyai/orca
- Stars：89782
- 语言：TypeScript
- 创建时间：2026-03-17
- 最近更新：2026-10-12
- 官方简介：Orca is the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. Available on desktop, mobile and remote runtime.

---

> Orca 是一个「Agent 开发环境」（ADE）：把 Claude Code、Codex、OpenCode、Grok 等任意终端里的编码 Agent 放进各自独立的 git worktree 并行运行，用一套桌面界面统一管理终端、diff、浏览器和任务。最适合手上已有多个 Agent 订阅、想同时推进多条改动线又不想互相踩文件的开发者。

## 它到底解决什么问题

日常用 AI 写代码，最烦的不是模型不够聪明，而是**并行不起来**：一个 Agent 在改 `OrderService.java`，另一个也在改同一个文件，冲突、覆盖、来回 rebase。Orca 的思路是把「一个任务 = 一个隔离 worktree = 一个 Agent」固定下来：

- **并行 worktree**：一条提示词可以扇出给多个 Agent，每个跑在自己的 git worktree 里，跑完对比结果，挑最好的合并。
- **自带订阅**：官方明确「Bring your own agent / subscription」，用你已有的 Claude Code、Codex 等订阅，Orca 本身不替你买模型额度。
- **终端即工作台**：官方称终端为 Ghostty 级、WebGL 渲染，支持无限分屏，滚动历史在重启后仍保留。
- **评审闭环**：可以在 AI 生成的 diff 任意行上留评论并回传给 Agent，也能在应用内浏览 PR、issue 和项目看板。
- **手机端伴随**：iOS App Store 与 Android APK 可监控、催办 Agent，Agent 跑完会通知你。
- **Orca CLI**：Agent 也能反过来驱动 Orca，官方给出的命令示例包括 `orca worktree create`、`snapshot`、`click`、`fill`。

> 一句话：它不是又一个聊天式编程助手，而是**给一堆 CLI Agent 用的调度台 + 工作区管理器**。

<!-- asset:blog-1 start -->
![Orca 并行 worktree 工作流](/img/ai-news/stablyai-orca/blog-1.png)

*图：Orca 并行 worktree 工作流*
<!-- asset:blog-1 end -->


## 支持哪些 Agent

官方口径是「任何 CLI Agent，只要能在终端里跑，就能在 Orca 里跑」，并点名了一批：

| 类别 | 官方点名的 Agent |
| --- | --- |
| 主流 | Claude Code、Codex、Grok、Cursor、GitHub Copilot |
| 开源/自托管 | OpenCode、OpenClaude、Goose、Cline、Amp、Charm |
| 其他 | Muse、DeepSeek Harness、ZCode、MiMo Code、Antigravity、Pi、oh-my-pi、Hermes Agent、Devin、Auggie、Autohand Code、CodeBuddy、Codebuff、Freebuff、Command Code 等 |

对 Java / Spring 开发者来说，这意味着你现有的 Claude Code 或 Codex 订阅可以直接复用，不需要换模型供应商。

## 环境与前置依赖

| 项目 | 说明 |
| --- | --- |
| 操作系统 | 官方标注支持 macOS、Windows、Linux |
| 运行时 | 桌面应用形态，从官网下载安装包；主语言为 TypeScript |
| 必备 | 本机需有 **git**，因为并行隔离依赖 worktree |
| 必备 | 至少一个可在终端运行的编码 Agent CLI，并已登录你的订阅账号 |
| 可选 | 手机端 iOS / Android 应用，用于远程监控 |
| 可选 | 一台可通过 SSH 访问的远程机器，用于把 Agent 跑在更强的机器上 |
| 许可证 | MIT |

> 官方未公开说明具体的 Windows 最低版本、内存或磁盘要求，安装前建议先确认下载页给出的安装包类型。

## 安装与配置（Windows + PowerShell）

### 第一步：装 Orca 桌面端

1. 打开官网下载页 `https://onorca.dev/download`，选择 Windows 版本下载。
2. 运行下载到的安装程序，按向导完成安装。
3. 启动 Orca，首次进入会有引导流程（官方仓库中存在 onboarding 相关资源）。

### 第二步：确认 git 可用

在 PowerShell 中执行 `git --version`，能打印版本号即可。若提示找不到命令，先安装 Git for Windows 并重开终端。

### 第三步：准备一个可用的 Agent CLI

Orca 不内置模型，需要你本机已有能跑的 Agent。以 Claude Code 为例，先在 PowerShell 里确认它能在普通终端中正常启动并已登录，再回到 Orca 里使用。

### 第四步：把 Java / Spring 项目接进来

1. 在 Orca 中打开你的 Spring 项目目录（例如 `C:\work\order-service`）。
2. 让 Orca 基于该仓库创建 worktree，每个 worktree 对应一条独立分支，互不干扰。
3. 在某个 worktree 对应的终端里启动你的 Agent CLI，让它在这个隔离目录里改代码。
4. 需要同时推进多条线时，重复创建 worktree，把同一条提示词分发给多个 Agent。
5. 在 Orca 内查看各 worktree 的 diff，逐条评审后合并胜出的那条。

> 关于 `orca.yaml`：官网首页出现「set up orca.yaml」的表述，但公开资料未给出该文件的字段说明与完整示例，**请以应用内引导和官方文档为准，不要照抄网上流传的配置**。

### 第五步（可选）：手机端与远程

- 手机端：iOS 从 App Store 搜索 Orca 安装；Android 使用官方发布的 APK（仓库中给出的版本为 0.0.52）。
- 远程：官方支持 SSH worktree，可在远程机器上跑 Agent，并带自动重连与端口转发。

<!-- asset:code-1 start -->
```powershell
git --version
```
<!-- asset:code-1 end -->


## 如何确认装好了

- Orca 能正常启动并进入主界面，能看到项目 / worktree 列表。
- 能成功为一个 git 仓库创建 worktree，且该 worktree 在文件系统中真实存在、分支名正确。
- 在 Orca 的终端里能正常启动你的 Agent CLI，并看到它开始输出。
- 在 Orca 内能看到该 worktree 的 diff 视图，且改动内容与 Agent 实际修改一致。

<!-- asset:blog-2 start -->
![装好后的四个确认点](/img/ai-news/stablyai-orca/blog-2.png)

*图：装好后的四个确认点*
<!-- asset:blog-2 end -->


## 融入 Trae Work 与 Java 工作流的现实情况

需要说清楚：**官方未提供与 Trae Work 的集成方式，也未提供 Java / Spring 的 SDK 或 MCP 服务接入路径**。公开资料里没有 Orca 作为 MCP Server、Skill 包或 Java 依赖的任何说明。

因此对「Windows + Trae Work + Java / Spring」的读者，现实可行的用法是**并列使用**，而不是深度集成：

1. 用 Trae Work 做日常的 Java 编码、重构、单测补全。
2. 把需要并行探索的任务（例如「同一需求给出三种实现方案」「批量补 Spring 集成测试」）交给 Orca 里的多个 Agent，各自在独立 worktree 中完成。
3. 在 Orca 里对比 diff、留评论、合并；合并后的分支再回到 Trae Work 中继续精修。
4. 若希望自动化，可用 Orca CLI 在 PowerShell 中驱动 worktree 的创建与操作，把它当作脚本化的工作区管理命令，而不是 Java 依赖。

> 如果你的诉求是「在 Trae Work 里一键调用 Orca」，目前没有官方支持的路径，不要尝试自行拼凑未公开的配置。

## 社区评价（来自 Hacker News 讨论）

在题为《Show HN: Open Source 'Conductor + Ghostty'》的讨论中（21 points，10 条评论）：

- 有用户表示「It's been working super well for me. First tool that actually works well on Linux.」——对 Linux 支持评价积极。
- 有用户拿它与 cmux 对比，作者回应了几点差异：Orca 的标签是顶层而非嵌在面板内（作者也承认这是个人偏好）、有 GitHub 原生集成（关联 PR、显示状态、关联 issue）、非聚焦终端面板也有 AI 状态指示、可手动把 worktree 标记为未读、内置文件查看器 / 搜索 / git diff 查看器，并指出 cmux 仅支持 Mac。

> 讨论热度不算高，样本有限，建议把它当作「同类工具差异点」的参考，而不是质量背书。

## 局限与风险

| 维度 | 情况 |
| --- | --- |
| 许可证 | MIT，可自由使用与修改 |
| 费用 | 应用本身免费开源；模型额度来自你自己的 Agent 订阅，成本取决于你已有的订阅 |
| 成熟度 | 仓库创建于 2026-03-17，更新至 2026-10-12，属于快速迭代期；官方自称「we ship daily」，功能列表常滞后于实际版本 |
| 平台差异 | 官方标注三平台支持，但社区反馈中「在 Linux 上表现好」被单独提及，Windows 上的实际体验公开资料较少 |
| 集成面 | 与 Trae Work、Java / Spring 无官方集成；`orca.yaml` 等配置细节未公开 |
| 安全 | 应用会驱动终端、浏览器与 SSH 远程连接，并可能使用 Computer Use 操作桌面应用；公开资料未给出权限模型与沙箱说明，建议先在非核心仓库试用 |
| 数据 | 涉及 GitHub / Linear 账号连接与代码仓库访问，公开资料未说明数据处理与存储策略 |

## 值不值得试

- **值得试**：你已经在用 Claude Code / Codex 等 CLI Agent，且经常需要同时推进多条改动线；或者你想把 Agent 跑在远程机器上、用手机盯进度。
- **可以观望**：你主要在 Trae Work 内完成全部工作，且没有并行 worktree 的痛点；或者你的项目对权限与数据流向有严格合规要求。
- **不建议**：你期待的是「在 Trae Work 里以 MCP / Skill / SDK 形式调用 Orca」——这条路径官方没有提供。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring 后端项目（Maven 或 Gradle 构建，含 Controller / Service / Repository 分层与 JUnit 测试）。我准备试用 Orca 这个 Agent 开发环境，它能把多个 CLI 编码 Agent 放进各自独立的 git worktree 并行运行。

目标：请帮我把 Orca 接入我的日常流程，并完成一次真实的并行改造试用。

具体要求：
1. 先检查我的项目是否适合用 git worktree 并行：确认当前分支、是否有未提交改动、构建命令是什么，并给出清理建议。
2. 设计一个适合并行拆分的任务：例如「为订单模块补一组 Spring 集成测试」或「把某个 Service 的异常处理重构为统一异常体系」，把它拆成 3 条互不冲突、可独立完成的子任务，每条子任务说明它主要改动哪些文件，确保不会互相覆盖。
3. 给出在 Orca 中创建 3 个 worktree 并分别启动 Agent 的操作顺序，用 Windows PowerShell 描述每一步，包括 worktree 的命名建议与分支命名建议。
4. 说明每个 Agent 的提示词应该怎么写，要求包含：改动范围、必须遵守的项目规范（包名、日志、异常、测试框架）、完成后必须运行的构建与测试命令。
5. 给出合并阶段的检查清单：如何对比 3 个 worktree 的 diff、如何判断哪一份实现最好、合并前必须跑哪些命令确认没有破坏构建。
6. 明确告诉我哪些环节 Orca 官方没有提供与 Trae Work 或 Java 的集成方式，不要编造配置路径或命令。

请按步骤输出，命令用 PowerShell 写法，不要省略参数。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
