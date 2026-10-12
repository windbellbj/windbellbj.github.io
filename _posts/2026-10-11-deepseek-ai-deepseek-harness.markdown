---
layout: post
title: "DeepSeek Harness 使用说明书：一切皆插件的开源 Agent 运行壳"
subtitle: "一条命令起本地 Web UI，模型可换、能力全靠插件拼装，Java 后端也能上手试"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - Agent Harness
news_category: harness
---

- 来源：重点跟踪清单
- 仓库：https://github.com/deepseek-ai/deepseek-harness
- Stars：247485
- 语言：TypeScript
- 创建时间：2026-08-13
- 最近更新：2026-10-09
- 官方简介：DeepSeek Harness: Everything is a Plugin.

---

> DeepSeek Harness（命令名 `dsh`）是 DeepSeek 官方开源的 Agent Harness（智能体运行壳）：它把模型适配器、工具注册表、会话日志、Agent 循环本身都做成可替换插件，让你拥有一个属于自己的编码/办公 Agent 运行时，而不是一个封闭成品。最适合想掌控 Agent 底层、愿意折腾插件、且能接受预览版频繁破坏性变更的开发者。

## 它到底是什么

DeepSeek Harness 由 DeepSeek AI 开源，基于 Cordis 的「一切皆插件（everything is a plugin）」架构构建，其设计思想来自论文《A Programming Paradigm for Spatiotemporal Composability》。项目主语言为 TypeScript，采用 MIT 许可证。

官方对 Agent 的拆解是：**Agent = Model + Harness**。模型只负责输出文本，它自己无法打开文件、执行命令或记住上一轮对话；Harness 就是包裹在模型外面的那一层——工作区、工具、权限、会话记忆，以及让工作持续推进的循环。

与 Claude Code、Codex 这类「成品 Harness」不同，dsh 的模型适配器、工具注册表、会话日志、Agent 循环全部是可替换插件，官方文档称之为「没有需要打补丁的特权内核」。

它可以作为桌面应用运行（官网提供 macOS Apple 芯片版与 Windows 64 位版下载），也可以通过代码启动为网页。

<!-- asset:blog-1 start -->
![Agent 与 Harness 的关系](/img/ai-news/deepseek-ai-deepseek-harness/blog-1.png)

*图：Agent 与 Harness 的关系*
<!-- asset:blog-1 end -->


## 能帮你做什么

官网列出的能力范围包括：

| 场景 | 具体能力 |
| --- | --- |
| 日常工作 | 整理资料、分析表格、撰写文档、制作汇报 |
| 编写代码 | 理解项目、修复问题、开发功能、运行测试 |
| 资料查证 | 搜索资料、交叉核对、给出带来源的结论 |
| 后台任务 | 运行脚本、批量处理文件、后台执行并随时查看进度 |
| 插件扩展 | 安装现有插件，或自己编写插件定制工作方式 |

官网演示中，用户用一句「帮我写一个『番茄时钟』插件」，DSH 便加载 `cordis-plugin-development` 技能、读取技能文件、查询运行时插槽、写入插件文件、调用 `plugin_manager · install_bundle` 安装并验证，全程约 5 分 24 秒完成。

## 核心概念：插件、技能与创造模式

- **插件（Plugin）**：dsh 的最小能力单元。工具、技能、界面都可以通过插件扩展。官方在 GitHub 上用 `dsh-plugin` 话题标签聚合社区插件。
- **创造模式（Creator mode）**：通过对话直接创建插件。官网演示里，DSH 会先加载 `cordis-plugin-development` 技能，再读取 `skills/cordis-plugin-development/SKILL.md`，然后动手写代码。
- **技能（Skill）**：以 `SKILL.md` 形式存在的可加载能力说明，例如插件开发技能。
- **自动化任务**：实验性插件，支持按计划触发任务。官网示例中通过 `schedule_create` 创建了「每周五 17:00（北京时间）整理本周项目记录生成周报」的定时任务。
- **开发者工具**：可查看执行轨迹与详细运行信息，排查工具调用和任务执行问题，包括时长、轮次、调用次数、系统提示词、上下文、工具参数与结果、Schema、计时等。
- **其他实验性插件**：智能体团队、自动授权审查、语音输入、终端、Agent 循环、子智能体等。

<!-- asset:blog-2 start -->
![核心概念速览](/img/ai-news/deepseek-ai-deepseek-harness/blog-2.png)

*图：核心概念速览*
<!-- asset:blog-2 end -->


## 环境与前置依赖

| 项目 | 要求 |
| --- | --- |
| Node.js | 第三方指南称需要 `^22.19 || >=24`，奇数版本（如 Node 23）无法启动 |
| 包管理器 | 从源码运行时使用 `pnpm` |
| API Key | 第三方指南称需要 DeepSeek API Key，且账户需有余额或可用额度 |
| 操作系统 | 官网提供 macOS（Apple 芯片）与 Windows（64 位）桌面端 |

> 注意：Node.js 版本要求来自第三方指南，官方仓库说明中仅写「Install Node.js」，未给出具体版本区间。

## 安装与启动

### 方式一：npx 一条命令启动（推荐先试这个）

1. 安装 Node.js。
2. 在 Windows PowerShell 中进入你想让 Agent 工作的项目目录，例如：`cd D:\work\my-spring-project`
3. 执行：`npx @deepseek-ai/dsh web`
4. 默认会在 `http://127.0.0.1:3080` 启动 Web UI，并在本地启动时自动用默认浏览器打开。
5. 如果不想自动打开浏览器，加上参数：`npx @deepseek-ai/dsh web --no-open`

> 通过 SSH 启动时，只会打印主机 URL，因为本地转发地址由 SSH 客户端或编辑器掌控。

### 方式二：从源码运行

1. 克隆仓库：`git clone https://github.com/deepseek-ai/deepseek-harness.git`
2. 进入目录：`cd deepseek-harness`
3. 安装依赖：`pnpm install`
4. 构建产物：`pnpm run build`
5. 启动 Web UI：`pnpm dsh web`

其中 `pnpm run build` 负责准备仓库产物，`pnpm dsh web` 直接使用已构建产物、不会重新构建。

### 方式三：桌面端

官网提供 macOS（Apple 芯片）与 Windows（64 位）桌面端下载。另有第三方站点提供社区维护的 DSH Desktop 打包版（内置运行时，无需单独安装系统 Node），但该站点明确声明这是社区维护的开源分发版，**不是 DeepSeek 官方产品**，升级前应检查其 GitHub Release 并备份重要配置。

### 开发调试

`pnpm run dev:web` 会在一个终端里完成构建、服务与源码改动后的客户端包重建；`make help` 会列出 Web 与 Desktop 对应的 Make 目标。

<!-- asset:code-2 start -->
```powershell
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```
<!-- asset:code-2 end -->


<!-- asset:code-1 start -->
```powershell
cd D:\work\my-spring-project
npx @deepseek-ai/dsh web
npx @deepseek-ai/dsh web --no-open
```
<!-- asset:code-1 end -->


## 如何确认启动成功

- 终端打印出本地地址，默认是 `http://127.0.0.1:3080`。
- 浏览器打开该地址后能看到 Web UI 界面（新会话、插件、自动化任务、工作区等入口）。
- 在界面里发起一次对话，能看到「已思考」「工具调用」等执行轨迹，说明 Agent 循环正常工作。

## 融入 Windows + Trae Work + Java/Spring 工作流

**官方未提供与 Trae Work / Java 的集成方式。** 官方仓库说明、官网文档中均未出现 MCP 服务接入、Skill 放入技能目录、Java SDK 或 Spring 集成相关的说明，因此不存在可照做的配置路径或命令，请勿自行编造。

目前可确认的接入形态只有两种：

1. **本地 Web UI**：在 PowerShell 中进入你的 Spring 项目目录后执行 `npx @deepseek-ai/dsh web`，让 Agent 的工作区落在该项目上，再在浏览器里与它对话。
2. **桌面端应用**：下载 Windows 64 位桌面端，直接以应用形式运行。

如果你的目标是「在 Trae Work 里用上它」，现阶段只能把 dsh 当作一个并行的独立工具使用，而不是嵌进 Trae Work 的插件体系。

## 版本与发布状态

- 官方仓库说明标注为 **developer preview（开发者预览版）**，并明确警告「**THERE WILL BE COMPATIBILITY-BREAKING CHANGES**」（将出现破坏兼容性的变更）。
- 第三方指南在 2026 年 10 月 9 日复核时称：npm 的 `latest` 与 `next` 标签均指向 `v0.2.0-rc.2`，`alpha` 标签指向 `v0.2.1-alpha.1`；该指南的安装流程最初基于 `0.1.0-rc.6` 验证。
- 第三方指南还提到，dsh 于 2026 年 8 月 13 日与 V4-Pro 一同开源，两天内 GitHub Star 数突破 10 万。

> 上述具体版本号均来自第三方指南，官方仓库说明中未列出当前版本号。

## 局限与风险

- **成熟度**：官方自述为开发者预览版，迭代迅速，兼容性会破坏。第三方指南直接建议「今天就需要生产级 API 稳定性」的用户暂缓使用。
- **许可证**：项目本身为 MIT；第三方依赖及其许可证在 `THIRD_PARTY_NOTICES.md` 中披露。
- **安全**：官方要求运行项目前先阅读安全须知（`SAFETY.md`）。
- **费用**：项目开源免费，但第三方指南称使用需要 DeepSeek API Key 且账户需有余额，模型调用本身会产生费用。
- **社区分发版风险**：第三方 DSH Desktop 为社区维护，非官方产品，升级前需备份配置。

## 社区评价（来自 Hacker News 讨论）

相关讨论帖包括《DeepSeek Harness developer preview》（747 分，314 条评论）与《DeepSeek Harness Desktop for macOS and Windows》（417 分，228 条评论）。

正面反馈集中在插件架构与桌面端体验：

- 有用户表示在 macOS 上安装后「是个猛兽」，与之前的 harness 相同但变成了点一下 Dock 就能跑的应用；所有设置与工作区都会迁移，不会丢失。该用户唯一不满的是缺少用 `cmd +` / `cmd -` 调整字号的方式，于是自己动手写插件——随后表示「让 DSH 写一个增减字号的插件，它交付了；又让它写一个在提问和任务完成时响铃的插件，同样完美交付」，并称赞「同一套插件架构，由同一个 AI 来扩展」。
- 另一位用户分享：让 DSH 做一个新闻聚合器，它用 RSS 源从 30 个新闻站点搭出了一个相当不错的应用，花费不到 50 美分。

也有质疑与观望的声音：

- 有评论直言「如果它不比 omp 更好我就不试」。
- 有人追问「它最好的功能是什么」「相比其他 harness 好在哪、有什么是别人做不到的」，并认为「所有 LLM 在某种程度上表现都差不多，区别在于个人偏好、token 成本和可定制性」。

## 快速上手建议

1. 先确认 Node 版本落在 `^22.19 || >=24` 区间内，用 `node -v` 检查。
2. 准备 DeepSeek API Key 并确认账户有余额。
3. 在 PowerShell 里 `cd` 到你的 Spring 项目目录，执行 `npx @deepseek-ai/dsh web`。
4. 浏览器打开 `http://127.0.0.1:3080`，先让它读一遍项目结构、跑一次测试，感受工具调用轨迹。
5. 想扩展能力时，直接在对话里描述需求，让它以插件形式实现并安装。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 后端项目，项目根目录是 D:\work\my-spring-project，使用 Maven 构建，JDK 17。

目标：请作为 DeepSeek Harness（dsh）帮我完成一次完整的项目体检，并给出可执行的改进清单。

具体要求：
1. 先读取项目根目录结构，识别出这是一个 Spring Boot 多模块还是单模块项目，列出所有 pom.xml 的位置。
2. 阅读主启动类、application.yml / application.properties，总结当前配置了哪些关键项（端口、数据源、日志级别、profile 划分）。
3. 扫描所有 Controller，输出一张表：HTTP 方法、路径、入参类型、返回类型、是否有参数校验注解。
4. 找出所有 Service 层里直接抛 RuntimeException 或未做空值判断的位置，按文件路径 + 行号列出。
5. 检查是否存在硬编码的密钥、密码、连接串，若有请指出文件与行号，但不要在输出里回显密钥原文。
6. 运行 mvn -q -DskipTests compile 验证当前代码能否编译通过，把失败信息原样贴出来。
7. 最后给出一个按优先级排序的改进清单，每条包含：问题、影响、建议改法、涉及文件。

输出格式：用 Markdown，先给一段不超过 200 字的总体结论，再按上面的编号分节展开。所有涉及文件的地方都写成 相对路径:行号 的形式，方便我直接跳转。
```

把上面这段指令整段复制给 dsh，就能在几分钟内得到一份针对你 Spring 项目的体检报告。

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
