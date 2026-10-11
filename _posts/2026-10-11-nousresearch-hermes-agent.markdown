---
layout: post
title: "Hermes Agent 上手：会自己长技能的 AI 智能体"
subtitle: "Nous Research 出品，自带学习闭环，Windows 原生可跑，还能接 Telegram"
date: 2026-10-11 23:45:03 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/NousResearch/hermes-agent
- Stars：252731
- 语言：Python
- 创建时间：2025-07-22
- 最近更新：2026-10-11
- 官方简介：The agent that grows with you

---

## 解决什么问题

README 把 Hermes Agent 定位为「自我改进的 AI 智能体」（The self-improving AI agent），由 Nous Research 打造。它声称是「唯一内置学习闭环的 agent」：能从经验中创建技能、在使用中改进技能、主动提醒自己持久化知识、检索自己过去的对话，并跨会话构建对你的持续加深的模型。

从工程视角看，它要解决的是「AI 助手每次对话都从零开始」的问题：

- **经验不沉淀**：复杂任务完成后会自动创建技能（autonomous skill creation after complex tasks），技能在使用中自我改进。
- **记忆不连续**：agent 自管理的记忆配合周期性提醒（periodic nudges），并用 FTS5 会话搜索 + LLM 摘要实现跨会话回忆，另有 Honcho 的辩证式用户建模。
- **绑定本机**：它不绑定在你的笔记本上，可以跑在 5 美元 VPS、GPU 集群或空闲时几乎不花钱的 serverless 基础设施上，你从 Telegram 就能和它对话。
- **模型锁定**：支持 Nous Portal、OpenRouter、OpenAI、你自己的 endpoint 等多家 provider，用 `hermes model` 切换，无需改代码。

README 未提供针对 Java / Spring 项目的专门能力说明。

## 核心概念

README 中明确出现的核心概念如下：

- **学习闭环（closed learning loop）**：agent 自管理记忆 + 周期性提醒；复杂任务后自主创建技能；技能在使用中自我改进；FTS5 会话搜索配合 LLM 摘要做跨会话回忆；Honcho 辩证式用户建模；兼容 agentskills.io 开放标准。
- **终端界面（TUI）**：完整 TUI，支持多行编辑、斜杠命令自动补全、会话历史、打断并重定向（interrupt-and-redirect）、流式工具输出。
- **消息网关（gateway）**：Telegram、Discord、Slack、WhatsApp、Signal 和 CLI 全部来自单个 gateway 进程；支持语音备忘转录、跨平台会话连续性。
- **定时自动化**：内置 cron 调度器，可投递到任意平台，用自然语言描述日报、夜间备份、每周审计等无人值守任务。
- **委派与并行**：可派生隔离的 subagent 并行工作；可写 Python 脚本通过 RPC 调用工具，把多步流水线压缩成零上下文成本的回合。
- **七种终端后端**：local、Docker、SSH、Singularity、Modal、Daytona、Vercel Sandbox；其中 Daytona 与 Modal 提供 serverless 持久化，空闲时休眠、按需唤醒。
- **面向研究**：批量轨迹生成、轨迹压缩，用于训练下一代工具调用模型。
- **两个入口**：用 `hermes` 启动终端 UI，或运行 gateway 后从 Telegram、Discord、Slack、WhatsApp、Signal、Email 对话；进入会话后许多斜杠命令在两个界面通用。
- **MCP 集成**：文档目录中有 MCP Integration 一节，说明可连接任意 MCP server 以扩展能力。

## 前置依赖

README 明确提到的依赖与前提：

- **Windows 原生安装**：PowerShell 一行命令即可，CLI、gateway、TUI 和工具全部原生可用，不需要 WSL。若更想用 WSL2，Linux/macOS 的一行命令在 WSL2 中同样可用。
- **安装器代管的组件**：源码安装器把 Python 3.14、Node.js、npm、ripgrep、FFmpeg 以及 Python 依赖交给 PM 处理。
- **Git**：如果系统没有 Git，安装器会把经过校验的 Git for Windows 归档放进 Hermes 的工具存储中，不会替换你的系统 Git。
- **安装位置**：Windows 原生安装位于 `%LOCALAPPDATA%\hermes`；WSL2 安装位于 `~/.hermes`，与 Linux 相同。
- **模型 provider**：可使用 Nous Portal、OpenRouter、OpenAI、你自己的 endpoint 等；README 未提供完整的 provider 清单，只给出文档链接。
- **Android / Termux**：aarch64 设备有签名 APT 仓库，分 `stable`（带 tag 的发布）与预发布 `canary` 两个通道，包内含 Python、Node.js 和 TUI，需使用 Termux 指南而非桌面/服务器安装脚本。

README 未提供具体的磁盘空间、内存、网络等硬件门槛数值。

## 安装与配置

以下步骤按「Windows + Trae Work 的 Java 程序员」视角组织。

**第一步：在 PowerShell 中安装（Windows 原生）**

1. 打开 PowerShell。
2. 执行 `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`。
3. 等待安装器完成，它会代管 Python 3.14、Node.js、npm、ripgrep、FFmpeg 与 Python 依赖；若缺少 Git，会把校验过的 Git for Windows 归档放进 Hermes 工具存储。
4. 安装完成后，程序位于 `%LOCALAPPDATA%\hermes`。

如果你更想用 WSL2，则改用 Linux/macOS 的一行命令 `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`，安装位置为 `~/.hermes`。

**第二步：初始化与配置**

1. 在终端执行 `hermes setup`，运行完整安装向导，一次性配置所有内容。
2. 执行 `hermes model` 选择 LLM provider 与模型。
3. 执行 `hermes tools` 配置启用哪些工具。
4. 需要单项配置时用 `hermes config set` 与 `hermes config get`。
5. 如果不想分别收集模型、网页搜索、图像生成、TTS、云浏览器五套 API key，可执行 `hermes setup --portal`：它会通过 OAuth 登录、把 Nous 设为 provider 并开启 Tool Gateway；之后用 `hermes portal info` 随时查看接线情况。
6. 如果是从 OpenClaw 迁移过来，可用 `hermes claw migrate`（支持 `--dry-run`、`--preset user-data`、`--overwrite`）。

**第三步：融入 Trae Work 日常工作流**

README 未提供与 Trae Work / Java 的集成方式。README 中与「接入其他工具」相关的唯一线索是文档目录里的 MCP Integration 一节（Connect any MCP server for extended capabilities），以及社区项目 computer-use-linux 被描述为「面向 Hermes 和其他 MCP host 的 Linux 桌面控制 MCP server」——也就是说 Hermes 自身可以作为 MCP host 去连接别的 MCP server，但 README 没有说明 Hermes 能否作为 MCP server 被 Trae Work 调用，也没有给出任何 Trae Work 侧的配置路径或命令。

因此，在 Trae Work 中可行的做法仅限于：在 Trae Work 的内置终端里把它当普通 CLI 使用（执行 `hermes` 进入交互式 CLI，或执行 `hermes gateway` 启动消息网关），以及在 Java/Spring 项目中把它当作一个独立的命令行工具来调用。README 未提供 Skill 目录放置方式、MCP 服务接入方式，也未提供 Java/Spring SDK 或 HTTP 集成方式。

**第四步：常用维护命令**

- `hermes update` 更新到最新版本。
- `hermes doctor` 诊断问题。
- `hermes gateway setup` 与 `hermes gateway start` 启动消息网关。

## 最小可用示例

把下面这段整段复制给 Trae Work，让它帮你在本地把 Hermes Agent 跑起来并做一次 Java 场景试用。

```text
背景：我在 Windows 上开发，主力语言是 Java / Spring，日常用 Trae Work 写代码。我想试用 Nous Research 的 Hermes Agent（仓库 NousResearch/hermes-agent），它是一个自带学习闭环的 AI 智能体，支持 Windows 原生安装。

目标：
1. 在我的 Windows 机器上完成 Hermes Agent 的原生安装，并确认安装位置在 %LOCALAPPDATA%\hermes。
2. 完成初始化配置，选定一个可用的模型 provider 与模型。
3. 跑通一次真实对话，并让它帮我处理一个 Java 相关的具体任务。

要求：
- 安装只用官方 PowerShell 一行命令，不要用 WSL，也不要自己编译源码。
- 每一步都告诉我该在哪个终端里执行、执行什么命令、预期看到什么输出。
- 如果 Windows Defender 或杀毒软件把 %LOCALAPPDATA%\hermes\bin\uv.exe 报成恶意软件，先按官方说明做真实性校验（用 gh attestation verify 校验 astral-sh/uv 的发布包，并比对文件哈希），确认无误后再把整个 bin 文件夹加入白名单，不要只加文件哈希。
- 配置完成后，用 Hermes 帮我做这件事：读取我当前 Spring Boot 项目里的一个 Controller 类，解释它的接口契约，并给出三条可落地的改进建议。
- 全程不要编造 Hermes 的命令；只用官方 README 里出现过的命令，例如 hermes、hermes setup、hermes model、hermes tools、hermes config set、hermes config get、hermes gateway、hermes doctor、hermes update。
- 最后告诉我：Hermes 的哪些能力（记忆、技能、cron、subagent、消息网关）适合我这种 Java 后端日常使用，哪些暂时用不上。
```

## 验证方法

按 README 提供的信息，可用以下步骤验证安装是否可用：

1. **确认命令存在**：在终端执行 `hermes`，README 说明这会启动交互式 CLI 并开始对话。
2. **确认模型可用**：执行 `hermes model`，应能进入 LLM provider 与模型的选择流程。
3. **确认工具配置可用**：执行 `hermes tools`，应能配置启用哪些工具。
4. **确认配置读写可用**：执行 `hermes config get` 打印单项配置值，执行 `hermes config set` 设置单项配置值。
5. **确认诊断可用**：执行 `hermes doctor`，README 说明它用于诊断任何问题。
6. **确认版本更新通道可用**：执行 `hermes update`，README 说明它更新到最新版本。
7. **确认消息网关可用**：执行 `hermes gateway setup` 与 `hermes gateway start`，然后给机器人发一条消息；README 说明 CLI 与消息平台共享 `/new`、`/reset`、`/model`、`/personality`、`/retry`、`/undo`、`/compress`、`/usage`、`/insights`、`/skills` 等斜杠命令。
8. **确认 Portal 接线情况**：若使用了 `hermes setup --portal`，执行 `hermes portal info` 查看已接好的能力。
9. **确认 Windows 安装位置**：检查 `%LOCALAPPDATA%\hermes` 目录是否存在。

README 未提供单元测试、健康检查端点或性能基准类的验证方式。

## 风险与注意事项

- **杀毒软件误报**：README 明确警告，Windows Defender 或 Bitdefender 等可能把 `%LOCALAPPDATA%\hermes\bin\uv.exe` 隔离，这是误报。该文件是 Astral 的 `uv`（Rust 写的 Python 包管理器），基于机器学习的杀毒引擎常把「会下载并安装包的无签名 Rust 二进制」标记为可疑。README 给出了用 `gh attestation verify` 校验 astral-sh/uv 发布包并比对哈希的验证流程，并建议把整个 `bin` 文件夹加入白名单而不是文件哈希，因为 Hermes 每次更新 `uv` 哈希都会变。
- **安装器会改动工具链**：源码安装器把 Python 3.14、Node.js、npm、ripgrep、FFmpeg 和 Python 依赖交给 PM 处理；若系统没有 Git，它会暂存一份校验过的 Git for Windows 归档到 Hermes 工具存储中（README 强调不会替换系统 Git）。对已有 Java 工具链的机器，建议先确认这些组件不会与现有环境冲突。
- **平台差异**：Android / Termux 必须使用专门的 Termux 指南，不能用桌面/服务器安装脚本；Windows 原生与 WSL2 的安装位置不同（`%LOCALAPPDATA%\hermes` 与 `~/.hermes`）。
- **更新归属**：README 提到 MSIX/App Installer 包有独立的更新归属，具体细节指向安装文档，README 未展开。
- **权限与安全**：文档目录中有 Security 一节，涉及命令审批、DM 配对、容器隔离，但 README 正文未给出具体默认策略，README 未提供细节。
- **与 Trae Work / Java 的集成**：README 未提供与 Trae Work / Java 的集成方式，也没有给出任何 Java SDK、HTTP 接口或 Spring 集成说明。
- **模型与费用**：README 未提供各 provider 的价格、配额或速率限制信息。

## 替代方案

README 中直接提到的可替代或可迁移对象：

- **OpenClaw**：README 专门有一节「Migrating from OpenClaw」，说明 Hermes 可以自动导入其设置、记忆、技能和 API key。首次运行 `hermes setup` 时会自动检测 `~/.openclaw` 并询问是否迁移；也可随时执行 `hermes claw migrate`（支持 `--dry-run` 预览、`--preset user-data` 不迁移密钥、`--overwrite` 覆盖冲突）。导入内容包括 SOUL.md 人设文件、MEMORY.md 与 USER.md 记忆条目、用户创建的技能（导入到 `~/.hermes/skills/openclaw-imports/`）、命令允许列表、消息设置、API key（Telegram、OpenRouter、OpenAI、Anthropic、ElevenLabs）、TTS 资源、工作区指令 AGENTS.md。也可使用 `openclaw-migration` 技能做交互式、带 dry-run 预览的迁移。
- **HermesClaw**：社区微信桥，可在同一个微信账号上同时运行 Hermes Agent 和 OpenClaw。
- **computer-use-linux**：面向 Hermes 和其他 MCP host 的 Linux 桌面控制 MCP server，具备 AT-SPI 无障碍树、Wayland/X11 输入、截图和合成器窗口定位能力。

README 未提供其他同类 agent 框架的对比或替代建议。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
