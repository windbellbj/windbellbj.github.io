---
layout: post
title: "gstack 使用说明书：把 Claude Code 变成 23 个角色的虚拟工程团队"
subtitle: "YC 总裁 Garry Tan 开源的斜杠命令技能包，30 秒装好，先跑 /office-hours 和 /review 试试手感"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI技能
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/garrytan/gstack
- Stars：136001
- 语言：TypeScript
- 创建时间：2026-03-11
- 最近更新：2026-10-11
- 官方简介：Use Garry Tan's exact Claude Code setup: 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA

---

> gstack 是一套面向 Claude Code 的开源斜杠命令技能包，用 23 个「专家角色」和 8 个强力工具，把单个 AI 助手变成一支覆盖产品、架构、设计、评审、QA、安全与发布的虚拟工程团队。

## 它到底解决什么问题

大多数开发者把 AI 当成一把万能锤：一段模糊的多任务指令丢进去，出来的是没有焦点的平庸结果。gstack 的出发点完全不同——**AI 不应该停留在一种通用模式里，它需要明确的「认知档位」**。

它针对的是这几类具体痛点：

- **没有产品思维**：助手只会照字面实现你说的功能，从不反问「这是不是该做的东西」。
- **评审质量不稳定**：一句「review 我的 PR」每次深度都不一样，没有结构化审计，只有表层模式匹配。
- **发布全靠手工**：一句「ship 这个」会演变成同步分支、跑测试、开 PR 的漫长拉锯。
- **看不见界面**：助手能写代码却看不到你的应用，无法验证 UI 状态、布局错乱和登录流程。
- **QA 成为瓶颈**：开浏览器、点页面、眯眼看布局，人工 QA 是大多数 bug 溜进生产的通道。

作者 Garry Tan 是 Y Combinator 的总裁兼 CEO，此前是 Palantir 最早的工程/产品/设计成员之一，联合创办了 Posterous（后被 Twitter 收购），并搭建了 YC 内部社交网络 Bookface。他称 gstack 为自己的「开源软件工厂」，每天都在用。

## 核心概念：一个助手，多个专家角色

gstack 的核心理念是把单个 AI 助手变成一支虚拟开发团队。每个角色称为一个 **Skill**，通过斜杠命令激活，覆盖从产品愿景到上线复盘的完整生命周期。

> 规划不是评审，评审不是发布，创始人的品味不等于工程的严谨。把这些全部搅在一起，你只会得到四者的平庸混合体。gstack 给你的是明确的档位——随时告诉模型你现在需要哪种大脑。

官方简介里列出的角色包括：重新思考产品的 CEO、锁定架构的工程经理、拦截 AI 垃圾产出的设计师、找生产 bug 的评审者、开真实浏览器的 QA 负责人、跑 OWASP + STRIDE 审计的安全官，以及负责发布 PR 的发布工程师。**23 个专家角色加 8 个强力工具，全部是斜杠命令，全部是 Markdown，全部免费，MIT 许可证。**

第三方站点 gstacks.org 的描述口径略有不同，称其为「九个覆盖完整开发生命周期的技能」（该站标注版本 v0.4.1、16,000+ stars、1,800+ forks），与官方仓库的「23 个角色 + 8 个工具」说法不一致，此处并列两种说法供参考。

从架构视角看，gstack 的组件大致分为几层：规划与交付（Agent 宿主、产品规划、Autoplan）、实现、评审与保障（代码评审、QA 工作流、安全审计、预检门禁、发布策略）、浏览器与文档（浏览服务、浏览器生命周期、无头显示、设计工作流、PDF 生成）、记忆与集成（记忆摄取、Gbrain 执行），以及共享运行时（状态根、出口凭据、重生成、结果码、产物校验）。

<!-- asset:blog-1 start -->
![gstack 组件分层结构](/img/ai-news/garrytan-gstack/blog-1.png)

*图：gstack 组件分层结构*
<!-- asset:blog-1 end -->


## 环境前置依赖

| 依赖 | 要求 |
|------|------|
| Claude Code | 必需，官方安装入口 |
| Git | 必需 |
| Bun | v1.4.2+ 为测试版本；低于 1.3.3 会被安装脚本拒绝（该版本会让编译后的工具读取项目的 `.env`），介于两者之间会给出警告 |
| Node.js | 仅 Windows 需要 |
| Aside 浏览器 | macOS 15+ 推荐；浏览器类技能、`/make-pdf`、`/diagram` 会优先驱动它并使用你已登录的真实会话。没有它时，安装脚本会构建 gstack 自带的浏览器，同样的技能改用自带浏览器 |
| `/cso` 额外依赖 | 需要带全部四个 `--no-compile-autoload-*` 构建标志的 Bun 版本，以及原生工具链：Linux 上支持静态编译的 C 编译器、macOS 上的 Xcode 命令行工具、Windows 上的 Visual Studio 2022 Build Tools（含 Desktop development with C++）。缺失时安装脚本会装好其余部分、清理过期的 CSO 辅助程序，`/cso` 会报告 `not assessed` 并说明前置条件 |

官方给出的安装耗时参考：在一台 4 vCPU 的 Linux 云机器上（v1.91.13.0、干净的 HOME、包含二进制构建和 Chromium 下载），`./setup` 在克隆后耗时 31 秒。网络较慢和笔记本会更久。

## 在 Windows + Trae Work 上安装

> **重要前提**：官方公开的安装路径全部围绕 Claude Code 展开，明确支持的宿主为 Claude Code、OpenAI Codex CLI、OpenCode、Cursor、Factory Droid、Kiro、GitHub Copilot CLI、Antigravity CLI、Slate、OpenClaw。**官方未提供与 Trae Work 的集成方式，也未提供 Java / Spring 的 SDK 或 HTTP 接入方式。** 下面的步骤是在 Windows 上按官方方式安装 gstack，再把它作为技能目录接入你的 AI 编程助手工作流；如果你的 Trae Work 支持读取 Claude 技能目录或自定义技能，可据此自行尝试，官方没有为此背书。

### 第 1 步：安装 Bun 与 Git

在 PowerShell 中确认 Git 可用：`git --version`。安装 Bun 后确认版本不低于 1.3.3，推荐 v1.4.2 及以上：`bun --version`。Windows 上还需要 Node.js，可用 `node --version` 确认。

### 第 2 步：克隆并运行安装脚本

在 PowerShell 中依次执行：

1. `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git $HOME\gstack`
2. `cd $HOME\gstack`
3. `./setup`

官方给出的 Claude Code 默认安装位置是 `~/.claude/skills/gstack`，对应 Windows 下的 `$HOME\.claude\skills\gstack`。如果你希望走这条默认路径，把第 1 步的克隆目标换成 `$HOME\.claude\skills\gstack` 即可。

### 第 3 步：选择宿主

裸跑 `./setup` 只为 Claude Code 安装。要指定其他宿主用 `--host <name>`，要为本机检测到的所有宿主安装用 `--host auto`：

- `./setup --host auto`
- `./setup --host codex`
- `./setup --status`（每个安装输出一行：宿主、层级、作用域、版本、路径）

显式指定 `--host X` 只安装 X，绝不改动其他宿主的安装。`/gstack-upgrade` 会刷新它登记过的每一个安装，每个宿主一行，并报告哪些失败。

### 第 4 步：团队模式（可选，适合共享仓库）

在仓库内执行 `(cd $HOME\.claude\skills\gstack && ./setup --team) && $HOME\.claude\skills\gstack\bin\gstack-team-init required && git add .claude/ CLAUDE.md && git commit -m "require gstack for AI-assisted work"`。这样仓库里不存放任何 vendored 文件，没有版本漂移，也不用手动升级；每个 Claude Code 会话开始时做一次快速自动更新检查（限流为每小时一次，网络失败安全，完全静默）。把 `required` 换成 `optional`，队友会收到提示而不是被阻断。

### 第 5 步：接入你的日常工作流

gstack 的形态是**技能目录 + 斜杠命令**，不是 MCP 服务，也不是 Java 依赖。对 Java / Spring 项目而言，可行的融入方式是：

- 把 gstack 安装到你的 AI 编程助手能读取的技能目录下，在会话中用斜杠命令调用。
- 在项目根目录的 `CLAUDE.md` 中加入 gstack 段落，声明所有网页浏览走 gstack 的 `/browse` 技能、不要使用 `mcp__claude-in-chrome__*` 工具，并列出可用技能清单。
- 在 Spring 项目里，让 `/review` 审你的分支改动、`/qa` 打你的本地或预发接口、`/ship` 走发布流程、`/cso` 做安全审计。

> 再次强调：**官方未提供与 Trae Work / Java 的集成方式**，也没有公开的 MCP 配置路径或 SDK 接入示例。请勿自行编造配置项。

<!-- asset:code-2 start -->
```powershell
./setup --host auto
./setup --host codex
./setup --status
```
<!-- asset:code-2 end -->


<!-- asset:code-1 start -->
```powershell
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git $HOME\gstack
cd $HOME\gstack
./setup
```
<!-- asset:code-1 end -->


## 快速上手：六步判断它是否适合你

1. 完成安装（约 30 秒的安装流程）。
2. 运行 `/office-hours`，描述你正在构建的东西。
3. 对任何功能想法运行 `/plan-ceo-review`。
4. 对任何有改动的分支运行 `/review`。
5. 对你的预发 URL，或一个隔离的本地 API、CLI、任务、webhook 运行 `/qa`。
6. 到此为止。你会知道它是否适合你。

官方列出的可用技能包括：`/office-hours`、`/plan-ceo-review`、`/plan-eng-review`、`/plan-design-review`、`/design-consultation`、`/design-shotgun`、`/design-html`、`/review`、`/deslop-shared-libs`、`/test-audit`、`/ship`、`/eval-plan`、`/land-and-deploy`、`/canary`、`/benchmark`、`/browse`、`/connect-chrome`、`/qa`、`/qa-only`、`/design-review`、`/scrape`、`/setup-browser-cookies`、`/setup-deploy`、`/setup-gbrain`、`/retro`、`/investigate`、`/document-release`、`/document-generate`、`/codex`、`/cso`、`/autoplan`、`/plan-devex-review`、`/devex-review`、`/careful`、`/freeze`、`/guard`、`/unfreeze`、`/gstack-upgrade`、`/learn`。

## 如何确认安装成功

- 运行 `./setup --status`，每个已安装宿主输出一行，包含宿主、层级、作用域、版本和路径。
- 在会话中调用 `/office-hours`，能进入产品提问流程即说明技能已加载。
- 检查安装目录下是否存在技能文件；官方提到一次全局 Claude 安装从 632 个 `SKILL.md` 文件（34.7 MB）精简到它自己的 63 个（2.5 MB），可用于对照规模是否正常。
- 若 `/cso` 报告 `not assessed`，说明缺少原生工具链前置条件，其余部分通常已装好。

## 各宿主支持层级

| 宿主 | 层级 | 安装参数 | 首次调用 | 安全技能 | 外部评审需求 | 修复方式 |
|------|------|----------|----------|----------|--------------|----------|
| Claude Code | full | `--host claude`（默认） | `/office-hours` | 强制（钩子阻断） | Codex CLI，需登录 | `./setup --host claude` |
| OpenAI Codex CLI | experimental | `--host codex` → `${CODEX_HOME:-~/.codex}/skills/gstack-*/` | 请求 `gstack-office-hours` | 建议性，不阻断 | Claude Code CLI，需登录 | `./setup --host codex` |
| OpenCode | experimental | `--host opencode` → `~/.config/opencode/skills/gstack-*/` + `/gstack-*` 命令 | `/gstack-office-hours` | 建议性，不阻断 | Codex CLI，需登录 | `./setup --host opencode` |
| Cursor | experimental | `--host cursor` → `~/.cursor/skills/gstack-*/` | 请求 `gstack-office-hours` | 建议性，不阻断 | Codex CLI，需登录 | `./setup --host cursor` |
| Factory Droid | experimental | `--host factory` → `~/.factory/skills/gstack-*/` | 请求 `gstack-office-hours` | 建议性，不阻断 | Codex CLI，需登录 | `./setup --host factory` |
| Kiro | experimental | `--host kiro` → `~/.kiro/skills/gstack-*/` | 请求 `gstack-office-hours` | 建议性，不阻断 | Codex CLI，需登录 | `./setup --host kiro` |
| GitHub Copilot CLI | experimental | `--host copilot` → `~/.copilot/skills/gstack-*/` | `/gstack-office-hours` | 建议性，不阻断 | Codex CLI，需登录 | `./setup --host copilot` |
| Antigravity CLI | experimental | `--host agy`（或 `--host antigravity`）→ `~/.gemini/antigravity-cli/skills/gstack-*/` | `/gstack-office-hours` | 建议性，不阻断 | Codex CLI，需登录 | `./setup --host agy` |
| Slate | instruction-only | `--host slate`（指向 Claude 安装；Slate 读取 `.claude/skills`） | 通过 Claude 安装调用 `/office-hours` | 建议性，不阻断 | — | `./setup --host claude` |
| OpenClaw | instruction-only | `--host openclaw`（打印 digest 路径；ACP 拉起 Claude Code） | — | — | — | — |

层级含义：**full** 经过真实工作流运行认证；**experimental** 能安装并通过一致性测试，但尚无认证运行；**instruction-only** 不安装任何东西，安装脚本只打印需要复制的内容。

## 其他接入方式

**OpenClaw**：OpenClaw 通过 ACP 拉起 Claude Code 会话，因此只要 Claude Code 装了 gstack，所有 gstack 技能都能直接用。在 `AGENTS.md` 中加入「Coding Tasks」段落，告诉会话在编码时使用 gstack 技能，例如安全审计用「Load gstack. Run /cso」，代码评审用「Load gstack. Run /review」，QA 测试 URL 用「Load gstack. Run /qa https://...」，端到端做功能用「Load gstack. Run /autoplan, implement the plan, then run /ship」，先规划再动手用「Load gstack. Run /office-hours then /autoplan. Save the plan, don't implement.」。

**原生 OpenClaw 技能（通过 ClawHub）**：四个方法论技能可直接在你的 OpenClaw agent 中运行，无需 Claude Code 会话，安装命令为 `clawhub install gstack-openclaw-office-hours gstack-openclaw-ceo-review gstack-openclaw-investigate gstack-openclaw-retro`。

| 技能 | 作用 |
|------|------|
| `gstack-openclaw-office-hours` | 用 6 个逼问式问题做产品拷问 |
| `gstack-openclaw-ceo-review` | 用 4 种范围模式做战略挑战 |
| `gstack-openclaw-investigate` | 根因调试方法论 |
| `gstack-openclaw-retro` | 每周工程复盘 |

## 局限与风险

- **宿主覆盖有限**：官方认证（full 层级）的只有 Claude Code，其余宿主均为 experimental 或 instruction-only。**Trae Work 不在官方支持列表中，官方未提供集成方式。**
- **安全技能并非处处强制**：只有 Claude Code 上的安全技能是强制阻断（钩子拦截），其他宿主为建议性、不阻断。
- **`/cso` 依赖较重**：需要特定 Bun 构建标志加原生工具链，Windows 上要装 Visual Studio 2022 Build Tools 的 C++ 桌面开发组件，缺失时该技能不可用。
- **CSO 运行时镜像拉取有时间限制**：每个自动预加载有 30 秒窗口加一段有界安装配额；慢速镜像仓库可设 `GSTACK_CSO_IMAGE_PULL_TIMEOUT_SECONDS=120`（可接受范围 5–300 秒）。单个镜像超时不会占用其余镜像的窗口，安装脚本会报告部分进度，下次运行会从本地 Docker 中已有的确切 digest 继续。完整预加载上限为一小时。
- **多宿主安装会做文件清理**：为其他宿主渲染的副本会被修剪，生成文件移到 `~/.gstack/backups/host-renders/`，无法证明是 gstack 生成的文件保持原位。官方提到此举是为了避免 Cursor-agent 在技能树上卡死（#1694）。
- **许可证**：MIT，可自由 fork、改进、自用。
- **成熟度**：仓库创建于 2026-03-11，最近更新 2026-10-11，主语言 TypeScript。第三方站点标注版本为 v0.4.1，官方仓库未在已公开内容中给出对应版本号，两者口径不一致。
- **作者自述的产出数据存在争议**：官方说明中给出了「2026 年约 810 倍于 2013 年节奏」「年初至 4 月 18 日已产出 2013 年全年的 240 倍」等基于逻辑代码变更的统计，并主动回应了关于 LOC 指标的批评，附有方法论与复现脚本说明。这些是作者自述数据，非独立第三方验证。

<!-- asset:blog-2 start -->
![gstack 主要局限](/img/ai-news/garrytan-gstack/blog-2.png)

*图：gstack 主要局限*
<!-- asset:blog-2 end -->


## 社区评价（来自 Hacker News 讨论）

Hacker News 上《gstack – Garry Tan's Claude Code Setup》一帖获得 15 分、15 条评论。讨论中的真实反馈包括：

- 有评论称「这东西简直离谱。你基本上在 conductor.build 里得到一个 agent，它会从 claude 那里为你的产品和工程问题起草多选题回复。我的代码质量和开发速度都大幅提升。」
- 有评论询问它是否只针对 Claude Code，能否也装到 pi-agent 上。
- 有评论调侃「尽管名字相似，pi 和 python 毫无关系。谢天谢地。」

整体讨论热度不高，样本有限，建议结合自己的技术栈实际试用后再判断。

## 给 Java / Spring 开发者的试用建议

gstack 的价值集中在**流程角色化**：把「想清楚做什么」「锁架构」「挑生产 bug」「真浏览器 QA」「安全审计」「发布」拆成独立命令，避免一个模糊提示词包打天下。对 Spring 项目，最值得先试的是 `/review`（审分支改动）、`/qa`（打本地或预发接口）、`/cso`（安全审计）和 `/autoplan`（先出计划再实现）。

需要清醒认识的是：**它没有官方 MCP 服务形态，没有 Java SDK，也没有 Trae Work 集成路径**。如果你的日常工作流完全绑定 Trae Work，需要先确认 Trae Work 是否能读取 Claude 技能目录或自定义斜杠命令，否则只能把它当作 Claude Code 侧的辅助工具单独使用。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 后端项目，代码托管在 Git，日常需要做代码评审、接口 QA 和安全检查。我了解到 gstack 是一套面向 Claude Code 的开源斜杠命令技能包，包含 /review、/qa、/cso、/autoplan 等角色化技能，但它官方只支持 Claude Code 等宿主，没有 Trae Work 集成方式。

请你帮我完成以下事情：
1. 先检查我的机器上是否已安装 Git、Bun（版本是否 >= 1.3.3，推荐 1.4.2+）和 Node.js，把检查命令和结果列出来。
2. 给出在 Windows PowerShell 下把 gstack 克隆到 $HOME\.claude\skills\gstack 并运行 ./setup 的完整步骤，每一步说明这条命令在做什么。
3. 运行 ./setup --status 并解释输出中每一列（宿主、层级、作用域、版本、路径）的含义。
4. 判断我的 Trae Work 是否有可能读取 .claude/skills 目录或自定义斜杠命令；如果没有官方依据，请直接告诉我「官方未提供与 Trae Work 的集成方式」，不要编造配置路径或命令。
5. 如果无法接入 Trae Work，请给我一个替代方案：在 Claude Code 中对我当前 Spring Boot 项目的某个 feature 分支依次运行 /review、/qa（打本地接口）、/cso，并说明每个命令我应该提供什么输入、预期得到什么产出。
6. 最后列出这次试用中所有需要我确认的前置条件（例如 /cso 需要的 Visual Studio 2022 Build Tools 与 C++ 桌面开发组件），以及缺失时的降级表现。

要求：所有命令用 Windows PowerShell 写法；不要编造 gstack 的版本号、配置项或路径；遇到官方没有公开说明的地方，直接标注「官方未公开说明」。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
