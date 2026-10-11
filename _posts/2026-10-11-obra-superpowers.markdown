---
layout: post
title: "Superpowers 初体验：给编码 Agent 装上开发方法论"
subtitle: "一套可组合技能包，让 AI 先想清楚再写代码，支持多种编码 Agent"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/obra/superpowers
- Stars：297467
- 语言：Shell
- 创建时间：2025-10-09
- 最近更新：2026-10-10
- 官方简介：An agentic skills framework & software development methodology that works.

---

## 解决什么问题

Superpowers 是一套面向编码 Agent 的完整软件开发方法论，构建在一组可组合的 skills 以及一些初始指令之上，这些指令确保你的 Agent 会真正使用这些 skills。

README 描述的核心痛点是：Agent 一看到你在构建东西，往往不会先退一步问清楚你到底想做什么，而是直接跳进去写代码。Superpowers 让 Agent 先停下来，把真正的意图从对话中梳理出来，形成 spec，再分块展示给你确认；设计通过后生成实现计划，然后进入 subagent-driven-development 流程，由多个 Agent 逐个完成工程任务、检查并评审彼此的工作。README 提到，Agent 连续自主工作数小时而不偏离既定计划并不罕见。

由于 skills 会自动触发，你不需要做任何特殊操作，编码 Agent 就“拥有 Superpowers”。

## 核心概念

- **Skills（技能）**：可组合的技能集合，是整套方法论的基础单元。README 的 What's Inside 列出了完整技能库，分为 Testing、Debugging、Collaboration、Meta 四类。
- **自动触发**：skills 会自动触发，无需手动调用。README 强调“The agent checks for relevant skills before any task. Mandatory workflows, not suggestions.”（Agent 在任何任务前都会检查相关 skills，这是强制工作流而非建议）。
- **基础工作流（The Basic Workflow）**：README 给出 7 步流程——brainstorming（构建前激活，梳理真实意图）、using-git-worktrees（设计批准后创建隔离工作区与新分支、跑项目初始化、验证干净的测试基线）、writing-plans（把工作拆成 2-5 分钟一个的小任务，每个任务有确切文件路径、完整代码、验证步骤）、subagent-driven-development 或 executing-plans（前者每个任务派发全新 subagent 并在每个任务后评审，最彻底；后者在当前会话内联实现所有任务，最后对整个分支做一次全新评审，最省成本）、test-driven-development（实现期间强制 RED-GREEN-REFACTOR，先写失败测试、看它失败、写最小代码、看它通过、提交；删除在测试之前写的代码）、requesting-code-review（任务之间按计划评审，按严重程度报告问题，Critical 问题阻塞进度）、finishing-a-development-branch（任务完成时验证测试，给出 merge/PR/keep/discard 选项，清理 worktree）。
- **Harness（运行壳）**：README 明确“Installation differs by harness. If you use more than one, install Superpowers separately for each one.”（安装方式因 harness 而异，如果你使用多个，需要为每一个单独安装）。
- **诊断技能**：当会话行为异常（skill 不该触发却触发、该静默却静默、Agent 忽略计划、重复劳动、消耗超出预期的 token）时，可以让编码 Agent 调用 **diagnosing-superpowers** skill 来定位问题。
- **遥测开关**：brainstorming 的可选可视化伴侣功能中的 Prime Radiant logo 默认从官网加载，包含所用 Superpowers 版本，但不包含项目、prompt 或编码 Agent 的任何细节。可通过环境变量 `SUPERPOWERS_DISABLE_TELEMETRY` 设为任意真值来关闭，同时也遵循 Claude Code 的 `DISABLE_TELEMETRY` 和 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 退出选项。

## 前置依赖

README 未提供统一的前置依赖清单。从 README 可以确认的事实是：

- 你需要一个受支持的编码 Agent / harness。README 的 Getting Started 列出了 Claude Code、Antigravity、Codex App、Codex CLI、Cursor、Devin CLI、Factory Droid、Gemini CLI、GitHub Copilot CLI、Grok Build CLI、Kimi Code、OpenCode、Pi、Qwen Code、Hermes Agent、Muse。
- 如果你使用多个 harness，需要为每一个单独安装。
- 仓库主语言为 Shell。

除上述内容外，README 未提供具体的运行时版本、操作系统要求或依赖包要求。

## 安装与配置

README 未提供与 Trae Work / Java 的集成方式。以下先给出 README 中列出的通用安装方式，再说明在你（Windows + Trae Work + Java/Spring）环境下的现状。

### 通用安装（按 harness 选择其一）

1. **Claude Code**：通过官方 Claude 插件市场安装，执行 `/plugin install superpowers@claude-plugins-official`；或注册 Superpowers 市场后安装——先执行 `/plugin marketplace add obra/superpowers-marketplace`，再执行 `/plugin install superpowers@superpowers-marketplace`。
2. **Antigravity**：执行 `agy plugin install https://github.com/obra/superpowers`。README 说明 Antigravity 会列出每个已安装 skill 的描述，`using-superpowers` skill 的描述会提示模型在对话开始时加载该 skill；用同样的命令重新安装即可更新。
3. **Codex App**：在 Codex 应用中点击侧边栏的 Plugins，在 Coding 区域应能看到 `Superpowers`，点击 Superpowers 旁边的 `+` 并按提示操作。
4. **Codex CLI**：打开插件搜索界面 `/plugins`，搜索 `superpowers`，选择 `Install Plugin`。
5. **Cursor**：在 Cursor Agent 聊天中执行 `/add-plugin superpowers`，或在插件市场中搜索 "superpowers"。
6. **Devin CLI**：执行 `devin plugins install obra/superpowers`；更新用 `devin plugins update superpowers`。
7. **Factory Droid**：先执行 `droid plugin marketplace add https://github.com/obra/superpowers`，再执行 `droid plugin install superpowers@superpowers`。
8. **Gemini CLI**：执行 `gemini extensions install https://github.com/obra/superpowers`；更新用 `gemini extensions update superpowers`。
9. **GitHub Copilot CLI**：先执行 `copilot plugin marketplace add obra/superpowers-marketplace`，再执行 `copilot plugin install superpowers@superpowers-marketplace`。
10. **Grok Build CLI**：执行 `grok plugin install superpowers@xai-official --trust`；或在 TUI 中打开 `/marketplace` 搜索 Superpowers 并安装。
11. **Kimi Code**：打开插件管理器 `/plugins`，进入 `Marketplace` > `Superpowers` 安装；或直接从仓库安装 `/plugins install https://github.com/obra/superpowers`。详细文档见 `docs/README.kimi.md`。
12. **OpenCode**：告诉 OpenCode “Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md”。详细文档见 `docs/README.opencode.md`。
13. **Pi**：执行 `pi install git:github.com/obra/superpowers`；本地开发可用 `pi -e /path/to/superpowers` 以临时包形式加载。README 说明 Pi 包会加载 Superpowers skills 以及一个小扩展，在会话启动时和压缩后再次注入 `using-superpowers` 引导；Pi 有原生 skills，因此不需要兼容性的 `Skill` 工具。
14. **Qwen Code**：执行 `qwen extensions install obra/superpowers`，提示时选择 `superpowers`；更新用 `qwen extensions update superpowers`。
15. **Hermes Agent**：执行 `hermes plugins install obra/superpowers --enable`，安装后重启所有活跃的 Hermes 会话。README 特别提示：Hermes 没有 post-compaction hook，因此第一轮之后发生压缩的超长会话会丢失引导，如果 skills 停止触发请开新会话。
16. **Muse**：从本地 checkout 安装可执行 `muse plugins install ./` 然后 `muse plugins approve superpowers`；或先 `git clone https://github.com/obra/superpowers.git`，再 `muse plugins install ./superpowers` 和 `muse plugins approve superpowers`。更新用 `muse plugins update superpowers`。安装后需重启活跃的 Muse 会话，让 `SessionStart` hook 生效。

### 在你的 Trae Work + Java 工作流中

- README 未提供与 Trae Work / Java 的集成方式。README 的安装章节没有列出 Trae Work，也没有提供 MCP 服务接入、Skill 目录放置、CLI 调用或 Java/Spring SDK/HTTP 集成中的任何一种方式。
- 因此，无法从 README 得出在 Trae Work 中安装 Superpowers 的步骤，也不应假设存在某个配置路径或命令。
- README 中可复用的通用事实是：安装方式因 harness 而异，且每个 harness 需要单独安装。若你的 Trae Work 支持上述任一 harness 的插件机制，可参考对应章节；但 README 未说明这种兼容性。

## 最小可用示例

下面这段指令可以直接整段复制给 Trae Work 等 AI 编程助手，用于在 Java/Spring 场景下试用 Superpowers 的工作流（先梳理意图、再出计划、再按 TDD 实现）。

```text
背景：我是一个 Java 后端程序员，在 Windows 上用 Trae Work 开发，技术栈以 Java / Spring 为主。我想试用 Superpowers 这套面向编码 Agent 的开发方法论，请按它的基础工作流来推进我的需求。

目标：为我的 Spring 项目新增一个 REST 接口，用于按 ID 查询订单详情。

要求：
1. 先不要写代码。先进入 brainstorming 阶段，通过提问帮我把真实意图和边界条件梳理清楚（例如：订单不存在时返回什么、是否需要鉴权、返回字段范围、分页是否需要），然后把你的理解复述给我确认。
2. 我确认设计后，再进入 writing-plans 阶段，把工作拆成 2-5 分钟一个的小任务，每个任务给出确切的文件路径、完整代码和验证步骤。
3. 实现阶段严格按 test-driven-development 执行 RED-GREEN-REFACTOR：先写会失败的测试、确认它失败、再写最小实现让它通过、然后提交。不要先写实现再补测试。
4. 每个任务完成后做一次代码评审，按严重程度报告问题，Critical 问题必须阻塞后续进度。
5. 全部任务完成后，验证测试是否通过，并告诉我可以 merge、提 PR、保留分支还是丢弃。
```

## 验证方法

README 中给出的可执行验证方式如下：

1. **Muse 场景的验证**：README 明确写道，安装后启动一个全新会话并发送 `Let's make a react todo list`，一个正常工作的安装会在写任何代码之前自动触发 `brainstorming`。
2. **通用观察点**：按 The Basic Workflow 的描述，正常工作时 Agent 在任何任务前都会检查相关 skills；brainstorming 会在构建任何东西之前激活。
3. **出问题时的诊断**：让编码 Agent 执行“figure out what went wrong with superpowers in this session”，它会调用 **diagnosing-superpowers** skill；要检查更早的会话，可以指定会话名：“figure out what went wrong with superpowers in session `<id>`”。该 skill 会读取会话记录，用行级证据报告发生了什么，并可按需打包一份脱敏的 bundle 用于提交 bug 报告。

除上述内容外，README 未提供其他验证命令或检查清单。

## 风险与注意事项

- **多 harness 需分别安装**：README 明确说明安装方式因 harness 而异，使用多个 harness 时需要为每一个单独安装。
- **Hermes 的压缩限制**：Hermes 没有 post-compaction hook，第一轮之后发生压缩的超长会话会丢失引导；如果 skills 停止触发，需要开新会话。
- **Muse 的 hook 审批**：Muse 安装后需重启活跃会话让 `SessionStart` hook 生效；skills 立即生效，但 hooks 首次安装时需要审批。
- **遥测**：brainstorming 的可选可视化伴侣功能中的 Prime Radiant logo 默认从官网加载，包含所用 Superpowers 版本，但不包含项目、prompt 或编码 Agent 的细节，也看不到点击或你在构建什么。可通过环境变量 `SUPERPOWERS_DISABLE_TELEMETRY` 设为任意真值关闭，同时也遵循 Claude Code 的 `DISABLE_TELEMETRY` 和 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`。
- **更新行为**：README 说明 Superpowers 的更新在一定程度上取决于编码 Agent，但通常是自动的。
- **贡献限制**：README 说明一般不接受新 skills 的贡献，且对 skills 的任何更新都必须在其支持的所有编码 Agent 上可用。
- **Trae Work / Java 集成风险**：README 未提供与 Trae Work / Java 的集成方式，因此无法评估在该环境下的兼容性与风险。

## 替代方案

README 未提供替代方案。README 中与“替代”相关的唯一信息是：安装方式因 harness 而异，如果你使用多个 harness，需要为每一个单独安装 Superpowers；以及贡献流程中提到，对 skills 的更新必须在其支持的所有编码 Agent 上可用。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
