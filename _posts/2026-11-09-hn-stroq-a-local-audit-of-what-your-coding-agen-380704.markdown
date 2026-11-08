---
layout: post
title: "Stroq：给编码 Agent 做本地审计与命令拦截"
subtitle: "读 Claude Code/Codex 会话，查密钥外泄、追命令来源，用本地 hooks 拦危险命令"
date: 2026-11-09 04:56:12 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - Agent Harness
news_category: harness
---

- 来源：Hacker News Show HN
- 项目链接：https://github.com/AGGIB/Stroq
- HN 讨论：https://news.ycombinator.com/item?id=50380704（93 points）

---

# Stroq：给编码 Agent 做本地审计与命令拦截

> 一句话定位：一个本地运行的 AI 编码 Agent 安全审计工具，读你的 Claude Code / Codex 会话记录，找出密钥外泄与「命令来自 Agent 读到的文本」的痕迹，并用本地 hooks 在下次执行前拦下危险命令。适合把编码 Agent 放权跑在自己机器上、又担心它乱执行的人。

## 它是什么

Stroq 是开源（Apache-2.0）、无遥测的本地安全平台，面向 Claude Code、Cursor、Codex CLI 等编码 Agent。核心是两件事：

- **事后审计**：读取你最近 30 天的 Agent 会话、密钥文件、Agent 工作过的目录，生成一张「卡片」，显示有多少命令来自 Agent 读到的文本、哪些密钥离开了你的机器。只打印密钥名，不打印值。
- **事前拦截**：`stroq init` 安装 hooks，在每个工具调用执行前判断——拒绝 `curl | sh`、拒绝携带已知密钥的对外请求；当命令重复了 Agent 读过的文本时，先问你并指出那段文本。

本地只写 `~/.stroq` 下一个小缓存，不发任何数据，不需要账号。需要 Node.js 22 或更高版本。

## 为什么值得试

对 Java 后端 + Windows + Trae Work 的日常场景，价值主要在三点：

1. **看得见**：Agent 在你项目里跑过什么、为什么跑，有据可查，而不是靠记忆。
2. **拦得住一部分**：`stroq init` 后，明显危险的命令会先弹确认，而不是直接执行。
3. **查收来的代码**：`stroq inspect` 可以在打开/运行别人发来的目录之前先扫一遍。

但要清楚它的边界——这也是 HN 讨论里最集中的质疑。

## 社区怎么评价

HN 讨论（93 points）里最有价值的是这条批评：

> 「审计」怎么防危险命令？听起来太晚了——如果 Agent 已经在你个人电脑上跑了 `rm -rf`，事后看到 16:48 的记录有什么用？这解决的是错的问题。至少给它单独的用户、限制路径和网络，别指望「审计」来防。

作者本人直接承认：

> 你说得对。那条命令只生成报告，不阻止任何事。`stroq init` 装 hooks 会在危险命令执行前要求确认——但那是过滤器，不是沙箱。

另有评论补充了审计的必要性：访问控制策略很难一开始就定好，权限会随时间膨胀，审计能让你在没出大事之前发现策略漏洞。

还有真实案例讨论：伪装成面试仓库的恶意代码（controller 里藏 `eval()`、zip 里带 `.git/hooks`），作者回应——第一种场景 hook 只能检测到 `npm test` 命令本身；第二种场景 `stroq inspect` 能在打开目录前识别 hook 并告警，并表示会据此改进。

有人建议做成常驻后台守护 + 菜单栏告警，作者回复「好主意」。

**结论**：它是有用的审计与轻量过滤层，不是沙箱。别把它当安全边界。

## 怎么开始试用

前置：Node.js 22+。以下命令在项目目录或任意终端执行：

1. `npx @stroq/cli` —— 生成你自己的会话卡片（读最近 30 天会话，只打印密钥名）。
2. `npx @stroq/cli show 1` —— 查看卡片上某个时刻背后的证据。
3. `npx @stroq/cli init` —— 安装 hooks，开始拦截。
4. `npx @stroq/cli inspect` —— 在运行别人发来的目录前先检查。
5. `npx @stroq/cli why` —— 查看某次操作为什么被拦。
6. `npx @stroq/cli attack` —— 在沙箱里看 Stroq 拦下 36 种已知攻击。
7. `npx @stroq/cli uninstall` —— 卸载。

其他命令用 `npx @stroq/cli help --all` 查看。

<!-- asset:code-1 start -->
```powershell
npx @stroq/cli
npx @stroq/cli show 1
npx @stroq/cli init
npx @stroq/cli inspect
npx @stroq/cli why
npx @stroq/cli attack
npx @stroq/cli uninstall
```
<!-- asset:code-1 end -->


## 对 Trae Work 用户的现实判断

- **与 AI 辅助开发有关**，不用跳过。
- 官方明确支持的 Agent 是 Claude Code、Cursor、Codex CLI 等；**Trae Work 是否在支持列表内，暂无公开资料**，`init` 的 hooks 能否挂到 Trae Work 上，官方未公开说明。
- 在 Windows 上，`~/.stroq` 缓存路径与 hooks 的具体落点，官方未公开说明。
- 最稳妥的用法：先用 `npx @stroq/cli` 和 `inspect` 做只读审计（不依赖 Agent 集成），确认价值后再试 `init`。

```text
背景：我是 Java/Spring 后端程序员，在 Windows 上用 Trae Work（AI IDE）开发，想评估 Stroq（https://github.com/AGGIB/Stroq）这个本地 AI 编码 Agent 安全审计工具是否值得纳入日常工作流。已知：它读取 Claude Code / Codex 等 Agent 的会话，生成密钥外泄与命令来源报告；`stroq init` 安装 hooks 在危险命令执行前要求确认；`stroq inspect` 可在运行他人目录前检查；需要 Node.js 22+；Apache-2.0、无遥测；作者承认 hooks 是过滤器而非沙箱。

目标：帮我判断它对我的实际价值，并给出可执行的试用步骤。

要求：
1. 先说明它解决什么问题、不解决什么问题（明确它不是沙箱）。
2. 结合我的环境（Windows + Trae Work + Java/Spring），指出哪些功能可用、哪些依赖 Claude Code/Codex 集成而存疑；对官方未公开说明的部分直接标注「暂无公开资料」，不要推测。
3. 给出一份分阶段试用清单：先只读审计（不装 hooks），再评估是否安装 hooks；每步写清命令与预期输出、以及如何回滚（uninstall）。
4. 列出 3 个我应当重点验证的风险点（例如密钥名是否被误报、hooks 是否影响正常构建命令、inspect 对 .git/hooks 的识别效果）。
5. 最后给一句结论：对我这种场景，建议用、观望还是不用，并说明理由。
```

---

> 本文由 AI 综合Show HN 原帖与社区讨论撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。

<!-- asset:blog-1 start -->
![Trae Work 用户使用建议](/img/ai-news/hn-stroq-a-local-audit-of-what-your-coding-agen-380704/blog-1.png)

*图：Trae Work 用户使用建议*
<!-- asset:blog-1 end -->
