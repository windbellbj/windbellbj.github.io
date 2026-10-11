---
layout: post
title: "gstack：把 Claude Code 变成 23 人虚拟工程团队"
subtitle: "YC 总裁 Garry Tan 开源的全套 AI 开发工作流，30 秒装好就能跑"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/garrytan/gstack
- Stars：135939
- 语言：TypeScript
- 创建时间：2026-03-11
- 最近更新：2026-10-11
- 官方简介：Use Garry Tan's exact Claude Code setup: 23 opinionated tools that serve as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, and QA

---

## 解决什么问题

gstack 要解决的是「一个人怎么像二十人团队一样交付」的问题。README 开篇引用 Andrej Karpathy 的话说明这一变化：他已经很久没有亲手敲过一行代码。作者 Garry Tan 是 Y Combinator 的总裁兼 CEO，他称 gstack 就是自己的答案——过去 60 天里，他在全职运营 YC 的同时交付了 3 个生产服务、40 多个功能。

README 给出的核心判断是：gstack 把 Claude Code 变成一个虚拟工程团队——一个重新思考产品的 CEO、一个锁定架构的工程经理、一个抓 AI 垃圾设计的设计师、一个找生产 bug 的评审、一个开真实浏览器的 QA 负责人、一个跑 OWASP + STRIDE 审计的安全官，以及一个负责发 PR 的发布工程师。共 23 个专家角色和 8 个强力工具，全部是斜杠命令、全部是 Markdown、全部免费、MIT 许可。

README 明确的目标用户是：创始人和 CEO（尤其是还想亲手交付的技术型创始人）、第一次使用 Claude Code 的人（用结构化角色替代空白提示词）、技术负责人和资深工程师（在每次 PR 上做严格评审、QA 和发布自动化）。

## 核心概念

gstack 是一个流程，不是一堆工具的集合。README 用一句话概括它的运行顺序：**Think → Plan → Build → Review → Test → Ship → Reflect**。每个技能的输出喂给下一个技能：`/office-hours` 写出的设计文档会被 `/plan-ceo-review` 读取，`/plan-eng-review` 写出的测试计划会被 `/qa` 接手，`/review` 抓到的 bug 由 `/ship` 验证是否修好。

README 中列出的主要技能角色包括：

- `/office-hours`：YC 式办公时间，六个逼问式问题，在写代码前重构你的产品定位，产出设计文档。
- `/plan-ceo-review`：CEO / 创始人视角，四种模式（Expansion、Selective Expansion、Hold Scope、Reduction）。
- `/plan-eng-review`：工程经理视角，锁定架构、数据流、图、边界情况和测试。
- `/plan-design-review`、`/design-review`：设计评审与修复，含 AI Slop 检测。
- `/review`：资深工程师视角，找能过 CI 但在生产爆炸的 bug，自动修复明显问题。
- `/qa`、`/qa-only`：QA 负责人 / 报告员，探索浏览器、API、CLI、任务和 webhook 行为。
- `/cso`：首席安全官，带应用模型、独立挑战和显式覆盖范围的安全审计。
- `/ship`、`/land-and-deploy`、`/canary`：发布工程师与 SRE 视角，从同步主干、跑测试到合并 PR、等 CI、验证生产健康。
- `/document-release`、`/document-generate`：技术写作者，按 Diataxis 框架生成或审计文档。
- `/retro`：工程经理视角的每周回顾，`/retro global` 可跨所有项目和 AI 工具运行。
- `/browse`、`/scrape`、`/setup-browser-cookies`：给 agent 装上眼睛，驱动浏览器。
- `/autoplan`：一条命令跑完 CEO → 设计 → DX → 工程评审的完整流水线。

此外还有 `/investigate`（系统化根因调试，铁律是「不调查不修复」）、`/test-audit`、`/deslop-shared-libs`、`/benchmark`、`/eval-plan`、`/pair-agent` 等。

## 前置依赖

README 明确列出的依赖如下：

- Claude Code（默认宿主）
- Git
- Bun v1.4.2+（这是测试过的版本；setup 会拒绝低于 1.3.3 的 Bun，因为那会让编译后的工具读到项目的 `.env`，中间版本会给出警告）
- Node.js（仅 Windows 需要）

macOS 上推荐安装 Aside 浏览器（macOS 15+）：浏览器类技能、`/make-pdf` 和 `/diagram` 会优先驱动它，使用你真实的已登录会话。没有 Aside 时，`./setup` 会构建 gstack 自带的浏览器，同样的技能改用那个。

`/cso` 额外需要：一个带全部四个 `--no-compile-autoload-*` 构建标志的 Bun 版本，以及原生工具链——Linux 上需要支持静态编译的 C 编译器，macOS 上需要 Xcode 命令行工具，Windows 上需要带「使用 C++ 的桌面开发」的 Visual Studio 2022 Build Tools。如果这些缺失，setup 会安装其他所有内容、移除过期的 CSO 辅助文件，`/cso` 会报告 `not assessed` 并说明前置条件。

README 未提供对 Trae Work 的任何依赖说明。

## 安装与配置

README 给出的安装方式全部围绕 Claude Code 展开，标准流程约 30 秒（作者在 4 vCPU Linux 云机器、干净 HOME 环境下实测 `./setup` 耗时 31 秒，含二进制构建和 Chromium 下载；网络慢和笔记本会更久）。

**通用安装步骤（README 原文路径）：**

1. 打开 Claude Code，把 README 中给出的安装指令粘贴进去，让 Claude 执行。
2. 该指令要求运行 `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`。
3. 然后在 CLAUDE.md 中加入一个「gstack」小节，说明所有网页浏览都使用 gstack 的 `/browse` 技能、绝不使用 `mcp__claude-in-chrome__*` 工具，并列出可用技能清单（`/office-hours`、`/plan-ceo-review`、`/plan-eng-review`、`/plan-design-review`、`/design-consultation`、`/design-shotgun`、`/design-html`、`/review`、`/deslop-shared-libs`、`/test-audit`、`/ship`、`/eval-plan`、`/land-and-deploy`、`/canary`、`/benchmark`、`/browse`、`/connect-chrome`、`/qa`、`/qa-only`、`/design-review`、`/scrape`、`/setup-browser-cookies`、`/setup-deploy`、`/setup-gbrain`、`/retro`、`/investigate`、`/document-release`、`/document-generate`、`/codex`、`/cso`、`/autoplan`、`/plan-devex-review`、`/devex-review`、`/careful`、`/freeze`、`/guard`、`/unfreeze`、`/gstack-upgrade`、`/learn`）。
4. 最后询问用户是否也要把 gstack 加到当前项目，让队友也能用。

**团队模式（README 推荐）：** 在仓库内运行 `(cd ~/.claude/skills/gstack && ./setup --team) && ~/.claude/skills/gstack/bin/gstack-team-init required && git add .claude/ CLAUDE.md && git commit -m "require gstack for AI-assisted work"`。README 说明这样仓库里没有 vendored 文件、没有版本漂移、无需手动升级；每个 Claude Code 会话开始时做一次快速自动更新检查（限流为每小时一次、网络失败安全、完全静默）。把 `required` 换成 `optional` 则是提醒而非阻止队友。

**安装到其他 agent：** 裸跑 `./setup` 只为 Claude Code 安装。用 `--host <name>` 选择其他 agent，或用 `--host auto` 为机器上检测到的每个 agent 安装。README 给出的示例是 `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack`，然后 `cd ~/gstack && ./setup --host auto`（或 `./setup --host codex`），再用 `./setup --status` 查看每个安装的 host、tier、scope、version、path。README 列出的宿主包括 Claude Code（full）、OpenAI Codex CLI、OpenCode、Cursor、Factory Droid、Kiro、GitHub Copilot CLI、Antigravity CLI（均为 experimental），以及 Slate、OpenClaw、Hermes、GBrain（instruction-only）。

**instruction-only 方式：** 把 `agents-digest/gstack-AGENTS.md` 这个 2KB 摘要复制到你的 agent 会读取的位置（例如追加到项目的 `AGENTS.md`）。它携带 gstack 的理念、复用阶梯和语气规则，无需安装。摘要第一行显示其 gstack 版本，升级后需要重新复制。

**关于 Trae Work 与 Java：** README 未提供与 Trae Work / Java 的集成方式。README 中出现的宿主列表不包含 Trae Work，也没有提到 MCP 服务接入、Java SDK 或 Spring 集成。因此无法给出在 Trae Work 中安装 gstack 的可靠步骤。

## 最小可用示例

README 的「See it work」章节展示了一个完整流程：用户说想做一个日历每日简报应用，然后依次运行 `/office-hours`、`/plan-ceo-review`、`/plan-eng-review`，批准计划后 agent 在 11 个文件中写了 2,400 行（约 8 分钟），接着 `/review` 自动修复 2 个问题并询问一个竞态条件修复，`/qa https://staging.myapp.com` 打开真实浏览器点击流程并找到并修复一个 bug，最后 `/ship` 让测试从 42 个增加到 51 个并开出 PR。

下面这段指令可以直接整段复制给 Trae Work 等 AI 编程助手，用于在 Java 项目上试用 gstack 的思路（注意：README 未提供 Trae Work 集成方式，此指令仅用于让助手按 gstack 的方法论协助你，不代表 gstack 已在 Trae Work 中安装）：

```text
背景：我是一个 Java 后端程序员，在 Windows 上用 Trae Work 开发，技术栈以 Java / Spring 为主。我在 GitHub 上看到 garrytan/gstack 这个项目，它把 Claude Code 变成一套虚拟工程团队（23 个专家角色 + 8 个工具，全部是斜杠命令和 Markdown，MIT 许可），流程是 Think → Plan → Build → Review → Test → Ship → Reflect。

目标：请参照 gstack 的方法论，帮我把手头这个 Spring 服务的一个新功能从想法推进到可提交的 PR。

要求：
1. 先扮演 /office-hours 的角色，用逼问式提问帮我重新审视这个功能到底要解决什么痛点，不要直接接受我的功能描述，指出我可能没说出口的真实需求。
2. 再扮演 /plan-eng-review 的角色，锁定架构、数据流、边界情况和测试计划，把隐藏假设摆到明面上。
3. 然后给出实现方案，说明要改哪些类、哪些接口、哪些配置。
4. 最后扮演 /review 的角色，指出这段实现里能过 CI 但可能在生产出问题的点，以及哪些测试是无效的。
5. 全程用中文回答，涉及代码时给出 Java / Spring 的具体写法。
6. 如果某一步你缺少必要信息，先问我，不要自己编造。
```

## 验证方法

README 给出的验证路径是：

1. 按 Quick start 的顺序执行：先安装 gstack，然后运行 `/office-hours` 描述你在构建什么。
2. 对任何功能想法运行 `/plan-ceo-review`。
3. 对任何有改动的分支运行 `/review`。
4. 对你的 staging URL，或一个隔离的本地 API、CLI、任务、webhook 运行 `/qa`。
5. README 明确说：到这里就停下来，你会知道这东西是否适合你。

如果安装了多个宿主，可以用 `./setup --status` 查看每个安装的 host、tier、scope、version、path 一行。`/gstack-upgrade` 会刷新它注册过的每个安装，每个宿主一行，并说明哪些失败了。

README 未提供针对 Trae Work 的验证方法。

## 风险与注意事项

- **Bun 版本有硬性门槛。** README 说明 setup 会拒绝低于 1.3.3 的 Bun，因为那会让编译后的工具读到项目的 `.env`；1.3.3 到 1.4.2 之间会给出警告。
- **`/cso` 可能无法完整运行。** 它需要带全部四个 `--no-compile-autoload-*` 构建标志的 Bun 加原生工具链。缺失时 setup 会安装其他内容并移除过期 CSO 辅助文件，`/cso` 报告 `not assessed`。README 还说明：目前尚未发布合格的运行时或扫描器 profile，因此审计只做静态评估；项目测试完成度仍标记为 `self_reported`，因为目标代码控制测试过程。
- **CSO 镜像预加载有超时。** 每个自动预加载有 30 秒窗口加一个有界 setup 额度；慢速 registry 可设置 `GSTACK_CSO_IMAGE_PULL_TIMEOUT_SECONDS=120`（接受范围 5–300 秒）。一个镜像超时不消耗其余镜像的窗口，setup 会报告部分进度，后续运行会从本地 Docker 中已有的确切 digest 继续。完整预加载上限为一小时。
- **模型选择不会静默回退。** README 说明如果选择的模型无效或账号无法使用，gstack 会停下并给出修复信息，把外部评审报告为不可用，绝不静默切换到默认值。嵌套 Codex 评审还会隐藏已安装技能运行（`-c skills.include_instructions=false`），以免评审变成整个嵌套技能运行。
- **Copilot 与 Antigravity 有特殊限制。** Copilot 忽略技能 hooks，所以 `/careful` 和 `/freeze` 在那里只是建议；`COPILOT_HOME` 不是 `~/.copilot` 时 setup 会拒绝且不做任何改动。Antigravity CLI 只写 `~/.gemini/antigravity-cli/skills/gstack*`，从不触碰 Gemini CLI 的 `~/.gemini/skills` 和设置。
- **`/claude` 已改名。** 现在叫 `/claude-code`，需要重新运行 `./setup --host <name>` 迁移受管安装。
- **README 未提供**关于数据隐私、许可证之外的合规要求、Java 生态兼容性或 Trae Work 兼容性的说明。

## 替代方案

README 未提供替代方案章节，也未与其他同类工具做对比。README 中提到的相邻项目只有：OpenClaw（Peter Steinberger 构建，README 称其有 247K GitHub stars，gstack 可通过 ACP 在其中工作）、ClawHub（可安装四个原生 OpenClaw 技能：`gstack-openclaw-office-hours`、`gstack-openclaw-ceo-review`、`gstack-openclaw-investigate`、`gstack-openclaw-retro`），以及 impeccable、Google Stitch 等会读取 `DESIGN.md` 的工具。README 未提供这些是否可作为 gstack 替代品的说明。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
