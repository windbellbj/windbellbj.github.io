---
layout: post
title: "Claude Code 使用说明书：终端里的智能体编码工具"
subtitle: "在 Windows + Trae Work 的 Java/Spring 工作流中快速试用 Anthropic 官方编码 Agent"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - 编码Agent
news_category: agent-cli
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/anthropics/claude-code
- Stars：150232
- 语言：TypeScript
- 创建时间：2025-02-22
- 最近更新：2026-10-11
- 官方简介：Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows - all through natural language commands.

---

> Claude Code 是 Anthropic 推出的智能体编码工具，常驻终端、理解整个代码库，用自然语言帮你改代码、跑命令、处理 Git 流程；最适合习惯命令行、想让 AI 直接动手改项目的开发者。

## 它是什么，能解决什么问题

Claude Code 是一个 **agentic coding tool（智能体编码工具）**：它读取你的代码库、编辑文件、执行命令，并与你的开发工具集成。官方定位是「住在终端里」，通过自然语言指令完成日常任务、解释复杂代码、处理 Git 工作流。

它同时提供多种使用形态：终端 CLI、IDE 扩展（VS Code、JetBrains）、桌面应用、网页端，以及 GitHub 上的 `@claude` 提及方式。对 Java 后端开发者来说，最直接的入口是终端 CLI。

典型适用场景：

- 让 AI 跨多个文件定位并修复 Bug，例如排查重复扣款、并发提交一类问题
- 为已有模块补测试、写迁移脚本、做多日期的重构迁移
- 解释一个陌生仓库的结构与关键流程
- 在终端里直接完成 Git 相关操作

## 核心概念与工作原理

- **终端优先**：主体是一个命令行程序，进入项目目录后运行即可开始会话。
- **理解整个代码库**：它会读取文件、搜索代码，再决定改哪里，而不是只处理你粘贴的片段。
- **多端可用**：终端、IDE、桌面、网页、Slack、GitHub 都能用同一套能力。
- **插件与市场（Marketplace）**：插件是扩展 Claude Code 功能的包，市场是插件的目录。Anthropic 维护三个通用市场：官方（`claude-plugins-official`）、社区（`claude-community`）、演示（`claude-code-plugins`）。安装插件时在 `@` 后写市场名，例如 `/plugin install commit-commands@claude-plugins-official`。
- **数据收集**：使用过程中会收集反馈，包括使用数据（如代码被接受或拒绝）、相关对话数据，以及通过 `/bug` 命令提交的反馈。官方声明有隐私保护措施，包括对敏感信息限制保留期限、限制对用户会话数据的访问，以及明确不将反馈用于模型训练。

## 环境与前置依赖

| 项目 | 要求 |
| --- | --- |
| 操作系统 | macOS、Linux、Windows 均可用 |
| Node.js | 官方仓库徽章标注 Node.js 18+ |
| Windows 建议 | 推荐安装 Git for Windows，以便 Claude Code 使用 Bash 工具；未安装时改用 PowerShell 作为 shell 工具 |
| 账号 | 多数形态需要 Claude 订阅或 Anthropic Console 账号；终端 CLI、VS Code、JetBrains 也支持第三方提供商 |
| 网络 | 安装脚本需从官方地址下载 |

> 官方已明确：**通过 npm 安装的方式已废弃**，请使用下面推荐的安装方式。

## 在 Windows 上安装

以下命令在 **Windows PowerShell** 中执行。判断自己是否在 PowerShell：提示符形如 `PS C:\`；如果看到 `C:\` 而没有 `PS`，说明你在 CMD。

1. 打开 PowerShell，执行官方推荐的原生安装脚本：`irm https://claude.ai/install.ps1 | iex`
2. 或者使用 WinGet 安装：`winget install Anthropic.ClaudeCode`
3. 安装命令执行期间不会显示下载进度，属正常现象。
4. 安装完成后，**新开一个终端窗口**，运行 `claude --version`。能打印出版本号即表示安装成功。
5. 如果提示 `claude` 找不到或无法识别，说明安装目录还没加入 PATH，需要按官方「Fix your PATH」说明处理。

> 常见报错对照：出现 `The token '&&' is not a valid statement separator`，说明你在 PowerShell 而不是 CMD；出现 `'irm' is not recognized as an internal or external command`，说明你在 CMD 而不是 PowerShell。

原生安装会在后台自动更新，保持最新版本。

## 快速上手

1. 在终端中进入你的 Spring 项目目录，例如 `cd D:\workspace\my-spring-service`。
2. 运行 `claude` 启动会话。
3. 用自然语言描述任务，例如让它解释某个 Service 的调用链、为某个 Controller 补集成测试、或排查一个并发问题。
4. 需要反馈问题时，在会话内使用 `/bug` 命令，或到 GitHub 仓库提 issue。

## 如何确认安装与运行成功

- 运行 `claude --version`，能输出版本号即安装成功。
- 在项目目录运行 `claude` 后能进入交互会话，即运行正常。
- 若命令未找到，优先检查 PATH；若安装脚本报语法错误、403 等，按官方「Troubleshoot installation」对照错误处理。

## 融入 Trae Work 与 Java/Spring 工作流

需要说明的是：**官方未提供与 Trae Work 的集成方式**，也没有公开的 Java/Spring SDK 或 MCP 服务接入路径。因此现实可行的做法是把它当作**独立的终端 CLI**，与 Trae Work 并行使用：

1. 在 Trae Work 里正常编写和调试 Spring 代码。
2. 需要跨文件重构、批量补测试、解释陌生模块时，切到 PowerShell，在项目根目录运行 `claude`。
3. 让 Claude Code 直接修改工作区文件，改完回到 Trae Work 查看 diff、运行 Maven/Gradle 构建与测试。
4. 涉及 Git 的操作（查看改动、整理提交）也可以交给它处理。

> 如果你希望以插件形式扩展能力，可在会话内用 `/plugin marketplace add <owner>/<repo>` 添加市场，再用 `/plugin install <插件名>@<市场名>` 安装插件。官方未公开说明这些插件能否被 Trae Work 直接复用。

## 局限与风险

- **许可证与费用**：多数使用形态需要 Claude 订阅或 Anthropic Console 账号，属于付费服务；具体条款见官方商业服务条款与隐私政策。
- **数据收集**：官方会收集使用数据、对话数据与反馈，虽声明不用于模型训练，但涉及代码内容，企业环境需自行评估合规性。
- **安装方式变更**：npm 安装已废弃，老教程里的 `npm install -g @anthropic-ai/claude-code` 不再推荐。
- **Windows 体验依赖 shell**：未装 Git for Windows 时会退回 PowerShell 作为 shell 工具，行为可能不同。
- **与 Trae Work 无官方集成**：无法作为 MCP 服务或 Skill 直接挂进 Trae Work，只能并行使用。

## 社区评价（来自 Hacker News 讨论）

- 关于「Claude Code 对请求做隐写标记」的讨论获得 2445 分、750 条评论。有评论认为这类反观测技术与恶意软件的手法相似，但破解单个指纹技术并不难；难点在于持续对抗所有技巧，且未打补丁的版本本身会成为指纹。
- 关于「Claude Code 源码通过 NPM 注册表中的 map 文件泄露」的讨论获得 2095 分、1022 条评论，热度极高，反映出社区对其实现细节的强烈关注。
- 关于 Claude 3.7 Sonnet 与 Claude Code 的发布讨论获得 2127 分、963 条评论。

## 一句话结论

如果你想要一个能直接动手改代码、跑命令、处理 Git 的终端智能体，且不介意付费与数据收集条款，Claude Code 值得第一时间试用；但它在 Windows 上目前只能作为独立 CLI 与 Trae Work 并行，别指望无缝嵌入。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 项目，已经安装了 Claude Code 终端 CLI，希望用它提升日常开发效率。

目标：请作为我的结对编程助手，帮我在当前 Spring 项目里完成一次小范围但完整的改造。

具体要求：
1. 先阅读项目结构，告诉我这是一个什么类型的 Spring 项目（Maven 还是 Gradle、有哪些主要模块、入口类和配置文件在哪）。
2. 找出一个 Controller 及其对应的 Service，解释这条调用链的职责划分，指出其中可能存在的并发或事务问题。
3. 为该 Service 的核心方法补充单元测试，使用项目已有的测试框架（JUnit 5 / Mockito 优先），测试文件放在符合项目约定的目录下。
4. 所有改动请直接写入文件，并在完成后列出修改了哪些文件、每个文件改了什么。
5. 不要修改与本次任务无关的代码，不要升级依赖版本。
6. 最后给出我在 Windows PowerShell 中验证改动的命令，例如运行测试和构建的命令。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
