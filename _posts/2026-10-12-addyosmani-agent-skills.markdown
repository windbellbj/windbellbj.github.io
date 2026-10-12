---
layout: post
title: "Agent Skills 使用说明：给 AI 编程助手装上高级工程师的工作流"
subtitle: "24 个 Markdown 技能包，把 spec、测试、评审、上线这些「看不见的活」变成 Agent 的强制动作"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI技能
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/addyosmani/agent-skills
- Stars：105030
- 语言：JavaScript
- 创建时间：2026-02-15
- 最近更新：2026-10-10
- 官方简介：Production-grade engineering skills for AI coding agents.

---

> **Agent Skills 是一套面向 AI 编程代理的「生产级工程技能包」：它把资深工程师在写代码之外真正做的事——写规格、拆任务、先写测试、评审、上线检查——固化成 24 个结构化工作流，让 Agent 在每个开发阶段都按同一套质量门禁执行。最适合已经用 AI 写代码、但被「能跑就行」的原型级产出折磨过的开发者，尤其是希望把 AI 产出直接推到生产环境的 Java/Spring 后端。**

## 它到底解决什么问题

AI 编程代理的默认行为是走最短路径：你说要一个功能，它就把功能写出来，不问有没有规格、不先写测试、不考虑这次改动是否跨过了信任边界、也不管 PR 交到评审人手里是什么样子。它产出代码、宣布完成、继续下一个任务。

Agent Skills 的作者把这件事讲得很直白：资深工程师的工作大部分不体现在 diff 里——暴露假设、写规格、把工作拆成可评审的小块、选择无聊但稳妥的设计、留下「结果正确」的证据、把改动控制到人能真正读完的规模。这些步骤之所以被 Agent 跳过，和初级工程师跳过它们的理由一样：它们不可见，而奖励信号指向的是「任务完成」，不是「任务完成且设计文档存在」。

这套技能包就是把资深工程师的脚手架重新装回去。它编码的是 Google 工程实践里那些耳熟能详的东西——Hyrum 定律、测试金字塔、主干开发——但形式不是文章，而是**带步骤、带检查点、带退出条件的工作流**。

> 一个关键区分：技能不是参考文档，不是「关于测试你应该知道的一切」。技能是工作流——先写会失败的测试、运行它、看着它失败、写最少代码让它通过、看着它通过、重构。前者让 Agent 生成看起来合理的文字然后跳过真正的测试；后者让 Agent 有具体的事可做，也让你有具体的东西可验证。

## 核心概念：技能、命令与生命周期

### 技能（Skill）是什么

一个技能是一个带 frontmatter 的 Markdown 文件，在情境需要时被注入 Agent 的上下文，介于「系统提示片段」和「运维手册」之间。每个技能包含步骤、验证门禁，以及一张**反合理化表（anti-rationalization table）**——把 Agent 用来跳过步骤的原话（比如「我稍后再补测试」）逐条列出并给出反驳。

技能采用渐进式披露：`SKILL.md` 是入口，配套的参考材料只在需要时加载，以控制 token 消耗。

### 八个斜杠命令映射开发阶段

| 你在做什么 | 命令 | 核心原则 |
|---|---|---|
| 定义要构建什么 | `/spec` | 先有规格，再写代码 |
| 规划怎么构建 | `/plan` | 小而原子的任务 |
| 增量地构建 | `/build` | 一次一个切片 |
| 证明它能工作 | `/test` | 测试就是证据 |
| 设定质量标准 | `/constraints` | 一次决定，处处执行 |
| 合并前评审 | `/review` | 改善代码健康度 |
| 审计 Web 性能 | `/webperf` | 先测量再优化 |
| 简化代码 | `/code-simplify` | 清晰优先于聪明 |
| 发布到生产 | `/ship` | 更快就是更安全 |

命令之外，技能也会根据你正在做的事自动激活：设计 API 会触发 `api-and-interface-design`，构建 UI 会触发 `frontend-ui-engineering`，等等。

### 24 个技能覆盖完整 SDLC

技能包共 25 个技能——24 个生命周期技能加一个 `using-agent-skills` 元技能。按阶段划分，官方列出的代表性技能包括：

| 阶段 | 技能 | 作用 |
|---|---|---|
| 元 | `using-agent-skills` | 把 incoming 的工作映射到正确的技能工作流，定义共享操作规则 |
| 定义 | `interview-me` | 一次一个问题地访谈，挖出你真正想要的东西，直到约 95% 置信度 |
| 定义 | `idea-refine` | 结构化的发散/收敛思考，把模糊想法变成具体提案 |
| 定义 | `spec-driven-development` | 写 PRD，覆盖目标、命令、结构、代码风格、测试与边界 |
| 定义 | `constraint-driven-development` | 访谈出质量门槛，写入 `CONSTRAINTS.md`，按成本放置检查 |
| 规划 | `planning-and-task-breakdown` | 把规格拆成小的、可验证的、带验收标准和依赖顺序的任务 |
| 构建 | `incremental-implementation` | 薄垂直切片——实现、测试、验证、提交；特性开关、安全默认值、可回滚 |
| 构建 | `test-driven-development` | 红-绿-重构、测试金字塔（80/15/5）、DAMP 优于 DRY、Beyoncé 规则 |
| 构建 | `context-engineering` | 在正确的时间给 Agent 正确的信息——规则文件、上下文打包、MCP 集成 |
| 构建 | `source-driven-development` | 每个框架决策都基于官方文档——验证、引用来源、标记未验证内容 |
| 构建 | `doubt-driven-development` | 对每个非平凡决策做对抗式全新上下文评审，可选跨模型升级 |
| 构建 | `frontend-ui-engineering` | 组件架构、设计系统、状态、响应式、WCAG 2.1 AA 无障碍 |
| 评审 | `code-review-and-quality` | 五轴评审、约 100 行改动规模、严重度标签、评审速度规范 |
| 评审 | `security-and-hardening` | OWASP Top 10 防护、认证模式、密钥、依赖审计 |
| 评审 | `performance-optimization` | 测量优先——Core Web Vitals 目标、性能剖析、包分析、N+1 修复 |
| 发布 | `shipping-and-launch` | 发布前检查清单、特性开关生命周期、分阶段推出、回滚流程 |

> 官方仓库说明在截取范围内列出了 25 个技能中的大部分，完整清单以仓库 `skills/` 目录为准。

### `/build auto`：一次批准，自主执行

如果规格已经存在、想减少手工步骤，`/build auto` 会生成计划并在一次批准后实现每个任务。它去掉的是任务之间的人工切换，不是验证：每个任务仍然是测试驱动、单独提交，遇到失败或高风险步骤会暂停。

<!-- asset:blog-1 start -->
![开发阶段与斜杠命令映射](/img/ai-news/addyosmani-agent-skills/blog-1.png)

*图：开发阶段与斜杠命令映射*
<!-- asset:blog-1 end -->


## 环境与前置依赖

- **宿主 Agent**：技能是纯 Markdown，任何接受系统提示或指令文件的 Agent 都能用。官方明确列出原生集成或适配路径的包括 Claude Code、Cursor、Antigravity CLI、Gemini CLI、Windsurf、OpenCode、GitHub Copilot、Kiro、Codex、Command Code 等，官方称可通过 skills CLI 安装进 70+ 个 Agent。
- **Node.js / npx**：走通用安装路径需要 `npx`，即本机要有可用的 Node.js 环境。
- **Git**：本地克隆、以及部分插件市场的底层克隆需要 Git。官方特别提示，Claude Code 的 marketplace 通过 SSH 克隆仓库，如果 GitHub 上没有配好 SSH key，会报 `git@github.com: Permission denied (publickey)`。
- **许可证**：MIT。官网首页标注「24 skills, MIT licensed」。
- **与 Trae Work / Java 的关系**：官方列出的宿主清单里没有 Trae Work，也没有提供 Java/Spring 的 SDK 或 HTTP 集成方式。**官方未提供与 Trae Work / Java 的集成方式**，需要按「其他 Agent」路径自行接入（见下文）。

## 安装与配置（Windows + Trae Work）

### 路径一：通用 skills CLI（推荐先试这条）

官方给出的最快路径是开放的 skills CLI，一条命令装进 70+ 个 Agent。在 Windows PowerShell 中：

1. 先浏览有哪些技能，不实际安装：`npx skills add addyosmani/agent-skills --list`
2. 安装全部 25 个技能：`npx skills add addyosmani/agent-skills`
3. 或者只装单个技能，例如合并前的五轴评审：`npx skills add addyosmani/agent-skills --skill code-review-and-quality`
4. 其他常用单装示例：`npx skills add addyosmani/agent-skills --skill interview-me`（需求拷问，一次一个问题）、`npx skills add addyosmani/agent-skills --skill test-driven-development`（强制的红-绿-重构）。

> **只装单个技能时有个已知缺口**：按技能单独 `npx` 安装只会复制 `skills/<name>/`，不会复制仓库级的 `references/` 目录。技能本身仍可用，但指向共享检查清单的路径会失效。官方建议改用整仓集成、克隆仓库，或把需要的检查清单复制进已安装技能内的 `references/` 目录。该可移植性问题记录在仓库 issue #361。

### 路径二：本地克隆 + 手动接入 Trae Work

由于官方没有 Trae Work 的原生集成，最稳妥的做法是把技能当作「其他 Agent」处理——它们是纯 Markdown，可以喂给任何接受指令文件的 Agent。

1. 克隆仓库到本地：`git clone https://github.com/addyosmani/agent-skills.git`
2. 进入仓库查看 `skills/` 目录，每个子目录下有一个 `SKILL.md`，这就是技能入口。
3. 在 Trae Work 中，把你要用的技能内容作为项目级指令或规则文件引入。官方对其他宿主的通用建议是：技能内容放进项目的规则/指令配置，短策略放规则文件，**不要把完整技能粘贴进规则**。
4. 如果你希望 Agent 能读到共享检查清单，保留整个克隆下来的仓库目录结构，不要只复制单个 `SKILL.md`。

> 官方对 Cursor 的说明可以直接类比：把工作流技能放在 `.cursor/skills/`，短策略放在 `.cursor/rules/*.mdc`，两个目录都在你的项目里，仓库本身不附带 `.cursor/` 文件夹。Trae Work 的具体技能目录名官方未公开说明，需要你按 Trae Work 自身的规则文件机制来放置。

### 路径三：如果你同时用 Claude Code / Codex / Gemini CLI

这些是官方有原生集成的宿主，可以作为对照验证技能包是否正常工作：

- Claude Code 插件市场：`/plugin marketplace add addyosmani/agent-skills`，然后 `/plugin install agent-skills@addy-agent-skills`。遇到 SSH 报错时，可改用完整 HTTPS 地址：`/plugin marketplace add https://github.com/addyosmani/agent-skills.git`。Windows 上若仍报 publickey 错误，官方推荐的变通是配置 Git 一次性把 GitHub SSH 地址重写为 HTTPS：`git config --global url."https://github.com/".insteadOf git@github.com:`
- Claude Code 本地开发：`claude --plugin-dir /path/to/agent-skills`
- Codex（CLI v0.122+）：`codex plugin marketplace add addyosmani/agent-skills`，再 `codex plugin add agent-skills@agent-skills`，之后在对话里用 `@` 调用，例如 `@spec-driven-development`
- Gemini CLI：`gemini skills install https://github.com/addyosmani/agent-skills.git --path skills`，或从本地克隆 `gemini skills install ./agent-skills/skills/`
- Antigravity CLI：`agy plugin install https://github.com/addyosmani/agent-skills.git`
- Command Code：`cmd skills add addyosmani/agent-skills`，加 `--global` 装到所有项目，加 `-s spec-driven-development` 装指定技能

### 路径四：Java / Spring 项目里怎么用

Agent Skills 本身不是库，不提供 Maven/Gradle 依赖，也没有 Java SDK 或 HTTP 服务。**官方未提供与 Java/Spring 的集成方式**。它对 Java 项目的价值在于：把 `spec-driven-development`、`test-driven-development`、`code-review-and-quality`、`security-and-hardening` 这些工作流注入你的 AI 助手，让它在写 Spring 代码时先出规格、先写 JUnit 测试、按五轴标准自评、按 OWASP Top 10 检查输入校验与认证逻辑。

<!-- asset:code-1 start -->
```powershell
npx skills add addyosmani/agent-skills --list
npx skills add addyosmani/agent-skills
npx skills add addyosmani/agent-skills --skill code-review-and-quality
npx skills add addyosmani/agent-skills --skill interview-me
npx skills add addyosmani/agent-skills --skill test-driven-development
```
<!-- asset:code-1 end -->


## 快速上手：确认它真的生效

1. 在 Trae Work 里新建或打开一个 Spring 项目。
2. 引入 `spec-driven-development` 技能内容，然后对助手说：帮我为「用户注册接口」写规格。
3. **成功信号**：助手不再直接甩出 Controller 代码，而是先产出覆盖目标、命令、结构、代码风格、测试与边界的 PRD 式文档。
4. 引入 `test-driven-development`，让它实现规格里的第一个任务。**成功信号**：它先写一个会失败的测试，运行并展示失败，再写最少代码让它通过，然后重构。
5. 引入 `code-review-and-quality`，让它评审刚才的改动。**成功信号**：输出按五个轴组织，给出严重度标签，并指出改动规模是否超过约 100 行。
6. 如果它开始说「我稍后再补测试」，检查技能里的反合理化表是否被正确加载——这是判断技能有没有真正注入上下文的最直接标志。

<!-- asset:blog-2 start -->
![确认技能生效的成功信号](/img/ai-news/addyosmani-agent-skills/blog-2.png)

*图：确认技能生效的成功信号*
<!-- asset:blog-2 end -->


## 局限与风险

- **成熟度**：仓库创建于 2026-02-15，最近更新 2026-10-10，主语言 JavaScript，MIT 许可。作者在博客中称项目「刚过 27K stars」，而仓库元信息与第三方站点显示的数字在 10 万量级，两处说法不一致，以仓库页面实时数据为准。
- **单技能安装的引用缺口**：如前所述，单独安装不会带上仓库级 `references/`，共享检查清单路径会失效，官方已记录为 issue #361。
- **宿主兼容性差异**：生命周期斜杠命令（`/spec`、`/plan`、`/build`、`/test`、`/review`、`/ship`）是 Claude Code 的命令，在 GitHub Copilot 等宿主里不会出现，需要按技能名调用（如 `/spec-driven-development`）。Antigravity CLI 的部分版本中，旧式命令 TOML 会被报告为已转换，但包装命令不可发现，需要直接调用底层的命名空间技能。
- **Trae Work 无官方支持**：没有原生集成，也没有公开的技能目录约定，接入方式需要自行摸索，且官方未承诺兼容。
- **费用**：技能包本身 MIT 免费，但它会显著增加 Agent 的上下文与交互轮次，实际成本取决于你所用 Agent 的计费方式，官方未公开说明相关开销数据。
- **安全**：技能内容会作为指令注入 Agent 上下文，来源是公开仓库，但把任何第三方指令文件接入生产项目的 AI 助手前，建议先通读内容，尤其是涉及认证、密钥、依赖审计的 `security-and-hardening`。

## 社区评价（来自 Hacker News 讨论）

相关讨论帖包括《Agent Skills》（544 points，260 条评论）、《Agent Skills》（376 points，212 条评论），以及《SkillsBench: Benchmarking how well agent skills work across diverse tasks》（364 points，171 条评论）。

- 有评论者表示，过去几个月试用技能彻底改变了对 LLM 的看法：不再把 LLM 和 Agent 当作「我们构建的产品的一个功能」，而是当作「我们构建的产品的用户」。他尝试为内部工具写技能，发现失败时往往不只是 LLM 的问题，也是工具本身的问题——做不了显而易见的事、文档很烂、API 返回不透明的错误信息。这些是人类靠口口相传的隐性知识绕过去的问题。
- 另一条被引用的观点更激进：如果你今天在做产品，你正在做的功能在 Claude Code 能用它之前都不算完成；技能和 MCP 不是「锦上添花」，而会变得和 SEO、无障碍一样重要，几年后如果你的产品不能被 Agent 发现和使用，它可能等于不存在。
- 也有评论者认同「无处不在的 LLM 是一种强制力量，逼着大家去补上长期投入不足的人类可读文档」，但同时表示对 MCP 本身仍持保留态度。
- 实际使用者反馈：有人采纳了其中几个技能，API 设计和 UI 测试相关的尤其有帮助。
- 也有顾虑：有人担心装了之后不好删，并认为每个技能最好按开发者个人定制；底下有人反问——插件不就是一组文件吗，为什么会删不掉。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 后端项目，技术栈是 Spring Boot + Maven + JUnit 5，代码库已有一定规模。我已经把 addyosmani/agent-skills 的技能内容作为项目指令引入了 Trae Work。

目标：请用 Agent Skills 的工作流，帮我把「用户注册接口」这个需求从规格推进到可评审的代码，全程遵守技能里的质量门禁。

具体要求：
1. 先按 spec-driven-development 输出一份 PRD，覆盖：目标与非目标、接口契约（路径、方法、请求/响应字段、错误码）、涉及的项目结构与包名、代码风格约定、测试策略、明确的边界（哪些不做）。在我确认之前不要写任何实现代码。
2. 按 planning-and-task-breakdown 把 PRD 拆成小的、可验证的任务，每个任务给出验收标准和依赖顺序，标注哪些任务可以并行。
3. 按 test-driven-development 实现第一个任务：先写会失败的 JUnit 5 测试，运行并展示失败输出，再写最少代码让它通过，展示通过输出，最后重构。不要跳过「看着它失败」这一步。
4. 按 security-and-hardening 检查这个接口：输入校验、密码存储、认证与授权边界、密钥管理、依赖风险，逐条给出结论和依据。
5. 按 code-review-and-quality 对最终改动做五轴评审，给出严重度标签，并说明改动规模是否控制在约 100 行以内；如果超出，给出拆分建议。
6. 全程如果你想说「稍后再补测试」或「这个先跳过」，停下来，把这句话和反合理化表里的对应条目一起展示给我，由我决定。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
