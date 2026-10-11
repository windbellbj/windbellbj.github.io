---
layout: post
title: "ARTEX AI自主渗透测试系统上手指南"
subtitle: "Go+Next.js双图架构的LLM多agent渗透系统，本地隔离环境学习与验证"
date: 2026-10-11 22:08:59 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
---

- 仓库：https://github.com/mhtsec/ARTEX
- Stars：3076
- 语言：Go
- 创建时间：2026-10-08
- 官方简介：AI 自主渗透测试系统 | 百度“agent+”攻防挑战赛冠军项目

---

## 解决什么问题

ARTEX 是一套 **LLM 多 agent 驱动的自主渗透系统**，官方简介为「AI 自主渗透测试系统」，是百度「agent+」攻防挑战赛冠军项目。它要解决的问题是：把渗透测试中「目标是什么」和「测到了什么程度」这两件事拆开管理，并让多个 agent 在事件驱动的闭环里自主推进攻击链路。

README 给出的核心机制包括：

- **双图架构**：资产图（全局共享的资产真值库）与探索图（每任务独立的推进链），两图通过锚点相连，支撑资产测试覆盖度与资产覆盖图。
- **worker 间过程级信息交换**：后续 worker 可以检索其他 work 的执行过程，复用尚未写成正式 fact 的观察。
- **planner 多轮共享 todolist**：让有前后依赖的多步攻击链在「事件驱动 + 无状态会话」下稳定推进、不重复、不错序。
- **人在环路**：提供 mainagent 对话、拦截审批、审批记录详情等能力。
- **资产同步**：支持从 ScopeSentry 直接同步资产数据，免去重复收集。

需要特别注意的是，README 明确声明 **ARTEX 仅供个人学习、代码研究与本地技术验证使用，不得用于对任何线上系统或网站发起实际测试**。

## 核心概念

- **资产图（Asset Graph，全局共享）**：跨任务同一份的资产真值库。节点为 `root_domain / subdomain / ip / service / app / endpoint`，归属公司；域名→子域→服务→端点的父子关系与去重 key 全部由程序计算，agent 只提交原始信息。
- **探索图（Exploration Graph，每任务独立）**：一次任务的「思考与推进」过程。节点为 `goal（目标）/ intent（意图）/ fact（事实）/ finding（漏洞）/ hint（提示）`，靠 `spawns / derived_from / yields / proves` 等边连成血缘链。
- **锚点**：`exploration_anchors(node_id, asset_id)` 把意图/事实/漏洞锚定到具体资产上，从而既能从探索方向看它打的是哪些资产，也能从某个资产反查它被哪些意图测过。
- **planner（规划者）**：唯一意图生成者。读探索图态势、判目标，只在有未覆盖的新方向时派意图进 frontier。
- **worker（执行者 ×N）**：领一条意图，用真实工具执行，把新资产/事实/漏洞写回两图后即停。每个任务的 work agent 数在「系统设置」里配置，默认 3。
- **goals**：目标分解 + 提取范围。
- **mainagent**：人在环路对话。
- **frontier 意图队列**：planner 派意图、worker 用 `claimNext` 领意图的队列。
- **norma SDK**：agent 能力由 `norma` SDK 提供（`agentcore` / `tool` / `permission` / `harness` / `memory` / `transcript`）。
- **记录型 MITM 代理**：流量记录代理，MITM + CA 留痕，worker 的 Bash / HTTP 全程留痕。
- **guard / intercept**：工具审批门。
- **enrich**：DNS / HTTP 异步补全。
- **MCP · skills · memory · report**：扩展与支撑子系统。
- **漏洞复测（retester）**：新版后端首次启动会预置可编辑的「漏洞复测」Agent，结论分为「仍可复现」「已修复」「无法确认」。

## 前置依赖

README 明确提到的依赖：

- **PostgreSQL**：必需依赖数据库。
- **LLM**：探索需配置 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`，也可在 UI 里配。
- **Docker**：方式一安装脚本会检测 / 自动安装 Docker；方式二使用 Docker Compose。
- **Go**：方式四从源码编译单二进制需要 Go 工具链（README 未提供具体 Go 版本号）。
- **Node.js / npm**：前端静态导出需要 `npm ci && npm run build:static`（README 未提供具体 Node 版本号）。
- **镜像内已含工具**：ripgrep/curl/vim/npm/nmap 等。
- **可选环境变量**：`ARTEX_LLM_PROVIDER` / `ARTEX_LLM_MODEL` / `ARTEX_LLM_BASE_URL` / `ARTEX_LLM_PROXY`；数据库可用 `ARTEX_PG_DSN` 覆盖。

README 未提供 Windows 原生安装的专门说明，但方式三提到 Windows 为 `start.bat`，方式五的 Release 目标包含 Windows amd64。

## 安装与配置

本工具不直接作用于 Jekyll 博客站点本身。ARTEX 是一个独立的 Go 后端 + Next.js 前端的渗透测试系统，与 Jekyll 3.9.5 静态博客、`scripts/` 自动化脚本、GitHub Actions 工作流没有直接集成点。下面给出在 Windows 10/11 本地开发机（已装 Python 3.12 与 Ruby）上试用的步骤。

### 步骤一：准备环境

README 推荐使用一键安装脚本，脚本会检测 / 自动安装 Docker。在 Windows 上建议先安装 Docker Desktop，并确认 `docker` 与 `docker compose` 可用。

### 步骤二：克隆仓库

```
git clone https://github.com/mhtsec/ARTEX.git
cd ARTEX
```

### 步骤三：选择安装方式

**方式一：一键安装脚本（推荐）**

```
./install.sh
```

脚本会让你选 ① 全部 Docker 或 ② 本地编译运行：

- ① 全部 Docker：填一个 Postgres 密码（可回车随机）→ 自动写 `.env` → `docker compose up -d`。
- ② 本地运行：选数据库（连已有 / 用 Docker 起一个）→ 生成 `config.json` → `go` 编译内嵌单二进制 → 启动。

**方式二：Docker Compose（手动）**

```
git clone https://github.com/mhtsec/ARTEX.git
cd ARTEX
cp .env.example .env
docker compose up -d
```

`.env` 中填 `POSTGRES_PASSWORD`、可选 `ANTHROPIC_API_KEY`。

README 说明：原镜像源 `autumn27/artex` 已从 Docker Hub 删除，镜像现由本仓库自维护为 `mianhuatang11/artex`。镜像源不可用（或想自行改代码）时，本地从纯源码构建：`docker compose build && docker compose up -d`。Dockerfile 为多阶段构建（前端静态导出 → Go 静态编译 → 运行镜像），默认走国内友好依赖源，可加 `--build-arg GOPROXY=... / --build-arg NPM_REGISTRY=...` 覆盖。

**方式三：下载预编译二进制（Releases）**

到原仓库 Releases 下载对应平台的 zip（本备份仓库不托管二进制）。解压后得到 `artex` + `start.sh`（Windows 为 `start.bat`）+ `skills/` + `config.example.json`：

```
cp config.example.json config.json
./start.sh
```

README 强调：请用 `start.sh` / `start.bat` 启动，而不是直接跑 `./artex`。它是个守护脚本，页面上的「一键更新」靠它完成换装。后台常驻：`nohup ./start.sh >artex.log 2>&1 &`。

**方式四：从源码编译单二进制**

```
cd web && npm ci && npm run build:static && cd ..
cp -r web/out server/webui/dist
CGO_ENABLED=0 go build -tags embedui -o artex ./cmd/artex
./start.sh
```

**方式五：构建跨平台 Release 压缩包**

```
./build.sh --release
```

产物为 `dist/artex-0.3.3-*.zip`。默认生成 Linux amd64/arm64、macOS amd64/arm64 和 Windows amd64 的 zip 包。可用 `ARTEX_TARGETS` 自定义目标。

### 步骤四：访问与初始化

装好后打开 **http://localhost:8787**，首次进入 `/setup` 设置管理员密码。

### 步骤五：配置数据库与 LLM

数据库配置在 `config.json`（或用环境变量 `ARTEX_PG_DSN` 覆盖）：

```
{
  "database": {
    "host": "127.0.0.1", "port": 5432,
    "user": "artex", "password": "yourpass",
    "dbname": "artex", "sslmode": "disable"
  }
}
```

LLM 配置：`export ANTHROPIC_API_KEY=sk-...`（或 `OPENAI_API_KEY`），也可在 UI 的「LLM 配置」页填写。

### 步骤六：常用参数

`./start.sh -addr :8787 -proxy :8788`，其中 `-addr` 为前端+API，`-proxy` 为流量录制代理。启动脚本会把参数原样透传给 `artex`。

### 反向代理部署（可选）

前端和 API/SSE 都由同一个后端端口（默认 `:8787`）提供，实时活动流默认走同源地址，因此无需配置 `NEXT_PUBLIC_SSE_BASE`。SSE 是长连接 + 持续推送，反代必须关闭缓冲，否则浏览器能连上却收不到事件。README 提供了 Nginx 示例，关键项为 `proxy_buffering off`、`proxy_cache off`、`proxy_read_timeout 3600s`、`proxy_http_version 1.1`、`proxy_set_header Connection ""`。

## 最小可用示例

把下面这段指令整段复制给任意 AI 编程助手，让它在你的本地环境里协助完成 ARTEX 的隔离试用准备：

```text
背景：我在 Windows 10/11 本地开发机上，已安装 Python 3.12 与 Ruby。我日常维护一个 Jekyll 3.9.5 静态博客（GitHub Pages 部署，仓库 windbellbj/windbellbj.github.io），含 Python 标准库编写的 scripts/ 自动化脚本与 GitHub Actions 工作流。现在我想在完全隔离的本地环境中学习并验证开源项目 ARTEX（https://github.com/mhtsec/ARTEX，AI 自主渗透测试系统，Go 后端 + Next.js 前端，依赖 PostgreSQL 与 LLM）。

目标：帮我在本地把 ARTEX 跑起来并完成首次初始化，全程只在本机隔离环境内操作，不对任何线上系统或网站发起实际测试。

要求：
1. 先确认我的机器上 Docker 与 docker compose 是否可用；若不可用，告诉我需要先安装什么。
2. 指导我克隆 https://github.com/mhtsec/ARTEX.git 到本地独立目录，不要放在我的 Jekyll 博客仓库里。
3. 优先走 README 的「方式一：一键安装脚本」，说明 install.sh 会让我在「① 全部 Docker」和「② 本地编译运行」之间选择，并解释两种选择的差别。
4. 如果一键脚本在我的环境里不可用，改用「方式二：Docker Compose（手动）」，提醒我 cp .env.example .env 并填写 POSTGRES_PASSWORD，以及可选的 ANTHROPIC_API_KEY。
5. 提醒我镜像源为 mianhuatang11/artex；若拉取失败，改用 docker compose build && docker compose up -d 从纯源码本地构建。
6. 启动后告诉我访问 http://localhost:8787，首次进入 /setup 设置管理员密码。
7. 提醒我配置 LLM：export ANTHROPIC_API_KEY=sk-...（或 OPENAI_API_KEY），也可在 UI 的「LLM 配置」页填写。
8. 提醒我 README 的免责声明：ARTEX 仅供个人学习、代码研究与本地技术验证使用，不得用于对任何线上系统或网站发起实际测试。
9. 每一步都给出我可以在 Windows 终端里直接执行的命令，并说明预期输出。
```

## 验证方法

README 提供的可执行验证步骤：

1. **访问首页**：装好后打开 http://localhost:8787，首次进入 `/setup` 设置管理员密码。能打开并完成初始化即说明服务已启动。
2. **在线 Demo 对照**：README 提供在线 Demo https://artex-demo.mhtsec.com（纯前端 + Mock 数据，无需后端），可用于对照界面与交互。
3. **本地开发与测试**：
   - `./dev.sh` 启动后端(:8787) + 流量代理(:8788) + 前端 next dev(:5173)，访问 http://localhost:5173。
   - 后端单独运行：`go run ./cmd/artex`（不带 `-tags embedui` 则不内嵌前端）。
   - 前端单独运行：`cd web && npm run dev`（`/api` 反代到后端，带热更新）。
   - 测试：`go test ./...`。
   - Mock 预览（无后端）：`cd web && NEXT_PUBLIC_MOCK=1 npm run dev`。
4. **漏洞复测验证**：任务详情的「复测」页签可分页选择本任务的漏洞、查看历次结论和证据，并手动发起复测。启动后保留当前页签，显示转圈图标和「复测中」；确认修复后同步更新漏洞状态。
5. **更新链路验证**：在「系统配置」页（侧边栏「系统配置」→ `/system/settings`）的「版本与更新」卡片里检查并安装新版本。README 说明更新会下载当前平台发布包 → 比对 Release 的 `SHA256SUMS` → 用 `-h` 冒烟测试新二进制 → 暂存为 `artex.new` → 程序退出，由 `start.sh` / `start.bat` 重新拉起并完成换装。

## 风险与注意事项

- **使用限制（README 明确声明）**：ARTEX 仅供个人学习、代码研究与本地技术验证使用，不得用于对任何线上系统或网站发起实际测试。
- **禁止事项（README 明确列出）**：严禁使用本工具对任何网站、线上服务或联网系统发起扫描、探测、利用或攻击（无论是否获得授权、是否为自有资产）；严禁用于任何实际的渗透测试、攻防对抗或生产环境；严禁用于非法入侵、数据窃取、勒索、拒绝服务或任何破坏性、犯罪性活动；严禁从事违反所在国家/地区法律法规的行为。
- **合规责任**：使用者须自行遵守所在国家/地区关于网络安全、数据保护与计算机犯罪的全部法律法规（在中国大陆包括但不限于《网络安全法》《数据安全法》《个人信息保护法》及相关司法解释）。因使用本工具产生的一切法律责任与后果，均由使用者自行承担。
- **免责声明**：本项目按「现状（AS IS）」提供，不附带任何明示或默示的担保。作者及贡献者不对使用本工具所导致的任何直接或间接损失、数据丢失、系统损坏或法律纠纷承担责任。下载、安装或使用本项目，即表示已阅读、理解并同意上述全部条款。
- **开源协议**：AGPL-3.0。衍生作品必须同样以 AGPL-3.0 开源；若修改本项目并通过网络向用户提供，也必须向这些用户公开对应的完整源码。
- **镜像源风险**：原 Docker 镜像源 `autumn27/artex` 已失效，现由本仓库自维护镜像 `mianhuatang11/artex`。拉取失败时可 `docker compose build` 从纯源码本地构建。
- **更新会中断正在运行的任务**：更新即重启，请在空闲时进行。
- **Docker 下更新只换程序、不换镜像**：镜像里的 playwright / nmap 等工具链不会跟着升级，且 `docker compose up -d` 重建容器后会退回镜像自带的版本。
- **回滚限制**：上一版本保留为 `artex.old`，可回滚，但数据库结构不会回退。
- **开发构建不给更新**：版本号是 `dev` 或 `git describe` 带后缀时禁用。
- **UPX 兼容性**：UPX 自解压二进制可能与部分 Linux 内核、虚拟化环境或安全策略不兼容，因此默认不启用。
- **SSE 反代**：反代必须关闭缓冲，否则浏览器能连上却收不到事件（表现为活动流一直转圈）。
- **复测记录范围**：本版历史记录通过漏洞详情和会话查看，暂未纳入漏洞报告导出或任务归档包，也未自动关联流量包。演示模式只生成明确标注的模拟记录，不请求真实目标。
- **备份建议**：升级前仍建议先备份 `./data` 与数据库。

## 替代方案

README 中提到的相关项目：

- **ScopeSentry**（https://github.com/Autumn-27/ScopeSentry）：ARTEX 支持从 ScopeSentry 直接同步资产数据，免去重复收集。
- **norma**（https://github.com/Autumn-27/norma）：ARTEX 的 agent 能力由该 SDK 提供。
- **AegisHook**（https://github.com/RuoJi6/AegisHook）：ARTEX 的审批记录详情展示结构参考了 AegisHook 的审批详情组件。
- **Cairn**（https://github.com/oritera/Cairn）：README 参考列表中列出。

README 未提供其他同类替代方案的对比说明。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
