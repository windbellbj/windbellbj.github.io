---
layout: post
title: "Caveman 实测：让编码 Agent 少说少读省 65% token"
subtitle: "给 Trae Work 里的 Java 程序员：一个 Skill 加一个本地代理，代码照旧精确"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/JuliusBrussee/caveman
- Stars：111038
- 语言：Go
- 创建时间：2026-04-04
- 最近更新：2026-10-11
- 官方简介：🪨 why use many token when few token do trick. Viral skill + proxy for coding agents that cuts 65% of tokens by talking like a caveman.

---

## 解决什么问题

Caveman 要解决的是编码 Agent 的 token 浪费问题。README 的说法是：**Caveman make your AI agent say less and read less. Code stay exact. Brain still big.**（让 AI Agent 说得更少、读得更少，代码保持精确，脑子照样好使）。

它从两个方向下手：

- **说得少（Skill）**：让 Agent 的回答变成极简风格。README 给的例子是，同一个 React 重渲染问题的解释，普通 Agent 用 63 token，Caveman Agent 用 20 token，修复方案完全一样。
- **读得少（Proxy）**：让 Agent 读取的日志、CSV、YAML、JSON、测试输出被压缩。README 给出的数据是：六类文件合计从 130,611 token 压到 22,994 token，文件层面减少 82.4%；整个 Claude Code 会话从 885,793 token 降到 591,673 token，**会话层面减少 33.2%**，且 18 个答案 18 个正确。

README 还引用了外部验证：Adobe Research 的 CAVEWOMAN 论文（八个模型、五个数据集）报告每个模型成本降低 1.4 到 2.4 倍、最高 3 倍；Elastic 在 Elasticsearch Labs 的改造版报告响应 token 减少 63.6% 且“零信息损失”；JetBrains 用 86 个真实编码任务做配对 A/B，报告**无可测量的质量损失**（p = 0.82），输出 token 减少 8.5%。

对 Java 程序员来说，痛点很具体：一次 `mvn test` 或 `gradle build` 的失败输出、一份巨大的 JSON 响应、一段几千行的日志，塞进上下文后既贵又挤占推理空间。Caveman 的 Proxy 正是冲这类“噪音文件”去的。

## 核心概念

README 把 Caveman 分成“两块石头”：

**大石头：the proxy（代理）**

- 压缩 Agent **读进去**的内容：日志、测试输出、JSON、diff、网页。
- 跑在你自己的机器上，用你自己的 key 和 Claude Pro/Max 登录。
- 每个原始文件都留在你的磁盘上，Agent 随时可以把它拉回来。
- README 强调：安装后第一次运行，之后直接敲 `claude` 就一直是 caveman 状态。

**小石头：the skill（技能）**

- 只压缩 Agent **说出来的**内容，不涉及代理。
- 通过 `npx skills add JuliusBrussee/caveman -g` 安装。
- README 称其可在 Claude Code、Codex、Gemini CLI、Cursor、Windsurf、Cline、Copilot 以及 30+ 更多工具中工作。

**Caveman 的说话规则**（README 用表格列出，这里转述要点）：

- **Answer first**：`[thing] [action] [reason]. [next step].` 没有问候、没有“let me”、没有复述、没有“hope this helps”。
- **One idea per sentence**：基于 ASD-STE100（为飞机维修手册写的受控英语），每句最多 20 词，主动语态，一个东西一个叫法。
- **Meaning never dropped**：冠词可以省，但 *not*、*never*、*no*、*only* 永远不省；数字和单位保持精确。
- **Payload verbatim**：代码、命令、路径、错误信息、你已有的代码注释，逐字符不动。小改动只显示改动行，不重贴整个文件。
- **Quiet tool runs**：工具调用之间不闲聊，每个阶段一行，结果一行。
- **Knows when to stop**：安全警告、不可逆操作、分步指令、反问用户、用户困惑时，恢复完整句子，之后继续省。
- **Never performs**：不演“me think”，不加 caveman 前缀。如果 caveman 说法不更短，就用普通说法。
- **Your prompts stay yours**：你的提示词永远不会被改写。README 引 Adobe 的研究说改写提示词会适得其反。

**三档语气**：`/caveman`（20 token）、`/ultracave`（14 token）、`/megacave`（13 token，README 示例里是文言文）。

**其他能力**：`caveman browse` 把网页压成给 Agent 读的版本（200 行表格场景下 121 token 对比 Playwright 快照的 15,704 token，小 129.8 倍）；`/caveman-compress` 压缩 `CLAUDE.md` 这类记忆文件（五个样本合计 4,138 token 对比 6,198 token，每个文件小 22.8% 到 49.1%，标题、代码块、路径全部保留）。

## 前置依赖

README 明确提到的依赖只有两项：

- **Node.js 22.13+**：出现在 Install 一节的代理说明中，也出现在“Every agent on your machine at once”的一行安装命令说明里。
- **npm**：安装命令基于 npm；README 提到 npm 12 或更新版本会阻止 git 安装，v3.2.0 起的一行命令会自行处理这一点。

其他 README 提及的环境信息：

- Windows 用户可用 PowerShell 5.1+ 执行一行安装。
- 中间件/SDK 的 Python 版本要求为 Python 3.11+（这是给自建 Agent 的人用的，不是 Skill 本身）。
- 代理使用你自己的 key 和 Claude Pro/Max 登录。

README 未提供 Java、JDK、Maven、Gradle 相关的任何依赖要求。

## 安装与配置

下面按“Windows + Trae Work 的 Java 程序员”视角组织。**注意：README 未提供与 Trae Work / Java 的集成方式**，因此凡是 README 没写的接入路径，本文一律不编造，只给出 README 中真实存在的安装方式，以及你需要自行确认的部分。

**第 1 步：确认 Node 版本**

在 Trae Work 的终端或 Windows PowerShell 中执行 `node -v`，确认不低于 22.13。README 未提供 Node 的安装方式。

**第 2 步：安装 CLI 与代理（大石头）**

README 给出的命令是 `npm install -g @caveman-ai/cli && caveman setup --install`。随后用 `caveman claude` 启动，README 列出的可选目标还有 codex、gemini、aider、kilo、qwen、opencode、hermes、openclaw、pi。README 说明：第一次运行之后，直接敲 `claude` 就保持 caveman 状态。

**第 3 步：只想要短回答就装 Skill（小石头）**

README 给出的命令是 `npx skills add JuliusBrussee/caveman -g`。README 说明：如果它没有自动启动，输入 `/caveman`（Codex 中是 `$caveman`）；想关掉就说 `stop caveman`。

**第 4 步：Windows 专用一行安装（可选）**

README 给出 PowerShell 5.1+ 的命令：`irm https://raw.githubusercontent.com/JuliusBrussee/caveman/v3.2.0/install.ps1 | iex`。README 还提到，如果 npm 是 12 或更新版本，可以用 `npx --allow-git=root -y github:JuliusBrussee/caveman#v3.2.0`。

**第 5 步：卸载**

README 给出的命令是 `npx -y github:JuliusBrussee/caveman -- --uninstall`，npm 12+ 需要额外加 `--allow-git=root`。

**关于融入 Trae Work 日常工作流**

README 列出的支持清单是 Claude Code、Codex、Gemini CLI、Cursor、Windsurf、Cline、Copilot 以及 30+ 更多（详见 INSTALL.md），**README 未提供与 Trae Work / Java 的集成方式**，也没有给出任何 MCP 服务配置、Skill 目录路径或 IDE 插件形态的说明。因此：

- 不要假设它能作为 MCP 服务接入 Trae Work——README 未提供。
- 不要假设存在固定的 Skill 目录路径——README 未提供。
- 不要假设有 Java/Spring SDK——README 提供的中间件只有 TypeScript（`npm install @caveman-ai/middleware @caveman-ai/sdk`）和 Python（`pip install 'caveman-middleware[langchain]' caveman-sdk`）两条线，**没有 Java 版本**。

可以确认的只有一件事：README 说安装坏了的话，可以在该仓库里打开你的 Agent，说“Read CLAUDE.md and INSTALL.md, install caveman for me.”，让 Agent 自己修。这是 README 唯一给出的“通用兜底”路径。

## 最小可用示例

把下面这段整段复制给 Trae Work，让它先帮你判断 Caveman 在你的 Java 项目里值不值得装、怎么装。

```text
背景：我在 Windows 上用 Trae Work 开发 Java / Spring 后端项目，构建工具是 Maven 或 Gradle。我最近看到开源项目 Caveman（GitHub: JuliusBrussee/caveman），它宣称通过“让编码 Agent 少说少读”来省 token：Skill 部分压缩 Agent 的输出，Proxy 部分压缩 Agent 读进去的日志、CSV、YAML、JSON、测试输出，README 声称六类文件合计减少 82.4%、整个会话减少 33.2% 的输入 token。

目标：帮我判断它是否适合我当前的工作流，并给出可执行的落地步骤。

要求：
1. 先读 https://github.com/JuliusBrussee/caveman 的 README 和 INSTALL.md，只依据原文回答，不要凭印象补充。
2. 明确告诉我：README 里有没有提到 Trae Work 的接入方式？如果没有，直接说“README 未提供”，不要猜配置路径或命令。
3. 列出 README 中真实存在的安装命令，并标注每条命令对应的前置条件（例如 Node.js 版本要求）。
4. 针对我的 Java 项目，指出哪一类文件最可能被 Proxy 压缩（参考 README 里 CSV / Logs / YAML / Test output / JSON / HTML 的对比数据），并说明 HTML 那一行 README 是怎么说的。
5. 告诉我 README 里关于隐私和遥测的原文结论，以及关闭遥测的命令。
6. 如果 README 明确写了 Caveman 在某些情况下会“输”（例如按请求计费而非按 token 计费），把这些情况列出来。
7. 最后给一个建议：我是先只装 Skill，还是直接装 Proxy，理由基于 README 的事实。
```

## 验证方法

README 提供了若干可执行的验证路径，按从轻到重排列：

1. **看 token 去向**：执行 `caveman learn`，README 说它会从磁盘上已有的 Agent 历史中，给你的 token 花在哪里做排名。
2. **逐条应用优化**：执行 `caveman learn implement`，README 说它会一次一个 diff 地应用修复，且只在你同意时执行。
3. **做真实 A/B**：执行 `caveman trial -- claude`，README 说这是在你自己的工作上对真实会话做 A/B。
4. **压缩噪音命令输出**：执行 `caveman shrink -- pnpm test`（README 的示例用的是 pnpm，你可以换成自己的构建命令），验证压缩效果。
5. **压缩网页**：执行 `caveman browse <url>`，README 说它给出压缩后的网页，而不是 15,000 token 的转储。
6. **看历史统计**：执行 `caveman stats`，README 说是你的 token 历史。
7. **看当前模式**：在 Agent 里输入 `/caveman status` 查看模式，`/caveman off` 停止；`/caveman-stats` 查看当前 Claude Code 会话的真实 token 用量；`/caveman-help` 一屏看全部模式和命令。
8. **像素模式预演**：执行 `caveman convert --dry-run`，README 称其为“模型以图像方式读取 skill”的像素模式。

README 未提供针对 Java 项目或 Trae Work 的专门验证步骤。

## 风险与注意事项

以下均基于 README 原文：

- **HTML 目前是负收益**：README 的表格里，HTML 文件压缩前后都是 21,670 token（none yet），而整个会话反而从 140,687 涨到 154,641，**9.9% worse**。README 解释：HTML 还没有压缩器，所以 caveman 付了开销却没换回收益。
- **按请求计费时省不到钱**：README 明确写道，如果你是按请求而不是按 token 付费（例如 GitHub Copilot premium requests），更短的答案成本相同，那就跳过它。
- **Skill 本身有 token 开销**：README 说 `/caveman` 规则大约 1,160 token 文本（tiktoken 计数），这部分加到账单上多少取决于缓存，README 说**尚未测量**。
- **不要改写用户提示词**：README 引 Adobe 研究发现，把用户的提示词 caveman 化会让回答更长更差，所以 caveman 从不碰你的提示词。
- **遥测默认开启**：README 说 `caveman` CLI 默认发送使用统计：运行的命令、token 数量、随机安装 ID、操作系统、IP。README 强调**绝不发送**你的提示词、代码或文件路径。可用 `caveman telemetry off` 或 `DO_NOT_TRACK=1` 永久关闭。完整清单和删除已发送数据的方法在 SECURITY.md。Skill 本身在本机运行，不发送任何东西。
- **Claude 网页/手机端路径未经端到端测试**：README 在“Claude on the web, the phone app, or Cowork”一节中明确写“Not tested end to end yet.”。
- **基准数据的适用范围**：README 说明每个基准文件是在 61 到 72 KB 的噪音里藏一条记录，并提醒“your files will vary”；会话数据来自 2026 年 8 月，当时的引擎只能把 JSON 压到 8,106 token。
- **Skill 数据未在本版本重跑**：README 说 skill 的十道开发题数据“Measured on the 3.1.0 skill text, not yet re-run on this release's.”。
- **商标**：“Caveman”和石头 logo 是 Julius Brussee 的商标；代码本身是 Apache-2.0。

README 未提供关于 Java 生态、Trae Work 兼容性或企业内网部署的风险说明。

## 替代方案

README 本身没有列出竞品或替代方案。README 中与“替代”最接近的内容是：

- **只装 Skill 而不装 Proxy**：README 明确把这两者当作可选路径——“Only want shorter answers? Get just the skill”。
- **自建 Agent 时用中间件替代 CLI**：README 提供 TypeScript 的 `@caveman-ai/middleware` + `@caveman-ai/sdk`，以及 Python 3.11+ 的 `caveman-middleware[langchain]` + `caveman-sdk`，作为包在 Vercel AI SDK、LangChain、OpenAI 或 Anthropic 调用外面的一层包装。README 还提到“One container for the whole team”的部署文档。
- **README 提到的外部相关工作**：Adobe Research 的 CAVEWOMAN 论文、JetBrains 的博客、Elastic 的 elastic-caveman，这些是引用或改造 Caveman 的工作，不是竞品。

除此之外，README 未提供其他替代方案的对比。对于 Java 程序员而言，README 未提供任何 Java 侧的替代实现或等价 SDK。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
