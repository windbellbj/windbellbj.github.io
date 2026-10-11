---
layout: post
title: "graphify：把代码库变成可查询知识图谱的 /graphify 技能"
subtitle: "本地 AST 解析、每条边可解释、不用向量库，Trae 用户可直接装来试"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: skill
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/Graphify-Labs/graphify
- Stars：125515
- 语言：Python
- 创建时间：2026-04-03
- 最近更新：2026-10-11
- 官方简介：Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill for Claude Code, Cursor, Codex, and Gemini CLI: local deterministic AST parsing, every edge explained, no vector store.

---

## 解决什么问题

日常在 Trae Work 里问 AI「这个 Spring 项目里认证是怎么连到数据库的」，助手往往只能靠 grep 和逐个读文件，既慢又费 token。graphify 想解决的就是这件事：把整个项目（代码、文档、SQL schema、配置、PDF、图片、视频）映射成一张**可查询的知识图谱**，让你「查询而不是 grep」。

README 给出的核心卖点：

- **代码部分免费且完全本地**：代码用 tree-sitter AST 解析，确定性、不用 LLM，数据不出本机。文档、PDF、图片、视频则走助手模型或你配置的 API key 做语义抽取。
- **每条边都有解释**：每个连接被标记为 `EXTRACTED`（源文件中显式存在）或 `INFERRED`（由 graphify 解析推断），你能分清哪些是直接读出来的、哪些是推出来的。
- **不是向量索引**：没有 embedding、没有向量库，是一张真正可以遍历的图。可以提问、追踪两个东西之间的路径、解释某个概念。

README 还提到 Graphify Cloud 是构建在 graphify 之上的常驻层（monorepo/跨仓库、形式化验证、Sentry/Jira 连接器等），属于商业产品，本文只介绍开源仓库本身。

## 核心概念

- **知识图谱（knowledge graph）**：graphify 把项目映射成的图结构，节点是概念，边是关系。
- **`/graphify` 技能**：在 AI 编程助手里输入 `/graphify .` 即可构建当前目录的图。README 明确它支持 Claude Code、Cursor、Codex、Gemini CLI、GitHub Copilot 等 20+ 平台。
- **三个产物文件**：构建后输出到 `graphify-out/` 目录，包含 `graph.html`（浏览器里点击节点、过滤、搜索）、`GRAPH_REPORT.md`（要点：关键概念、意外连接、建议问题）、`graph.json`（完整图，可随时查询而无需重读文件）。
- **边置信度标签**：`EXTRACTED` 表示源文件中显式存在，`INFERRED` 表示由解析推断得出。
- **God nodes（枢纽节点）**：连接度最高的概念，让你看到一切都流经哪里。
- **Communities（社区）**：图被 Leiden 算法切分成子系统，标签不依赖 LLM。
- **跨文件链接**：`calls` / `imports` / `inherits` / `mixes_in` 等关系通过 tree-sitter AST 在约 40 种语言间解析。
- **查询三件套**：`graphify query "<question>"` 返回限定范围的子图；`graphify path A B` 追踪两点如何相连；`graphify explain "X"` 解释单个概念。
- **Rationale + doc refs**：`# NOTE:` / `# WHY:` 注释和 ADR/RFC 引用会成为一等节点，链接到代码。
- **graph.json 中的版本字段**：持久化的图包含 `graph.schema_version`（供集成方检测不兼容的格式变化）和 `graph.graphify_version`（标识产出该图的 Graphify 版本）。

## 前置依赖

README 的 Prerequisites 表格给出：

- **Python**：最低 3.10+，检查命令 `python --version`。
- **uv（推荐）**：任意版本，检查命令 `uv --version`。
- **pipx（替代方案）**：任意版本，检查命令 `pipx --version`。

Windows 快速安装（README 原文）：`winget install astral-sh.uv`。

README 还提示：官方 PyPI 包名是 `graphifyy`（双 y），PyPI 上其他 `graphify*` 包与其无关；CLI 命令仍然是 `graphify`。官方源码仓库是 Graphify-Labs/graphify。

## 安装与配置

以下步骤按「Windows + Trae Work + Java/Spring 项目」的读者视角整理，命令全部来自 README。

**第 1 步：装 Python 与 uv。** 在 Windows 上执行 `winget install astral-sh.uv`，并确认 `python --version` 显示 3.10 以上。

**第 2 步：安装 graphify 包。** README 推荐用隔离环境安装：`uv tool install graphifyy`。如果装完找不到 `graphify` 命令，README 提示运行 `uv tool update-shell`。替代方案是 `pipx install graphifyy` 或 `pip install graphifyy`（后者可能需要配置 PATH）。

**第 3 步：把技能注册到你的 AI 助手。** README 的通用命令是 `graphify install`。针对 Trae，README 的「Pick your platform」表格里明确列出了两条：

- Trae：`graphify install --platform trae`
- Trae CN：`graphify install --platform trae-cn`

README 对该平台的说明是：Trae 使用 Agent tool 做并行子代理分发，且**不支持 `PreToolUse` hooks**，因此 `AGENTS.md` 是它的常驻机制。

**第 4 步（可选）：项目级安装。** 如果不想装到用户目录，而是装进当前仓库，README 给出 `graphify install --project`，并说明项目级安装会写到当前目录下，例如 `.claude/skills/graphify/SKILL.md` 或 `.agents/skills/graphify/SKILL.md`（外加一个按需加载的 `references/` 附属目录），并打印可提交文件的 `git add` 提示。

**第 5 步（可选）：按需装扩展。** README 的 Optional extras 表格列出很多可选依赖，与 Java 后端场景相关的有：`uv tool install "graphifyy[sql]"`（SQL schema 抽取）、`uv tool install "graphifyy[postgres]"`（实时 PostgreSQL 内省，配合 `--postgres DSN`）、`uv tool install "graphifyy[pdf]"`（PDF 抽取）、`uv tool install "graphifyy[office]"`（`.docx` 与 `.xlsx`）、`uv tool install "graphifyy[mcp]"`（MCP stdio server）、`uv tool install "graphifyy[neo4j]"`（Neo4j 推送）、`uv tool install "graphifyy[falkordb]"`（FalkorDB 推送）、`uv tool install "graphifyy[chinese]"`（中文查询分词，jieba）。

**关于融入 Trae Work 日常工作流：**

- README 明确支持 Trae 平台安装（`graphify install --platform trae`），安装后在助手内输入 `/graphify .` 构建图。
- README 提到存在 MCP stdio server 扩展（`graphifyy[mcp]`），但**README 未提供与 Trae Work 的 MCP 接入配置方式**，也未给出在 Trae Work 中作为 MCP 服务接入的具体步骤。
- README 未提供与 Java / Spring 项目的 SDK 或 HTTP 集成方式。
- README 未提供在 Trae Work 终端中作为 CLI 调用的专门说明；不过 README 说明 `graphify query`、`graphify path`、`graphify explain` 可以直接在命令行对 `graph.json` 查询，脚本可通过退出码读取结果：`0` 表示有答案，`3` 表示名称有歧义，`4` 表示没有匹配节点。

**让助手总是用这张图：** README 说明，构建完图后在项目里跑一次 `graphify <platform> install`（例如 `graphify claude install` 或 `graphify codex install`，或 `graphify install --platform <name>`），会写入一个小配置文件，告诉助手在回答代码库问题时先查知识图谱，优先用 `graphify query "<question>"` 这类限定查询，而不是读完整报告或 grep 原始文件。README 把平台分成两类：Hook 平台（Claude Code、Gemini CLI）会在搜索类工具调用前自动触发 hook；指令文件平台（Codex、OpenCode、Cursor 等）则通过 `AGENTS.md`、`.cursor/rules/` 等常驻指令文件提供同样的「先查询」引导。Trae 属于后者，靠 `AGENTS.md`。

**卸载：** README 给出 `graphify uninstall` 一次性从所有平台移除（加 `--purge` 会同时删除 `graphify-out/`），也可以用按平台的命令，例如 `graphify claude uninstall`。

## 最小可用示例

下面这段可以直接整段复制给 Trae Work，让它帮你在这个 Java/Spring 项目上跑通 graphify 并做一次真实查询。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring 后端项目，项目里有 Java 源码、application.yml 之类的配置、若干 SQL 建表脚本和一份接口文档 PDF。我想先小范围试用 graphify，看看它能不能替代我平时靠 grep 和逐个读文件来理解代码的方式。

目标：
1. 确认本机已满足 graphify 的前置依赖（Python 3.10+、uv），没有的话告诉我怎么装。
2. 用官方包名安装 graphify（注意 PyPI 包名是 graphifyy，双 y，CLI 命令是 graphify），并把它注册到 Trae（README 里 Trae 对应的命令是 graphify install --platform trae）。
3. 在当前项目根目录构建知识图谱，产出 graphify-out/ 下的 graph.html、GRAPH_REPORT.md、graph.json 三个文件。
4. 构建完成后，先用 graphify explain 解释一个我项目里的核心类（比如我的主 Service 或 Controller），再用 graphify path 追踪「某个 Controller」到「某个 Repository 或数据库访问层」之间的最短路径，最后用 graphify query 问一个自然语言问题，比如「认证相关的代码是怎么连到数据库的」。

要求：
- 每一步都告诉我你实际执行的命令和真实输出，不要编造结果。
- 如果某一步失败，把报错原文贴出来，并对照 README 的 Troubleshooting 思路排查，不要自己发明配置项。
- 注意区分输出里每条边的置信度标签：EXTRACTED 是源文件里显式存在的，INFERRED 是 graphify 推断出来的，请分别举例说明。
- 代码解析是本地 tree-sitter AST，不需要 API key；但如果要解析文档和 PDF，需要走语义抽取，请先告诉我这一步会用到哪个后端、是否需要我提供 API key，再决定要不要做。
- 最后给我一份简短结论：这张图对我这个 Spring 项目有没有用、哪些问题它答得好、哪些答得不好。
```

## 验证方法

按 README 的事实，可以这样验证：

1. **确认安装成功**：在终端执行 `graphify --help` 或直接执行 `graphify install`，看命令是否被识别。README 提示若出现 `command not found`，可运行 `uv tool update-shell`，并指向官方 Installation 与 Troubleshooting 文档。
2. **确认技能注册成功**：在 Trae 里输入 `/graphify .`，看是否能触发构建。README 说明构建后会在 `graphify-out/` 下产出三个文件。
3. **检查产物**：确认 `graphify-out/graph.html`、`graphify-out/GRAPH_REPORT.md`、`graphify-out/graph.json` 三个文件存在。用浏览器打开 `graph.html`，README 说可以点击节点、过滤、搜索。
4. **检查版本字段**：README 说明持久化的图里包含 `graph.schema_version` 和 `graph.graphify_version`，可以打开 `graph.json` 确认这两个字段存在。
5. **跑一次查询**：执行 `graphify explain "<你的类名>"`，README 展示的输出格式包含 Source、Community、Degree 和 Connections 列表，每条连接带 `[EXTRACTED]` 或 `[INFERRED]` 标签。
6. **跑一次路径查询**：执行 `graphify path "A" "B"`，README 展示的输出是「Shortest path (N hops)」加一条逐跳路径。
7. **检查退出码**：README 说明脚本可以读退出码判断结果——`0` 有答案、`3` 名称有歧义、`4` 没有匹配节点。README 还特别说明：当一个名字匹配到多个节点时，graphify 会拒绝并列出候选，而不是猜一个。
8. **检查查询日志**：README 说明每次 `graphify query`、`graphify path`、`graphify explain` 和 MCP `query_graph` 调用都会以 JSON Lines 格式记录到 `~/.cache/graphify-queries.log`（时间戳、问题、语料、返回节点数、耗时），默认不存完整子图。

## 风险与注意事项

以下均基于 README 原文：

- **包名陷阱**：官方 PyPI 包是 `graphifyy`（双 y），README 明确说 PyPI 上其他 `graphify*` 包与其无关。装错包是真实风险。
- **隐私边界要分清**：代码文件本地 tree-sitter 处理，不出本机，纯代码语料不需要 API key，`graphify extract` 可完全离线；混合仓库可加 `--code-only` 只索引代码。视频/音频用 faster-whisper 本地转写，不出本机。但**文档、PDF、图片会被送到你的 AI 助手做语义抽取**（通过 `/graphify` 技能，用你 IDE 会话所用的模型）。无头模式 `graphify extract` 需要配置 `GEMINI_API_KEY` / `GOOGLE_API_KEY`、`MOONSHOT_API_KEY`、`ANTHROPIC_API_KEY`、`OPENAI_API_KEY`、`DEEPSEEK_API_KEY`、运行中的 Ollama（`OLLAMA_BASE_URL`）、AWS 凭证链（Bedrock，无需 API key），或 `claude` CLI 二进制（Claude Code，无需 API key）。`--dedup-llm` 用同一个 key。
- **数据驻留**：README 说明 `graphify extract` 会根据设置了哪个 API key 自动选择 provider，优先级为 Gemini → Kimi → Claude → OpenAI → DeepSeek → Azure → Bedrock → Ollama。对有数据驻留要求的代码，用 `--backend ollama`（完全本地）或显式传 `--backend`。README 特别提示 Kimi（`MOONSHOT_API_KEY`）会路由到中国的 Moonshot AI 服务器。
- **查询日志**：默认会写 `~/.cache/graphify-queries.log`。可用 `GRAPHIFY_QUERY_LOG_DISABLE=1` 关闭，或用 `GRAPHIFY_QUERY_LOG=/dev/null` 静默但不关闭代码路径。
- **无遥测**：README 声明没有 telemetry、没有使用追踪、没有分析。
- **Trae 平台限制**：README 明确 Trae 不支持 `PreToolUse` hooks，常驻机制是 `AGENTS.md`。
- **Codex 的 hook 是空操作**：README 说明 Codex 的 `PreToolUse` hook 是故意设计成 no-op 的，因为 Codex Desktop 会拒绝 `hookSpecificOutput.additionalContext`，真正起作用的是 `AGENTS.md`。
- **两套指令不要混用**：README 提醒，如果同时使用本地 CLI 技能和 MCP 连接，要分清各自查的是哪张图，选一条主查询路径，而不是把两段无条件指令都塞进 `AGENTS.md`。README 明确 `graphify install` 只安装本地助手集成，**不建立 MCP 连接**。
- **README 未提供**：与 Trae Work 的 MCP 接入配置方式、与 Java/Spring 的 SDK 或 HTTP 集成方式、具体的版本号与兼容性矩阵，README 均未提供。

## 替代方案

README 本身没有列出竞品或替代方案清单，只在 Benchmarks 表格里把 graphify 与 mem0、supermemory、dense RAG 做了对比（LOCOMO n=300 上 recall@10 为 0.497，对比 mem0 0.048、supermemory 0.149；QA accuracy 45.3%，对比 supermemory 49.7%、mem0 27.3%；LongMemEval-S n=50 上 QA accuracy 76%，与 dense RAG 持平；ERPNext cross-tool n=6 上 key-fact coverage 82.0%，对比 grep/read 基线 70.8%；图构建的 LLM credits 为 0）。

README 还提到 Graphify Cloud 是构建在 graphify 之上的常驻层，提供 monorepo/跨仓库、形式化验证、SDLC 全局代码审查、Sentry/Jira 连接器等能力，可作为「按需构建的本地图」之外的另一种选择。

除此之外，README 未提供其他替代方案的说明。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
