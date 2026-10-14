---
layout: post
title: "Impeccable 使用说明：让 AI 编码助手学会做设计"
subtitle: "1 个 Skill、24 条命令、59 条确定性检测规则，把 AI 生成的千篇一律前端界面拉回设计水准"
date: 2026-10-15 04:23:58 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI技能
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/pbakaus/impeccable
- Stars：81164
- 语言：JavaScript
- 创建时间：2025-11-16
- 最近更新：2026-10-14
- 官方简介：The design language that makes your AI harness better at design.

---

> Impeccable 是一套给 AI 编码助手用的「设计语言」：它把设计判断力、反套路规则和浏览器实时迭代能力打包成一个 Skill，让 Claude Code、Cursor、Trae 等工具在写前端时不再产出千篇一律的模板脸。最适合用 AI 写前端、但苦于界面「一眼 AI」的全栈与后端开发者。

## 它解决什么问题

所有模型都在同一批 SaaS 模板上训练过。跳过设计指导，你会在每个项目里看到同样的几个破绽：什么都用 Inter 字体、紫到蓝的渐变、卡片里再套卡片、彩色背景上放灰字、每个标题上方都顶着一个圆角方块图标。

Impeccable 的定位就是补上这块：给 Agent 一套共享的设计词汇，让它在动手前先想清楚受众、目的、使用场景和约束，动手时遵守明确的反模式清单，动手后还能用确定性规则自动挑错。

官方给出的能力清单：

| 组成 | 说明 |
|------|------|
| 1 个 Skill | 通过 `/impeccable <command> <target>` 调用 |
| 24 条命令 | `polish`、`audit`、`critique`、`distill`、`animate`、`bolder`、`quieter` 等 |
| 59 条确定性检测规则 | CLI 与浏览器扩展可在无 LLM、无 API Key 的情况下运行 |
| 实时浏览器迭代 | `live` 与 `generate` 命令在浏览器里直接改元素 |

## 核心概念

**PRODUCT.md 与 DESIGN.md 分工明确。** `/impeccable init` 会检查项目，只追问真正缺失的产品事实，然后写入 `PRODUCT.md`，记录受众、目的、运行环境、约束、语气和证据。视觉方向则单独记录在 `DESIGN.md`，两者不混为一谈。

**命令即设计词汇。** 所有命令都走 `/impeccable` 前缀，例如：

- `/impeccable craft`：先定形态再构建，带视觉迭代的完整流程
- `/impeccable shape`：写代码前先规划 UX/UI
- `/impeccable critique`：UX 设计评审，看层级、清晰度、情感共鸣
- `/impeccable audit`：技术质量检查，覆盖无障碍、性能、响应式
- `/impeccable polish`：交付前最后一轮，对齐设计系统
- `/impeccable harden`：错误处理、国际化、文本溢出、边界情况

也可以用 `/impeccable pin <command>` 生成独立快捷方式，例如 `pin audit` 之后就能直接敲 `/audit`。

**反模式清单是硬约束。** 官方明确列出要避免的做法：不用被滥用的字体（Arial、Inter、系统默认）、不在彩色背景上用灰字、不用纯黑纯灰（永远带色调）、不把所有东西都塞进卡片、不嵌套卡片、不用弹跳/弹性缓动。

**验证是有界多轮，不是死循环。** 官方强调：完整构建一次，用一批检查（Web 端桌面与移动一起）看一遍，一次性修完所有问题，最多再确认一轮就停手。开放式自我 QA 是在烧用户的钱。

## 环境与前置依赖

- **Skill 本身不需要运行时。** 每份 Skill 都自带一个小启动器（`scripts/impeccable`，Windows 下是 `impeccable.cmd`），它运行 Impeccable 引擎——一个自包含二进制文件，要么就在启动器旁边，要么首次运行时下载到 `~/.impeccable/bin/`。
- **Node 只在用 `npx impeccable` 安装器时才涉及**，它只是同一个二进制的壳；手动复制和 Git 子模块两种方式完全不需要 Node。
- **Windows 上没有 `sh` 时**，调用 `impeccable.cmd` 而不是 `impeccable`。
- 官方支持的工具包括 Cursor、Claude Code、Gemini CLI、Codex CLI、Grok Build、Hermes Agent、Veto、Trae 等。

## 安装与配置

### 方式一：CLI 安装器（推荐）

在项目根目录执行：

```powershell
npx impeccable install
```

它会列出检测到的 harness 目录或已安装 CLI（例如 `~/.claude`、`~/.codex`、`~/.grok`、`~/.hermes`、`~/.veto`，或项目内的 `.cursor`），让你保留检测结果或自定义提供方，然后询问装到当前项目还是全局。脚本里可以用 `--providers=claude,codex,cursor,grok,hermes,veto` 和 `--scope=project|global` 跳过这两步选择。

更新已有安装：

```powershell
npx impeccable update
```

> Codex 用户在安装或更新后要打开 `/hooks` 并在提示时批准项目 hook。Codex 按 hook 定义追踪信任，改动 `.codex/hooks.json` 的更新可能再次要求批准。Grok Build 用户需要先信任项目文件夹（`/hooks-trust` 或带 `--trust` 启动），`.grok/hooks/` 下的脚本才会运行。

### 方式二：Git 子模块

适合想把 Impeccable 纳入版本管理、通过 Git 更新的团队：

```powershell
git submodule add https://github.com/pbakaus/impeccable .impeccable
npx impeccable link --source=.impeccable --providers=claude,cursor
git add .gitmodules .impeccable .claude .cursor
git commit -m "Add Impeccable skills"
```

提供方按项目需要选择，可选值包括 `claude`、`cursor`、`gemini`、`codex`、`github`、`grok`、`hermes`、`opencode`、`pi`、`qoder`、`trae`、`trae-cn`、`rovo-dev`、`vibe`、`veto`。该命令从 `.impeccable/dist/universal/` 链接单个 Skill 文件夹，除非加 `--force`，否则不会动已存在的真实 Skill 目录。

后续更新：

```powershell
git submodule update --remote .impeccable
npx impeccable link --source=.impeccable --providers=claude,cursor
```

### 方式三：插件安装

**VS Code 里的 GitHub Copilot：**从 Visual Studio Marketplace 安装，或执行 `code --install-extension renaissance-geek.impeccable`。要求 VS Code 1.109.3+、Copilot Chat 访问权限和受信任的本地工作区。在 Chat 的 Agent 模式下试 `/impeccable polish`。这是纯 Skill 扩展，不装自动 hook，注意别在同一工作区/配置里重复安装。

**Claude Code：**`/plugin marketplace add pbakaus/impeccable`，然后打开 `/plugin` 从列表安装。

**Grok Build：**`grok plugin install pbakaus/impeccable#plugin --trust`。`#plugin` 后缀装的是精简插件包（skills、agents、hooks），不是完整 monorepo。

### 方式四：从官网下载

访问 impeccable.style，下载对应工具的 ZIP，解压到项目里。

### 方式五：从仓库复制

**Trae（与你最相关）：**

```powershell
# Trae 国内版
cp -r dist/trae/.trae-cn/skills/* ~/.trae-cn/skills/

# Trae 国际版
cp -r dist/trae/.trae/skills/* ~/.trae/skills/
```

> Trae 有两个版本，配置目录不同：国内版是 `~/.trae-cn/skills/`，国际版是 `~/.trae/skills/`。复制完成后需要重启 Trae IDE 才能激活 Skill。

其他工具的项目内复制路径：Cursor 用 `cp -r dist/cursor/.cursor your-project/`；Claude Code 用 `cp -r dist/claude-code/.claude your-project/`；OpenCode 用 `cp -r dist/opencode/.opencode your-project/`；Pi 用 `cp -r dist/pi/.pi your-project/`；Gemini CLI 用 `cp -r dist/gemini/.gemini your-project/`；GitHub Copilot 用 `cp -r dist/github/.github your-project/`；Grok Build 用 `cp -r dist/grok/.grok your-project/`。

> Cursor 的 Skill 需要额外设置：在 Cursor Settings → Beta 切到 Nightly 通道，并在 Cursor Settings → Rules 里启用 Agent Skills。Gemini CLI 需要先装预览版 `npm i -g @google/gemini-cli@preview`，再在 `/settings` 里启用「Skills」，用 `/skills list` 验证。

### 融入 Trae Work 的日常工作流

对在 Windows 上用 Trae Work 写 Java / Spring 的你，落地路径是**把 Impeccable 作为 Skill 放进 Trae 的技能目录**：

1. 在项目根目录执行 `npx impeccable install`，在提供方选择里保留或勾选 `trae` / `trae-cn`。
2. 或者手动复制：国内版执行 `cp -r dist/trae/.trae-cn/skills/* ~/.trae-cn/skills/`，国际版执行 `cp -r dist/trae/.trae/skills/* ~/.trae/skills/`。
3. 重启 Trae IDE 激活 Skill。
4. 在 Trae 的对话里输入 `/impeccable init` 完成一次性初始化。

> 官方未提供与 Trae Work / Java 的集成方式，也没有 MCP 服务形态或 Java SDK。Impeccable 面向的是前端界面设计，Spring 后端代码本身不在它的作用范围内；如果你的 Spring 项目里包含 Thymeleaf、JSP 或前后端一体的页面，可以把它当作页面层的设计助手来用。

## 快速上手

1. 在项目根目录运行 `npx impeccable install`。
2. 在 AI 编码工具里运行 `/impeccable init`。它会检查项目、只追问真正缺失的产品事实，并写出 `PRODUCT.md`。访客模式和视觉方向留到每个界面单独决定；既有的或新建的视觉系统单独记录在 `DESIGN.md`。
3. 用具体命令干活，例如：

```text
/impeccable audit blog           # 审计博客首页 + 文章页
/impeccable critique landing     # UX 设计评审
/impeccable polish settings      # 交付前最后一轮
/impeccable harden checkout      # 补错误处理 + 边界情况
```

也可以直接描述需求，例如 `/impeccable redo this hero section`。

4. 想固定常用命令，用 `/impeccable pin <command>`，例如 `pin audit` 之后直接敲 `/audit`。

<!-- asset:code-1 start -->
```powershell
/impeccable audit blog           # 审计博客首页 + 文章页
/impeccable critique landing     # UX 设计评审
/impeccable polish settings      # 交付前最后一轮
/impeccable harden checkout      # 补错误处理 + 边界情况
```
<!-- asset:code-1 end -->


## 如何确认安装成功

- 安装器会打印它检测到的 harness 目录或已安装 CLI，确认列表里有你的 Trae 目录。
- 重启 Trae 后，在对话里输入 `/impeccable`，能触发命令补全或命令表即说明 Skill 已加载。
- 每个会话开始时，Skill 会运行一次 `<skill-base-dir>/scripts/impeccable context`（Windows 无 `sh` 时用 `impeccable.cmd`），加载 `PRODUCT.md`、`DESIGN.md` 和对应界面简报。如果启动器不可用，Agent 会先发一条消息说明「Context loading did not run; I'll read the existing project context directly.」，然后直接读现有的 `PRODUCT.md` 和 `DESIGN.md`，不臆造缺失内容。

## 局限与风险

- **只做前端设计。** 它不参与 Spring 后端逻辑、接口设计或数据库层，别指望它提升 Java 代码质量。
- **需要人工把关。** 官方明确要求：改事实性文案或新增声明前必须先问；精修保留原有身份、行为和范围外的一切，重设计才是替换。
- **验证轮次有上限。** 官方刻意限制自我 QA 轮次，如果你期待它无限打磨，会与设计取向冲突。
- **平台差异。** Hermes 上不安装设计 hook（没有 hook 面），项目级安装后需要跑一次 `hermes skills trust`；Veto 收到的是打包 Skill，放在 `~/.veto/skills/` 下，不运行原生 Impeccable 编辑 hook。
- **许可证与费用：**官方未公开说明具体许可证条款；官网与社区多次强调「免费」，但正式授权信息暂无公开资料。

<!-- asset:blog-1 start -->
![使用前需知的边界](/img/ai-news/pbakaus-impeccable/blog-1.png)

*图：使用前需知的边界*
<!-- asset:blog-1 end -->


## 社区评价

来自 Hacker News 讨论及公开社交平台的真实反馈：

- 「Uninstall whatever frontend skill you're using. Replace it with Impeccable.」
- 「Impeccable is the most slept on tool for incorporating design thinking into coding workflows.」
- 「This is probably what Figma Make should be.」
- 「Impeccable is hands down the best UI design skill out there. I use it daily and recommend it to others as well.」
- 「It has taken my ability to ship complex and beautiful designs to another level.」
- 「Claude skills are mostly BS. These ones are the rare, truly useful ones.」
- 「It's crazy that @impeccable_ai is free. It replaces some paid products while being better than them.」

也有用户提到它带来了「第一次真正感受到 AI 带来的 10 倍生产力提升」。整体评价集中在两点：反套路效果明显、免费且质量超出预期。

## 命令速查

| 命令 | 作用 |
|------|------|
| `craft` | 先定形态再构建，带视觉迭代的完整流程 |
| `init` | 一次性初始化：收集产品上下文、写 PRODUCT.md、配置实时模式、推荐下一步 |
| `document` | 从现有项目代码生成根目录 DESIGN.md |
| `extract` | 把可复用组件和 token 抽进设计系统 |
| `shape` | 写代码前规划 UX/UI |
| `critique` | UX 设计评审：层级、清晰度、情感共鸣 |
| `audit` | 技术质量检查（无障碍、性能、响应式） |
| `polish` | 最后一轮：对齐设计系统、准备交付 |
| `bolder` / `quieter` | 放大无聊的设计 / 收敛过于大胆的设计 |
| `distill` | 剥离到本质 |
| `harden` | 错误处理、国际化、文本溢出、边界情况 |
| `onboard` | 首次运行流程、空状态、激活路径 |
| `animate` / `colorize` / `typeset` / `layout` | 加动效 / 引入策略性色彩 / 修字体层级 / 修布局节奏 |
| `delight` / `overdrive` | 加惊喜时刻 / 加技术性炫技效果 |
| `clarify` / `adapt` / `optimize` | 改文案 / 适配设备 / 性能优化 |
| `live` / `generate` | 浏览器里的视觉变体模式 / 自动生成指定元素的变体 |

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring 项目，项目里包含需要自己写的前端页面（Thymeleaf 模板 / 静态页面）。我打算用 Impeccable 这个设计 Skill 来提升页面质量，避免 AI 生成千篇一律的界面。

目标：把 Impeccable 接入我的 Trae Work 工作流，并完成一次真实的页面改造。

具体要求：
1. 先确认我的 Trae 是国际版还是国内版，据此把 Impeccable 的 Skill 复制到 ~/.trae/skills/ 或 ~/.trae-cn/skills/，然后提醒我重启 Trae IDE。
2. 重启后，引导我在项目根目录执行 /impeccable init，帮我梳理这个 Spring 项目的受众、目的、使用场景和约束，生成 PRODUCT.md。
3. 挑一个我项目里现有的页面，先用 /impeccable critique 做一次 UX 评审，再用 /impeccable audit 跑技术质量检查（无障碍、性能、响应式），把发现的问题列成清单。
4. 按清单一次性修完，最后用 /impeccable polish 做交付前收尾。
5. 全程遵守 Impeccable 的反模式清单：不用 Inter / Arial / 系统默认字体，不在彩色背景上用灰字，不用纯黑纯灰，不嵌套卡片，不用弹跳缓动。
6. 每一步都告诉我你在执行哪条命令、改动了哪些文件，改动前先说明理由。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
