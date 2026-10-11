---
layout: post
title: "rehan-remade/universal-modder"
subtitle: "Point Claude at any game. Skills, tools and the fal MCP that"
date: 2026-10-11 22:25:57 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
---

- 仓库：https://github.com/rehan-remade/universal-modder
- Stars：6548
- 语言：Python
- 创建时间：2026-09-30
- 官方简介：Point Claude at any game. Skills, tools and the fal MCP that let Claude Code mod almost any PC game you own: recon, reverse engineering, fal-generated art/3D/audio, in-game testing, showcase videos.

---

> AI 生成服务本次不可用，以下内容由脚本按规则从 README 提取，可能不完整。

## 解决什么问题

Point Claude at any game. Skills, tools and the fal MCP that let Claude Code mod almost any PC game you own: recon, reverse engineering, fal-generated art/3D/audio, in-game testing, showcase videos.

## 核心概念

README 未提供专门的概念说明，请结合官方文档确认。

## 前置依赖

见下方 README 安装章节，或让 AI 助手协助确认。

## 安装与配置

## Install

Pick your agent. Each gets the same skills (Agent Skills format), the fal MCP server, and the `um` CLI.

| Agent | Install |
|---|---|
| **Claude Code** | `/plugin marketplace add rehan-remade/universal-modder`<br>`/plugin install universal-modder@universal-modder` |
| **Codex** | `codex plugin marketplace add rehan-remade/universal-modder`<br>`codex plugin add universal-modder@universal-modder` |
| **Gemini CLI** | `gemini extensions install https://github.com/rehan-remade/universal-modder` |
| **VS Code / Copilot** | Enable `chat.plugins.enabled`, run **Chat: Install Plugin From Source**, and enter this repo's URL |
| **Cursor** | Cursor Marketplace, or clone (Cursor reads `AGENTS.md` and `.cursor/mcp.json`) |
| **OpenCode** | Clone and run `opencode` inside it (`opencode.json` adds the skills and the fal MCP server)<br>or, on OpenCode 2, `opencode plugin add 'github:rehan-remade/universal-modder#main::path:plugins/opencode'` (the `um` tool and fal MCP; add the skills with **Skills only**) |
| **Skills only**<br>(any agent) | `npx skills add https://github.com/rehan-remade/universal-modder` |
| **Anything else** | `git clone https://github.com/rehan-remade/universal-modder` and start your agent inside it |

Inside a clone, each agent finds the skills where it looks for them: `.agents/skills` (Codex, Gemini CLI,
Copilot, Cursor, OpenCode) and `.claude/skills` (Claude Code) are copies of `skills/`. Instructions are in
`AGENTS.md`, which `CLAUDE.md` and `GEMINI.md` point to. MCP config is in `.mcp.json`, `.codex/config.toml`,
`.cursor/mcp.json`, `.vscode/mcp.json` and `opencode.json` (which also points OpenCode at `skills/`).

Without a clone, OpenCode 2 installs the plugin in `plugins/opencode/` with `opencode plugin add`: one
`um_run` tool that passes its arguments straight to the CLI and runs `um` from PATH (see below), plus the
fal MCP server when `FAL_KEY` is set and none is configured. A clone doesn't need it. See
`plugins/opencode/README.md`.

**The `um` CLI.** Plugin installs and clones put it on PATH (OpenCode's plugin install doesn't). Anywhere else:
```bash
uv tool install git+https://github.com/rehan-remade/universal-modder     # or: pipx install git+...
```
**For assets,** get a [fal API key](https://fal.ai/dashboard/keys). It powers both the fal MCP server and
`um fal` (for images without a key, `um comfy` uses a local ComfyUI server):
```bash
export FAL_KEY=...
```
You also need Git, Python 3.10+ and ffmpeg. `uv` is recommended. Blender is needed for 3D → sprite renders.
Windows games are driven natively or from WSL.

## 最小可用示例

将下面指令整段复制给任意 AI 助手，让它结合你的环境给出可执行步骤：

```text
你是一名资深工程师助手。我想在当前项目中了解并评估下面这个 AI 工具/技能：

名称：rehan-remade/universal-modder
链接：https://github.com/rehan-remade/universal-modder
官方简介：Point Claude at any game. Skills, tools and the fal MCP that let Claude Code mod almost any PC game you own: recon, reverse engineering, fal-generated art/3D/audio, in-game testing, showcase videos.
Stars：6548

请先阅读它的 README 与官方文档，然后：
1. 用中文说明它解决什么问题、核心概念与前置依赖；
2. 结合我的环境（Windows + Python 3.12 + Ruby + Jekyll 静态博客）给出安装、配置步骤和最小可用示例；
3. 给出验证方法，并指出风险与替代方案；
4. 关键信息缺失时先列出需要我确认的问题，不要擅自假设。
```

## 验证方法

按安装章节执行后，以 README 中的用法示例运行验证；也可让 AI 助手根据你的实际环境给出验证命令。

## 风险与注意事项

新项目可能存在 API 变动、依赖冲突或安全风险，引入前请审查仓库与许可证。

## 替代方案

README 未提供替代方案对比，可让 AI 助手基于同类工具给出。

---

> 本文 AI 生成服务本次不可用，由脚本规则提取/兜底生成，详情请查阅来源：GitHub README。
