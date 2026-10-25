---
layout: post
title: "Omnara：可自托管的持久化 Agent 平台"
subtitle: "开源版 Claude Managed Agents，用 API 跑持久化智能体，Postgres 存状态、任意机器当执行沙箱"
date: 2026-10-26 03:25:43 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - Agent Harness
news_category: harness
---

- 来源：Hacker News Show HN
- 项目链接：https://github.com/omnara-ai/omnara
- HN 讨论：https://news.ycombinator.com/item?id=50183892（114 points）

---

# Omnara：把「Agent 运行壳」做成可自托管的 API

> 一句话定位：Omnara 是一个开源、可自托管的「托管式 Agent 平台」，对标 Claude Managed Agents 与 OpenAI Agents API——你用一次 API 调用创建 Agent，它负责跑 Agent 循环、分配沙箱、管理密钥/权限/RBAC，状态存在 Postgres 里，重启不丢、空闲不烧钱。适合想把 Agent 从「笔记本上的一个进程」升级成「云端可持久运行的服务」的后端工程师。

## 它是什么

作者 Kartik 在 Show HN 里讲得很直白：早期他们做的是给 Claude Code / Codex 远程遥控的手机 App，但 harness 跑在笔记本上，合盖就停，搬到云沙箱又要同步代码和 Agent 状态。于是他们重做成**云端运行 Agent、任何客户端通过 API 对话、同时仍能把你的笔记本当作它的执行机器之一**。

官方自我定位是「像 opencode / codex 那样的 harness server，但是持久、可扩展」，并自带文件与 shell 工具、子 Agent、上下文压缩、权限确认、MCP、skills、memory 等常规 harness 能力。

## 为什么值得看：架构上的两个关键选择

**1. 日志即 Agent，落在 Postgres 里**

- 多数 harness（Claude Code、Codex、OpenCode、Pi、Goose 等）把 Agent 循环跑在一个长生命周期进程里，日志写 JSONL 或 SQLite 文件。
- Omnara 把日志做成 Postgres 中的**追加式事件日志**，输入、模型输出、工具调用分别存为带类型的表。
- 循环跑在**无状态 worker** 上：一个 worker 只跑一轮（一次模型调用，或它产生的工具调用），然后释放 Agent，把下一轮丢进 Postgres 队列，谁空闲谁接。因此同一 Agent 的每一轮可以跑在不同机器的不同进程上。
- 每轮结果在**一个事务**里提交：模型输出、工具调用、用量、下次唤醒一起成功或一起失败；worker 中途挂掉则不提交，租约过期后由别的 worker 重试。
- 等待用户、等待工具、等待重试的 Agent **不占用 worker**，所以一个 worker 能复用给成千上万个 Agent。

**2. 控制面与执行面分离**

- 跑 Agent 循环的 worker 所在机器，**不是** Agent 执行命令的机器。
- 任何有网的 macOS / Linux 机器（你的笔记本、任意云沙箱）跑一个小守护进程 `omnarad`，主动向外连接 Omnara，**不需要开放入站端口**。
- Agent 由此获得该机器上的工具，比如执行命令、编辑文件；一个 Agent 可以接多台机器。

<!-- asset:blog-1 start -->
![事件日志+无状态worker+租约重试](/img/ai-news/hn-omnara-open-source-alternative-to-claude-man-183892/blog-1.png)

*图：事件日志+无状态worker+租约重试*
<!-- asset:blog-1 end -->


## 社区怎么评价

HN 上 114 points，讨论集中在「持久化 Agent 是不是新东西」这一点上，观点分裂：

- 支持方：有人提到相关演讲 *log is agent*，作者回应「日志即 Agent 是我们把持久性做进 harness 的核心洞察」。也有人提到 pi-durable 等同类项目，认为大家正在向「持久化 Agent」收敛（pi durable、Cloudflare Agents on Durable Objects、Vercel durable harness）。
- 质疑方：有评论认为这不过是「任何 Chat Web UI 背后的那个 API」，持久化、可恢复、错误恢复、分支与 fork 从第一版 ChatGPT 起就是标配；也有人指出 Codex 一直用追加式 `.jsonl` 存会话，「日志放文件还是放数据库没区别」。
- 作者回应：去年 Claude、Codex 等确实是把一切存在磁盘上的一个大 JSON 文件里，现在越来越多人改成这种设计。

**给读者的判断**：争论的焦点是「新颖性」，不是「可用性」。如果你只是想要一个本地编码助手，Omnara 的卖点对你意义不大；如果你需要**多租户、可恢复、按需唤醒的 Agent 服务**，它的架构取舍值得读。

## 对 Java 后端 / Windows + Trae Work 用户的价值

需要如实说明：**Omnara 本身不是 AI 编程助手、不是 IDE 插件，也不是给 Trae Work 用的 Skill 包**，它和「在 IDE 里补全代码」这条线基本无关。它的价值在另一侧：

| 场景 | 是否值得试 |
| --- | --- |
| 想在 IDE 里更快写 Spring 代码 | 不必，直接用 Trae Work 即可 |
| 想给团队/产品做一个可自托管的 Agent 后端服务 | 值得，架构与 API 设计可参考 |
| 想把长任务 Agent 跑在云上、笔记本只当执行机 | 值得，`omnarad` 主动外连的设计对 Windows 内网环境友好 |
| 想找 Java/Spring 生态的现成 SDK | 暂无公开资料，官方示例以 CLI 与 YAML 为主 |

几点现实提醒：

- 官方快速开始用的是 **Node.js 22+ 的 CLI**（`npx omnara ...`），仓库主体是 Go（有 `go.mod`、`cmd`、`internal`、`sqlc.yaml`），**没有看到 Java 客户端**。
- 守护进程 `omnarad` 官方描述支持 **macOS / Linux**，Windows 是否可直接跑，**官方未公开说明**；在 Windows 上更现实的做法是把它跑在 WSL 或一台 Linux 机器上。
- 自托管需要 Postgres，仓库提供 `compose.yaml` / `compose.override.yaml`，属于「有 Docker 就能起」的路子。
- 许可证 Apache-2.0，可商用自托管；也可直接用 Omnara Cloud。

<!-- asset:blog-2 start -->
![Java后端视角的价值与提醒](/img/ai-news/hn-omnara-open-source-alternative-to-claude-man-183892/blog-2.png)

*图：Java后端视角的价值与提醒*
<!-- asset:blog-2 end -->


## 怎么开始试用

**路线 A：云端最快验证（不改本地环境）**

1. 在 `app.omnara.com` 登录，首个项目自带模型提供方 `omnara-openrouter` 和一个托管沙箱池 `default-pool`。
2. 把示例配置存为 `agent.yaml`：版本 `v1`、一段 instruction、`model.provider_config: omnara-openrouter`、`machine_sources` 指向 `default-pool`。
3. 用 Node.js 22+ 执行 `npx omnara agents launch --file agent.yaml --name "Machine assistant" --message "..."`，首次会打开浏览器登录。
4. 用 `npx omnara agents chat <agent-id>` 在终端对话，或到 dashboard 里看。

**路线 B：自托管**

1. 克隆仓库，参考 `compose.yaml` 起服务（需要 Postgres）。
2. 参照 `.env.example` 配置环境变量，接自己的模型提供方。
3. 在目标机器上跑 `omnarad` 守护进程，让它主动连回你的 Omnara 实例。
4. 用 API 创建 Agent、发消息、流式接收事件。

**路线 C：只想读设计**

直接看仓库里的 `api/openapi`、`migrations`、`internal` 与 `skills/setup-omnara-agent`，把「事件日志 + 无状态 worker + 租约重试」这套模式对照你熟悉的 Spring 事务与消息队列来理解，收获可能比装起来更大。

<!-- asset:code-1 start -->
```powershell
npx omnara agents launch --file agent.yaml --name "Machine assistant" --message "..."
npx omnara agents chat <agent-id>
```
<!-- asset:code-1 end -->


## 一句话结论

Omnara 是一个**架构清晰、可自托管的 Agent 运行壳**，不是编码助手。Java 后端值得花半小时读它的持久化设计；想立刻提升写代码效率的话，这条可以先跳过。

```text
背景：我在 Windows 上用 Trae Work 做 Java/Spring 后端开发，看到开源项目 Omnara（github.com/omnara-ai/omnara），它是可自托管的「托管式 Agent 平台」，对标 Claude Managed Agents：用 API 创建 Agent，Agent 循环跑在无状态 worker 上，事件日志存 Postgres，每轮一个事务提交、失败靠租约重试，执行命令的机器通过主动外连的守护进程 omnarad 接入。

目标：帮我判断它是否值得引入我的日常工作流，并给出最小验证路径。

要求：
1. 先用 5 句话讲清它的核心机制，重点解释「事件日志 + 无状态 worker + 租约重试」相比单进程 harness 的实际收益与代价。
2. 明确回答：它能否替代或增强我在 Trae Work 里的编码体验？如果不能，说明它真正适合的场景。
3. 评估在 Windows 环境下的可行性：omnarad 是否支持 Windows、是否需要 WSL、自托管需要哪些依赖（Postgres、Docker、Node 版本等）。若资料不足请直接说「官方未公开说明」，不要猜测。
4. 给出两条路线的最小可执行步骤：A 用 Omnara Cloud 快速验证；B 本地自托管。每步写清命令或配置文件要点。
5. 从 Java/Spring 工程师视角，指出这套架构里可以借鉴到后端系统的设计点（事务边界、幂等、租约、队列），并指出潜在坑。
6. 最后给一个明确结论：现在就试 / 观望 / 跳过，并说明理由。
```

---

> 本文由 AI 综合Show HN 原帖与社区讨论撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
