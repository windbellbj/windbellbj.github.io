---
layout: post
title: "Gemini CLI 上手：把 Gemini 塞进终端"
subtitle: "10 万星开源终端 AI Agent，免费额度 + MCP 扩展，Java 程序员也能马上试"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: agent-cli
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/google-gemini/gemini-cli
- Stars：107286
- 语言：TypeScript
- 创建时间：2025-04-17
- 最近更新：2026-10-10
- 官方简介：An open-source AI agent that brings the power of Gemini directly into your terminal.

---

## 解决什么问题

Gemini CLI 是 Google 开源的 AI agent，官方定位是「把 Gemini 的能力直接带进你的终端」，提供从 prompt 到模型的最直接路径（README 原文：lightweight access to Gemini, giving you the most direct path from your prompt to our model）。

README 列出的典型用途包括：

- 查询和编辑大型代码库（Query and edit large codebases）
- 用多模态能力从 PDF、图片或草图生成新应用
- 用自然语言调试和排查问题
- 自动化操作任务，例如查询 pull request、处理复杂的 rebase
- 通过 MCP server 接入新能力
- 在脚本中非交互式运行，实现工作流自动化
- 用内置 Google Search grounding 获取实时信息
- 会话 checkpointing，保存并恢复复杂会话
- 用自定义上下文文件 GEMINI.md 为项目定制行为

对 Java 后端程序员来说，它对应的是「终端里的编码 Agent」这一形态：不依赖 IDE 图形界面，直接在命令行里对 Spring 项目提问、改代码、跑命令。

## 核心概念

- **Terminal-first**：README 明确写着 Designed for developers who live in the command line，交互入口就是终端里的 `gemini` 命令。
- **Gemini 3 模型与 1M token 上下文**：README 在 Why Gemini CLI 与 OAuth 认证部分都提到 Gemini 3 models 与 1M token context window。
- **内置工具（Built-in tools）**：Google Search grounding、文件操作、shell 命令、web fetching。
- **MCP（Model Context Protocol）支持**：README 把 Extensible 列为特性之一，并说明可在 `~/.gemini/settings.json` 中配置 MCP server 来扩展自定义工具。
- **GEMINI.md 上下文文件**：README 的 Core Features 中列出 Context Files (GEMINI.md)，用于给 Gemini CLI 提供持久上下文。
- **Checkpointing**：保存与恢复会话。
- **非交互模式（Headless / Scripting）**：通过 `-p` 与 `--output-format` 在脚本中使用。
- **认证方式三选一**：Sign in with Google（OAuth）、Gemini API Key、Vertex AI。
- **发布通道**：preview、stable（latest）、nightly 三个 tag。
- **GitHub 集成**：通过 Gemini CLI GitHub Action 做 PR 评审、Issue 分诊、在 issue/PR 中 @gemini-cli 求助、自定义工作流。

## 前置依赖

README 未提供完整的系统规格要求，只说明「See Gemini CLI installation, execution, and releases for recommended system specifications and a detailed installation guide」，即推荐配置与详细安装指南在官方文档站点，README 本身未列出。

从 README 给出的安装方式可以推断出的依赖：

- Node.js / npm 环境（README 提供 `npx @google/gemini-cli` 与 `npm install -g @google/gemini-cli` 两种方式）
- 或者 Homebrew（macOS/Linux）、MacPorts（macOS）、Anaconda（受限环境）
- 一种认证凭据：Google 账号（OAuth）、Gemini API Key，或 Vertex AI 的 API Key + 项目配置

README 未提供 Windows 专属的安装说明，也未提供 Java、JDK、Maven、Gradle 相关的任何前置要求。

## 安装与配置

以下步骤按「Windows + Trae Work + Java/Spring 技术栈」的读者视角组织，命令均以行内代码给出。

**第 1 步：准备 Node.js 环境**

README 的安装方式以 npm 为主，因此先在 Windows 上准备可用的 Node.js 与 npm。README 未提供 Windows 上安装 Node.js 的具体步骤，请按 Node.js 官方方式安装。

**第 2 步：选择一种安装方式**

README 给出的可选方式（原文命令）：

1. 免安装直接运行：`npx @google/gemini-cli`
2. 全局安装（npm）：`npm install -g @google/gemini-cli`
3. Homebrew（macOS/Linux）：`brew install gemini-cli`
4. MacPorts（macOS）：`sudo port install gemini-cli`
5. Anaconda（受限环境）：先 `conda create -y -n gemini_env -c conda-forge nodejs`，再 `conda activate gemini_env`，然后 `npm install -g @google/gemini-cli`

对 Windows 用户而言，README 中可直接对应的是第 1、2 种（npx 与 npm 全局安装）；Homebrew 与 MacPorts 是 macOS/Linux 方案，Anaconda 方案 README 标注为 for restricted environments。

**第 3 步：选择发布通道（可选）**

README 说明三个通道：

- Preview：每周二 UTC 23:59 发布，未完全验证，安装用 `npm install -g @google/gemini-cli@preview`
- Stable：每周二 UTC 20:00 发布，是上周 preview 的完整晋升加修复，安装用 `npm install -g @google/gemini-cli@latest`
- Nightly：每天 UTC 00:00 发布，来自 main 分支，安装用 `npm install -g @google/gemini-cli@nightly`

**第 4 步：完成认证**

README 给出三种方式：

1. Sign in with Google（OAuth）：先运行 `gemini`，然后选择 Sign in with Google，按提示在浏览器完成认证。README 说明该方式免费额度为 60 requests/min 与 1,000 requests/day，并支持 Gemini 3 模型与 1M token 上下文。若使用组织提供的付费 Code Assist License，需要先设置 Google Cloud Project：`export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"`，再运行 `gemini`。
2. Gemini API Key：从 `https://aistudio.google.com/apikey` 获取 key，设置 `export GEMINI_API_KEY="YOUR_API_KEY"`，再运行 `gemini`。README 说明该方式免费额度为每天 1000 requests（Gemini 3，flash 与 pro 混合）。
3. Vertex AI：设置 `export GOOGLE_API_KEY="YOUR_API_KEY"` 与 `export GOOGLE_GENAI_USE_VERTEXAI=true`，再运行 `gemini`。README 说明该方式面向企业团队与生产负载。

注意：README 中的认证示例使用 `export` 语法，属于类 Unix shell 写法；README 未提供 Windows 下设置环境变量的具体写法。

**第 5 步：配置 MCP server（可选）**

README 说明在 `~/.gemini/settings.json` 中配置 MCP server 以扩展自定义工具，并给出使用形态示例：`@github List my open pull requests`、`@slack Send a summary of today's commits to #dev channel`、`@database Run a query to find inactive users`。具体配置字段与结构，README 指向 MCP Server Integration 指南，README 正文未提供。

**第 6 步：融入 Trae Work 日常工作流**

README 未提供与 Trae Work / Java 的集成方式。README 中与 IDE 相关的内容只有 IDE Integration（VS Code companion）这一条文档链接，未提及 Trae Work。

因此，在 Trae Work 中可考虑的落地方式只能基于 README 已确认的事实来推断：Gemini CLI 是终端优先的工具，可在 Trae Work 的终端中作为 CLI 调用；README 提到它支持 MCP 与自定义扩展，但 README 未提供把它作为 MCP 服务接入 Trae Work 的配置方式，也未提供在 Java/Spring 项目中通过 SDK 或 HTTP 集成的说明。

## 最小可用示例

把下面这段指令整段复制给 Trae Work 等 AI 编程助手，让它帮你在 Windows 上完成 Gemini CLI 的安装、认证与一次针对 Spring 项目的试用。

```text
背景：我在 Windows 上使用 Trae Work 开发，技术栈是 Java / Spring Boot，项目用 Maven 构建。我想试用开源的 Gemini CLI（仓库 google-gemini/gemini-cli），它是一个终端优先的 AI agent。

目标：在不破坏我现有环境的前提下，完成 Gemini CLI 的安装、认证，并让它对我当前的 Spring Boot 项目做一次只读的代码理解演示。

要求：
1. 先检查我机器上是否已有可用的 Node.js 与 npm，并告诉我版本；如果没有，给出 Windows 上的安装建议。
2. 按官方 README 的方式安装 Gemini CLI，优先使用 npm 全局安装（npm install -g @google/gemini-cli）；如果我希望免安装试用，则改用 npx @google/gemini-cli。不要使用 Homebrew 或 MacPorts，因为我在 Windows 上。
3. 安装完成后，指导我完成认证。请把 README 中的三种方式（Sign in with Google、Gemini API Key、Vertex AI）各自的适用场景和免费额度讲清楚，并告诉我 Windows 下设置环境变量的正确写法（README 只给了 export 写法，请说明 Windows 的对应做法）。
4. 认证完成后，在当前 Spring Boot 项目根目录启动 Gemini CLI，并让它执行一次只读任务：总结这个项目的模块结构、主要 Controller / Service / Repository 分层，以及 application.yml 中的关键配置项。明确要求它不要修改任何文件。
5. 演示非交互模式：用 gemini -p "..." 的形式对项目提一个问题，并说明 --output-format json 与 --output-format stream-json 的区别与适用场景。
6. 最后告诉我：如何在项目里放置 GEMINI.md 来提供持久上下文，以及 README 中提到的 MCP server 配置在 ~/.gemini/settings.json 中的用途。如果 README 没有给出具体配置字段，请直接说明「README 未提供」，不要编造。
7. 全程只使用 README 中出现的命令与参数，不要引入 README 未提及的第三方工具或配置路径。
```

## 验证方法

按 README 提供的信息，可以用以下步骤确认安装与运行是否正常：

1. 安装完成后，在终端运行 `gemini`，确认能进入交互界面。README 的 Getting Started 部分把 `gemini` 作为在当前目录启动的方式。
2. 验证多目录支持：运行 `gemini --include-directories ../lib,../docs`，确认可以同时纳入多个目录。
3. 验证指定模型：运行 `gemini -m gemini-2.5-flash`，确认可以切换模型。
4. 验证非交互模式：运行 `gemini -p "Explain the architecture of this codebase"`，确认能返回一段文本回答。
5. 验证结构化输出：运行 `gemini -p "Explain the architecture of this codebase" --output-format json`，确认返回结构化 JSON。
6. 验证流式输出：运行 `gemini -p "Run tests and deploy" --output-format stream-json`，确认返回按行分隔的 JSON 事件流。README 说明该模式适用于监控长时间运行的操作。
7. 验证认证额度：README 说明 Sign in with Google 方式为 60 requests/min 与 1,000 requests/day，Gemini API Key 方式为每天 1000 requests，可据此判断是否触达限额。
8. 遇到问题时，README 建议使用 `/bug` 命令直接在 CLI 中报告问题，并指向 Troubleshooting Guide 与 FAQ。

README 未提供针对 Windows 的专门验证步骤，也未提供 Java/Spring 项目的验证用例。

## 风险与注意事项

- **发布通道风险**：README 明确说明 preview 版本「will not have been fully vetted and may contain regressions or other outstanding issues」，nightly 版本「should be assumed there are pending validations and issues」。生产或重要项目上建议使用 stable（latest）。
- **认证与配额**：免费额度与条款 README 指向 Google Cloud 的 quotas 文档；README 未在正文中给出完整的配额与计费细节。
- **环境变量写法**：README 的认证示例使用 `export`，属于类 Unix 写法，README 未提供 Windows 对应写法，Windows 用户需要自行处理。
- **MCP 配置细节缺失**：README 只说明在 `~/.gemini/settings.json` 中配置 MCP server，未给出字段结构，需查阅官方 MCP Server Integration 指南。
- **IDE 集成范围**：README 的 IDE Integration 只提到 VS Code companion，未提及 Trae Work，也未提供与 Java 项目的 SDK/HTTP 集成方式。
- **安全相关**：README 在 Advanced Topics 中列出 Sandboxing & Security、Trusted Folders、Enterprise Guide、Telemetry & Monitoring，说明存在沙箱、可信目录、企业部署与遥测等机制，但 README 正文未展开具体策略。
- **许可证**：Apache License 2.0。
- **卸载**：README 指向 Uninstall Guide，正文未给出卸载命令。

## 替代方案

README 未提供与其他工具的对比，也未列出替代方案。

README 中可作为「互补而非替代」参考的相关项目只有：

- **Gemini CLI GitHub Action**（google-github-actions/run-gemini-cli）：把 Gemini CLI 集成进 GitHub 工作流，用于 PR 评审、Issue 分诊、按需协助与自定义工作流。
- **MCP server 生态**：README 提到可用 MCP server 连接新能力，并举例 media generation with Imagen、Veo 或 Lyria（指向 GoogleCloudPlatform/vertex-ai-creative-studio 的 mcp-genmedia 实验）。
- **官方学习资源**：README 提供 DeepLearning.AI 上的免费课程 Free Course，以及 Official Roadmap、Changelog、NPM Package、GitHub Issues、Security Advisories 等链接。

除上述内容外，README 未提供其他替代方案的说明。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
