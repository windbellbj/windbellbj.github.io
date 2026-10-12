---
layout: post
title: "Pi 使用说明书：极简可扩展的编码 Agent Harness"
subtitle: "一个能改、能拆、能自动化的终端编码智能体，Java 后端也能用，但接入 Trae Work 需绕路"
date: 2026-10-12 04:44:19 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - Agent Harness
news_category: harness
---

- 来源：GitHub 近期爆火
- 仓库：https://github.com/earendil-works/pi
- Stars：114320
- 语言：TypeScript
- 创建时间：2025-08-09
- 最近更新：2026-10-12
- 官方简介：AI agent toolkit: unified LLM API, agent loop, TUI, coding agent CLI

---

> Pi 是一个极简、可扩展的 Agent Harness（智能体运行壳）：它把统一的多模型 LLM API、Agent 循环、终端 UI 和编码 Agent CLI 打包成一套可被你自己改造的工具，最适合愿意动手定制工作流、喜欢在终端里驱动 AI 写代码的开发者。

## 它到底是什么

Pi 的官方定位是「minimal, extensible agent harness that you can make your own」——一个你可以据为己有的极简可扩展智能体运行壳。它的口号是「Adapt Pi to your workflows, not the other way around」，也就是让工具迁就你的流程，而不是反过来。

它由一组 npm 包组成，核心是命令行编码 Agent，同时对外暴露可复用的库：

| 包名 | 作用 |
|------|------|
| `@earendil-works/pi-coding-agent` | 交互式编码 Agent CLI，日常直接用的就是它 |
| `@earendil-works/pi-ai` | 统一的多厂商 LLM API（OpenAI、Anthropic、Google 等） |
| `@earendil-works/pi-agent-core` | 带工具调用与状态管理的 Agent 运行时 |
| `@earendil-works/pi-tui` | 带差分渲染的终端 UI 库 |
| `@earendil-works/pi-durable` | 持久化会话、任务与文档运行时（实验性） |
| `@earendil-works/chord` | 面向服务、复制状态、RPC 与插件的应用组合运行时 |
| `@earendil-works/pi-telemetry` | 厂商中立的遥测契约与参考适配器 |

官方明确说明：Pi 自带强大的默认能力，但**刻意不做 sub-agents（子智能体）和 plan mode（计划模式）**。想要这些功能，要么让 Pi 自己给你写，要么装一个按你想法实现的包。

<!-- asset:blog-1 start -->
![Pi 的 npm 包组成](/img/ai-news/earendil-works-pi/blog-1.png)

*图：Pi 的 npm 包组成*
<!-- asset:blog-1 end -->


## 适用场景与它解决的问题

Pi 面向的是「一个开发者在终端里驱动一个编码 Agent」这种工作方式。官方对它的定位说得很直白：Pi 编码 Agent 是为在你的（远程）机器上、终端里、由一个人驱动而设计的；如果进程挂了，你看一眼发生了什么，然后让它继续。

它适合这些情况：

- 你想在项目目录里直接起一个能读写代码、调用工具的终端 Agent，而不是被锁在某个 IDE 里。
- 你想用扩展、技能、提示词模板、主题去改造 Agent 的行为，甚至打包成 Pi package 通过 npm 或 git 分享。
- 你想把 Agent 能力嵌进自己的程序：可以用打印模式或 JSON 模式自动化，可以通过 RPC 控制，也可以用 TypeScript SDK 构建应用。
- 你想统一管理多家模型供应商的调用，而不是为每家写一套适配。

它不太适合这些情况：

- 你想要开箱即用的图形界面、内置权限沙箱、子智能体编排和计划模式——这些要么没有，要么需要你自己补。
- 你希望零配置就能安全地让 Agent 在敏感机器上自由行动——官方明确说没有内置权限系统。

## 核心概念：Harness、会话、Agent、工具、任务

官方在介绍 Pi Durable 时给出了对 harness 的完整定义，这套概念同样适用于理解 Pi 本身：

- **Harness（运行壳）**：存储，加上并行运行一个或多个大模型会话所需的机械结构。它提供模型可调用的工具，以及工具运行所在的执行环境。
- **Conversation（会话）**：你与 Agent 之间的一次交互，以 transcript（记录）形式保存。
- **Agent**：大模型加上它的设置（比如思考等级）以及它能调用的工具。
- **Execution environment（执行环境）**：工具干活的地方，可以是你的笔记本、一台远程 VM，或一个内存沙箱。哪个会话拿到哪些工具、哪个执行环境，由每个会话自己决定。
- **Task（任务）**：harness 运行的每一件事，从调用模型到执行工具，都是一个任务。

存储方面，Pi Durable 提供 memory、SQLite 和 JSONL 三种后端，并附带一致性测试套件与基准，方便你实现自己的后端。SQLite 与 JSONL 存储代码不使用 Node API，因此加一个小适配器就能跑在 Bun 上或 Cloudflare Durable Object 里。同一时刻只有一个进程拥有某个存储，其他客户端附着到该进程上。

## 环境与前置依赖

- **Node.js 22.19 或更新版本**。官方安装脚本在 macOS、Linux、Windows 上都能按需帮你装 Node。
- 操作系统：官方提供 macOS、Linux、Windows 安装器；Nix 方式支持 Linux 与 macOS 的 ARM64 和 x86-64。
- 正常 npm 安装**不需要依赖的生命周期脚本**。
- 如果你走 Nix 路线，Nix 构建是离线的，内置模型数据来自 `nix/model-catalog.json` 中固定的 pi.dev 模型目录修订版；运行时 Pi 仍会像往常一样用 pi.dev 上更新的目录数据覆盖。

## 安装：Windows 上的可照做步骤

### 方式一：官方安装脚本（推荐，依赖被固定）

1. 打开 PowerShell。
2. 执行 `powershell -c "irm https://pi.dev/install.ps1 | iex"`。
3. 该安装器会固定所有依赖，后续用 `pi update` 更新 Pi。

### 方式二：npm 全局安装（不固定传递依赖）

1. 确认 Node 版本不低于 22.19，可用 `node -v` 查看。
2. 执行 `npm install -g --ignore-scripts @earendil-works/pi-coding-agent`。
3. 官方提示：这种方式**不会固定传递依赖**，与安装脚本的差别就在这里。

### 方式三：Nix

在支持 Nix 的环境里可以 `nix run github:earendil-works/pi/stable` 直接运行，`stable` 指向最新发布；用 `nix profile add github:earendil-works/pi/stable` 安装，用 `nix profile upgrade pi` 更新。想钉住版本就用发布标签，例如 `github:earendil-works/pi/v1.0.0`；用 `github:earendil-works/pi` 则拿到 `main` 上未发布的改动。Nix 会从源码构建 Pi。

### 从旧包名升级

如果你之前装的是旧 scope 的包，官方给出的迁移方式是执行 `pi update`。注意：如果你还没到 0.73.1，第一次只会更新到 0.73.1（旧名字下的最后一个版本，也是唯一具备升级到新版本能力的版本），所以**可能需要跑两次更新**。旧包 `@mariozechner/*` 已被标记弃用并指向新的 `@earendil-works/*` 名字，但并未下架，因此旧安装和被钉住的依赖仍可复现。包名对应关系如下：

| 旧包 | 新包 |
|------|------|
| `@mariozechner/pi-coding-agent` | `@earendil-works/pi-coding-agent` |
| `@mariozechner/pi-agent-core` | `@earendil-works/pi-agent-core` |
| `@mariozechner/pi-ai` | `@earendil-works/pi-ai` |
| `@mariozechner/pi-tui` | `@earendil-works/pi-tui` |
| `@mariozechner/pi-web-ui` | `@earendil-works/pi-web-ui` |

<!-- asset:code-1 start -->
```powershell
powershell -c "irm https://pi.dev/install.ps1 | iex"
node -v
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
nix run github:earendil-works/pi/stable
nix profile add github:earendil-works/pi/stable
nix profile upgrade pi
pi update
```
<!-- asset:code-1 end -->


## 快速上手

1. 在 PowerShell 里进入你想让 Pi 工作的项目目录，例如 `cd D:\work\my-spring-app`。
2. 输入 `pi` 启动。
3. 在 Pi 内部运行 `/login`，连接一个订阅或 API key，从而接入内置的 AI 供应商。
4. 直接给 Pi 一个任务。

除了交互模式，官方还支持几种用法：打印模式或 JSON 模式用于自动化，RPC 用于外部控制，TypeScript SDK 用于构建应用。官方还举了一个真实集成案例：OpenClaw。

## 如何确认安装成功

- 在 PowerShell 里执行 `pi`，能进入交互界面即说明 CLI 可用。
- 进入后执行 `/login`，能完成供应商连接，说明模型侧配置通了。
- 想验证更新通道，执行 `pi update`，观察是否能正常拉取新版本。
- 从源码跑的话，官方提供了 `./pi-test.sh`，可以在任意目录下从源码启动 pi。

## 融入 Trae Work 与 Java / Spring 工作流

先说结论：**官方未提供与 Trae Work / Java 的集成方式**。官方公开的接入路径只有四条——交互式使用、打印或 JSON 模式自动化、RPC 控制、TypeScript SDK 构建应用。没有 MCP 服务形态，没有 Skill 目录约定，也没有 Java SDK 或 HTTP 服务端的官方说明。

因此在 Windows + Trae Work + Java/Spring 的日常里，现实可行的做法是**并行使用**，而不是把 Pi 塞进 Trae Work：

1. 在 Trae Work 里正常写你的 Spring 代码。
2. 需要 Pi 介入时，单独开一个 PowerShell 窗口，`cd` 到同一个项目根目录，运行 `pi`。
3. 让 Pi 在这个目录里做重构、补测试、读日志、批量改配置等任务。
4. 两边共享同一份工作区文件，靠 Git 做同步与回退。

如果你确实想让 Java 程序调用 Agent 能力，官方给出的唯一程序化路径是 **TypeScript SDK**，这意味着你需要一个 Node 侧的中间层，而不是在 Spring 里直接引依赖。官方未公开说明存在 Java 客户端。

> 注意：不要自行猜测 Pi 的 MCP 配置路径或 Skill 目录结构。官方公开材料中没有这些内容，写错配置只会浪费时间。

## 权限、隔离与安全

这是使用 Pi 前必须知道的一条硬信息：**Pi 不包含用于限制文件系统、进程、网络或凭据访问的内置权限系统**。默认情况下，它以启动它的用户和进程的权限运行。

如果你需要更强的边界，官方建议把 Pi 容器化或沙箱化，并给出三种模式：

- **Gondolin 扩展**：把 `pi` 和供应商认证留在宿主机上，同时把内置工具和 `!` 命令路由进一个本地 Linux 微型 VM。
- **纯 Docker**：把整个 `pi` 进程跑在本地容器里，做简单隔离。
- **OpenShell**：把整个 `pi` 进程跑在策略控制的沙箱里。

## 供应链加固

官方把 npm 依赖变更当作需要审查的代码变更来对待，具体做法包括：

- 直接外部依赖钉死到精确版本，内部 workspace 包保持版本范围。
- `.npmrc` 设置 `save-exact=true` 和 `min-release-age=2`，避免 npm 解析时用到当天发布的依赖。
- `package-lock.json` 是依赖的唯一事实来源；除非设置 `PI_ALLOW_LOCKFILE_CHANGE=1`，提交钩子会阻止误提交 lockfile。
- `npm run check` 会校验直接依赖是否钉死、原生 TypeScript 导入兼容性，以及生成的 coding-agent 安装锁。
- pi.dev 安装器从 `packages/coding-agent/install-lock/` 安装，该目录由根 lockfile 生成，用来钉住传递依赖；npm 包则不钉传递依赖。
- 本地发布冒烟测试与 npm 发布使用同一个 tarball 打包器，npm 发布的是已验证的 tarball，而不是重新打包 workspace 目录。
- 本地发布安装、文档中的 npm 安装、`pi update --self` 在支持的地方都使用 `--ignore-scripts`。
- CI 用 `npm ci --ignore-scripts` 安装，并有定时 GitHub 工作流运行 `npm audit --omit=dev` 与 `npm audit signatures --omit=dev`。
- 安装锁生成对依赖生命周期脚本有显式白名单，新的生命周期脚本依赖会先让检查失败，直到被审查通过。

## 局限与风险

- **没有内置权限系统**：这是官方白纸黑字写的，默认继承启动用户与进程的全部权限。在 Windows 上直接对生产仓库或含密钥的目录运行，风险由你承担。
- **刻意缺少 sub-agents 与 plan mode**：官方说这是设计取舍，不是缺陷。想要就得自己写或装包。
- **成熟度**：Pi 1.0 于 2026 年 10 月 1 日发布，官方称经过大量加固与维护，认为它已是可靠的基础。但同一时间发布的 Pi Durable 被官方明确定义为**实验性**新包。
- **版本号命名的争议**：Hacker News 上有评论表示「很高兴看到 Pi 发展得这么好，它毫无疑问是我最喜欢的 harness，但我不太清楚为什么是 1.0.0 而不是 0.100.0」。
- **配置目录位置的争议**：Hacker News 上有一条讨论《Pi coding agent: config folder is out of place on Linux》获得 56 分、21 条评论。有评论称这个问题困扰了他一段时间，也是他去尝试其他编码 Agent 的原因之一；他认为虽然配置目录最终不影响性能，但官方处理这件事的方式让他有些沮丧，而且官方已经非常明确表示不会改。也有评论给出另一种态度：大模型让 fork 和打补丁变得极其简单，遇到合并冲突也很好修，直接改成你想要的样子就行。
- **许可证**：MIT。
- **费用**：Pi 本身是 MIT 开源，但你需要自备模型供应商的订阅或 API key，这部分费用取决于你选的供应商，官方未公开说明 Pi 自身的收费模式。

<!-- asset:blog-2 start -->
![使用 Pi 前需知的风险](/img/ai-news/earendil-works-pi/blog-2.png)

*图：使用 Pi 前需知的风险*
<!-- asset:blog-2 end -->


## 社区评价（来自 Hacker News 讨论）

- 正面：有评论称「它毫无疑问是我最喜欢的 harness」。
- 中性/质疑：同一条讨论里有人质疑 1.0.0 的版本号选择。
- 负面：在配置目录的讨论中，有用户表示因此转向其他编码 Agent，并提到自己找到了 maki，还想再看看 crush。
- 实用主义：有评论认为与其纠结，不如直接 fork 改掉自己不喜欢的地方。

## 开发与本地构建（可选）

如果你要改 Pi 本身，官方给出的开发命令是：`npm install --ignore-scripts` 安装全部依赖且不跑生命周期脚本；`npm run build` 刷新模型数据后构建所有包；`npm run build:offline` 用现有模型数据离线重建；`npm run check` 做 lint、格式化和类型检查；`./test.sh` 跑测试（没有 API key 时会跳过依赖 LLM 的测试）；`./pi-test.sh` 从源码运行 pi，可在任意目录执行。

想在 monorepo 之外使用本地包，可以 `npm run pack:packages -- --out .artifacts/pi-packages` 把所有公开包构建成一套连贯的本地产物；模型数据已就绪时加 `--offline-model-data` 避免联网。随后用 `node scripts/use-local-packages.mjs` 配合 `--manifest`、`--consumer`、`--package` 参数把外部项目指向这套产物，每个直接依赖重复一次 `--package`。该命令会把消费方的 `package.json` 更新为内容寻址的本地 `file:` 引用，并把传递覆盖写到 npm 的 `package.json` 或 pnpm 的 `pnpm-workspace.yaml`。安装或更新消费方期间要保持产物目录可用，改动 Pi 源码后两条命令都要重跑。

从发布源码构建独立二进制：GitHub release 附带一个带版本号的源码归档，由该 release 的 `SHA256SUMS` 覆盖。解压后运行与官方独立二进制相同的构建脚本 `./scripts/build-binaries.sh --offline-model-data --platform linux-x64 --out "$PWD/out"`。归档内含发布模型数据与原生预构建产物，`--offline-model-data` 表示用这些数据而不刷新供应商目录；脚本会安装依赖并连同运行时资源一起构建可执行文件，依赖已备好时可传 `--skip-install`。

<!-- asset:code-2 start -->
```powershell
npm install --ignore-scripts
npm run build
npm run build:offline
npm run check
./test.sh
./pi-test.sh
npm run pack:packages -- --out .artifacts/pi-packages
node scripts/use-local-packages.mjs
```
<!-- asset:code-2 end -->


## 分享你的开源编码会话

官方鼓励把用 Pi 或其他编码 Agent 做的开源工作会话分享出来，理由是公开的 OSS 会话数据能用真实任务、工具使用、失败与修复来改进编码 Agent，而不是靠玩具基准。发布会话使用 `badlogic/pi-share-hf`，需要一个 Hugging Face 账号、Hugging Face CLI 和 `pi-share-hf`。

```text
背景：我在 Windows 上用 Trae Work 开发一个 Java / Spring 后端项目，想试用 Pi 这个终端编码 Agent，但不想让它乱动我的仓库。

目标：请帮我在当前 Spring 项目里安全地完成一次小范围试用，并给出可回退的操作。

具体要求：
1. 先告诉我这个项目里哪些目录和文件属于高风险（含密钥、含生产配置、含数据库迁移脚本），并列出建议排除的清单。
2. 给我一份在 Windows PowerShell 下从零安装 Pi 的步骤，包含 Node 版本检查、安装命令、以及验证安装成功的命令。
3. 给我一份在项目根目录启动 Pi 并完成 /login 的操作顺序。
4. 设计一个最小试用任务：只在一个新建的独立包或独立目录里，让 Pi 帮我生成一个 Spring Boot 的 REST Controller 和对应的单元测试，不修改任何已有文件。
5. 告诉我如何用 Git 检查 Pi 到底改了哪些文件，以及如何一键回退到试用前的状态。
6. 说明 Pi 没有内置权限系统这件事对我在公司机器上使用的实际影响，并给出至少两种隔离方案。
7. 如果我想让 Java 程序调用 Agent 能力，说明官方目前只提供 TypeScript SDK 这一事实，并给出一个 Node 中间层的最小思路，不要编造 Java 依赖或 MCP 配置。
```

---

> 本文由 AI 综合官方仓库、项目官网与第三方公开资料撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
