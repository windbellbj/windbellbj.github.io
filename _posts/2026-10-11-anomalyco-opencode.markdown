---
layout: post
title: "OpenCode 使用说明书：开源 AI 编程代理，终端里的编码搭子"
subtitle: "212K Star 的开源编码 Agent，支持 75+ 模型提供商，Windows 上也能装，Java 后端值得一试"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - 编码Agent
news_category: agent-cli
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/anomalyco/opencode
- Stars：212733
- 语言：TypeScript
- 创建时间：2025-04-30
- 最近更新：2026-10-11
- 官方简介：The open source coding agent.

---

> OpenCode 是一个开源 AI 编程代理（coding agent），让你在终端、桌面端或 IDE 里用自然语言驱动代码编写、分析与重构；它最适合习惯命令行、想自由切换 Claude/GPT/Gemini 等任意模型、又在意代码隐私的开发者。

## 它解决什么问题

日常写 Java / Spring 时，很多活儿是重复且琐碎的：翻一个陌生模块的调用链、给一堆 DTO 补 getter/setter、把一段老代码重构成新写法、排查一个 NPE 到底从哪冒出来。OpenCode 把这些交给一个能读写你本地仓库、能跑命令、能看 LSP 诊断的代理来做。

它的几个关键卖点：

- **模型自由**：通过 Models.dev 支持 75+ LLM 提供商，包括 Claude、GPT、Gemini，也支持本地模型；内置免费模型，也可以登录 GitHub Copilot 或 ChatGPT Plus/Pro 账户复用已有订阅。
- **多形态**：终端界面（TUI）、桌面应用（BETA）、Web 界面、IDE 扩展（VS Code / Cursor / Zed / Windsurf / VSCodium）都有。
- **多会话**：同一个项目里可以并行启动多个代理。
- **隐私优先**：官方称不存储你的代码或上下文数据。
- **LSP 集成**：自动为 LLM 加载合适的 LSP，对 Java 这类强类型语言尤其有用。

## 核心概念：Agent 与模式

OpenCode 内置两个可切换的代理，用 `Tab` 键在它们之间切换：

| 代理 | 权限 | 适用场景 |
| --- | --- | --- |
| **build** | 默认，完整访问权限 | 实际开发、改代码 |
| **plan** | 只读 | 分析、探索代码库、规划改动；默认拒绝文件编辑，跑 bash 命令前会请求许可 |

另外还有一个 **general** 子代理，用于复杂搜索和多步任务，在消息里用 `@general` 调用。

## 环境与前置依赖

- **Node.js 生态**：如果用 npm 安装，需要 Node 环境。
- **Windows 支持**：官方提供 Scoop 和 Chocolatey 两种 Windows 包管理器安装方式；也可以直接下载独立 CLI 二进制（Windows ARM64 / x64 / x64 baseline）。
- **注意**：官方文档明确写着「Windows package managers are not supported」——这与仓库说明里给出的 `scoop install opencode`、`choco install opencode` 存在冲突，**两种说法并列，请以实际安装结果为准**。
- **版本提示**：安装前请移除 0.1.x 之前的旧版本。

## 安装（Windows PowerShell）

### 方式一：Scoop（推荐先试）

1. 如果还没装 Scoop，先按 Scoop 官网说明装好。
2. 执行 `scoop install opencode`。
3. 如果失败，改用下面的 npm 方式。

### 方式二：Chocolatey

1. 以管理员身份打开 PowerShell。
2. 执行 `choco install opencode`。

### 方式三：npm 全局安装

1. 确认已装 Node.js。
2. 执行 `npm i -g opencode-ai@latest`。
3. 也可以用 `bun`、`pnpm`、`yarn` 替代 npm。

### 方式四：独立二进制

从 releases 页面下载 Windows 对应的独立 CLI 二进制（ARM64 / x64 / x64 baseline），解压后把所在目录加入 PATH。

### 桌面版（BETA）

- 从 releases 页面或 opencode.ai/download 下载 `opencode-desktop-windows-x64.exe`。
- 或用 Scoop：`scoop bucket add extras; scoop install extras/opencode-desktop`。

> 安装脚本的安装目录优先级为：`$OPENCODE_INSTALL_DIR` → `$XDG_BIN_DIR` → `$HOME/bin` → `$HOME/.opencode/bin`。Windows 上主要走包管理器或独立二进制，这套优先级主要针对类 Unix 环境。

## 快速上手

1. 安装完成后，在 PowerShell 里执行 `opencode` 启动终端界面。
2. 首次启动后用 `/connect` 连接模型提供商；也可以直接使用内置免费模型。
3. 用 `Tab` 在 **build** 和 **plan** 两个代理之间切换。
4. 在项目根目录下向它提问，比如「这个 Spring Boot 项目的 Controller 层有哪些接口没有做参数校验」。
5. 需要复杂搜索时，在消息里用 `@general` 调用通用子代理。
6. 想开 Web 界面，执行 `opencode pair`，会输出本地 URL、用户名和密码。

## 如何确认安装成功

- 在 PowerShell 里执行 `opencode --version` 或直接执行 `opencode`，能进入 TUI 即安装成功。
- 如果命令找不到，检查包管理器安装路径是否在 PATH 中，或改用独立二进制并手动加入 PATH。

## 融入 Trae Work / Java 工作流

**官方未提供与 Trae Work 的直接集成方式**，也没有公开的 Java / Spring SDK 或 MCP 服务端接入路径。因此不要指望在 Trae Work 里一键调用它。

可行的做法是**并行使用**：

1. 在 Trae Work 里正常写 Java 代码。
2. 另开一个 PowerShell 窗口，在同一个项目根目录下启动 `opencode`。
3. 让 OpenCode 做只读分析（切到 **plan** 代理），把结论贴回 Trae Work 继续改。
4. 需要它直接改代码时切到 **build** 代理。

> 如果你的目标是「在 Trae Work 里通过 MCP 调用一个编码代理」，OpenCode 目前不是这个形态；它本身是一个独立的终端/桌面/IDE 代理，而不是供其他 IDE 调用的 MCP 服务。

## 局限与风险

- **许可证**：官方未在给出的资料中明确说明具体许可证类型，使用前请自行到仓库确认。
- **成熟度**：桌面应用标注为 BETA；官方文档同时存在 V1 和 V2 两套安装命令（`opencode.ai/install` 与 `opencode.ai/v2/install`），说明产品仍在快速迭代，命令可能变动。
- **Windows 支持存在矛盾**：仓库说明给了 Scoop / Chocolatey，官方文档却写「Windows package managers are not supported」，实际体验可能不稳定。
- **与 Anthropic 的冲突**：Hacker News 上有两条高热度讨论——《Anthropic blocks third-party use of Claude Code subscriptions》（625 分，513 条评论）和《Anthropic takes legal action against OpenCode》（483 分，398 条评论）。社区高赞评论认为，这是 Anthropic 对第三方客户端复用 Claude Code 凭证/订阅的打击，属于灰色地带；也有评论认为 Anthropic 在推理上亏钱，所以想尽量封禁这类用户。**如果你打算用 Claude 订阅跑 OpenCode，需要留意账号风险。**
- **费用**：OpenCode 本身开源免费，但模型调用可能产生费用；官方提供 OpenCode Go（$10/月）订阅，以及 OpenCode Zen 精选模型服务。

## 社区评价（来自 Hacker News 讨论）

- 有评论认为 Anthropic 此举是「对第三方客户端的打压」，且「周四晚上毫无预警地部署，必然引发轩然大波」。
- 有评论直言「他们在每次推理上都亏钱，所以当然想尽可能多地封禁用户」。
- 也有评论把这件事和 Anthropic 威胁 OpenClaw 联系起来，认为「Anthropic 在开源社区真的在到处树敌」。
- 另有评论引用 Dario 多次表示不认为开放权重模型有价值，认为这是「恐惧驱动的行为，护城河正在快速缩小」。

## 一句话建议

如果你想要一个**不绑定单一厂商、能在终端里直接读写 Java 仓库、支持 LSP 的开源编码代理**，OpenCode 值得花半小时装来试试；但如果你重度依赖 Claude 订阅，先想清楚账号风险。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 项目，想试用 OpenCode 这个开源编码代理来辅助日常开发。

目标：帮我把 OpenCode 接入我的日常工作流，并完成一次真实的小任务。

具体要求：
1. 先确认我的环境：Windows + PowerShell，已装 Node.js，项目是 Maven 多模块 Spring Boot 项目。
2. 给出在 Windows 上安装 OpenCode 的可行步骤（优先 Scoop，失败则 npm 全局安装），并说明如何验证安装成功。
3. 说明如何用 /connect 连接模型提供商，以及如何用 Tab 在 build 和 plan 两个代理之间切换。
4. 给我一个具体的试用任务：让 OpenCode 在 plan 模式下分析我的 Controller 层，找出所有缺少参数校验的接口，并输出一份清单。
5. 再让它在 build 模式下，为其中一个接口补上 @Valid 注解和对应的校验注解，并说明改了哪些文件。
6. 提醒我注意：官方未提供与 Trae Work 的直接集成，所以只能并行开一个 PowerShell 窗口使用；同时提醒我 Claude 订阅可能存在的账号风险。
```

## 参考链接

- 仓库：https://github.com/anomalyco/opencode
- 官网：https://opencode.ai
- 文档：https://opencode.ai/docs
- 下载：https://opencode.ai/download
- Discord：https://opencode.ai/discord
- Hacker News 讨论：https://news.ycombinator.com/item?id=46625918

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
