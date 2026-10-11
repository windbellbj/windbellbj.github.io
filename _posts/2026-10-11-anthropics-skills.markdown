---
layout: post
title: "anthropics/skills 使用说明书：给 Claude 装上可复用的专业技能包"
subtitle: "Agent Skills 官方示例仓库，含文档处理与 skill-creator，Windows + Trae Work 的 Java 开发者可先跑通再决定是否…"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI技能
news_category: skill
---

- 来源：重点跟踪清单
- 仓库：https://github.com/anthropics/skills
- Stars：180508
- 语言：Python
- 创建时间：2025-09-22
- 最近更新：2026-10-09
- 官方简介：Public repository for Agent Skills

---

> 这是一套「技能包」标准与官方示例集合：把指令、脚本和资源打包成文件夹，让 Claude 在需要时动态加载，从而在特定任务上表现更稳定、更可复现。最适合想给 AI 编程助手补上「专业动作」的开发者，尤其是需要文档处理、技能自建与评测流程的团队。

## 它到底解决什么问题

日常用 AI 写代码，最烦的不是「不会写」，而是「每次都要重新交代一遍规矩」：项目用什么分层、日志怎么打、单测怎么写、接口文档放哪。**Skills 的思路是把这些规矩固化成文件夹**，里面包含指令、脚本和资源，Claude 只在任务相关时才加载，不相关就不占用上下文。

官方对它的定位是：技能教 Claude 以可复现的方式完成特定任务，比如按公司品牌规范生成文档、按组织特定流程分析数据，或自动化个人任务。

它强调四个特性：

| 特性 | 含义 |
| --- | --- |
| 可组合 | 技能可以叠加，Claude 自动判断需要哪些并协调使用 |
| 可移植 | 同一套格式，在 Claude 应用、Claude Code 和 API 中通用 |
| 高效 | 只在需要时加载所需的最小信息与文件 |
| 强大 | 可以包含可执行代码，用于传统编程比生成 token 更可靠的任务 |

## 核心概念：一个技能就是一个文件夹

每个技能自成一体，放在自己的文件夹里，核心是一个 `SKILL.md` 文件，包含 Claude 使用的指令和元数据。

`SKILL.md` 的 frontmatter 只需要两个字段：

- **`name`**：技能的唯一标识，小写、用连字符代替空格
- **`description`**：完整描述这个技能做什么、什么时候该用它

frontmatter 下面的 Markdown 正文，就是 Claude 在该技能激活时要遵循的指令、示例和准则。

仓库里还提供了 `./spec`（Agent Skills 规范）和 `./template`（技能模板），可以当作起点。

## 仓库里都有什么

技能示例覆盖四大类：创意与设计、开发与技术、企业与沟通、文档技能。

其中文档创建与编辑技能（`skills/docx`、`skills/pdf`、`skills/pptx`、`skills/xlsx`）是支撑 Claude 文档能力的底层实现。**注意许可证差异**：仓库中许多技能是开源的（Apache 2.0），但这四个文档技能属于 source-available 而非开源，官方把它们公开出来，是作为生产级 AI 应用中更复杂技能的参考。

第三方目录站 skills.sh 上还单独收录了 `skill-creator` 技能，描述为：创建、测试并迭代改进 AI 智能体技能，带结构化评测与基准测试；引导走完整个技能开发生命周期（意图捕获、起草、测试用例创建、评测、基于反馈迭代）；并行运行「带技能」与「不带技能」的测试用例来衡量影响，记录耗时与 token 用量做定量对比；生成基于浏览器的交互式评审页面，展示输出、定性反馈和跨迭代的基准指标（通过率、延迟、token 效率）；还包含描述优化，通过测试 20 条真实触发/非触发查询、最多迭代 5 轮来提升技能触发准确率。

## 环境与前置依赖

- **Python**：仓库主语言为 Python，部分技能内含脚本（例如评测查看脚本 `eval-viewer/generate_review.py`）。具体 Python 版本要求官方未公开说明。
- **使用渠道**：技能可在 Claude 应用、Claude Code 和 Claude API 中使用。Claude 应用侧，Skills 面向 Pro、Max、Team 和 Enterprise 用户开放；Team 和 Enterprise 用户需要管理员先在组织范围内启用 Skills。
- **API 侧**：技能可以加入 Messages API 请求，并有 `/v1/skills` 端点用于程序化管理。

> 官方明确声明：这些技能仅用于演示和教育目的。虽然部分能力在 Claude 中可用，但你从 Claude 得到的实现和行为可能与这些技能展示的不同。用于关键任务前，务必在自己的环境中充分测试。

## 安装与配置

### 路线一：在 Claude Code 中作为插件市场安装

1. 在 Claude Code 中执行 `/plugin marketplace add anthropics/skills`，把该仓库注册为插件市场。
2. 选择 `Browse and install plugins`。
3. 选择 `anthropic-agent-skills`。
4. 选择 `document-skills` 或 `example-skills`。
5. 选择 `Install now`。

也可以跳过浏览界面，直接安装：`/plugin install document-skills@anthropic-agent-skills` 或 `/plugin install example-skills@anthropic-agent-skills`。

安装后，直接提到技能即可使用。例如装了 `document-skills` 插件后，可以让 Claude Code「Use the PDF skill to extract the form fields from `path/to/some-file.pdf`」。

### 路线二：在 Claude 应用中使用

这些示例技能对 Claude.ai 的付费计划已经可用。要使用仓库中的技能或上传自定义技能，按官方「Using skills in Claude」文档的说明操作，并在设置中启用 Skills。

### 路线三：通过 Claude API 使用

可以使用 Anthropic 预置技能，也可以上传自定义技能，具体见 Skills API 快速上手文档。

### 路线四：用 skills.sh 的 CLI 安装单个技能

第三方目录站给出的安装命令是 `npx skills add https://github.com/anthropics/skills --skill skill-creator`，用于单独添加 `skill-creator` 技能。

### 关于 Trae Work 与 Java 项目

**官方未提供与 Trae Work / Java 的集成方式。** 仓库说明中给出的接入路径只有 Claude Code 插件市场、Claude 应用和 Claude API 三条，没有 MCP 服务形态、没有 Java SDK、也没有面向其他 IDE 的配置说明。因此不存在可照抄的 Trae Work 技能目录路径或 Spring 依赖坐标，不要凭猜测填写。

在 Windows + Trae Work 的日常开发中，可行的做法是**把技能当作可复用的提示资产来用**：把 `SKILL.md` 的正文内容整理成项目内的规范文档或提示模板，在 Trae Work 里按需引用；如果你所在环境支持自定义技能目录，请以该工具自身的官方说明为准。

## 快速上手：从零写一个技能

1. 想清楚这个技能要做什么、大致怎么做。
2. 在仓库的 `template` 基础上新建一个文件夹。
3. 写 `SKILL.md`，frontmatter 填 `name` 和 `description`，正文写指令、示例和准则。
4. 准备几条测试提示词，在带该技能的环境里跑一遍。
5. 从定性和定量两个角度评估结果，不满意就改，重复迭代。
6. 满意后扩大测试集，在更大规模上再验一次。

如果只是想先感受效果，可以直接用 `skill-creator`：它会先判断你处在流程的哪一步，再跳进来帮你推进——你说「我想给 X 做个技能」，它会帮你收敛范围、写草稿、写测试用例、确定评估方式、跑完所有提示词并循环；如果你已经有草稿，它会直接进入评测与迭代环节。

## 怎么确认装好了、跑通了

- **Claude Code**：插件安装完成后，在对话里直接点名技能（例如让 PDF 技能去抽取某个 PDF 的表单字段），能正常触发即说明生效。
- **Claude 应用**：Claude 会根据任务自动调用相关技能，无需手动选择，你甚至能在它的思考链里看到技能被调用。
- **skill-creator 流程**：跑完测试用例后，用 `eval-viewer/generate_review.py` 生成评审页面，能看到输出、定性反馈以及通过率、延迟、token 效率等基准指标，说明评测链路是通的。

## 社区评价

来自 Hacker News 讨论的反馈集中在两点：一是「技能即文件夹 + 按需加载」这种轻量约定比一次性塞满上下文更实用；二是对文档技能 source-available 而非开源的许可证边界有讨论，认为用于参考可以，直接商用需谨慎。

## 局限与风险

- **成熟度**：官方定位是演示与教育用途，行为可能与 Claude 实际能力不一致，关键任务前必须自测。
- **许可证**：多数技能为 Apache 2.0，但 `docx`、`pdf`、`pptx`、`xlsx` 四个文档技能是 source-available，不是开源，使用前需确认合规边界。
- **费用**：Claude 应用侧 Skills 面向 Pro、Max、Team、Enterprise 付费计划；API 侧按用量计费。
- **安全**：技能可以包含可执行代码，第三方技能等同于引入外部脚本，来源不明的技能不要直接在生产环境运行。第三方审计信息显示该仓库的 `skill-creator` 通过 Gen Agent Trust Hub 与 Snyk 审计，Socket 给出 Warn 提示。
- **平台绑定**：官方接入路径围绕 Claude 生态，跨平台可移植性由 Agent Skills 开放标准承诺，但具体到 Trae Work 等第三方工具，官方未公开说明支持情况。

## 给 Java / Spring 开发者的试用建议

先别急着自建技能。用 `skill-creator` 走一遍完整流程，感受「起草—测试—评测—迭代」的节奏，再决定要不要把团队的 Spring 分层规范、日志规范、单测模板沉淀成技能。文档类技能可以直接拿来处理接口文档、需求文档的格式转换。

```text
背景：我在 Windows 上用 Trae Work 开发，技术栈是 Java / Spring Boot，团队有一套固定的后端开发规范（Controller 只做参数校验与编排、Service 承载业务、DTO 与 Entity 分离、统一返回体、日志用 SLF4J 占位符、单测用 JUnit 5 + Mockito）。

目标：帮我把这套规范做成一个可复用的「技能包」，让 AI 助手在写 Spring 代码时自动遵循，而不是每次重新交代。

具体要求：
1. 先帮我梳理这个技能应该覆盖哪些规则，按「必须遵守」和「建议遵守」两档列出，控制在 15 条以内，每条一句话说清。
2. 按 Agent Skills 的格式产出 SKILL.md：frontmatter 只包含 name（小写连字符）和 description（说明这个技能做什么、什么时候该用），正文包含指令、正例与反例各一段、以及准则清单。
3. 针对这个技能设计 5 条测试提示词，覆盖：新建一个 REST 接口、给已有 Service 加事务、写一个带 Mock 的单测、重构一段臃肿的 Controller、评审一段不符合规范的代码。
4. 说明如何判断这个技能是否真的生效：给出「带技能」和「不带技能」两种情况下，我应该重点对比哪些输出差异。
5. 最后告诉我，如果要把这个技能迭代得更好，下一轮应该补充哪些测试用例。

请直接输出 SKILL.md 的完整内容和测试提示词清单，不要省略。
```

把上面这段整段复制给 Trae Work 或其他 AI 编程助手，就能得到一份可以直接落地的技能草稿。

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
