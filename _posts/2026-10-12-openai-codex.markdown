---
layout: post
title: "OpenAI Codex CLI 使用说明：终端里的轻量编码 Agent"
subtitle: "Windows + Trae Work 的 Java 程序员，如何装、怎么用、值不值得试"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - 编码Agent
news_category: agent-cli
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/openai/codex
- Stars：128675
- 语言：Rust
- 创建时间：2025-04-13
- 最近更新：2026-10-11
- 官方简介：Lightweight coding agent that runs in your terminal

---

> OpenAI Codex CLI 是一个跑在本机终端里的轻量编码 Agent，能读写代码、执行命令、操作文件，最适合习惯命令行、想给日常开发加一个「随叫随到的结对程序员」的开发者。

## 它是什么，解决什么问题

Codex 是 OpenAI 推出的 AI 编码 Agent，用于写代码、修 bug 等软件工程任务，2025 年 4 月以 Codex CLI 的形式发布，是一个在终端本地运行的开源编码 Agent。它把 OpenAI 的语言模型和本地代码、命令行任务连接起来，让模型能够编写和修改代码、执行命令、通过轻量界面与文件交互。

除了 CLI，Codex 还有几种形态：ChatGPT 网页版、面向 Windows 和 macOS 的桌面应用，以及若干 IDE 集成。如果你想要的是编辑器里的 Codex，官方指向 VS Code、Cursor、Windsurf 的 IDE 安装入口；如果想要桌面应用体验，可以运行 `codex app` 或访问 Codex App 页面；如果你要找的是 OpenAI 的云端 Agent（Codex Web），则去 chatgpt.com/codex。

**注意区分**：本说明针对的是终端里的 Codex CLI（开源，Apache-2.0），不是云端 Codex Web，也不是闭源的桌面应用。

## 适合谁用

- 习惯在终端里干活、希望用自然语言驱动「改代码 + 跑命令」的开发者；
- 想把编码 Agent 当成 Linux 小工具一样嵌进 CI、PR 审查等流程的团队（社区讨论中有人这样描述它的用法）；
- 已经有 ChatGPT Plus、Pro、Business、Edu 或 Enterprise 订阅的用户，可以直接用订阅额度登录使用。

如果你更想要图形化、开箱即用的体验，桌面应用或 IDE 集成可能更顺手；如果你需要云端托管的 Agent，则应看 Codex Web。

## 核心概念与工作方式

- **本地运行**：Codex CLI 在你的电脑本地跑，直接面对你的代码目录和命令行环境。
- **登录方式二选一**：运行 `codex` 后选择 **Sign in with ChatGPT**，用 ChatGPT 订阅（Plus、Pro、Business、Edu、Enterprise）使用；也可以用 API key，但需要额外的配置步骤。
- **多形态共存**：CLI、桌面应用、IDE 插件、云端 Web 是同一品牌下的不同入口，按场景选择。

## 环境与前置依赖

| 项目 | 说明 |
| --- | --- |
| 操作系统 | Windows、macOS、Linux 均有安装方式 |
| 账号 | 推荐 ChatGPT 订阅账号；也可用 API key（需额外配置） |
| 包管理器（可选） | npm 或 Homebrew 也可安装 |
| 网络 | 独立安装脚本默认从 `https://releases.openai.com/codex` 下载，失败时回退到 GitHub Releases |

## 在 Windows 上安装

以下命令均为 Windows PowerShell 写法。

1. **用官方脚本安装（推荐）**：执行 `powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"`。
2. **强制走 GitHub Releases**：如果默认下载源不可用，先设置环境变量再安装——`$env:CODEX_INSTALLER_USE_RELEASES_OPENAI_COM='false'; irm https://chatgpt.com/codex/install.ps1 | iex`。该变量也接受 `0` 和 `no`。
3. **用 npm 安装**：`npm install -g @openai/codex`。
4. **手动下载二进制**：到 GitHub 最新 Release 页面下载对应平台的可执行文件。每个压缩包内只有一个带平台名的文件，解压后建议重命名为 `codex`。

安装完成后，直接运行 `codex` 即可开始。

<!-- asset:code-1 start -->
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
$env:CODEX_INSTALLER_USE_RELEASES_OPENAI_COM='false'; irm https://chatgpt.com/codex/install.ps1 | iex
npm install -g @openai/codex
```
<!-- asset:code-1 end -->


<!-- asset:blog-1 start -->
![Windows 上安装 Codex CLI 的四种方式](/img/ai-news/openai-codex/blog-1.png)

*图：Windows 上安装 Codex CLI 的四种方式*
<!-- asset:blog-1 end -->


## 登录与配置

1. 运行 `codex`。
2. 选择 **Sign in with ChatGPT**，用你的 ChatGPT 账号登录。官方建议用 ChatGPT 账号登录，以便把 Codex 作为 Plus、Pro、Business、Edu 或 Enterprise 订阅的一部分使用。
3. 如果你选择 API key 方式，需要按官方认证文档完成额外配置。

## 如何确认安装成功

- 在 PowerShell 中运行 `codex`，能正常进入交互界面即安装成功。
- 若首次运行提示登录，说明二进制已就位，按提示完成 ChatGPT 登录即可。
- 若命令找不到，检查安装目录是否在 PATH 中，或改用 npm 全局安装方式重试。

## 融入 Trae Work + Java / Spring 工作流

**官方未提供与 Trae Work 的集成方式，也未提供 Java / Spring 专用的 SDK 或 MCP 服务接入路径。** 目前公开资料中，Codex CLI 的定位是终端里的编码 Agent，官方给出的接入形态是终端 CLI、桌面应用、IDE 集成（VS Code、Cursor、Windsurf）以及云端 Web，没有提到 Trae Work 或 Java 生态的专门集成。

因此，在 Windows + Trae Work 的日常里，可行的用法是把它当作**终端侧的补充工具**：

1. 在 Trae Work 里正常写 Java / Spring 代码。
2. 需要批量重构、跑命令、查代码库问题时，切到 PowerShell，在项目根目录运行 `codex`，让它直接面对你的 Maven / Gradle 工程。
3. 把 Codex 的输出（补丁、命令建议）拿回 Trae Work 里审阅、落地。

如果你的团队希望把编码 Agent 嵌进 CI 或 PR 审查，社区讨论中有人提到可以像使用 Linux 小工具一样使用它，但这属于使用者的自发实践，官方文档未给出针对 Java 项目的具体配方。

## 局限与风险

- **许可证分叉**：CLI 采用 Apache-2.0 许可证；桌面应用为专有软件。使用前请确认你用的是哪一部分。
- **账号依赖**：推荐路径依赖 ChatGPT 订阅；用 API key 需要额外配置，且计费方式不同。
- **成熟度**：Codex CLI 于 2025 年 4 月发布，到 2026 年 3 月 Codex 整体已有超过 200 万周活跃用户，OpenAI 正把它定位为更广泛的企业 Agent 平台。产品迭代快，行为可能随版本变化。
- **安全**：2026 年 3 月 OpenAI 推出了 Codex Security，一个用于识别和修复软件漏洞的应用安全 Agent。让 Agent 执行命令、修改文件本身带有风险，建议在受控目录和版本控制下使用。
- **社区反馈**：在 Hacker News 关于 Codex CLI 的讨论（516 points，289 条评论）中，有用户反馈遇到认证问题（「Just getting auth issues so far...」），也有人跟进表示同样遇到。这类问题多与登录配置相关，遇到时可先检查账号与网络。

<!-- asset:blog-2 start -->
![使用 Codex CLI 需注意的风险](/img/ai-news/openai-codex/blog-2.png)

*图：使用 Codex CLI 需注意的风险*
<!-- asset:blog-2 end -->


## 社区评价（来自 Hacker News 讨论）

- 有评论把 Codex CLI 视为对 Claude Code 的直接回应，并指出 Codex 是开源的、Claude Code 不是；讨论中提到的反编译争议实际指向 Claude Code，而非 Codex。
- 有观点认为编码 Agent CLI 在软件工程设计中是被低估的一环，可以像 `llm` 这类工具一样，把智能「撒」到 CI、PR 审查等场景里。
- 也有用户对宣传动图播放过快表示不满，认为看不清实际效果。
- 关于 Codex Security 的讨论热度更高（598 points，229 条评论），说明安全方向受到较多关注。

## 快速上手清单

1. 在 PowerShell 运行安装脚本：`powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"`。
2. 运行 `codex`。
3. 选择 **Sign in with ChatGPT** 并登录。
4. 在 Java / Spring 项目根目录再次运行 `codex`，让它读取工程。
5. 用自然语言提出第一个任务，例如让它解释某个 Service 类的调用链，或为某个 Controller 补一个单元测试。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 项目，项目用 Maven 构建，代码在本地 Git 仓库里。我已经在 PowerShell 里装好并登录了 OpenAI Codex CLI。

目标：请作为我的终端编码 Agent，帮我在当前 Spring Boot 工程里完成一次小范围、可审查的改造。

具体要求：
1. 先扫描项目结构，告诉我模块划分、主要分层（Controller / Service / Repository）和使用的 Spring Boot 版本。
2. 找出所有对外暴露的 REST 接口，列成表格：HTTP 方法、路径、对应方法、入参、返回类型。
3. 挑其中一个没有单元测试的 Controller，为它补一个基于 JUnit 5 + MockMvc 的测试类，放在标准的 src/test/java 目录下，包名与主代码一致。
4. 运行 Maven 测试命令验证新测试通过，把命令和结果贴给我。
5. 所有改动以补丁形式展示，先不要直接提交 Git，等我确认。

约束：不要改动生产代码的业务逻辑；不要引入新的第三方依赖；如果发现接口设计问题，只列出来并给出建议，不要擅自修改。
```

## 相关链接

- 官方文档：developers.openai.com/codex
- 仓库：github.com/openai/codex
- 云端版本：chatgpt.com/codex
- 桌面应用：运行 `codex app` 或访问 Codex App 页面
- IDE 集成：developers.openai.com/codex/ide（VS Code、Cursor、Windsurf）

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
