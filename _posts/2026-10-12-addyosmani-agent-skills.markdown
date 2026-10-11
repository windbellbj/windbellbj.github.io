---
layout: post
title: "Agent Skills：给 AI 编程助手装上资深工程师工作流"
subtitle: "25 个技能 + 9 条斜杠命令，把 spec、测试、评审、上线全流程固化进 Agent"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/addyosmani/agent-skills
- Stars：104935
- 语言：JavaScript
- 创建时间：2026-02-15
- 最近更新：2026-10-10
- 官方简介：Production-grade engineering skills for AI coding agents.

---

## 解决什么问题

AI 编程 Agent 默认走最短路径——跳过规格说明、测试、安全评审，以及那些让软件真正可靠的做法。Agent Skills 把资深工程师在构建软件时使用的工作流、质量门禁和最佳实践编码成技能，让 AI Agent 在开发的每个阶段都一致地遵循它们。

README 的原话是：这些不是通用提示词，而是有主见的、流程驱动的工作流，用来区分生产级质量和原型级质量。技能中融入了 Google 工程文化中的最佳实践，包括《Software Engineering at Google》和 Google 工程实践指南里的概念——API 设计中的 Hyrum 定律、测试中的 Beyonce 规则与测试金字塔、代码评审中的变更规模与评审速度规范、简化中的 Chesterton's Fence、Git 工作流中的主干开发、CI/CD 中的 Shift Left 与特性开关，以及一个专门的弃用技能（把代码视为负债）。

## 核心概念

**9 条斜杠命令映射开发生命周期**，每条命令自动激活对应技能：

- `/spec`：定义要构建什么，原则是「先规格后代码」
- `/plan`：规划怎么构建，原则是「小而原子的任务」
- `/build`：增量构建，原则是「一次一个切片」
- `/test`：证明它能工作，原则是「测试即证据」
- `/constraints`：设定质量标准，原则是「一次决定，处处执行」
- `/review`：合并前评审，原则是「改善代码健康度」
- `/webperf`：审计 Web 性能，原则是「先测量再优化」
- `/code-simplify`：简化代码，原则是「清晰胜过聪明」
- `/ship`：发布到生产，原则是「更快即更安全」

`/build auto` 可以在规格确定后一次性生成计划并实现所有任务：你批准一次计划，之后它自主运行。它去掉的是任务之间的人工介入，而不是验证——每个任务仍然是测试驱动、单独提交，遇到失败或高风险步骤会暂停。

技能也会根据你正在做的事自动激活：设计 API 触发 `api-and-interface-design`，构建 UI 触发 `frontend-ui-engineering`，等等。

**技能结构**：每个技能都遵循一致的解剖结构——frontmatter（name、description）、Overview（做什么）、When to Use（触发条件）、Process（分步工作流）、Rationalizations（借口与反驳）、Red Flags（出问题的信号）、Verification（证据要求）。

**关键设计选择**：

- 流程而非散文：技能是 Agent 遵循的工作流，不是阅读的参考文档，每步都有检查点和退出条件
- 反合理化：每个技能都包含一张常见借口表（例如「我稍后再加测试」）及有据可查的反驳
- 验证不可协商：每个技能都以证据要求结束——测试通过、构建输出、运行时数据，「看起来对」永远不够
- 渐进式披露：`SKILL.md` 是入口，支撑性参考只在需要时加载，保持 token 用量最小

**25 个技能**分为 24 个生命周期技能加 1 个 `using-agent-skills` 元技能，按 Define / Plan / Build / Verify / Review / Ship 分组，例如 `interview-me`、`idea-refine`、`spec-driven-development`、`constraint-driven-development`、`planning-and-task-breakdown`、`incremental-implementation`、`test-driven-development`、`context-engineering`、`source-driven-development`、`doubt-driven-development`、`frontend-ui-engineering`、`api-and-interface-design`、`browser-testing-with-devtools`、`debugging-and-error-recovery`、`code-review-and-quality`、`code-simplification`、`security-and-hardening`、`performance-optimization`、`git-workflow-and-versioning`、`ci-cd-and-automation`、`deprecation-and-migration`、`documentation-and-adrs`、`observability-and-instrumentation`、`shipping-and-launch`。

**4 个 Agent 角色**：`code-reviewer`（高级主任工程师，五轴代码评审）、`test-engineer`（QA 专家）、`security-auditor`（安全工程师）、`web-performance-auditor`（Web 性能工程师）。

**7 份参考清单**：`definition-of-done.md`、`testing-patterns.md`、`security-checklist.md`、`performance-checklist.md`、`accessibility-checklist.md`、`observability-checklist.md`、`orchestration-patterns.md`。

## 前置依赖

README 未提供明确的前置依赖清单。从 README 可推断的事实是：

- 技能是纯 Markdown，可与任何接受系统提示词或指令文件的 Agent 配合使用
- 最快的安装路径使用开放 skills CLI（`npx skills add`），README 称其可安装到 70+ 个 Agent（Claude Code、Cursor、Codex、Copilot、Cline 等）
- 部分原生集成有版本要求，例如 Codex 插件需要 Codex CLI v0.122+
- Claude Code 的 marketplace 安装通过 SSH 克隆仓库，README 提示若未配置 GitHub SSH 密钥需改用 HTTPS URL

README 未提供 Node.js 版本、操作系统要求等具体环境依赖说明。

## 安装与配置

README 未提供与 Trae Work / Java 的集成方式。以下为 README 中给出的通用安装步骤，供你在 Windows + Trae Work 环境下参考：

**方式一：通用 skills CLI（README 称为最快路径）**

1. 在 Trae Work 的终端中执行 `npx skills add addyosmani/agent-skills`，安装全部 25 个技能
2. 想先浏览再安装，执行 `npx skills add addyosmani/agent-skills --list`
3. 只装单个技能，执行 `npx skills add addyosmani/agent-skills --skill code-review-and-quality`（合并前的五轴评审）、`npx skills add addyosmani/agent-skills --skill interview-me`（需求盘问，一次一个问题）、`npx skills add addyosmani/agent-skills --skill test-driven-development`（红-绿-重构，强制执行）

注意：单技能 `npx` 安装只复制 `skills/<name>/`，不包含仓库级的 `references/` 目录。技能仍可用，但指向共享清单的路径不可用。README 建议改用整仓集成、克隆仓库，或把需要的清单复制到已安装技能内的 `references/` 目录。该可移植性缺口记录在 issue #361。

**方式二：其他 Agent 的原生集成**

README 列出了 Claude Code、Cursor、Antigravity CLI、Gemini CLI、Windsurf、OpenCode、GitHub Copilot、Kiro、Codex、Command Code 等宿主的具体安装方式，例如 Codex 用 `codex plugin marketplace add addyosmani/agent-skills` 加 `codex plugin add agent-skills@agent-skills`，Command Code 用 `cmd skills add addyosmani/agent-skills`。README 未提及 Trae Work 属于上述任一宿主，也未提供 Trae Work 的技能目录路径或 MCP 接入方式。

**方式三：手动放置**

README 说明技能是纯 Markdown，可与任何接受系统提示词或指令文件的 Agent 配合使用，并指向 `docs/getting-started.md`。README 未提供 Trae Work 对应的具体目录或配置文件名。

**融入日常工作流的建议**：README 未提供与 Trae Work / Java 的集成方式，因此无法给出经过验证的接入路径。可参考 README 中 Cursor 的做法（把工作流技能放在 `.cursor/skills/`，短策略放在 `.cursor/rules/*.mdc`，不要把完整技能粘进 rules），但 Trae Work 是否支持类似机制，README 未提供。

## 最小可用示例

把下面这段指令整段复制给 Trae Work，即可在 Java/Spring 项目里试用这套技能的工作流：

```text
背景：我是一个 Java 后端程序员，在 Windows 上用 Trae Work 开发，技术栈是 Java / Spring。我刚刚安装了 addyosmani/agent-skills 这套技能包，想在一个 Spring Boot 项目里试用它的工作流。

目标：为「给现有订单服务新增一个按订单号查询订单详情的 REST 接口」这件事，走一遍 spec → plan → build → test → review 的完整流程。

要求：
1. 先不要写代码。先用 interview-me 的方式一次只问我一个问题，把需求问清楚，直到你有约 95% 的把握；重点确认：接口路径与版本、鉴权方式、返回字段、订单不存在时的错误语义、分页与否、是否需要缓存。
2. 需求确认后，用 spec-driven-development 写一份 PRD，覆盖目标、命令、结构、代码风格、测试、边界。
3. 用 planning-and-task-breakdown 把 PRD 拆成小而可验证的任务，每个任务带验收标准和依赖顺序。
4. 用 incremental-implementation 一次只做一个切片：实现、测试、验证、提交，每个切片单独提交。
5. 用 test-driven-development 的红-绿-重构推进，测试遵循测试金字塔，优先 DAMP 而非 DRY。
6. 用 api-and-interface-design 检查接口契约：错误语义、边界校验、契约优先。
7. 最后用 code-review-and-quality 做五轴评审，变更规模控制在约 100 行，问题按 Nit / Optional / FYI 标注严重级别。
8. 每一步都要给出证据：测试通过输出、构建输出或运行时数据；不要用「看起来对」作为完成标准。
9. 如果某一步你打算跳过或简化，先说明理由，并对照技能里的反合理化表自查。
```

## 验证方法

README 未提供专门的验证命令或自检脚本。可执行的验证步骤基于 README 描述的行为：

1. 安装后确认技能已就位：README 提到 `npx skills add addyosmani/agent-skills --list` 可用于安装前浏览，安装后可在你的 Agent 中查看已安装技能列表（具体命令 README 未提供）。
2. 触发一条生命周期命令，例如在对话中输入 `/spec`，观察 Agent 是否进入规格驱动的工作流。README 说明这 9 条斜杠命令是 Claude Code 命令；GitHub Copilot 中不会出现这些命令，需要按名称调用技能（如 `/spec-driven-development`）。
3. 观察技能是否自动激活：README 称设计 API 会触发 `api-and-interface-design`，构建 UI 会触发 `frontend-ui-engineering`。
4. 检查技能是否产出证据：README 强调每个技能都以证据要求结束——测试通过、构建输出、运行时数据。若 Agent 只给出「看起来对」的结论，说明技能未按预期生效。
5. 若使用单技能安装，检查 `references/` 目录是否存在：README 指出单技能安装不包含仓库级 `references/`，共享清单路径会不可用。

## 风险与注意事项

- **单技能安装的可移植性缺口**：README 明确说明，单技能 `npx` 安装只复制 `skills/<name>/`，不含仓库级 `references/` 目录，指向共享清单的路径不可用。README 建议改用整仓集成、克隆仓库，或手动复制清单。该问题记录在 issue #361。
- **Claude Code marketplace 的 SSH 问题**：README 提示 marketplace 通过 SSH 克隆仓库，未配置 GitHub SSH 密钥会报错。Windows 或 macOS 上若 `/plugin install` 仍报 `git@github.com: Permission denied (publickey)`，README 推荐的变通方案是配置 Git 把 GitHub SSH URL 重写为 HTTPS：`git config --global url."https://github.com/".insteadOf git@github.com:`。
- **Antigravity CLI 的命令兼容性**：README 指出在受影响的 Antigravity CLI 版本中，旧式命令 TOML 被报告为已转换，但其包装命令不可发现，需要直接调用底层命名空间技能。
- **斜杠命令并非所有宿主通用**：README 说明生命周期斜杠命令（`/spec`、`/plan`、`/build`、`/test`、`/review`、`/ship`）是 Claude Code 命令，不会出现在 Copilot 中。
- **`/build auto` 的自主性**：README 说明它会自主运行，但每个任务仍是测试驱动、单独提交，遇到失败或高风险步骤会暂停。
- **与 Trae Work / Java 的集成**：README 未提供与 Trae Work / Java 的集成方式，也未提供 Trae Work 是否在支持宿主列表中的说明。
- **许可证**：MIT，README 说明可在项目、团队和工具中使用。

## 替代方案

README 在「How it compares」一节中明确提到两个可对比的替代方案：

- **Superpowers**（https://github.com/obra/superpowers）
- **Matt Pocock's skills**（https://github.com/mattpocock/skills）

README 指向 `docs/comparison.md`，称其中有三者的诚实并排对比，说明它们形态上的差异以及各自适用的场景，并包含一个受控的正面对比实验链接。README 未在正文中展开这些替代方案的具体差异内容。

此外，README 提到开放 skills CLI（https://github.com/vercel-labs/skills）可安装到 70+ 个 Agent，说明同一套技能也可通过该 CLI 生态分发到其他宿主。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
