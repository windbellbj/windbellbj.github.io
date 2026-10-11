---
layout: post
title: "OpenAI Codex CLI 上手：终端里的编码 Agent"
subtitle: "128k Star 的 Rust 编码智能体，Windows 上一条 PowerShell 命令装好"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: agent-cli
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/openai/codex
- Stars：128665
- 语言：Rust
- 创建时间：2025-04-13
- 最近更新：2026-10-11
- 官方简介：Lightweight coding agent that runs in your terminal

---

## 解决什么问题

Codex CLI 是 OpenAI 推出的编码 Agent（coding agent），它直接运行在你本机的终端里，而不是云端。README 对它的定位只有一句话："a coding agent from OpenAI that runs locally on your computer"。

对于日常在 Windows 上用 Trae Work 写 Java / Spring 的开发者来说，它解决的是「把 AI 编码能力放到终端里」这件事：你可以在命令行里直接让 Agent 干活，而不必切到编辑器或网页。README 同时给出了三条分流路径：想要编辑器内体验的（VS Code、Cursor、Windsurf）去装 IDE 版本；想要桌面应用体验的运行 `codex app` 或访问 Codex App 页面；想要 OpenAI 的云端 Agent（Codex Web）则去 chatgpt.com/codex。

需要明确的是：README 未提供 Codex CLI 与 Trae Work 的任何集成方式，也未提供与 Java / Spring 项目的 SDK 或 HTTP 集成说明。

## 核心概念

- **Codex CLI**：本仓库的主体，一个跑在本地终端里的编码 Agent，主语言为 Rust。
- **本地运行**：README 强调 "runs locally on your computer"，即 Agent 进程在你自己的机器上。
- **多种形态**：README 区分了 Codex CLI（终端）、IDE 插件（VS Code / Cursor / Windsurf）、桌面应用（`codex app`）以及云端 Agent（Codex Web）。
- **登录方式**：可以用 ChatGPT 账号登录（推荐，覆盖 Plus、Pro、Business、Edu、Enterprise 套餐），也可以用 API key，但后者需要额外配置。
- **安装渠道**：独立安装脚本（Mac/Linux 用 sh，Windows 用 PowerShell）、npm 包 `@openai/codex`、Homebrew cask `codex`，以及从 GitHub Release 下载二进制。

README 未提供关于 Agent 内部架构、工具调用协议、配置文件格式等更细的概念说明。

## 前置依赖

README 明确提到的前置条件有限：

- 一个终端环境。Windows 用户需要能运行 PowerShell。
- 若要使用 ChatGPT 套餐登录，需要一个 ChatGPT 账号，且套餐为 Plus、Pro、Business、Edu 或 Enterprise 之一。
- 若改用 API key，README 指出这需要 "additional setup"，并指向 developers.openai.com/codex/auth 的 "Sign in with an API key" 章节。
- 若走 npm 安装路线，需要本机有 npm；若走 Homebrew 路线，需要 Homebrew（README 中 Homebrew 命令为 `brew install --cask codex`）。

README 未提供具体的 Node 版本要求、Rust 版本要求或 Windows 版本要求。

## 安装与配置

以下步骤按 Windows + Trae Work 的读者视角组织。

**第一步：安装 Codex CLI（Windows）**

README 给出的 Windows 安装命令是 PowerShell 一行式：`powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"`。在 Trae Work 的内置终端里直接粘贴执行即可。

**第二步：可选的安装渠道**

如果不想用安装脚本，README 还提供了两条替代路径：

1. 用 npm 全局安装：`npm install -g @openai/codex`。
2. 用 Homebrew 安装：`brew install --cask codex`（README 未说明该命令在 Windows 上的可用性）。

另外，README 提到可以到 latest GitHub Release 页面下载对应平台的二进制包。但 README 列出的二进制包只覆盖 macOS（`codex-aarch64-apple-darwin.tar.gz`、`codex-x86_64-apple-darwin.tar.gz`）和 Linux（`codex-x86_64-unknown-linux-musl.tar.gz`、`codex-aarch64-unknown-linux-musl.tar.gz`），**未列出 Windows 二进制包**。README 还提示解压后建议把带平台名的可执行文件重命名为 `codex`。

**第三步：安装源回退开关（可选）**

README 说明独立安装器默认从 `https://releases.openai.com/codex` 下载，当元数据或资源下载不可用时会回退到 GitHub Releases。若要强制走 GitHub Releases，可设置环境变量 `CODEX_INSTALLER_USE_RELEASES_OPENAI_COM` 为 `false`（`0` 和 `no` 也接受）。Windows 下的写法是：先执行 `$env:CODEX_INSTALLER_USE_RELEASES_OPENAI_COM='false'`，再执行 `irm https://chatgpt.com/codex/install.ps1 | iex`。

**第四步：启动与登录**

安装完成后，README 说直接运行 `codex` 即可开始。首次运行后选择 **Sign in with ChatGPT** 登录，README 推荐用 ChatGPT 账号，以便作为 Plus、Pro、Business、Edu 或 Enterprise 套餐的一部分使用 Codex。也可以改用 API key，但 README 指出这需要额外配置。

**第五步：融入 Trae Work 日常工作流**

README 未提供与 Trae Work / Java 的集成方式。README 中唯一与编辑器相关的表述是：如果你想要编辑器内的 Codex（VS Code、Cursor、Windsurf），去 developers.openai.com/codex/ide 安装 IDE 版本——其中并未提及 Trae Work。因此，在 Trae Work 里最直接可行的用法，是在 Trae Work 的内置终端中把它当作命令行工具调用（即上面第一步到第四步的流程），而不是作为 MCP 服务、Skill 包或 SDK 依赖接入。README 未提供 MCP 接入方式、未提供 Skill 目录约定、未提供 Java/Spring SDK 或 HTTP 集成方式。

## 最小可用示例

把下面这段指令整段复制给 Trae Work 等 AI 编程助手，让它帮你在 Windows 上装好并跑通 Codex CLI，同时结合一个 Spring 项目做首次试用。

```text
背景：我是一名 Java 后端程序员，日常在 Windows 上使用 Trae Work 开发，技术栈以 Java / Spring 为主。我想试用 OpenAI 的 Codex CLI（仓库 openai/codex），它是一个跑在本地终端里的编码 Agent。

目标：帮我在 Windows 上完成 Codex CLI 的安装、登录，并用它在一个 Spring 项目里完成一次真实的小改动。

要求：
1. 先确认我当前终端是 PowerShell，然后执行官方 Windows 安装命令：powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"。如果这条失败，再尝试 npm install -g @openai/codex。
2. 安装完成后运行 codex，并引导我选择 Sign in with ChatGPT 完成登录；如果我打算用 API key，请提醒我这需要额外配置，并给出官方文档地址 developers.openai.com/codex/auth。
3. 登录成功后，让我在一个已有的 Spring Boot 项目根目录下启动 codex，先让它只读地浏览项目结构，说明它看到的模块划分和构建方式，不要修改任何文件。
4. 然后给我一个低风险的小任务，例如给某个 Controller 补一段参数校验或给某个 Service 方法补单元测试，让 Codex CLI 生成改动，我在确认 diff 之后再决定是否接受。
5. 全程只使用 README 中出现的命令和地址，不要编造任何配置路径、环境变量或子命令；如果某一步 README 没有说明，请直接告诉我"README 未提供"。
6. 最后用一段话总结：Codex CLI 在我的 Windows + Trae Work + Spring 工作流里，适合放在哪个环节使用。
```

## 验证方法

按 README 能直接执行的验证动作如下：

1. 安装完成后，在终端运行 `codex`，确认能正常启动并进入交互界面。
2. 在启动后的界面中选择 **Sign in with ChatGPT**，确认登录流程可以走通（README 推荐这种方式）。
3. 如果安装脚本下载异常，按 README 的说明设置 `CODEX_INSTALLER_USE_RELEASES_OPENAI_COM` 为 `false` 后重试，观察是否改为从 GitHub Releases 下载。
4. 如果走 npm 路线，可用 `npm install -g @openai/codex` 重装一次，确认包名正确。
5. 如果走 Homebrew 路线，可用 `brew install --cask codex` 确认 cask 名称正确。

README 未提供版本号查询命令、健康检查命令或自检子命令。

## 风险与注意事项

- **登录方式差异**：README 明确说用 API key 需要 "additional setup"，比 ChatGPT 账号登录多一步，别默认两者等价。
- **套餐限制**：用 ChatGPT 账号登录时，README 提到的适用套餐为 Plus、Pro、Business、Edu、Enterprise，其他套餐情况 README 未提供。
- **安装源**：独立安装器默认从 `https://releases.openai.com/codex` 下载，失败才回退 GitHub Releases；如果你所在网络对前者不友好，需要手动设置 `CODEX_INSTALLER_USE_RELEASES_OPENAI_COM=false`。
- **Windows 二进制缺失**：README 列出的 GitHub Release 二进制包只有 macOS 和 Linux，未列出 Windows 版本，因此 Windows 用户走「下载二进制」这条路 README 未提供明确指引。
- **Homebrew 在 Windows 上**：README 给出 `brew install --cask codex`，但未说明 Windows 上是否适用。
- **本地运行的含义**：README 只说它 "runs locally on your computer"，未说明数据如何上传、代码是否离开本机等细节，README 未提供。
- **与 Trae Work 的关系**：README 未提供与 Trae Work 的集成方式，不要假设它能作为 MCP 服务或 Skill 直接挂进 Trae Work。
- **许可证**：本仓库使用 Apache-2.0 License。

## 替代方案

README 本身给出的「替代形态」有三条，均来自同一项目：

1. **IDE 版本**：如果你想要编辑器内的 Codex，README 指向 developers.openai.com/codex/ide，支持 VS Code、Cursor、Windsurf。
2. **桌面应用**：运行 `codex app`，或访问 Codex App 页面。
3. **云端 Agent**：如果你要找的是 OpenAI 的云端 Agent（Codex Web），README 指向 chatgpt.com/codex。

除上述同项目内的形态区分外，README 未提供与其他同类工具的对比或替代建议。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
