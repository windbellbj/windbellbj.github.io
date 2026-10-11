---
layout: post
title: "ECC 上手：给编码 Agent 装上工程化操作系统"
subtitle: "71 个 Agent、311 个 Skill、记忆与安全扫描，一次装好融进你的日常开发流"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/affaan-m/ECC
- Stars：276939
- 语言：JavaScript
- 创建时间：2026-01-18
- 最近更新：2026-10-11
- 官方简介：The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.

---

## 解决什么问题

README 的定位是：你的 Agent 已经能写代码，但 ECC 给它一套协同的工程系统与工具箱——先规划再动手、用测试验证改动、从全新上下文里审查自己的工作、记住关键信息，并把反复奏效的做法沉淀成可复用的 skills 与工作流。

README 用一条流水线概括这套流程：`plan -> test -> implement -> review -> verify -> remember -> improve`。它的主张是：与其在每个 prompt 里重建这套流程，不如装一次，让它成为 Agent 工作方式的一部分。README 的口号是「Optimize the context window. Persist everything else.」（优化上下文窗口，其余一切持久化）。

README 明确说明：ECC 是 MIT 许可的开源项目，目前与 Claude Code 配合最好，有原生 Codex 与 Qoder 插件路径，并为 Cursor、OpenCode、Gemini、Zed、GitHub Copilot、Antigravity、Qwen 等 harness 提供能力受限的适配器，并提醒在假设功能对等之前先看支持状态矩阵。

## 核心概念

README 给出的核心组成与数量：

- Agents：71 个，覆盖规划、审查、构建修复、安全、架构与领域工作。
- Skills：311 个，覆盖 TDD、研究、安全、文档、前端、数据、ML、运维等。
- Commands：97 个，作为便捷入口，同时 ECC 正在转向 skills-first 的界面。
- Hooks and memory：运行时能力，包含强制约束、会话摘要、持续学习、instincts 与上下文控制。
- Rules：选择性加载的标准，按语言或项目挑选。
- AgentShield：内置扫描，覆盖 prompts、hooks、MCP 配置、权限、密钥与 agent 文件。

README 还提到三个公开标识符不可互换：GitHub 源码仓库 `affaan-m/ECC`、Claude marketplace/plugin 标识 `ecc@ecc`、npm 包 `ecc-universal`。npm 版本按版本 tag 发布（2.1、2.2……），而不是按每次提交发布；想要最新代码可以从 git 安装。

## 前置依赖

README 明确写出：

- 通用包需要 Node.js 18 或更新版本。
- Claude 插件安装还需要 Git，以及 `PATH` 中可用的 Claude Code 2.1 或更新版本。
- Qoder 的非交互 hook 环境同样适用 Node.js 18+ 的要求；其 MCP server 首次使用还需要 `npx` 与网络访问。

README 未提供针对 Java、Spring 或 Trae Work 的额外依赖说明。

## 安装与配置

README 反复强调一条原则：**每个 harness 只选一种安装方式，不要叠加安装**。同一 harness 装两次可能重复 skills、commands、hooks 或配置；装到多个 harness 则不会。

### 通用安装步骤（Windows 视角）

README 专门给了 Windows 首次使用的复制粘贴路径，按顺序为：

1. 安装 Node.js 18 或更新版本、Git、Claude Code。
2. 从 Windows 开始菜单打开 PowerShell。
3. 确认每个前置条件可用：`node --version`、`git --version`、`claude --version`。
4. 运行引导安装器：`npx ecc-universal@2.2.3 setup`。
5. 典型个人配置选择 **Global user**、**Standard** hooks，然后确认。
6. 启动新的 Claude Code 会话，运行 `/plugin list` 验证 `ecc@ecc` 已启用。

README 说明这条路径不需要克隆仓库；如果任一前置命令找不到，先安装或修复该前置条件再重跑 ECC setup。如果 npm 报版本或缓存错误，先确认 registry 版本：`npm view ecc-universal version`。

README 还列出其他包运行器的等价引导命令：pnpm 用 `pnpm dlx ecc-universal@2.2.3 setup`，Yarn 2+ 用 `yarn dlx ecc-universal@2.2.3 setup`，Bun 用 `bunx ecc-universal@2.2.3 setup`。Yarn Classic 1 不提供 `yarn dlx`，README 建议改用 `npx`、全局安装或升级 Yarn。

### 多 harness 引导

README 提供 `npx ecc-universal@2.2.3 install --guided`，可在一个流程里选择 Claude Code、Codex、Kimi Code 的任意组合，展示每个安装通道与目标位置，在首次写入前预检所有选择，并做一次最终确认。自动化场景可显式指定：`npx ecc-universal@2.2.3 install --guided --harness claude --harness codex --harness kimi --claude-scope local --claude-hooks standard --profile core --yes`。

README 还给出不写入的预检命令：`npx ecc-universal@2.2.3 install --guided --harness codex --dry-run` 与 `npx ecc-universal@2.2.3 install --profile core --target kimi --dry-run`。

### 其他可用命令

README 列出：`npx ecc-universal@2.2.3 consult "security reviews" --target claude`、`npx ecc-universal@2.2.3 install --profile minimal --target claude --with capability:machine-learning`、`npx ecc-universal@2.2.3 doctor --target kimi`。README 特别警告不要使用 `npx ecc-install --profile minimal --target claude`：`ecc-install` 是 `ecc-universal` 内部的二进制名，不是单独发布的 npm 包。

### Claude Code 原生插件路径

README 说明也可以在 Claude Code 内运行原生插件命令：`/plugin marketplace add https://github.com/affaan-m/ECC` 与 `/plugin install ecc@ecc`。README 提醒：如果选了这条路径就到此为止，不要再叠加完整手动安装；如果原生命令报已存在安装或 scope 冲突，改用 2.2 引导安装或先解决冲突的 Claude 插件 scope。

README 还说明 Claude Code 插件无法分发 `rules`，需要手动只添加你真正想要的规则包：先 `git clone https://github.com/affaan-m/ECC.git`，进入 ECC 目录，创建 `~/.claude/rules/ecc`，再复制 `rules/common`，并按你的技术栈复制对应语言包（README 示例用的是 `rules/typescript`，并注明替换成你自己的栈）。README 建议从 `rules/common` 加一个你实际使用的语言或框架包开始；如果装了插件，就不要之后运行 `./install.sh --profile full`。

README 还给出声明式写法：在 `~/.claude/settings.json` 中加入 `extraKnownMarketplaces`（source 为 github、repo 为 `affaan-m/ECC`）与 `enabledPlugins`（`ecc@ecc` 为 true），效果等同上面两条 `/plugin` 命令。

### 低上下文 / 无 hooks 路径

README 提供 `npx ecc-universal@2.2.3 install --profile minimal --target claude`，源码检出下的等价命令是 `./install.sh --profile minimal --target claude`，Windows 下是 `.\install.ps1 --profile minimal --target claude`。该 profile 有意排除 `hooks-runtime`。

README 说明：任何会落地 hook runtime 的安装都需要显式决定；没有 `--enable-hooks` 或 `--no-hooks` 时，安装器会先打印 hooks 能做什么，然后停止写入。引导安装器会交互式询问这个选择。

### 融入 Trae Work 与 Java 日常工作流

README 未提供与 Trae Work / Java 的集成方式。README 中出现的 harness 与编辑器目标为 Claude Code、Codex、Qoder、Cursor、OpenCode、Gemini、Zed、Antigravity、Qwen、Hermes、OpenClaw、Kimi、CodeBuddy、JoyCode、GitHub Copilot，未提及 Trae Work，也未提供 MCP 服务接入、Skill 目录投放、SDK 或 HTTP 集成方式。README 提到对没有原生 ECC 目标的 harness，可参考 manual adaptation guide，把一小部分 ECC skills 与工作流指令带进聊天式工具，但不假装 hooks 或原生 skill 发现可用。

## 最小可用示例

下面这段指令可直接整段复制给 Trae Work 等 AI 编程助手，用于在 Java/Spring 项目里试用 ECC 的工作流思路（注意：README 未提供 Trae Work 集成方式，此处仅借用其流程理念，不代表 ECC 已在 Trae Work 中安装成功）。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring Boot 后端项目，代码库已有单元测试与集成测试。

目标：请按 ECC 的工程流程理念，帮我完成一个小需求的端到端改动，而不是直接给代码。

要求：
1. 先规划：用要点列出你打算改哪些类、哪些接口、影响哪些调用方，等我确认后再动手。
2. 再测试：先写出或补充能复现该需求的失败测试（JUnit），说明测试放在哪个目录、断言什么。
3. 后实现：给出最小改动的 Java 代码，保持现有分层与命名风格，不要引入新的第三方依赖。
4. 自审查：换一个全新视角审查这次改动，指出潜在的空指针、并发、事务边界与兼容性问题。
5. 再验证：给出我应该在本地执行的验证步骤（编译、跑哪些测试、如何手工调用接口确认）。
6. 最后沉淀：把这次改动中可复用的经验总结成 3 条以内的规则，方便我下次直接复用。

约束：每一步都先说明你要做什么再输出内容；涉及不确定的地方直接说不确定，不要编造 API 或配置。
```

## 验证方法

README 给出的可执行验证步骤：

1. 启动一个新的 Claude Code 会话，运行 `/plugin list`，确认 `ecc@ecc` 已启用（这是 README 在 Windows 首次使用路径中给出的验证方式）。
2. 使用 `node scripts/ecc.js list-installed` 列出已安装内容。
3. 使用 `node scripts/ecc.js doctor` 做诊断。
4. 如果本地 Claude 配置被清空或重置，README 建议先跑 `node scripts/ecc.js list-installed`，再跑 `node scripts/ecc.js doctor` 与 `node scripts/ecc.js repair`，通常能在不重建整套配置的情况下恢复 ECC 管理的文件。
5. 安装前想先看文件计划，可用 `node scripts/ecc.js consult "security reviews" --target claude` 返回匹配组件、相关 profile 与预览/安装命令。
6. Codex 路径可用 `codex plugin list --json` 与 `node scripts/codex/check-plugin-cache.js` 检查。

README 未提供针对 Trae Work 或 Java 项目的验证方法。

## 风险与注意事项

README 明确提示的风险与约束：

- **只从官方渠道安装**：README 用 WARNING 强调只从 GitHub 仓库 `github.com/affaan-m/ECC`、npm 包 `ecc-universal` 与 `ecc-agentshield`、GitHub App、插件 slug `ecc@ecc`、官网 `ecc.tools` 安装；第三方重新上传与非官方镜像不由项目维护或审查，可能包含恶意软件。
- **不要叠加安装方式**：同一 harness 装两次可能重复 skills、commands、hooks 或配置。README 列出「可行」与「避免」的组合，并说明如果已经叠加安装且出现重复，直接跳到 Reset / Uninstall ECC。
- **版本固定不等于安全审计**：README 说明示例选择已发布的 ECC 2.2.3 版本，但版本固定不是安全审计或完整性检查；运行包代码前应审查发布源码与 registry 完整性，未发布改动请使用已审查的检出。
- **hooks 需要显式决定**：任何会落地 hook runtime 的安装都需要显式选择，否则安装器会打印说明后停止写入。
- **平台能力不对等**：README 提醒在假设功能对等前先看支持状态矩阵；Codex 原生 hooks 需要显式信任决定，且不使用 Claude 的四档 ECC hook profile；Qoder 不会把完整 Claude hook profile 复制过去，阻塞式工具 hooks、异步 stop 任务与 Claude 专有 matcher 不在初始原生集成范围内。
- **命名不可互换**：`affaan-m/ECC`、`ecc@ecc`、`ecc-universal` 三者用途不同；旧文章里的长 marketplace 标识只应视为遗留别名。
- **ECC 不会自动上传诊断信息**：README 在安装问题一节中说明 ECC never uploads diagnostics automatically。

README 未提供关于 Java 项目、Trae Work 或 Windows 特定安全风险的其他说明。

## 替代方案

README 未提供替代方案章节，也未列出与 ECC 功能对标的其他工具。README 仅说明：对没有原生 ECC 目标的 harness，可使用 manual adaptation guide，把一小部分 ECC skills 与工作流指令带入聊天式工具；以及 ECC Pro 是面向私有仓库的托管 GitHub App，开源部分永久保持 MIT 许可。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
