---
layout: post
title: "Hermes Agent 使用说明书：会自己长技能的 AI 智能体"
subtitle: "Nous Research 出品的自改进 Agent，支持 Windows 原生安装、多平台消息接入与技能自进化，Java 后端也能用"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - Agent Harness
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/NousResearch/hermes-agent
- Stars：252799
- 语言：Python
- 创建时间：2025-07-22
- 最近更新：2026-10-11
- 官方简介：The agent that grows with you

---

> Hermes Agent 是 Nous Research 打造的开源自主 AI 智能体，核心卖点是「内置学习闭环」——它会从对话经验里自动生成技能、在使用中持续改进技能、跨会话记住你的项目与偏好。最适合想把 AI 从「IDE 里的补全工具」升级成「常驻云端、随时可召唤的私人助理」的开发者，尤其是愿意折腾终端、想让 Agent 跑在 VPS 或服务器上而不是绑死在本机的人。

## 它到底解决什么问题

大多数 AI 编程助手是「会话制」的：关掉窗口，上下文清零，下次还得重新交代项目背景。Hermes Agent 试图解决的是**长期记忆与能力沉淀**：

- **技能自生成**：完成复杂任务后，Agent 会自主把过程固化成技能，下次遇到同类问题直接复用。
- **技能自改进**：技能在使用过程中会被持续优化，而不是写死不变。
- **跨会话记忆**：用 FTS5 做会话检索，配合 LLM 摘要实现跨会话回忆；并通过 Honcho 做辩证式用户建模，逐步建立「你是谁」的画像。
- **不绑本机**：可以跑在 5 美元的 VPS、GPU 集群，或 Daytona / Modal 这类空闲时几乎不花钱的 serverless 环境上，你从 Telegram 就能指挥它干活。

一句话概括：它不是 IDE 里的补全插件，而是一个**能长期在线、越用越懂你的自主智能体**。

<!-- asset:blog-1 start -->
![Hermes Agent 的四个核心卖点](/img/ai-news/nousresearch-hermes-agent/blog-1.png)

*图：Hermes Agent 的四个核心卖点*
<!-- asset:blog-1 end -->


## 核心概念与工作原理

| 概念 | 说明 |
| --- | --- |
| 学习闭环 | Agent 自主整理记忆并周期性自我提醒；复杂任务后自动创建技能；技能在使用中自我改进 |
| 技能系统 | 兼容 agentskills.io 开放标准，可用 `/skills` 浏览或以 `/<skill-name>` 直接调用 |
| 终端后端 | 共七种：local、Docker、SSH、Singularity、Modal、Daytona、Vercel Sandbox；其中 Daytona 与 Modal 支持 serverless 持久化，空闲休眠、按需唤醒 |
| 消息网关 | 单一 gateway 进程同时对接 Telegram、Discord、Slack、WhatsApp、Signal、Email 与 CLI，支持语音转写与跨平台会话连续性 |
| 子智能体 | 可派生隔离的 subagent 并行处理不同工作流；也可写 Python 脚本通过 RPC 调用工具，把多步流水线压缩成零上下文开销的一轮 |
| 定时自动化 | 内置 cron 调度器，用自然语言描述日报、夜间备份、每周审计等任务，无人值守运行 |
| 模型无关 | 支持 Nous Portal、OpenRouter、OpenAI、自建 endpoint 等多种 provider，用 `hermes model` 切换，不改代码、不锁定 |

<!-- asset:blog-2 start -->
![Hermes Agent 核心概念](/img/ai-news/nousresearch-hermes-agent/blog-2.png)

*图：Hermes Agent 核心概念*
<!-- asset:blog-2 end -->


## 环境与前置依赖

- **操作系统**：Windows 10/11 原生支持（无需 WSL）；macOS 12+；Linux 各发行版；Android/Termux 另有 aarch64 的 APT 仓库（分 stable 与 canary 两个通道）。
- **运行时**：安装脚本会代为处理 Python 3.14、Node.js、npm、ripgrep、FFmpeg 以及 Python 依赖。若系统缺少 Git，脚本会把经验证的 Git for Windows 归档放进 Hermes 自己的工具目录，**不会替换你系统的 Git**。
- **Windows 安装位置**：原生安装位于 `%LOCALAPPDATA%\hermes`；若走 WSL2，则与 Linux 一致位于 `~/.hermes`。
- **模型来源**：可自备各家 API Key，也可订阅 Nous Portal（免费档仅限免费模型；Plus 20 美元/月、Super 100 美元/月、Ultra 200 美元/月，付费档含每月额度与 200+ 模型及托管工具调用）。

## 安装与配置（Windows + PowerShell）

### 第一步：安装本体

在 PowerShell 中执行：

`iex (irm https://hermes-agent.nousresearch.com/install.ps1)`

这条命令会拉取官方安装脚本并直接执行，自动装好上述依赖。若你更习惯 WSL2，也可以在 WSL2 里用 Linux 一行命令：`curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`。

### 第二步：初始化配置

安装完成后依次执行：

1. `hermes setup` —— 运行完整设置向导，一次性配置好 provider、模型与各项参数。
2. 若不想逐个收集 API Key，可用 `hermes setup --portal` —— 通过 OAuth 登录 Nous Portal，自动把 Nous 设为 provider 并开启 Tool Gateway（网页搜索、图像生成、TTS、云浏览器统一走订阅）。
3. `hermes model` —— 随时切换 LLM provider 与模型。
4. `hermes tools` —— 配置启用哪些工具。
5. `hermes config set` / `hermes config get` —— 单独读写某个配置项。

### 第三步：启动对话

直接运行 `hermes` 进入交互式 CLI，开始聊天。

### 第四步（可选）：接入消息平台

想让 Agent 常驻云端、从手机指挥，执行 `hermes gateway setup` 完成平台配置，再 `hermes gateway start` 启动网关，之后在 Telegram / Discord / Slack / WhatsApp / Signal / Email 里给机器人发消息即可。

### 关于 Trae Work 与 Java 项目的接入

**官方未提供与 Trae Work / Java 的集成方式。** 公开资料中没有 Hermes Agent 作为 MCP 服务接入 IDE、作为 Skill 放入技能目录、或提供 Java/Spring SDK 的说明。它本身是一个独立的 Agent 运行壳，官方给出的入口是终端 CLI、桌面应用与消息平台网关。

对 Java 后端开发者而言，现实可行的用法是**并行使用**：在 Trae Work 里写 Spring 代码，同时让 Hermes Agent 在终端或云端承担跨会话的长期任务（例如定时生成日报、跑脚本、做资料检索）。若确实需要打通，只能自行基于其 CLI 或 Python RPC 能力做二次封装，官方暂无现成路径。

<!-- asset:code-1 start -->
```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
hermes setup
hermes setup --portal
hermes model
hermes tools
hermes config set
hermes config get
hermes
gateway setup
hermes gateway start
```
<!-- asset:code-1 end -->


## 快速上手

常用命令一览：

| 命令 | 作用 |
| --- | --- |
| `hermes` | 启动交互式 CLI，开始对话 |
| `hermes model` | 选择 LLM provider 与模型 |
| `hermes tools` | 配置启用的工具 |
| `hermes config set` / `hermes config get` | 设置 / 读取单项配置 |
| `hermes gateway` | 启动消息网关 |
| `hermes setup` | 完整设置向导 |
| `hermes claw migrate` | 从 OpenClaw 迁移 |
| `hermes update` | 更新到最新版 |
| `hermes doctor` | 诊断问题 |
| `hermes portal info` | 查看 Portal 已接通的能力 |

进入对话后，CLI 与消息平台共享大量斜杠命令：`/new` 或 `/reset` 开新会话、`/model [provider:model]` 换模型、`/personality [name]` 设定人格、`/retry` 与 `/undo` 重试或撤销上一轮、`/compress` 压缩上下文、`/usage` 查看用量、`/insights [--days N]` 看洞察、`/skills` 浏览技能、`/<skill-name>` 直接调用技能。CLI 中按 `Ctrl+C` 或直接发新消息可打断当前工作；消息平台用 `/stop`。

## 如何确认安装成功

1. 安装脚本跑完后，重载 shell：`source ~/.bashrc`（或 `source ~/.zshrc`）。Windows 原生安装下重开一个 PowerShell 窗口即可。
2. 运行 `hermes doctor`，它会诊断环境与配置问题，没有报错基本说明装好了。
3. 运行 `hermes`，能进入 TUI 并正常对话，即安装与模型配置均成功。
4. 若用了 Portal，运行 `hermes portal info` 确认 provider 与 Tool Gateway 已接通。

> **Windows 用户注意**：若杀毒软件（Bitdefender、Windows Defender 等）把 `%LOCALAPPDATA%\hermes\bin\uv.exe` 报为恶意软件，这是**误报**。该文件是 Astral 的 `uv`（Rust 写的 Python 包管理器），基于机器学习的杀毒引擎常误判这类会下载安装包的无签名 Rust 二进制。官方给出了用 GitHub CLI 做 attestation 校验的完整流程，校验通过且哈希比对为 `True` 即可放心。加白名单时请**加整个文件夹**而非文件哈希，因为 Hermes 每次更新 `uv` 哈希都会变：以管理员身份运行 PowerShell 后执行 `Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\hermes\bin"`。

<!-- asset:code-2 start -->
```powershell
source ~/.bashrc
source ~/.zshrc
hermes doctor
hermes
hermes portal info
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\hermes\bin"
```
<!-- asset:code-2 end -->


## 局限与风险

- **许可证**：MIT，可自由使用与修改。
- **费用**：软件本身免费开源，但模型 provider 与可选托管服务各自计费。Nous Portal 免费档仅限免费模型且有标准速率限制；付费档为 Plus 20 美元/月、Super 100 美元/月、Ultra 200 美元/月，分别含 22 / 110 / 220 美元月度额度（10% 赠送）与 10 / 50 / 100 美元的额度结转上限。云托管为可选项。
- **成熟度**：项目 2025-07-22 创建，迭代活跃。Docker Hub 上镜像体积约 1.3 GB，近期标签形如 `rc.13-v0.21.7-desktop`，仍带 rc 前缀，说明处于快速迭代期。
- **安全**：官方文档设有安全章节，涵盖命令审批、私聊配对、容器隔离；终端后端提供容器加固与命名空间隔离。但让一个自主 Agent 长期在线并持有工具调用权限，本身需要你自行评估风险边界。
- **数据留存**：对话、记忆、技能都会持久保存，换机器时记得备份 Hermes 数据目录。停止本地 Agent 只结束进程，不会删除已保存内容；但需要活跃 Agent 的任务在停止期间不会运行。

## 社区评价（来自 Hacker News 讨论）

在题为《Hermes Agent – Open-source AI agent with persistent memory》的讨论中（52 分、42 条评论），社区情绪颇为两极：

- 有评论者表示「惊讶它还没上首页，我的 X / LinkedIn 信息流里全是它」，并希望能有人把当下这一批 FOMO 框架（paperclip、hermes、pi、opencode、openclaw、nanoclaw、gastown 等）实际都玩一遍，做个第一印象横评——因为很可能「自己用 Claude Code / Codex / Cursor 手搓，效果也就只好那么一点点」。
- 也有评论给出区分：Pi 和 OpenCode 属于 Claude Code 的同类产品，而 Hermes 和 *claw 系列则试图做得更自主一些。
- 另有评论补充了 netclaw 作为同类候选。

总体看，社区认可它的自主性与记忆能力定位，但对「相比自建方案是否真有显著优势」仍持观望态度。

```text
背景：我是一名 Java 后端工程师，日常在 Windows 上用 Trae Work 开发 Spring 项目，想试用 Hermes Agent 这个自带学习闭环的自主智能体。

目标：请帮我在 Windows 上完成 Hermes Agent 的安装、配置与首次可用验证，并给出它与我现有 Java/Spring 开发工作流的配合方式。

具体要求：
1. 用 PowerShell 给出从零开始的完整步骤：安装脚本、依赖检查、hermes setup 配置向导、模型 provider 选择（我暂时不想订阅 Nous Portal，倾向用自备的 OpenAI 或 OpenRouter Key）。
2. 说明每一步执行后我应该看到什么输出，如何判断成功；并告诉我 hermes doctor 报错时常见的排查顺序。
3. 解释 Hermes 的技能系统与记忆机制，并举例说明：如果我经常做 Spring Boot 接口开发与 MyBatis 调试，它可能自动沉淀出什么样的技能，我该如何查看和手动调用这些技能。
4. 明确告诉我官方是否提供与 Trae Work、Java/Spring 项目的集成方式（MCP、Skill 目录、SDK、HTTP）。如果没有，请给出一个不依赖官方集成的务实用法建议，比如让它在终端或云端承担哪些与 Java 项目相关的长期任务。
5. 列出 Windows 上可能踩的坑，尤其是杀毒软件误报 uv.exe 的处理方式，以及加白名单时为什么应该加文件夹而不是文件哈希。
6. 最后给我一份最小验证清单：三条命令，确认安装、模型、对话三件事都正常。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
