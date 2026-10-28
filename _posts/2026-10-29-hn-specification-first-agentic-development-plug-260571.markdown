---
layout: post
title: "Spec-First：用规格驱动 AI 编码的 Claude Code 插件"
subtitle: "四步命令生成可验证 PR，适合想用规格约束 AI 行为的 Java 开发者参考"
date: 2026-10-29 05:29:09 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - AI IDE插件
news_category: ide-plugin
---

- 来源：Hacker News Show HN
- 项目链接：https://spec-first.dev/
- HN 讨论：https://news.ycombinator.com/item?id=50260571（34 points）

---

> 一个 Claude Code 插件，用「先写规格、再写代码」的流程约束 AI 编码，适合想减少 AI 随意发挥、追求可验证产出的开发者。

## 它是什么

**Spec-First** 是一个面向 Claude Code 的插件（也声称兼容 Codex、Cursor、Copilot），核心思路是：**先让 AI 写出一份可执行的规格（spec），再按规格生成代码**。作者用这套方法在 2026 年初至今生成了超过 1000 份规格、约 50 万行代码，并开源了配套的 Agent Smith 项目。

它把开发流程拆成四个命令：

| 命令 | 作用 |
| --- | --- |
| `/create-spec` | 根据你的描述和仓库现状，生成一份包含目标、事实（带文件与行号）、步骤和完成标准的规格，放在独立分支和 worktree 中 |
| `/review-spec` | 用脚本校验规格中引用的文件和行号是否存在，再由一个无聊天历史的新 Agent 对照代码审查规格，删减不必要的内容 |
| `/apply-spec` | 按规格步骤写代码和测试，并把非显而易见的决策记录到 `decisions/` 目录 |
| `/deliver-spec` | 通过构建和测试门禁后提交、推送并创建 PR，规格随 PR 一起提交 |

<!-- asset:blog-1 start -->
![Spec-First 四步流程](/img/ai-news/hn-specification-first-agentic-development-plug-260571/blog-1.png)

*图：Spec-First 四步流程*
<!-- asset:blog-1 end -->


## 解决什么问题

AI 编码常见的问题是「跑偏」：生成大量看似合理但不符合预期的代码，或者反复修改导致需求矛盾。Spec-First 试图用**规格作为红线**来约束 AI 的行为：

- **规格先行**：在写代码前先明确目标、事实依据和完成标准，减少 AI 的自由发挥空间。
- **双重校验**：脚本检查引用是否真实存在，新 Agent 从零审查规格，避免「自己审自己」。
- **门禁把关**：只有构建和测试通过才能提交，PR 中附带规格，方便追溯。
- **并行安全**：每个规格独立分支和 worktree，ID 基于时间生成，支持多个 Agent 并行工作。

<!-- asset:blog-2 start -->
![规格约束 AI 的四个要点](/img/ai-news/hn-specification-first-agentic-development-plug-260571/blog-2.png)

*图：规格约束 AI 的四个要点*
<!-- asset:blog-2 end -->


## 社区怎么看

Hacker News 上该帖获得 34 分，讨论集中在「规格驱动开发（SDD）是否真的有效」：

- **支持方**认为规格作为 Git 仓库的一部分，能让 Agent 理解历史决策，变更需求时也有据可查。
- **质疑方**指出规格容易过时，维护成本高，Agent 可能陷入审查旧上下文、浪费 token 的困境；有团队甚至开始移除规格文档，认为代码本身就是更好的真相来源。
- **折中观点**强调高层规划的重要性，但规格应聚焦「意图和决策」，而非重复代码已表达的内容。

作者回应称，规格由 Agent 创建和维护，并通过 `review-spec` 技能对照代码补充证据，只有目标与证据匹配才算通过。

## 对 Java / Spring 开发者的价值

**与 AI 辅助软件开发直接相关**，但需注意：

- 该项目目前以 **Claude Code 插件**形式提供，官方页面展示的示例是 TypeScript/Vite 项目。**是否支持 Java/Spring 生态、能否在 Trae Work 中直接使用，官方未公开说明**。
- 如果你在 Windows 上使用 Trae Work，可以借鉴其「规格先行 + 门禁校验」的思路，但插件本身可能需要 Claude Code 环境。
- 对于 Spring 项目，规格中引用的文件行号、构建命令（如 Maven/Gradle）需要自行适配，暂无公开资料说明是否开箱即用。

## 怎么开始试用

1. 访问项目页 https://spec-first.dev/ 了解完整流程。
2. 在 Claude Code 中执行：`/plugin marketplace add holgerleichsenring/specification-first-agentic-development`。
3. 安装后，在项目根目录用自然语言描述需求，依次运行 `/create-spec`、`/review-spec`、`/apply-spec`、`/deliver-spec`。
4. 查看 GitHub 仓库 https://github.com/holgerleichsenring/agent-smith 了解质量门禁的具体实现。

> 注意：官方页面未提供 Java/Spring 的专门示例，建议先在小型实验项目上验证流程，再考虑融入日常开发。

```text
背景：我是一名 Java 后端程序员，日常在 Windows 上使用 Trae Work（AI IDE）开发 Spring 项目。我看到了 Spec-First 这个 Claude Code 插件，它用「先写规格、再写代码」的流程约束 AI 编码。

目标：请帮我评估 Spec-First 的流程是否适合我的 Java/Spring 开发场景，并给出一个在 Trae Work 中借鉴其思路的轻量试用方案。

要求：
1. 用一段话总结 Spec-First 的核心流程（create-spec → review-spec → apply-spec → deliver-spec）及其优缺点。
2. 分析在 Java/Spring 项目中落地时可能遇到的适配问题（如构建命令、测试框架、文件引用方式）。
3. 设计一个最小试用步骤：选择一个简单的 Spring Boot 功能（如一个 REST 接口），模拟「规格先行」的流程，列出每一步的具体操作和预期产出。
4. 指出哪些环节可以借助 Trae Work 的现有能力（如代码生成、测试运行）完成，哪些需要额外工具。
5. 最后给出是否值得深入试用的建议，并说明理由。
```

---

> 本文由 AI 综合Show HN 原帖与社区讨论撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。

<!-- asset:code-1 start -->
```powershell
/plugin marketplace add holgerleichsenring/specification-first-agentic-development
```
<!-- asset:code-1 end -->
