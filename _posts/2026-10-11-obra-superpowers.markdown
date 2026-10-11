---
layout: post
title: "Superpowers 使用说明：给编码 Agent 装上软件开发方法论"
subtitle: "一套可组合的 Agent 技能框架，让 AI 先想清楚再写代码，强制 TDD 与代码评审"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI技能
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/obra/superpowers
- Stars：297701
- 语言：Shell
- 创建时间：2025-10-09
- 最近更新：2026-10-10
- 官方简介：An agentic skills framework & software development methodology that works.

---

> Superpowers 是一套面向编码 Agent 的「技能框架 + 软件开发方法论」：它让 AI 在动手写代码前先做需求澄清与设计，再按计划分任务实现，并强制走 TDD 与代码评审。最适合已经在用 Claude Code、Cursor、Codex、Gemini CLI 等编码 Agent，且希望把「先设计、后编码、有测试、有评审」变成默认工作方式的开发者。

## 它到底解决什么问题

多数编码 Agent 的通病是：一看到需求就急着写代码，跳过需求澄清、跳过设计、跳过测试，写出来的东西看着能跑，但结构混乱、缺少验证。Superpowers 的思路是把一整套工程纪律做成**可组合的技能（skills）**，并配上一段引导指令，确保 Agent 在合适的时机自动加载这些技能。

官方对它的定位是「a complete software development methodology for your coding agents」，即一套完整的软件开发方法论，而不只是一个提示词集合。

它主要覆盖这些场景：

| 场景 | 对应技能 | 作用 |
| --- | --- | --- |
| 需求还没想清楚 | `brainstorming` | 通过提问把真实意图问出来，再复述给你确认 |
| 需要隔离开发环境 | `using-git-worktrees` | 在新分支上建独立工作区，跑项目初始化，确认测试基线干净 |
| 需要可执行的实施计划 | `writing-plans` | 把工作拆成 2–5 分钟一个的小任务，每个任务带确切文件路径、完整代码、验证步骤 |
| 计划要落地 | `subagent-driven-development` / `executing-plans` | 前者每个任务派一个新子 Agent 并在之后评审（最彻底），后者在当前会话内逐任务实现、最后整体评审一次（最省成本） |
| 保证代码质量 | `test-driven-development` | 强制 RED-GREEN-REFACTOR：先写会失败的测试，看它失败，写最小实现，看它通过，提交 |
| 任务间把关 | `requesting-code-review` | 对照计划评审，按严重程度报告问题，严重问题阻塞推进 |
| 收尾 | `finishing-a-development-branch` | 验证测试，给出合并 / 提 PR / 保留 / 丢弃选项，清理工作区 |

此外还有调试向的 `systematic-debugging`（四阶段根因流程）、`verification-before-completion`（确认真的修好了）、`diagnosing-superpowers`（排查某次会话里技能为什么没按预期触发），以及元技能 `writing-skills`（按最佳实践写新技能）和 `using-superpowers`（技能系统入门）。

## 工作原理：技能是自动触发的

Superpowers 的核心机制有两层：

1. **技能库**：每个技能是一份结构化的操作说明，包含触发条件、步骤、检查清单。
2. **引导注入**：通过各 harness 的启动钩子（如 `SessionStart`）注入 `using-superpowers` 引导，让 Agent 在会话开始时就意识到「有技能可用，且该用就必须用」。

`using-superpowers` 的措辞相当强硬：如果某个技能适用于当前任务，Agent 没有选择余地，必须先调用相关技能再做出任何响应或动作——包括澄清性提问、翻代码库、看文件。官方同时说明，如果调用后发现不适用，可以不用。

官方强调这些是**强制工作流，不是建议**：Agent 在执行任何任务前都会检查是否有相关技能。

## 环境与前置依赖

- **一个受支持的编码 Agent / harness**：官方列出了 Claude Code、Antigravity、Codex App、Codex CLI、Cursor、Devin CLI、Factory Droid、Gemini CLI、GitHub Copilot CLI、Grok Build CLI、Kimi Code、OpenCode、Pi、Qwen Code、Hermes Agent、Muse。
- **每个 harness 需单独安装**：官方明确说明，如果你用多个 harness，需要为每一个分别安装 Superpowers。
- **Git**：工作流中涉及 git worktree、分支与提交，需要可用的 Git 环境。
- **主语言为 Shell**，仓库创建于 2025-10-09，最近更新于 2026-10-10。

> 注意：官方安装说明中**没有出现 Trae Work**，也没有提供 Java / Spring 专用的 SDK 或 HTTP 集成方式。也就是说，官方未提供与 Trae Work / Java 的集成方式。

## 安装与配置

### 通用原则

安装方式按 harness 不同而不同，没有统一的「一条命令装所有」。下面按官方列出的方式给出。由于官方未提供 Trae Work 的接入路径，Windows + Trae Work 用户请参考后文「在 Trae Work 工作流中的现实做法」。

### Claude Code

官方提供两条路径。

**路径一：Anthropic 官方插件市场**

1. 在 Claude Code 中执行 `/plugin install superpowers@claude-plugins-official`。

**路径二：Superpowers 自己的市场**

1. 注册市场：`/plugin marketplace add obra/superpowers-marketplace`
2. 安装插件：`/plugin install superpowers@superpowers-marketplace`

### 其他 harness 的安装命令

| Harness | 安装方式 |
| --- | --- |
| Antigravity | `agy plugin install https://github.com/obra/superpowers`，重复执行同一命令即可更新 |
| Codex App | 侧边栏点 Plugins，在 Coding 分类找到 Superpowers，点 `+` 按提示操作 |
| Codex CLI | 打开 `/plugins`，搜索 `superpowers`，选择 `Install Plugin` |
| Cursor | Agent 聊天中执行 `/add-plugin superpowers`，或在插件市场搜索 superpowers |
| Devin CLI | `devin plugins install obra/superpowers`，更新用 `devin plugins update superpowers` |
| Factory Droid | 先 `droid plugin marketplace add https://github.com/obra/superpowers`，再 `droid plugin install superpowers@superpowers` |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers`，更新用 `gemini extensions update superpowers` |
| GitHub Copilot CLI | 先 `copilot plugin marketplace add obra/superpowers-marketplace`，再 `copilot plugin install superpowers@superpowers-marketplace` |
| Grok Build CLI | `grok plugin install superpowers@xai-official --trust`，或在 TUI 里用 `/marketplace` 搜索安装 |
| Kimi Code | 打开 `/plugins`，进入 `Marketplace` > `Superpowers` 安装；或 `/plugins install https://github.com/obra/superpowers` |
| OpenCode | 让 OpenCode 执行：`Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md` |
| Pi | `pi install git:github.com/obra/superpowers`；本地开发可 `pi -e /path/to/superpowers` |
| Qwen Code | `qwen extensions install obra/superpowers`，提示时选 `superpowers`；更新用 `qwen extensions update superpowers` |
| Hermes Agent | `hermes plugins install obra/superpowers --enable`，安装后重启活动会话 |
| Muse | 本地检出后 `muse plugins install ./` 再 `muse plugins approve superpowers`；或克隆后 `muse plugins install ./superpowers` 再 `muse plugins approve superpowers` |

### 在 Trae Work 工作流中的现实做法

官方未提供与 Trae Work / Java 的集成方式，因此没有可直接照抄的配置路径或命令。可以确认的是：Superpowers 的形态是「技能包 + 引导注入」，依赖 harness 自身的插件/技能机制与启动钩子。在官方补齐 Trae Work 支持之前，可行的做法是把它当作**方法论参考**，把其中的工作流（先 brainstorming 澄清需求、再写计划、再 TDD、再评审）手动搬进你在 Trae Work 里的日常习惯。

> 请勿自行编造 Trae Work 的插件目录或配置文件名去「接入」Superpowers，官方没有公开这类路径。

## 快速上手

以 Claude Code 为例（其他 harness 安装后流程类似）：

1. 按上文对应命令安装插件。
2. 新开一个会话，直接描述你要做的东西，例如「我想给 Spring Boot 项目加一个订单导出接口」。
3. 观察 Agent 是否先触发 `brainstorming`：它应该先问你真实目标，而不是直接写代码。
4. 需求澄清后，它会分块把设计复述给你确认。
5. 你确认设计后，它生成实施计划，把工作拆成 2–5 分钟的小任务。
6. 你说「go」，它进入 `subagent-driven-development` 或 `executing-plans`，逐任务实现并评审。官方提到，Agent 一次自主工作几个小时而不偏离计划并不罕见。
7. 任务完成后触发 `finishing-a-development-branch`，验证测试并给出合并 / PR / 保留 / 丢弃选项。

官方描述的完整基础工作流顺序是：`brainstorming` → `using-git-worktrees` → `writing-plans` → `subagent-driven-development` 或 `executing-plans` → `test-driven-development` → `requesting-code-review` → `finishing-a-development-branch`。

## 如何确认安装成功

官方在 Muse 一节给出了一个可复用的验证方法：**新开一个会话，发送 `Let's make a react todo list`**。如果安装正常，Agent 会在写任何代码之前自动触发 `brainstorming`。

对 Java / Spring 场景，可以换成类似「Let's add a REST endpoint to my Spring Boot app」这类描述，观察是否先进入需求澄清而不是直接产出代码。

如果技能该触发却没触发，官方提供了排查技能 `diagnosing-superpowers`：直接让编码 Agent「figure out what went wrong with superpowers in this session」，它会读取会话记录、给出带行级证据的报告，必要时还能打包一份脱敏的 bug 报告材料。要查更早的会话，可以指定会话 id。

## 局限与风险

- **harness 覆盖有限**：官方支持列表里没有 Trae Work，也没有面向 Java / Spring 的 SDK 或 HTTP 集成。想在 Trae Work 里用，目前只能借鉴方法论，不能直接接入。
- **强制风格可能不合口味**：`using-superpowers` 的措辞是「如果技能适用，你没有选择余地」，这种强硬约束对喜欢自由发挥的开发者可能过于教条。
- **成本与耗时**：`subagent-driven-development` 每个任务派新子 Agent 并逐个评审，是最彻底也最贵的路径；官方也提供了更省的 `executing-plans`。
- **长会话可能丢引导**：官方在 Hermes Agent 一节明确说明，Hermes 没有 post-compaction 钩子，超长会话在首轮之后发生压缩会丢失引导，需要新开会话。其他 harness 的钩子行为官方未逐一说明。
- **遥测**：官方目录中存在「Visual companion telemetry」一节，但本次可获取的内容未展开其细节，具体采集范围与开关方式暂无公开资料。
- **许可证**：官方目录列出了 License 一节，但本次可获取的内容未包含具体许可证文本，具体条款暂无公开资料。
- **商业支持**：官方说明企业用户如需商业支持、额外工具或托管支出，可联系 sales@primeradiant.com。
- **贡献限制**：官方明确表示通常不接受新技能的贡献，且对技能的更新必须能在所有 harness 上工作。

## 社区评价

在 Hacker News 关于《Superpowers: How I'm using coding agents in October 2025》的讨论（435 points，231 条评论）中，热度最高的评论串实际上集中在 HN 自动改写标题这件事上：有用户指出原标题「Superpowers: How I'm using ...」被自动改成「Superpowers: I'm using ...」，导致「Superpowers」指代的对象完全变了——原意是「给 LLM 编码 Agent 的超级能力」，改后变成「LLM 编码 Agent 是人类的超级能力」。跟帖者普遍认为这种自动改写弊大于利。

需要说明的是，该讨论串中高赞内容主要围绕标题改写，而非对 Superpowers 本身技术能力的评价；本次可获取的社区内容中，未包含更多针对其工作流效果的实质性讨论。

## 生态与来源

- 作者：Jesse Vincent 及 Prime Radiant 团队。
- 社区渠道：Discord（discord.gg/35wsABTejz）、Issues（github.com/obra/superpowers/issues）、版本发布通知（primeradiant.com/superpowers/）。
- 在 Claude 插件市场上，该插件标注的安装量为 1,009,371；在 skills.sh 上 `using-superpowers` 技能标注安装量 260.2K。
- 安全审计方面，skills.sh 页面显示：Gen Agent Trust Hub 为 Warn，Socket 为 Pass，Snyk 为 Pass。

## 给 Java 后端的一次落地指令

下面这段可以直接整段复制给 Trae Work 等 AI 编程助手，让它按 Superpowers 的方法论带你走一遍 Spring 项目的小需求。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 项目，技术栈是 Java + Spring Boot + Maven，测试用 JUnit 5。我了解到一个叫 Superpowers 的 Agent 技能框架，它强调先澄清需求、再写计划、再严格 TDD、最后代码评审。官方没有提供 Trae Work 的集成方式，所以请你直接按这套方法论来协作，不要假装安装了插件。

目标：帮我在现有 Spring Boot 项目里新增一个「订单导出为 CSV」的 REST 接口，并全程遵循 Superpowers 的工作流。

具体要求：
1. 先不要写任何代码。先进入 brainstorming 模式，向我提问，把真实需求问清楚：导出字段有哪些、数据量多大、是否需要分页或流式写出、权限如何控制、文件名与编码怎么定、异常怎么返回。一次问不超过 5 个问题。
2. 把理解分块复述给我确认，每块短到我能快速读完。我确认后再进入下一步。
3. 确认后写一份实施计划，拆成 2–5 分钟一个的小任务。每个任务必须包含：确切的文件路径、要写的完整代码或方法签名、以及验证步骤（跑哪条 Maven 命令、期望看到什么结果）。
4. 实现阶段严格执行 TDD 的 RED-GREEN-REFACTOR：先写会失败的测试，运行 `mvn test` 确认它确实失败，再写最小实现让它通过，然后重构。任何在测试之前写下的生产代码都要删掉重来。
5. 每个任务完成后做一次自评审，对照计划检查是否有遗漏，按严重程度列出问题，严重问题必须解决后才能继续。
6. 全部完成后，运行完整测试，告诉我测试结果，并给出后续选项：直接提交、开分支提 PR、还是先保留改动。

约束：
- 所有命令用 Windows PowerShell 写法。
- 不要引入计划外的新依赖，遵循 YAGNI。
- 不要跳过测试直接给实现。
- 如果某一步你不确定，停下来问我，不要猜。
```

## 一句话结论

如果你已经在用官方支持的编码 Agent，并且认同「先设计、后编码、强制 TDD、任务间评审」这套纪律，Superpowers 值得花十分钟装上试一次；如果你主力是 Trae Work + Java，目前它更像一份可以手动照做的方法论清单，而不是一个能直接接入的插件。

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
