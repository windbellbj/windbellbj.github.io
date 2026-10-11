---
layout: post
title: "OpenCode 开源编码 Agent 上手：终端里的 AI 结对程序员"
subtitle: "212k Star 的开源编码 Agent，Windows 用 Scoop 一条命令装好，Tab 切换 build/plan"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: agent-cli
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/anomalyco/opencode
- Stars：212684
- 语言：TypeScript
- 创建时间：2025-04-30
- 最近更新：2026-10-11
- 官方简介：The open source coding agent.

---

## 解决什么问题

OpenCode 的官方定位是「The open source AI coding agent」（开源 AI 编码智能体）。README 给出的核心能力围绕「编码智能体」展开：它提供一个终端 UI（README 中展示了 OpenCode Terminal UI 截图），内置可切换的智能体，用于开发工作与代码分析。

从 README 能确认它解决的问题域是：让开发者在终端里与一个具备完整开发权限的 AI 智能体协作写代码，同时提供一个只读的规划智能体用于探索陌生代码库、规划改动。README 未提供更细的能力清单（例如具体支持哪些语言、是否支持多文件重构等），这些内容 README 未提供。

## 核心概念

README 明确给出的概念只有「Agents（智能体）」这一组：

- **build**：默认智能体，拥有完整访问权限，用于开发工作。
- **plan**：只读智能体，用于分析和代码探索。默认拒绝文件编辑；运行 bash 命令前会请求许可；适合探索不熟悉的代码库或规划改动。
- **general**：一个子智能体（subagent），用于复杂搜索和多步骤任务。它由内部使用，也可以在消息中用 `@general` 调用。

切换方式：使用 `Tab` 键在内置智能体之间切换。

此外 README 提到 OpenCode 有配置文件与文档站点（opencode.ai/docs），但 README 正文未展开配置项细节。

## 前置依赖

README 未提供系统要求、Node 版本要求、运行时依赖等前置条件说明。README 仅提示：安装前请移除 0.1.x 之前的旧版本。

从安装方式可以推断（README 事实层面）：它提供 npm 包 `opencode-ai`，也提供 Scoop、Chocolatey、Homebrew、pacman、paru、mise、nix 等包管理器安装渠道，以及一个 curl 安装脚本。README 未提供各渠道对应的最低环境版本。

## 安装与配置

以下步骤按「Windows + Java 后端开发者」的视角组织。所有命令请在你的终端中逐条执行。

**第 1 步：清理旧版本**

README 的 TIP 明确要求：安装前移除 0.1.x 之前的旧版本。如果你之前装过更早的版本，先卸载。

**第 2 步：选择一种安装方式（Windows）**

README 给出的 Windows 渠道有两个：

1. Scoop：`scoop install opencode`
2. Chocolatey：`choco install opencode`

通用渠道（README 列出，跨平台）：

1. npm：`npm i -g opencode-ai@latest`（README 注明也可用 bun / pnpm / yarn）
2. mise：`mise use -g opencode`
3. nix：`nix run nixpkgs#opencode`，或 `github:anomalyco/opencode` 获取最新 dev 分支
4. 安装脚本：`curl -fsSL https://opencode.ai/install | bash`（README 标注为 YOLO 方式）

**第 3 步：安装脚本的安装目录（仅当你用 curl 脚本时相关）**

README 说明安装脚本按以下优先级决定安装路径：

1. `$OPENCODE_INSTALL_DIR` —— 自定义安装目录
2. `$XDG_BIN_DIR` —— 符合 XDG Base Directory 规范的路径
3. `$HOME/bin` —— 标准用户二进制目录（若存在或可创建）
4. `$HOME/.opencode/bin` —— 默认兜底路径

README 给出的示例是：`OPENCODE_INSTALL_DIR=/usr/local/bin curl -fsSL https://opencode.ai/install | bash`，以及 `XDG_BIN_DIR=$HOME/.local/bin curl -fsSL https://opencode.ai/install | bash`。

**第 4 步：可选安装桌面应用（BETA）**

README 说明 OpenCode 也提供桌面应用，可从 releases 页面或 opencode.ai/download 下载。Windows 对应文件名为 `opencode-desktop-windows-x64.exe`。Windows 上也可用 Scoop 安装：`scoop bucket add extras; scoop install extras/opencode-desktop`。

**第 5 步：融入 Trae Work 日常工作流**

README 未提供与 Trae Work / Java 的集成方式。README 中没有提到 MCP 服务接入、Skill 技能目录、SDK 或 HTTP 集成等任何与 Trae Work 或 Java/Spring 项目对接的说明。因此：

- 不要假设存在 MCP 配置路径或 Skill 目录约定，README 未提供。
- 不要假设存在 Java SDK 或 HTTP API，README 未提供。
- 从 README 可确认的唯一使用形态是：它是一个在终端中运行的编码智能体（含终端 UI），因此现实可行的做法是在 Trae Work 的内置终端里把它当作一个 CLI 工具调用，与你的 Java 项目目录配合使用。这一「在终端中调用」的形态来自 README 对 Terminal UI 的展示，但 README 未明确描述与 Trae Work 终端的组合用法。

**第 6 步：配置**

README 未提供具体配置项、配置文件路径或配置示例，仅指向文档站点 opencode.ai/docs。请以该文档为准，不要凭猜测创建配置文件。

## 最小可用示例

下面这段指令可以直接整段复制给 Trae Work 等 AI 编程助手，用于在你的 Java 项目里试用 OpenCode。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring 后端项目，已经通过 Scoop 安装了 OpenCode（scoop install opencode），想先小范围试用它，而不是一上来就让它改我的生产代码。

目标：请帮我在当前 Spring 项目里完成一次「只读探索 + 小改动」的 OpenCode 试用。

要求：
1. 先告诉我如何在当前项目根目录启动 OpenCode，以及如何用 Tab 键在 build 和 plan 两个内置智能体之间切换。
2. 建议我先用 plan 智能体（只读、默认拒绝文件编辑、运行 bash 前会请求许可）来梳理这个项目的模块结构、主要 Controller/Service 分层和依赖注入方式，并说明为什么这一步适合用 plan 而不是 build。
3. 再给出一个适合用 build 智能体（默认、完整访问权限）完成的最小改动任务，例如给某个已有接口补充参数校验或补一段单元测试，并说明改动范围要控制在多小。
4. 说明在什么场景下应该在消息里用 @general 调用 general 子智能体（复杂搜索、多步骤任务），并给一个针对我这个 Java 项目的具体例子。
5. 如果 OpenCode 需要任何配置才能在我的项目里正常工作，请只引用 opencode.ai/docs 上的官方说明；如果文档里没有写，就直接告诉我「README 未提供」，不要编造配置路径或命令。
```

## 验证方法

README 未提供官方的验证步骤或自检命令。可执行的验证只能基于 README 已确认的事实：

1. 安装完成后，确认 `opencode` 命令在你的终端中可用（这是安装成功的最直接体现；README 未给出具体的版本查询命令）。
2. 启动后确认能看到 README 中展示的 OpenCode Terminal UI 界面。
3. 按 `Tab` 键，确认可以在 **build** 与 **plan** 两个内置智能体之间切换。
4. 切到 **plan** 智能体，尝试让它分析代码；按 README 描述，它应当默认拒绝文件编辑，并在运行 bash 命令前请求许可。
5. 在消息中输入 `@general`，确认可以调用 general 子智能体。

以上第 3、4、5 条直接对应 README 中对 Agents 的描述。除此之外的验证方式 README 未提供。

## 风险与注意事项

- **旧版本冲突**：README 明确提示，安装前请移除 0.1.x 之前的旧版本。
- **curl 安装脚本的风险**：README 把 `curl -fsSL https://opencode.ai/install | bash` 标注为「YOLO」，即直接把远程脚本管道给 shell 执行。在 Windows 上更推荐 README 列出的 Scoop / Chocolatey 渠道。
- **权限模型差异**：build 是完整访问权限的默认智能体，plan 是只读的。README 明确 plan 默认拒绝文件编辑、运行 bash 前请求许可。在真实项目里应优先用 plan 做探索，避免误改。
- **桌面应用为 BETA**：README 明确标注 Desktop App 为 BETA。
- **命名与归属**：README 特别声明，如果项目名里含「opencode」（如 opencode-dashboard、opencode-mobile），需在 README 中注明并非 OpenCode 团队构建、与其无关联。选型时注意区分同名第三方项目。
- **集成方式缺失**：README 未提供与 Trae Work、Java、Spring 的任何集成方式，也未提供 MCP、Skill、SDK、HTTP 相关说明。请勿自行假设。
- **配置细节缺失**：README 未提供配置文件格式与路径，仅指向 opencode.ai/docs。

## 替代方案

README 未提供任何替代方案、竞品对比或迁移路径。README 中提到的其他内容仅为：多语言 README（含简体中文 README.zh.md）、Discord 社区、X.com 账号、贡献指南 CONTRIBUTING.md，以及文档站点 opencode.ai/docs。这些都不是替代方案。

如需了解同类工具，README 未提供相关信息。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
