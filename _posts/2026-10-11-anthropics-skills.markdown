---
layout: post
title: "anthropics/skills：Claude Agent Skills 入门"
subtitle: "读懂官方 Skills 仓库结构、安装方式与最小落地流程，含 Windows 本地试用步骤"
date: 2026-10-11 22:08:59 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
---

- 仓库：https://github.com/anthropics/skills
- Stars：180442
- 语言：Python
- 最近推送：2026-10-09
- 官方简介：Public repository for Agent Skills

---

## 解决什么问题

根据 README，Skills 是「文件夹形式的指令、脚本与资源」，Claude 会动态加载它们，从而在专门任务上提升表现。Skills 的作用是教会 Claude 以可重复的方式完成特定任务，例如按公司品牌规范创建文档、按组织特定工作流分析数据，或自动化个人任务。

本仓库（anthropics/skills）是 Anthropic 对 Claude skills 的实现示例集合，用于展示 skills 系统能做什么。README 说明这些 skills 覆盖创意类应用（艺术、音乐、设计）、技术任务（测试 Web 应用、MCP server 生成）以及企业工作流（沟通、品牌等）。每个 skill 自包含在独立文件夹中，内含一个 `SKILL.md`，其中保存 Claude 使用的指令与元数据。

README 同时说明，仓库中的许多 skills 是开源的（Apache 2.0）；文档创建与编辑类 skills（`skills/docx`、`skills/pdf`、`skills/pptx`、`skills/xlsx`）是 source-available 而非开源，它们是 Claude 文档能力背后的实现，作为更复杂 skill 的参考分享给开发者。

## 核心概念

- **Skill**：一个文件夹，包含指令、脚本和资源，由 Claude 动态加载。
- **SKILL.md**：每个 skill 的核心文件，包含 YAML frontmatter 与指令正文。README 指出 frontmatter 只需要两个字段：`name`（唯一标识符，小写、用连字符代替空格）与 `description`（完整描述该 skill 做什么、何时使用）。
- **指令正文**：`SKILL.md` 中 frontmatter 下方的 Markdown 内容，包含 Claude 在该 skill 激活时遵循的指令、示例与指南。
- **Skill Sets**：README 列出三个目录——`./skills`（Creative & Design、Development & Technical、Enterprise & Communication、Document Skills 的示例）、`./spec`（Agent Skills 规范）、`./template`（skill 模板）。
- **Plugin marketplace**：在 Claude Code 中，本仓库可被注册为插件市场，并安装 `document-skills` 或 `example-skills` 插件。
- **Agent Skills 标准**：README 顶部说明，关于 Agent Skills 标准的信息见 agentskills.io。

## 前置依赖

README 未提供本仓库运行所需的完整依赖清单。根据 README 可确认的信息：

- 使用 Claude Code 方式时，需要 Claude Code 环境，因为相关命令是 Claude Code 的斜杠命令。
- 使用 Claude.ai 方式时，README 说明这些示例 skills 已对 Claude.ai 的付费计划可用。
- 使用 Claude API 方式时，README 指向 Skills API Quickstart 文档。
- 仓库主语言为 Python（来自仓库元信息），但 README 未说明具体 Python 版本要求。

README 未提供 Node、Ruby 或其他运行时依赖说明。

## 安装与配置

本工具不直接作用于 Jekyll 博客站点本身。它是 Claude 的 skills 仓库，与 Jekyll 3.9.5 静态博客、GitHub Pages 部署、`scripts/` 下的 Python 标准库脚本以及 GitHub Actions 工作流之间，README 未描述任何直接集成点。因此以下步骤是在你的 Windows 10/11 本地环境中试用该仓库的方式，而非改造博客的步骤。

1. 确认你已具备使用入口。README 给出三种入口：Claude Code、Claude.ai、Claude API。请先确定你要用哪一种。
2. 若使用 Claude Code：在 Claude Code 中运行 `/plugin marketplace add anthropics/skills`，把本仓库注册为插件市场。
3. 安装具体插件。README 给出两种方式：
   - 交互式：选择 `Browse and install plugins`，再选择 `anthropic-agent-skills`，然后选择 `document-skills` 或 `example-skills`，最后选择 `Install now`。
   - 直接安装：`/plugin install document-skills@anthropic-agent-skills` 或 `/plugin install example-skills@anthropic-agent-skills`。
4. 若使用 Claude.ai：README 说明这些示例 skills 已对付费计划可用；使用本仓库中的 skill 或上传自定义 skill，请按「Using skills in Claude」文档操作。
5. 若使用 Claude API：README 指向 Skills API Quickstart，用于使用 Anthropic 预置 skills 与上传自定义 skills。
6. 若你想自己创建 skill：按 README 的说明，新建一个文件夹，放入 `SKILL.md`，frontmatter 至少写 `name` 与 `description`，正文写指令、示例与指南；也可以使用仓库中的 `template-skill` 作为起点。

README 未提供在 Windows 上克隆仓库、安装 Python 依赖或配置环境变量的具体命令。

## 最小可用示例

下面这段内容可以整段复制给任意 AI 编程助手，用于在你的本地环境中落地一个最小 skill。

```text
背景：我在 Windows 10/11 本地开发机上工作，已安装 Python 3.12 与 Ruby。我的项目是一个 Jekyll 3.9.5 静态博客（GitHub Pages 部署，仓库 windbellbj/windbellbj.github.io），其中包含用 Python 标准库编写的 scripts/ 自动化脚本和 GitHub Actions 工作流。我现在想试用 anthropics/skills 仓库所描述的 Agent Skills 机制。

目标：帮我创建一个最小的自定义 skill，用于辅助维护这个 Jekyll 博客。

要求：
1. 按 anthropics/skills README 的说明，skill 是一个文件夹，里面必须有一个 SKILL.md。
2. SKILL.md 必须包含 YAML frontmatter，且只包含 README 要求的两个字段：name（小写、用连字符代替空格）和 description（完整描述这个 skill 做什么、何时使用）。
3. frontmatter 下方是 Markdown 正文，写清 Claude 在该 skill 激活时应遵循的指令、示例和指南。
4. 请把该 skill 放在我项目中的一个独立文件夹里，不要改动我现有的 Jekyll 配置、scripts/ 脚本和 GitHub Actions 工作流。
5. 创建完成后，告诉我如何验证这个 skill 的 frontmatter 与正文结构是否符合 README 描述。
6. 如果 README 没有说明某个细节（例如具体目录命名规范、字段长度限制），请明确标注「README 未提供」，不要自行编造。
```

## 验证方法

README 未提供专门的验证命令或测试脚本。可执行的验证步骤基于 README 中可确认的事实：

1. 结构验证：确认你创建的 skill 是一个独立文件夹，且其中存在 `SKILL.md`。
2. frontmatter 验证：确认 `SKILL.md` 顶部的 YAML frontmatter 至少包含 `name` 与 `description` 两个字段，且 `name` 为小写、用连字符代替空格。
3. 正文验证：确认 frontmatter 下方存在 Markdown 指令内容，且包含示例与指南。
4. 使用验证（Claude Code 路径）：按 README 描述，安装插件后「只需提及该 skill 即可使用」。例如 README 给出的示例是：安装 `document-skills` 插件后，可以让 Claude Code 执行类似「Use the PDF skill to extract the form fields from `path/to/some-file.pdf`」的请求。你可以用自己创建的 skill 做类似提及式调用，观察是否被加载。
5. 使用验证（Claude.ai 路径）：按 README 指向的「Using skills in Claude」文档操作后，在对话中调用该 skill。
6. 使用验证（Claude API 路径）：按 README 指向的 Skills API Quickstart 操作。

README 未提供自动化测试、CI 校验或 lint 工具的说明。

## 风险与注意事项

- README 的 Disclaimer 明确写道：这些 skills 仅用于演示与教育目的。虽然其中某些能力可能在 Claude 中可用，但你从 Claude 得到的实现与行为可能与这些 skills 中展示的不同。这些 skills 意在说明模式与可能性。
- README 强调：在把 skills 用于关键任务之前，务必在你自己的环境中充分测试。
- 许可差异：README 说明仓库中许多 skills 是开源的（Apache 2.0），但 `skills/docx`、`skills/pdf`、`skills/pptx`、`skills/xlsx` 是 source-available 而非开源。使用时需注意这一区别。
- README 未提供安全审计、权限模型、数据隐私或生产环境部署风险的说明。
- README 未提供版本兼容性矩阵或对特定 Claude 产品版本的保证。

## 替代方案

README 未提供替代方案的对比。README 中提到的相关资源包括：

- Agent Skills 标准：agentskills.io。
- 官方支持文档：「What are skills?」「Using skills in Claude」「How to create custom skills」。
- 工程博客：「Equipping agents for the real world with Agent Skills」。
- 合作伙伴 skills：README 的 Partner Skills 一节提到 Notion 的「Notion Skills for Claude」。

除上述内容外，README 未提供其他替代工具或方案的说明。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
