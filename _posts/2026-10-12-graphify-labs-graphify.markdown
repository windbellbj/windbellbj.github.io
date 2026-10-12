---
layout: post
title: "Graphify 使用说明：把 Java/Spring 代码库变成可查询知识图谱的 AI 技能"
subtitle: "本地 tree-sitter 解析、每条边可溯源、不依赖向量库，30 秒装好让 AI 助手查图而不是翻文件"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI技能
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/Graphify-Labs/graphify
- Stars：125560
- 语言：Python
- 创建时间：2026-04-03
- 最近更新：2026-10-11
- 官方简介：Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill for Claude Code, Cursor, Codex, and Gemini CLI: local deterministic AST parsing, every edge explained, no vector store.

---

> Graphify 是一个把代码库（连同文档、SQL schema、配置、PDF）解析成可查询知识图谱的 AI 助手技能：代码部分用 tree-sitter 在本地确定性解析、不调用大模型、不上传代码，之后你可以用 `query` / `path` / `explain` 让 AI 助手沿着真实路径查图，而不是反复 grep 和重读文件。最适合手上有一坨陌生或庞大的 Java/Spring 代码库、想让 AI 助手先「看懂全局」再动手的开发者。

## 它到底解决什么问题

日常用 AI 助手改 Java 项目时，最贵的成本不是写代码，而是让助手「重新认识」代码库：它一遍遍读文件、猜调用关系、把 token 烧在重复的上下文里。Graphify 的思路是先把整个仓库跑一遍，产出一张持久化的知识图谱，之后助手查图而不是翻文件。

它给出的核心能力：

| 能力 | 你会得到什么 |
|---|---|
| **God nodes** | 连接度最高的概念，一眼看出「所有东西都流过谁」 |
| **Communities** | 图谱按子系统切分（Leiden 聚类），标签不依赖大模型 |
| **跨文件链接** | `calls` / `imports` / `inherits` / `mixes_in`，经 tree-sitter AST 在约 40 种语言间解析 |
| **Query / Path / Explain** | 用自然语言提问、追踪两个东西之间的路径、解释单个概念，全部基于 `graph.json` |
| **理由与文档引用** | `# NOTE:` / `# WHY:` 注释和 ADR/RFC 引用会成为一等节点，挂到代码上 |
| **代码之外** | 文档、PDF、图片、音视频都能进同一张图 |
| **本地优先** | 代码用 tree-sitter 本地解析，不调用大模型、不出本机；只有文档/媒体的语义解析才会调用后端，且需要你自己配置 |

**关键区别：它不是向量索引。** 没有 embedding、没有向量库，是一张可以真正遍历的图。每条边都带置信标签：`EXTRACTED` 表示源码里显式存在，`INFERRED` 表示由 Graphify 解析推导出来——你能分清哪些是直接读到的、哪些是推断的。

## 核心概念与工作原理

一次运行会做这些事：

1. **本地 AST 解析**：用 tree-sitter 语法解析代码，产出确定性的结构信息，不消耗任何 LLM 额度。
2. **跨文件关系解析**：把 `calls` / `imports` / `inherits` / `mixes_in` 等关系在文件之间连起来。
3. **社区检测**：用 Leiden 算法把图切成子系统，标签不依赖大模型。
4. **语义补充（可选）**：文档、PDF、图片、视频走助手自身的模型或你配置的 API key 做语义解析。
5. **落盘**：结果写进 `graphify-out/` 目录，包含 `graph.html`、`GRAPH_REPORT.md`、`graph.json` 三个文件。

持久化的图里带有 `graph.schema_version`（便于集成方检测格式不兼容变化）和 `graph.graphify_version`（标明产出该图的 Graphify 版本）。

## 环境与前置依赖

| 依赖 | 最低要求 | 检查命令 | 安装方式 |
|---|---|---|---|
| Python | 3.10+ | `python --version` | python.org |
| uv（推荐） | 任意版本 | `uv --version` | `winget install astral-sh.uv` |
| pipx（备选） | 任意版本 | `pipx --version` | `pip install pipx` |
| 一个 AI 编程助手 | — | — | 用于技能工作流；纯 CLI 可脱离助手使用 |

**注意**：仅做代码提取不需要 API key；独立 CLI 也能在没有助手的情况下工作。

## 安装与配置（Windows PowerShell）

> **重要**：官方 PyPI 包名是 `graphifyy`（双 y），CLI 命令仍然是 `graphify`。PyPI 上其他 `graphify*` 包与 Graphify Labs 无关。官方源码仓库是 Graphify-Labs/graphify。

### 第一步：安装包

推荐用 uv 装到隔离环境：

1. 执行 `uv tool install graphifyy`。
2. 如果之后提示找不到 `graphify` 命令，执行 `uv tool update-shell`，然后**新开一个终端**。

备选方案：`pipx install graphifyy`，或 `pip install graphifyy`（后者可能需要手动配置 PATH）。

### 第二步：按需安装可选能力

只装你工作流需要的部分，多个 extras 可以组合，例如 `uv tool install "graphifyy[mcp,watch]"`。

| 能力 | 安装命令 |
|---|---|
| MCP 服务 | `uv tool install "graphifyy[mcp]"` |
| 文件监听 | `uv tool install "graphifyy[watch]"` |
| PDF | `uv tool install "graphifyy[pdf]"` |
| SQL 解析 | `uv tool install "graphifyy[sql]"` |
| Terraform | `uv tool install "graphifyy[terraform]"` |
| Office 文档 | `uv tool install "graphifyy[office]"` |
| 本地 Ollama 后端 | `uv tool install "graphifyy[ollama]"` |
| Leiden 聚类 | `uv tool install "graphifyy[leiden]"` |

如果 uv 提示已存在安装，用它的 `--reinstall` 选项替换该工具环境。

### 第三步：把技能注册到 AI 助手

1. 执行 `graphify install`，它会自动探测你机器上的助手。
2. 想指定平台就加参数，例如 `graphify install --platform codex`。
3. 想注册到当前仓库而不是用户目录，加 `--project`，例如 `graphify install --project --platform codex`。

项目级安装会写到当前目录下，例如 `.claude/skills/graphify/SKILL.md` 或 `.agents/skills/graphify/SKILL.md`，并附带一个按需加载的 `references/` 目录，同时打印 `git add` 提示。**提交前先看一遍安装器列出的文件清单**，项目级和用户级注册位置不同。

### 升级

1. 执行 `uv tool upgrade graphifyy`。
2. 重新执行 `graphify install --platform codex`（换成你实际用的平台），让技能文件与包版本对齐。
3. 如果你装过 git hooks，移动或重装 Python 环境后要重新执行 `graphify hook install`。

### 卸载注册

`graphify uninstall --project --platform codex` 可移除指定注册；`graphify uninstall` 移除跨平台的用户级注册。可选的 `--purge` 会一并删除 `graphify-out/`，不加则保留你的图。

## 如何融入 Trae Work 工作流

Graphify 官方列出的集成方式是「AI 编程助手技能」和「MCP 服务」两条路径，支持 Claude Code、Cursor、Codex、Gemini CLI、GitHub Copilot 等 17 个助手。**官方未提供与 Trae Work 的专门集成方式，也未提供 Java/Spring 的 SDK 或 HTTP 集成方式。** 因此对 Trae Work 用户，现实可行的路径是下面两条，具体是否可用取决于 Trae Work 是否支持读取对应技能目录或接入 MCP 客户端：

1. **技能目录路径**：Graphify 的 `graphify install` 会把技能写到助手约定的技能目录（如 `.claude/skills/graphify/`、`.agents/skills/graphify/`）。如果你的 Trae Work 支持读取同类技能目录，可尝试用 `--project` 方式把技能装进当前 Java 项目，再在 Trae Work 中调用。
2. **MCP 路径**：安装 `graphifyy[mcp]` 后，Graphify 可作为 MCP 服务被 MCP 客户端调用。若 Trae Work 支持配置 MCP 服务，可把 Graphify 的 MCP 服务加进去；官方文档提到，如果 MCP 客户端找不到 Graphify，**在客户端配置里使用可执行文件的绝对路径**。

> 由于官方未公开 Trae Work 的具体配置路径与命令，本文不给出任何未经证实的 Trae Work 配置写法。建议先在 PowerShell 里把 CLI 跑通（见下一节），确认图谱能正常生成，再决定用哪种方式接进 Trae Work。

## 快速上手

1. 在 PowerShell 里进入你的 Spring 项目根目录，例如 `cd D:\work\my-spring-service`。
2. 执行 `graphify install` 完成技能注册。
3. 在你的 AI 助手里输入 `/graphify .`，让它对当前目录建图。
4. 等待运行结束，检查项目下是否出现 `graphify-out/` 目录。
5. 用浏览器打开 `graphify-out/graph.html`，点击节点、筛选、搜索。
6. 阅读 `graphify-out/GRAPH_REPORT.md`，看关键概念、意外连接和建议问题。
7. 之后随时用 `graphify query "<你的问题>"` 提问，用 `graphify path A B` 追踪两个东西怎么连起来，用 `graphify explain "<概念>"` 解释单个概念——这些查询都基于 `graph.json`，不需要重新读你的文件。

官方给出的真实输出示例（在 FastAPI 代码库上运行）：执行 `graphify explain "APIRouter"` 会返回节点来源文件与行号、所属社区、度数，以及 47 条连接，每条连接标注 `[uses] [INFERRED]` 或 `[method] [EXTRACTED]` 这样的关系与置信标签；执行 `graphify path "FastAPI" "ModelField"` 会返回一条 3 跳的最短路径。

## 如何确认安装与运行成功

- `graphify --help` 能正常输出，说明 CLI 装好了。
- `graphify install` 执行后没有报错，并打印出注册的文件清单。
- 运行 `/graphify .` 后，项目根目录出现 `graphify-out/`，且其中包含 `graph.html`、`GRAPH_REPORT.md`、`graph.json` 三个文件。
- 用浏览器打开 `graph.html` 能看到可点击的力导向图。
- 执行一次 `graphify explain "<你项目里的某个类名>"`，能返回该节点的来源、社区、度数和连接列表。

## 性能与基准数据

官方公布的基准结果如下（所有系统在同一 harness、同一模型、同一预算下运行，由一位裁判评分，并对照第二位裁判做盲验证，一致率 90.6%，Cohen's kappa 0.81）：

| 基准 | 指标 | graphify | 对比 |
|---|---|---|---|
| LOCOMO (n=300) | recall@10 | **0.497** | mem0 0.048，supermemory 0.149 |
| LOCOMO (n=300) | QA 准确率 | 45.3% | supermemory 49.7%，mem0 27.3% |
| LongMemEval-S (n=50) | QA 准确率 | **76%** | 与 dense RAG 持平 |
| ERPNext 跨工具 (n=6) | 关键事实覆盖率 | **82.0%** | grep/read 基线 70.8% |
| 建图 | LLM 额度消耗 | **0** | 多数系统按 token 计费 |

注意：LOCOMO 的 QA 准确率上 supermemory 高于 graphify，而 recall@10 上 graphify 明显领先——两个指标看的是不同东西，别只看一个。

## 局限与风险

- **许可证**：开源核心采用 Apache 2.0。官网对比表把 Graphify 标为 open core（Apache 2.0），而 CodeRabbit、Greptile、Sourcegraph 标为专有。
- **商业版边界**：Graphify Cloud 是付费产品（提供 14 天免费试用），主打跨仓库/单仓持续建图、形式化验证、SDLC 级代码审查、Sentry/Jira 连接器等。官网称可降低 agent token 开销 80%。开源引擎可自行运行，但上述企业能力属于云端。
- **本地解析的边界**：代码解析完全本地、不调用大模型；但文档、PDF、图片、视频的语义解析需要助手自身的模型或你配置的 API key——也就是说这部分并非纯本地。
- **平台集成成熟度**：官方明确支持 17 个助手，但**未公开对 Trae Work 的支持**，也**未公开 Java/Spring 的 SDK 或 HTTP 集成方式**。接入 Trae Work 需要你自己验证技能目录或 MCP 配置是否可行。
- **包名易混淆**：PyPI 上存在同名近似包，官方包是 `graphifyy`，装错包可能带来安全与兼容风险。
- **版本兼容**：图格式带 `graph.schema_version`，跨版本升级后集成方需要检测格式变化；升级包后要重新注册技能，否则技能文件与包版本不一致。
- **数据规模**：仓库元信息显示 Star 数 125560、主语言 Python、创建于 2026-04-03、最近更新 2026-10-11；官网首页显示 125,545 GitHub stars、8.4M PyPI 下载、13.1M 仓库被索引。这些数字来自不同渠道，口径与时间点不同，仅供参考。

## 社区评价（来自 Hacker News 讨论）

暂无公开资料。

## 一句话建议

如果你的痛点是「AI 助手每次都要重新读一遍我的 Spring 项目」，Graphify 值得花 30 秒装来试：代码解析本地免费、每条边可溯源、不依赖向量库。但如果你重度依赖 Trae Work，请先确认它能否读取技能目录或接入 MCP 服务——官方目前没有给出 Trae Work 的集成说明。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring 后端项目，代码库比较大，AI 助手每次都要反复读文件、猜调用关系，token 消耗高且容易漏掉跨文件依赖。

目标：帮我把 Graphify 接入我的日常工作流，并在这个 Spring 项目上跑出第一张知识图谱，然后用它回答几个真实的代码理解问题。

具体要求：
1. 先确认我的环境：Python 版本是否 >= 3.10，uv 或 pipx 是否可用；如果缺，给出 Windows PowerShell 下的安装命令。
2. 用 uv 安装官方包 graphifyy，并说明如果安装后找不到 graphify 命令该怎么处理。
3. 执行 graphify install 注册技能；如果我想把技能注册到当前仓库而不是用户目录，告诉我该加什么参数，以及会生成哪些文件、哪些适合提交到 git。
4. 说明 Graphify 官方支持哪些 AI 助手，以及官方是否提供 Trae Work 的集成方式；如果没有，请明确告诉我，并给出在 Trae Work 中可能可行的两条路径（技能目录 / MCP 服务），以及每条路径需要我确认什么。
5. 在我的 Spring 项目根目录运行建图，告诉我产物在哪、三个产物文件分别是什么、怎么打开 graph.html。
6. 建图完成后，用 graphify explain 解释我项目里的一个核心类（比如某个 Service 或 Controller），并解释输出里的 EXTRACTED 和 INFERRED 分别代表什么。
7. 用 graphify path 追踪我项目里两个类之间的连接路径，并说明这条路径对排查依赖问题有什么用。
8. 最后给我一份「日常怎么用」的清单：什么场景该用 query、什么场景该用 path、什么场景该用 explain，以及升级 Graphify 后需要重新做哪些步骤。

注意：所有命令请用 Windows PowerShell 写法；不要编造 Trae Work 的配置路径或 Graphify 不存在的命令；如果某个能力需要额外安装 extras（比如 MCP、SQL 解析），请明确告诉我要装哪个 extras。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
