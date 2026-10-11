---
layout: post
title: "Orca 初体验：并行 Agent 编排的 ADE"
subtitle: "Windows 上装好 Orca，让多个编码 Agent 各占一个 worktree 同时干活"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/stablyai/orca
- Stars：89685
- 语言：TypeScript
- 创建时间：2026-03-17
- 最近更新：2026-10-11
- 官方简介：Orca is the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. Available on desktop, mobile and remote runtime.

---

## 解决什么问题

Orca 官方对自己的定位是「The AI Orchestrator for 100x builders」，也就是面向高强度开发者的 AI 编排器。它要解决的核心问题是：当你同时想用多个编码 Agent 干活时，如何把它们放在一起管理。

README 给出的答案是：Run Codex, ClaudeCode, OpenCode or Pi side-by-side — each in its own worktree, tracked in one place。即让多个 Agent 并排运行，每个 Agent 各自拥有一个独立的 git worktree，并在同一个地方被统一追踪。

README 还提到一个典型用法：Fan one prompt across five agents, each in its own isolated git worktree — compare the results and merge the winner。也就是把同一个提示词分发给五个 Agent，各自在隔离的 worktree 里干活，然后比较结果、合并胜出的那个。

对 Java 后端程序员来说，这对应的是「一个需求同时让几个 Agent 试不同实现，再挑最好的合并」这种场景。

## 核心概念

README 中明确出现的概念包括：

- **ADE**：官方简介称 Orca 是 the ADE for working with a fleet of parallel agents，即面向「并行 Agent 集群」的 ADE。README 未对 ADE 这一缩写给出展开解释。
- **Parallel Worktrees（并行 worktree）**：每个 Agent 运行在各自隔离的 git worktree 中，互不干扰，便于对比结果。
- **Supported Agents**：README 称 Works with any CLI agent — if it runs in a terminal, it runs in Orca。README 列出了大量已支持的 Agent，包括 Claude Code、Codex、Grok、Cursor、GitHub Copilot、Muse、DeepSeek Harness、ZCode、OpenCode、MiMo Code、Amp、OpenClaude、Antigravity、Pi、oh-my-pi、Hermes Agent、Devin、Goose、Auggie、Autohand Code、Charm、Cline、CodeBuddy、Codebuff、Freebuff、Command Code、Continue、Droid、Kilocode、Kimi、Kiro、Mistral Vibe、Qwen Code、Rovo Dev，并标注 + any CLI agent。
- **自带订阅**：官方简介称 Run any coding agent with your own subscription，即使用你自己的订阅来跑任意编码 Agent。
- **多端形态**：Available on desktop, mobile and remote runtime，即桌面端、移动端与远程运行时。
- **Orca CLI**：README 提到 Agents drive Orca too — script every workflow with `orca worktree create`、`snapshot`、`click`、`fill`。
- **Mobile Companion**：手机端伴侣应用，可在手机上监控和指挥 Agent，Agent 完成时收到通知并随时发送后续指令。
- **SSH Worktrees**：在远程机器上运行 Agent，包含完整文件编辑、git、终端，并支持自动重连与端口转发。
- **Design Mode**：在真实 Chromium 窗口中点击任意 UI 元素，把它的 HTML、CSS 和裁剪后的截图直接送进 Agent 的提示词。
- **Annotate AI Diffs**：在任意 diff 行上留评论并回传给 Agent，在 Orca 内完成 review、编辑与提交。
- **Computer Use**：当工作流需要真实交互时，让 Agent 操作桌面应用和可见 UI。

## 前置依赖

README 未提供一份独立的「前置依赖」清单。从 README 可确认的信息有：

- 桌面端支持 macOS、Windows、Linux 三个平台（README 徽章与 Install 章节均如此标注）。
- 使用方式是「运行任意 CLI Agent」，README 称只要能在终端里跑，就能在 Orca 里跑。因此你需要自行准备并登录好想用的 CLI Agent（例如 Claude Code、Codex 等），并使用自己的订阅。
- 并行 worktree 依赖 git worktree 机制，README 提到每个 Agent 在各自隔离的 git worktree 中运行。
- 移动端伴侣需要与桌面端配对使用。

除以上内容外，README 未提供具体的系统版本、内存、Node 版本等硬性依赖要求。

## 安装与配置

以下步骤站在「Windows + Java 后端 + 日常用 Trae Work」的读者视角给出。

**第一步：安装 Orca 桌面端**

README 的 Install 章节给出两种方式：

1. 从官网下载页获取：README 给出的下载入口是 onOrca.dev 的 download 页面。
2. 直接下载构建产物：README 明确列出了 Windows 安装包地址，即 releases 下的 `orca-windows-setup.exe`；同时列出 macOS Apple Silicon、macOS Intel、Linux AppImage 以及 All builds 的入口。

README 中给出的包管理器安装方式只有 macOS 的 Homebrew（`brew install --cask stablyai/orca/orca`）和 Arch Linux 的 AUR（`yay -S stably-orca-bin`，或 `stably-orca-git` 从源码构建）。README 未提供 Windows 上的包管理器（如 winget、scoop、chocolatey）安装命令。

**第二步：准备你要用的 CLI Agent**

Orca 本身不提供模型，README 的定位是运行你已有的 CLI Agent 并使用你自己的订阅。因此先在 Windows 上把想用的 CLI Agent 装好并完成登录，再回到 Orca 中使用。README 未提供各 Agent 的具体安装命令。

**第三步：在 Orca 中打开你的 Java / Spring 项目**

README 未提供「打开项目」的具体操作步骤描述。可确认的是 Orca 内置 VS Code 的编辑器（README 原文：VS Code's editor with autosave everywhere），并提供文件浏览器、Markdown/图片/PDF 预览等能力。

**第四步：用并行 worktree 跑多个 Agent**

README 描述的能力是：把同一个提示词分发给多个 Agent，每个 Agent 在各自隔离的 git worktree 中工作，然后对比结果并合并胜出的那个。README 未提供该操作在界面上的具体点击路径。

**第五步：融入 Trae Work 日常工作流**

- 作为 MCP 服务接入 Trae Work：README 未提供与 Trae Work / Java 的集成方式。README 全文未出现 MCP 相关描述。
- 作为 Skill 放入技能目录：README 未提供与 Trae Work / Java 的集成方式。README 全文未出现 Skill 相关描述。
- 在 Trae Work 终端中作为 CLI 调用：README 确实提供了 Orca CLI，并给出示例命令名 `orca worktree create`、`snapshot`、`click`、`fill`，文档入口指向 CLI overview 页面。但 README 未说明 Orca CLI 的安装方式、是否随桌面端一起提供、在 Windows 上的可执行文件名或路径。因此「在 Trae Work 终端里直接调用 orca 命令」这一路径，README 未提供可落地的配置说明。
- 在 Java / Spring 项目中通过 SDK 或 HTTP 集成：README 未提供与 Trae Work / Java 的集成方式。README 全文未提及 Java SDK、HTTP API 或 Spring 相关集成。

结论：就 README 而言，Orca 是一个独立的桌面应用（外加移动端伴侣与远程运行时），README 未提供把它嵌入 Trae Work 或 Java 项目的官方方式。可行的做法是让 Orca 与 Trae Work 并行使用：在 Orca 里跑并行 Agent 做多方案对比，在 Trae Work 里做日常编码。

**第六步（可选）：移动端伴侣**

README 给出 iOS 的 App Store 入口与 Android 的 APK 下载入口（README 标注版本为 0.0.52），并说明需要与桌面端配对，用于在手机上监控和指挥 Agent。

## 最小可用示例

下面这段指令可以直接整段复制给 Trae Work 等 AI 编程助手，用来规划一次 Orca 试用。

text
背景：我在 Windows 上用 Trae Work 做 Java / Spring 后端开发，项目用 git 管理。我准备试用 Orca（stablyai/orca），它是一个面向并行 Agent 的 ADE，官方说明是让多个 CLI 编码 Agent 各自在独立的 git worktree 中并排运行，并在同一个地方统一追踪，还可以把同一个提示词分发给多个 Agent 后对比结果、合并胜出的那个。

目标：请帮我把「用 Orca 并行跑多个 Agent 实现同一个 Spring 需求」这件事拆成一份可执行的试用计划。

要求：
1. 先列出我需要提前准备的东西：Windows 上安装 Orca 桌面端的入口、需要提前装好并登录的 CLI Agent、以及我的 Spring 项目需要处于什么 git 状态。
2. 设计一个适合对比的小需求，例如给一个已有的 Spring Boot 服务新增一个 REST 接口并补上单元测试，要求这个需求足够小，能在一次会话内完成。
3. 给出分发提示词时的写法建议：如何描述背景、目标、验收标准，让多个 Agent 在各自 worktree 中产出的结果具备可比性。
4. 给出对比与合并的检查清单：看哪些指标（编译是否通过、测试是否通过、改动范围、代码风格一致性），以及合并胜出分支前需要做哪些确认。
5. 明确标注哪些步骤是 Orca 官方 README 里写明的，哪些是你基于通用经验的建议，不要把我没确认过的命令或配置路径当成事实告诉我。


## 验证方法

README 未提供官方的验证步骤或自检命令。基于 README 中可确认的事实，可以按以下方式自行确认安装是否可用：

1. 确认桌面端能正常启动：从 README 给出的 Windows 安装包 `orca-windows-setup.exe` 安装后启动应用，确认能进入主界面。
2. 确认终端能力可用：README 称 Orca 提供 Ghostty-class terminals with WebGL rendering、infinite splits，以及重启后仍保留的 scrollback。可以打开终端并尝试分屏，确认终端可交互。
3. 确认能识别你的 CLI Agent：README 称 Works with any CLI agent — if it runs in a terminal, it runs in Orca。可以在 Orca 的终端里手动运行你已安装的 CLI Agent，确认它能正常启动。
4. 确认并行 worktree 生效：按 README 的描述，把同一个提示词分发给多个 Agent，确认每个 Agent 落在各自独立的 git worktree 中，且结果可以在同一处对比。
5. 确认 CLI 可用：README 提到 `orca worktree create`、`snapshot`、`click`、`fill` 这些命令名，可以在终端中尝试调用并观察是否被识别。README 未说明该 CLI 的安装方式与 Windows 下的可执行文件名，因此这一步能否成功以实际环境为准。
6. 确认移动端配对：如果使用移动端伴侣，按 README 的说明与桌面端配对，确认能在手机上收到 Agent 完成通知并发送后续指令。

## 风险与注意事项

- **订阅与账号**：官方简介明确说 Run any coding agent with your own subscription，即模型调用走你自己的订阅。README 提到 Account switcher & usage tracking 可以查看 Claude 和 Codex 的用量与限流重置时间，并支持热切换账号而无需重新登录。相关费用与额度由你所用 Agent 的订阅决定，README 未提供 Orca 自身的计费说明。
- **隐私与遥测**：README 在 Community & Support 中给出隐私与遥测文档入口，说明 Orca 会收集匿名使用数据，并提供了退出方式。README 未在正文中列出具体收集项。
- **代码签名**：README 的 Signed Builds 章节说明 Windows 代码签名由 SignPath.io 赞助/提供，证书由 SignPath Foundation 提供。
- **许可证**：README 标注 Orca 基于 MIT License 免费开源。
- **平台差异**：README 给出的包管理器安装方式仅覆盖 macOS 与 Arch Linux，Windows 用户需使用安装包。
- **移动端版本**：README 中 Android APK 标注为 0.0.52，iOS 走 App Store。README 未说明移动端与桌面端的版本兼容要求。
- **功能迭代速度**：README 自述 we ship daily, so this list is perpetually behind，并称 changelog 才是真正的功能列表。这意味着 README 描述可能与最新版本存在差异。
- **集成缺失**：README 未提供与 Trae Work、Java、Spring 的任何集成方式，也未提供 MCP、Skill、SDK、HTTP API 相关说明。

## 替代方案

README 未提供替代方案章节，也未将 Orca 与其他工具做对比。

从 README 可确认的相关信息是：Orca 支持接入大量 CLI 编码 Agent（包括 Claude Code、Codex、Cursor、GitHub Copilot、Cline、Continue、Qwen Code、Kimi、Kiro 等，并标注 + any CLI agent）。因此如果你的需求只是「用某一个 CLI Agent」，直接使用该 Agent 本身即可；Orca 的差异点在于把多个 Agent 放进并行 worktree 统一编排与追踪。

除上述内容外，README 未提供其他替代方案的说明。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
