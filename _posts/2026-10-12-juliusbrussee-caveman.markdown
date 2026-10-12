---
layout: post
title: "Caveman 使用说明：让编码 Agent 少说少读、省下 65% token"
subtitle: "一个技能包加一个本地代理，压缩 Agent 的输出与输入；Windows + Trae Work 的 Java 程序员怎么装、怎么试、值不值"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI技能
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/JuliusBrussee/caveman
- Stars：111058
- 语言：Go
- 创建时间：2026-04-04
- 最近更新：2026-10-11
- 官方简介：🪨 why use many token when few token do trick. Viral skill + proxy for coding agents that cuts 65% of tokens by talking like a caveman.

---

> Caveman 是一套给编码 Agent 用的「省 token」方案：一个技能包让 Agent 说话变短（代码、路径、数字原样不动），一个本地代理让它读进去的日志、CSV、JSON、测试输出大幅变小。最适合按 token 计费、又天天泡在 Claude Code / Codex / Cursor 这类 Agent 里的开发者；如果你在 Trae Work 里写 Java / Spring，它目前只能以「技能包」的形式间接用上，代理那条路走不通。

## 它到底解决什么问题

Agent 的账单和等待时间，一半花在它**说**的话上，一半花在它**读**的东西上。Caveman 把这两块分开处理：

| 方向 | 手段 | 官方给出的效果 |
|---|---|---|
| 输出（Agent 说的话） | 技能包，改变回答风格 | `/caveman` 在「Answer concisely.」基础上再省 3%，`/ultracave` 再省 35% |
| 输入（Agent 读的东西） | 本地代理，压缩日志/CSV/YAML/JSON/测试输出 | 单文件缩小 98.5%–99.1%，整段会话输入 token 少 33.2% |
| 网页内容 | `caveman browse` | 200 行表格页面 121 token，对比 Playwright 快照的 15,704 token，小 129.8 倍 |
| 记忆文件（如 `CLAUDE.md`） | `/caveman-compress` | 五个样本从 6,198 token 降到 4,138 token |

官方反复强调一条边界：**代码、命令、路径、错误信息、你原有的注释，一个字符都不改**。压缩的是寒暄、铺垫、复述和冗余表达，不是技术内容。

## 核心概念：两种「石头」

官方把功能分成两块，名字很直白：

- **大石头（the proxy）**：本地代理，压缩 Agent 读进来的内容。跑在你自己的机器上，用你自己的密钥和 Claude Pro/Max 登录态。原始文件始终留在你磁盘上，Agent 随时可以取回原文。
- **小石头（the skill）**：纯输出压缩，只让回答变短，不碰输入。安装最轻，兼容面最广。

技能包本身有多个强度档位，官方与第三方资料都提到 `/caveman`、`/ultracave`、`/megacave` 三档（第三方 skills.sh 页面还列出 lite、full、ultra、wenyan-lite、wenyan-full、wenyan-ultra 六种强度，两处说法不完全一致，以实际安装后的技能说明为准）。同一道 React 重渲染问题，三档分别是 20 / 14 / 13 token。

技能包的行为规则里有几条值得注意：

- **先给答案**，不打招呼、不说「让我来」、不复述、不写「希望有帮助」。
- **一句话一个意思**，参考航空维修手册用的受控英语标准 ASD-STE100：每句最多 20 词、主动语态、一个概念一个词。
- **否定词永不删**。`not`、`never`、`no`、`only` 必须保留，数字和单位保持精确。
- **安全场景自动退出压缩**：安全警告、不可逆操作确认、分步骤指令、反问用户、用户明显困惑时，恢复完整句子，之后再切回简短模式。
- **不改写你的提示词**。官方引用 Adobe Research 的结论：把用户的提问也「穴居化」会让回答更长更差，所以 Caveman 从不碰你的输入。

## 环境与前置依赖

| 项目 | 要求 |
|---|---|
| Node.js | 22.13 及以上（代理与 CLI 需要） |
| 操作系统 | Windows 可用，官方给出 PowerShell 5.1+ 的安装脚本 |
| 账号 | 代理模式使用你自己的 API 密钥或 Claude Pro/Max 登录态 |
| 许可证 | Apache-2.0 |
| npm 版本 | npm 12 及以上会拦截 git 安装，官方从 v3.2.0 起的一行命令已自行处理 |

> 官方明确说明：如果你是按**请求次数**付费（例如 GitHub Copilot 的 premium requests），回答变短并不会省钱，这种情况可以直接跳过。

## 安装与配置（Windows / PowerShell）

### 路线一：只装技能包（推荐 Trae Work 用户先走这条）

这是最轻的路径，只压缩输出，不涉及代理和密钥。

1. 确认 Node.js 版本不低于 22.13，在 PowerShell 里执行 `node -v` 查看。
2. 执行 `npx skills add JuliusBrussee/caveman -g` 安装技能包。
3. 官方列出的兼容宿主包括 Claude Code、Codex、Gemini CLI、Cursor、Windsurf、Cline、Copilot 等 30 多个。
4. 如果技能没有自动生效，在对话里输入 `/caveman`（Codex 里是 `$caveman`）手动触发。
5. 想关掉时说 `stop caveman` 或 `normal mode`。

### 路线二：装 CLI 与代理

1. 执行 `npm install -g @caveman-ai/cli && caveman setup --install`。
2. 用 `caveman claude` 启动，官方同时列出 `codex`、`gemini`、`aider`、`kilo`、`qwen`、`opencode`、`hermes`、`openclaw`、`pi` 等入口。
3. 首次运行之后，直接敲 `claude` 也会保持 Caveman 状态。

### 路线三：Windows 一键脚本

在 PowerShell 5.1+ 中执行 `irm https://raw.githubusercontent.com/JuliusBrussee/caveman/v3.2.0/install.ps1 | iex`，会为机器上所有受支持的 Agent 装上，并附带 Claude Code 状态栏徽章。

### 卸载

执行 `npx -y github:JuliusBrussee/caveman -- --uninstall`；npm 12 及以上需要额外加 `--allow-git=root`。

### 关于 Trae Work 与 Java / Spring

**官方未提供与 Trae Work 的集成方式，也未提供 Java / Spring 的 SDK 或 MCP 服务接入路径。** 官方列出的宿主清单里没有 Trae Work，官方给出的 SDK 只有 TypeScript 与 Python 两种（`npm install @caveman-ai/middleware @caveman-ai/sdk` 与 `pip install 'caveman-middleware[langchain]' caveman-sdk`，后者要求 Python 3.11+）。

因此对 Trae Work 用户来说，现实可行的做法只有一条：**把 Caveman 的技能文本作为规则内容引入 Trae Work 的自定义技能/规则机制**，让 Trae Work 里的助手按同样的风格回答。具体放置目录与配置方式取决于 Trae Work 自身的技能管理功能，官方未公开说明，需要按你本地 Trae Work 的版本自行确认。

> 不要照搬 Claude Code 的插件路径或 MCP 配置到 Trae Work，官方没有为 Trae Work 提供任何配置样例。

## 快速上手：先看它省不省

装好 CLI 之后，官方给了一组自检命令，建议按顺序跑：

1. `caveman learn` —— 从磁盘上已有的 Agent 历史里，统计你的 token 都花在哪。
2. `caveman learn implement` —— 一次一个 diff 地应用优化建议，只有你点同意才改。
3. `caveman trial -- claude` —— 拿你自己的真实任务做 A/B 对比。
4. `caveman shrink -- pnpm test` —— 压缩嘈杂的命令输出。
5. `caveman browse <url>` —— 用压缩后的网页替代上万 token 的原始页面。
6. `caveman stats` —— 查看你的 token 历史。

### 怎么确认装成功了

- 技能包路线：在对话里输入 `/caveman status`，它会报告当前模式；官方说明这个命令只报告、不改变状态。如果宿主不支持 hook，会显示 `(not tracked by this host)`。
- 代理路线：跑一次 `caveman stats`，能看到 token 历史记录即说明代理在工作。
- 最直接的验证：问一个技术问题，看回答是否变成「先给结论、无寒暄、代码块原样」的短句风格。

## 官方公布的实测数字

### 代理：整段会话少 33.2% 输入 token

| 文件类型 | 单文件压缩 | 整段会话节省 |
|---|---:|---:|
| CSV | 28,041 → 314（98.9%） | 55.1% |
| 日志 | 22,810 → 348（98.5%） | 50.2% |
| YAML | 20,447 → 178（99.1%） | 46.2% |
| 测试输出 | 18,806 → 203（98.9%） | 27.8% |
| JSON | 18,837 → 281（98.5%） | 26.4% |
| HTML | 无压缩器 | 反而差 9.9% |
| 六类合计 | 130,611 → 22,994（82.4%） | **33.2%** |

官方注明：18 道题 18 道答对；会话数据来自 2026 年 8 月，当时的引擎把 JSON 只压到 8,106 token；HTML 还没有压缩器，所以只付出了开销没有收益。

### 技能：十个开发问题上的输出 token

| 指令 | 输出 token |
|---|---:|
| 无指令 | 6,983 |
| `Answer concisely.` | 4,334 |
| `/caveman` | 4,119 |
| `/ultracave` | **2,693** |

官方说明这组数据测的是 3.1.0 版技能文本，尚未在本版本上重跑。

### 外部机构的验证

| 来源 | 设置 | 结果 |
|---|---|---|
| Adobe Research（CAVEWOMAN 论文，引用了本仓库） | 穴居风格输出，8 个模型，5 个数据集 | 每个模型成本降低 1.4–2.4 倍，最高 3 倍 |
| Elastic（Elasticsearch Labs） | 为 Elasticsearch 重做的穴居模式，8 个实时 MCP 场景 | 响应 token 少 63.6%，官方称「零信息损失」 |
| JetBrains | 86 个真实编码任务，配对 A/B | 质量无可测损失（p = 0.82），输出 token 少 8.5% |

## 社区评价（来自 Hacker News 讨论）

主帖《Caveman: Why use many token when few token do trick》拿到 904 分、366 条评论。另一篇独立测评《I benchmarked Claude Code's caveman plugin against "be brief."》拿到 89 分、67 条评论，作者用 24 个提示、5 组对照、由另一个 Claude 按评分表打分，共 120 条回答：

- 该测评作者的结论是：**「be brief.」在 token 数（419 对 401–449）和质量（0.985 对 0.970–0.976）上与 Caveman 基本打平**，Caveman 的额外价值在于输出结构一致、有强度档位、有自动退出压缩的安全机制。
- 评论区有人指出该测评每个提示每组只跑了一次，考虑到模型逐次运行的波动，安全类别上的差异可能只是噪声；作者回应承认这一点，表示分数差在 0.02 以内属于评委噪声范围，但没把同样的保留意见用到逐题 token 波动上。
- 也有评论从语言角度调侃，认为这种「去掉冠词和客套」的风格是把斯拉夫语系和日耳曼语系的优点合到了一起。

## 局限与风险

- **HTML 目前没有压缩器**，官方数据里这一类反而让会话变差 9.9%。
- **技能文本本身约 1,160 token**（tiktoken 计数），这部分开销对账单的影响取决于缓存，官方称尚未测量。
- **按请求计费的用户省不到钱**，官方直接建议跳过。
- **压缩有边界**：官方承认存在 Caveman 会输的场景，并单独列在 HONEST-NUMBERS 文档里。
- **第三方测评的样本量偏小**，单次运行、评委噪声、逐题波动等问题已被社区当面指出，作者也部分承认。
- **Trae Work 与 Java 生态没有官方支持**，强行套用其他宿主的配置路径有风险。
- **代理会接触你的密钥与登录态**，虽然官方强调全部在本机运行、原文留在本地磁盘，仍建议先在非敏感项目上试。
- 第三方插件目录提醒：安装前应查看仓库源码、近期维护情况与许可证，从最小权限开始，在安全环境里验证行为。

## 一句话结论

如果你按 token 付费、且大量时间花在让 Agent 读日志和测试输出上，Caveman 的代理值得一试，官方数据扎实、外部也有 Adobe 与 JetBrains 的旁证；如果你只是想让回答短一点，先试试在提示词里加一句「be brief.」，社区实测它和 Caveman 技能包几乎打平。至于 Trae Work + Java 这条线，目前只能手动借用它的风格规则，官方没有现成集成。

```text
背景：我在 Windows 上用 Trae Work 做 Java / Spring 后端开发，技术栈是 Spring Boot + Maven，日常需要让 AI 助手读日志、测试输出和 JSON 配置，token 消耗比较大。

目标：请帮我把 Caveman 的输出压缩风格落地到我的 Trae Work 工作流里，并评估是否值得再装它的本地代理。

具体要求：
1. 先检查我机器上的 Node.js 版本是否满足 22.13 及以上，如果不满足，告诉我 Windows 上最稳妥的升级方式。
2. 用 PowerShell 命令帮我安装 Caveman 技能包（npx skills add JuliusBrussee/caveman -g），并说明安装后如何验证它已经生效。
3. 官方没有提供 Trae Work 的集成方式，请根据我本地 Trae Work 的技能/规则管理功能，给出把 Caveman 风格规则引入的具体操作步骤；如果 Trae Work 当前版本不支持自定义技能，直接告诉我，不要编造配置路径。
4. 帮我设计一个对比实验：选一个真实的 Spring Boot 任务（比如排查一次接口 500 错误），分别在开启和关闭 Caveman 风格的情况下让助手回答，记录回答长度、是否遗漏关键信息（异常类名、堆栈行号、配置项路径）。
5. 评估阶段请明确告诉我：Caveman 的代理模式需要接触我的 API 密钥或登录态，是否值得在我当前项目上启用；如果我的用量是按请求次数计费而不是按 token 计费，直接建议我跳过代理。
6. 全程不要修改我项目里的任何代码文件，只做安装、配置和对比记录。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
