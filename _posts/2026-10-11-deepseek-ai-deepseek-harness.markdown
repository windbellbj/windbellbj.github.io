---
layout: post
title: "DeepSeek Harness 上手：一切皆插件的 Agent 运行壳"
subtitle: "DeepSeek 官方开源的 dsh，一条 npx 命令跑起 Web UI，Java 程序员也能先试为快"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: harness
---

- 来源：重点跟踪清单
- 仓库：https://github.com/deepseek-ai/deepseek-harness
- Stars：247391
- 语言：TypeScript
- 创建时间：2026-08-13
- 最近更新：2026-10-09
- 官方简介：DeepSeek Harness: Everything is a Plugin.

---

## 解决什么问题

DeepSeek Harness（命令名 `dsh`）是 DeepSeek AI 开源的一个 agent harness（智能体运行壳）。README 明确说明它基于 **everything-is-a-plugin**（一切皆插件）架构，并由 [Cordis](https://github.com/cordiverse/cordis) 驱动，其设计思想来自论文 _A Programming Paradigm for Spatiotemporal Composability_。

README 未提供更细粒度的能力清单、适用场景对比或与其它 harness 的差异说明，因此这里不展开推测。可以确认的是：它面向的是「运行智能体」这件事本身，并且把可扩展性放在架构核心位置。

需要特别注意的是，README 将当前阶段定义为 _developer preview_，并加粗提示 **THERE WILL BE COMPATIBILITY-BREAKING CHANGES.**（会有破坏兼容性的变更）。

## 核心概念

README 中明确出现的概念只有以下几个：

- **Agent Harness（智能体运行壳）**：README 对 `dsh` 的第一句定义就是「an open-source agent harness developed by DeepSeek AI」。
- **Everything is a Plugin（一切皆插件）**：README 用加粗强调的架构原则，说明整个 harness 的可组合方式。
- **Cordis**：底层依赖的项目，README 给出了仓库地址与对应论文标题。
- **Web UI**：`dsh web` 启动的界面，默认地址 `http://127.0.0.1:3080`。
- **dsh-plugin**：README 建议插件仓库添加的 GitHub topic，用于被发现。
- **Developer preview**：当前发布阶段，README 明确警告会有破坏性变更。

关于插件如何编写、harness 内部有哪些抽象、配置文件的格式与位置，README 未提供，需要查阅其文档站点与 `docs/` 目录。

## 前置依赖

README 中明确提到的依赖只有两项：

1. **Node.js**：README 在 npm 运行方式中写明「Install `Node.js`, then run」。README 未提供具体的最低版本号。
2. **pnpm**：仅在「Run from source」路径中出现，用于 `pnpm install`、`pnpm run build`、`pnpm dsh web`。README 未提供 pnpm 的最低版本要求。

从源码运行时还需要 `git` 用于克隆仓库，这是 README 命令中隐含的，但 README 未单独列为前置条件。

README 未提供操作系统要求。对于在 Windows 上使用 Trae Work 的 Java 程序员来说，README 未提供 Windows 专属说明或已知问题列表。

## 安装与配置

以下步骤严格按 README 给出的两条路径整理。

### 路径 A：通过 npm 直接运行（推荐先试这条）

1. 在 Windows 上安装 Node.js（README 只要求「Install Node.js」，未给出具体版本）。
2. 打开 Trae Work 内置终端（或任意终端），执行行内命令 `npx @deepseek-ai/dsh web`。
3. 该命令默认在 `http://127.0.0.1:3080` 启动 Web UI，并在本地启动时用默认浏览器打开它。
4. 如果不想自动打开浏览器，追加 `--no-open` 参数，即 `npx @deepseek-ai/dsh web --no-open`。
5. README 特别说明：SSH 启动时只会打印 host URL，因为本地转发地址由 SSH 客户端或编辑器持有。

### 路径 B：从源码运行

1. 执行 `git clone https://github.com/deepseek-ai/deepseek-harness.git`。
2. 执行 `cd deepseek-harness`。
3. 执行 `pnpm install`。
4. 执行 `pnpm run build`。README 说明这一步用于准备仓库构建产物。
5. 执行 `pnpm dsh web`。README 说明该命令直接使用已构建产物，不会重新构建。

### 开发相关（README 提及，非必需）

- `pnpm run dev:web`：在一个终端里完成构建、服务，并在源码改动时重建客户端 bundle。
- `make help`：列出 Web 与 Desktop 对应的 Make 目标。README 指出完整表格在开发指南的 application commands 章节。
- 开发入口文档为 `docs/development.md` 与 `docs/architecture.md`；面向 agent 的说明在 `AGENTS.md`。

### 如何融入 Trae Work / Java 工作流

README 未提供与 Trae Work / Java 的集成方式。README 中没有出现 MCP 服务接入、Skill 目录、SDK、HTTP API 或任何 IDE 插件相关的说明。因此：

- 不能确认它能否作为 MCP 服务被 Trae Work 调用；
- 不能确认它能否作为 Skill 放入技能目录；
- 不能确认存在 Java SDK 或可编程 HTTP 接口。

目前唯一可确认的接入形态是：在 Trae Work 的终端里以 CLI 方式运行 `npx @deepseek-ai/dsh web`，然后在浏览器中使用它启动的 Web UI。如果你的 Java/Spring 项目需要与它联动，README 未提供任何官方途径。

## 最小可用示例

下面这段指令可以直接整段复制给 Trae Work 等 AI 编程助手，用来在 Windows + Trae Work 环境下完成一次最小试用。

```text
背景：我在 Windows 上使用 Trae Work 做 Java / Spring 后端开发，本机已安装 Node.js。我想试用 DeepSeek 官方开源的 agent harness —— DeepSeek Harness（命令名 dsh，仓库 deepseek-ai/deepseek-harness）。它目前是 developer preview，README 明确警告会有破坏兼容性的变更。

目标：在不影响我现有 Java 项目的前提下，把 dsh 的 Web UI 在本机跑起来，并确认它能正常访问。

要求：
1. 先检查本机 Node.js 是否可用（例如 node -v、npm -v），把版本号告诉我；如果不可用，告诉我需要先装什么。
2. 在终端执行 npx @deepseek-ai/dsh web，并说明它默认监听 http://127.0.0.1:3080。
3. 如果浏览器自动打开失败，告诉我手动访问哪个地址；如果我不想自动打开浏览器，告诉我该加什么参数。
4. 全程只使用 README 中出现的命令，不要自行发明配置项、配置文件路径或环境变量；如果某一步 README 没有说明，直接告诉我「README 未提供」，不要猜测。
5. 最后把这次试用的步骤整理成一份简短记录，方便我以后重复执行。
```

## 验证方法

按 README 可确认的验证方式如下：

1. 执行 `npx @deepseek-ai/dsh web` 后，观察终端是否输出服务地址。
2. 在浏览器访问 `http://127.0.0.1:3080`，确认 Web UI 能打开。README 说明本地启动会自动打开默认浏览器，因此「浏览器自动弹出」本身也是一个可观察的验证信号。
3. 如果使用了 `--no-open`，则浏览器不会自动打开，需要手动访问上述地址来验证。
4. 若走源码路径，`pnpm run build` 与 `pnpm dsh web` 两条命令能正常结束、且 Web UI 可访问，即为通过。

README 未提供健康检查接口、日志位置、单元测试命令或任何自动化验证脚本。

## 风险与注意事项

- **破坏性变更**：README 用加粗大写强调 _developer preview_ 阶段 **THERE WILL BE COMPATIBILITY-BREAKING CHANGES.**，不要把它当作稳定依赖引入生产流程。
- **安全须知**：README 要求运行项目前先阅读 [safety notice](SAFETY.md)。具体内容 README 正文未展开，需自行查看该文件。
- **默认监听本地**：默认地址为 `http://127.0.0.1:3080`，README 未说明如何暴露到局域网或公网，也未提供鉴权相关说明。
- **SSH 场景差异**：README 指出 SSH 启动只打印 host URL，不会自动打开浏览器，因为本地转发地址由 SSH 客户端或编辑器持有。
- **许可证**：项目采用 MIT 许可证；第三方依赖及其许可证在 `THIRD_PARTY_NOTICES.md` 中披露。
- **反馈渠道**：README 建议通过 GitHub Discussions 提交反馈或 bug。

README 未提供数据隐私、模型调用计费、网络代理要求等方面的说明。

## 替代方案

README 未提供任何替代方案、竞品对比或迁移建议。

README 中唯一提到的相关项目是底层依赖 [Cordis](https://github.com/cordiverse/cordis)，但它是 dsh 的构建基础，而非替代品。

如需了解生态内的其它选择，README 未提供线索，建议自行检索。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
