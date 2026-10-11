---
layout: post
title: "Anatomy 技能：把技术概念画成等距机械图"
subtitle: "Claude Code 技能，用 SVG/WebGL/3D 生成可交互等距图解，零依赖 Node 构建"
date: 2026-10-11 22:08:59 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
---

- 仓库：https://github.com/wheresryan22/anatomy
- Stars：1483
- 语言：JavaScript
- 创建时间：2026-10-08
- 官方简介：A Claude Code skill that turns a technical idea into a detailed, interactive isometric figure of a real machine. It makes SVG with optional WebGL shaders and 3D, for docs, articles and landing pages.

---

## 解决什么问题

技术文章、文档和落地页常常需要一张能说明原理的图，但普通的方框加箭头很难把「机制」讲清楚。Anatomy 是一个 Claude Code 技能（Claude skill），它的做法是：让 Claude 先发明一个真实的物理对象，而这个对象的运转方式本身就是你要解释的概念。README 给出的例子是：一个「内容没变就跳过工作」的缓存键，被画成一把只有当所有弹子都对齐时才会转动的弹子锁；一个 GPU 上下文服务多个画布，被画成一台只有单个打印头的龙门绘图仪依次访问 16 个孔位。

随后 Claude 用几十个细小的、实心的、带明暗的零件把这个对象搭出来，放进一个带标题、提示和实时读数的卡片里，让它随鼠标和键盘平稳运动，并通过放大每一个接合处来自查。图里显示的每一个数字，都来自驱动零件运动的同一个小模型。

## 核心概念

- **Claude Code 技能（Agent Skill）**：一个根目录含 `SKILL.md` 的文件夹，本仓库就是这个文件夹。
- **三种图形**：SVG（核心，四色明暗的实心等距零件，从后往前绘制）；SVG + WebGL（用于线条画不出的火、尾焰、水、焦散、灯光、辉光、蒸汽，着色器运行在后 SVG 与前 SVG 之间的 canvas 上，使用图形自身的等距相机）；3D（beta，真正在三维中转动的零件，每帧按 kit 规则重新投影和重新着色）。
- **主题**：每张图分浅色或深色，浅色是技能优先设计的主题，着色器也一样。
- **kit**：绘制库，包含等距相机、实体与零件库（`iso-kit`）、任意轴上的回转体（`lathe.mjs`）、管道与线缆（`tube.mjs`）、WebGL 层（`gl.mjs`）、3D 运行时（`turn*.mjs`）以及 React 组件（`react/`）。除 React 组件外无依赖。
- **references**：Claude 按需打开的长文指南，包括 craft、kit API、motion、React、verification、WebGL、设计走查和 3D 模式。
- **验证**：`kit/audit.mjs` 证明几何正确（没有东西穿过别的东西、每个端点都落在支座上、每个重叠都按深度顺序绘制）；无头 Chrome 中 `scripts/capture.mjs` 与 `scripts/drive.mjs` 负责截图、特写和慢放接触表，`scripts/lines.mjs` 会让任何悬空结束的线失败，`scripts/turn-check.mjs` 检查 3D 图形。

## 前置依赖

README 的 Requirements 表列出：

- **Claude Code**：一切功能都需要，技能是为它写的。
- **Node.js 20.10+**：用于构建、kit 和检查。只用内置模块，无需 `npm install`。示例已在 Node 20.19 和 22.11 上逐字节重建。在 Node 20 上，浏览器脚本会用 `--experimental-websocket` 自行重启。
- **Chrome 或 Chromium**：用于检查。`capture.mjs`、`drive.mjs`、`lines.mjs` 和 `turn-check.mjs` 会在 macOS、Linux 和 Windows 的常见位置以及 Playwright 缓存中查找；其他二进制可设置 `CHROME_PATH`。它们以无头模式运行并开启 WebGL。
- **React 18+**：仅 React 输出需要，涉及 `kit/react/`、`examples/test-rig/` 和 `examples/spot-plate/`。

注意：README 未提及 Python 或 Ruby 依赖。

## 安装与配置

本工具不直接作用于 Jekyll 博客站点本身。它是一个 Claude Code 技能，产出的是独立的 HTML 页面、单独的 SVG 文件或 React/Next.js 组件，与 Jekyll 的构建流程没有直接集成点。

在 Windows 10/11 本地开发机上试用的步骤：

1. 确认已安装 Claude Code（README 要求）。
2. 确认 Node.js 版本不低于 20.10（README 说明构建与检查需要）。
3. 选择一种安装方式（README 的 Install 表）：
   - 用 skills CLI 装到用户级：`npx skills add wheresryan22/anatomy -g -a claude-code`，安装到 `~/.claude/skills/anatomy`。
   - 用 skills CLI 装到单个项目：`npx skills add wheresryan22/anatomy`，安装到 `.claude/skills/anatomy`。
   - 用 git 装到用户级：`git clone https://github.com/wheresryan22/anatomy.git ~/.claude/skills/anatomy`。
   - 用 git 装到单个项目：`git clone https://github.com/wheresryan22/anatomy.git .claude/skills/anatomy`。
   - 不用 git：下载 ZIP，解压后把文件夹从 `anatomy-main` 改名为 `anatomy`，移动到 `~/.claude/skills/`。
4. README 说明：skills CLI 会复制整个仓库（含示例，约 10 MB），其 1.7.1 版本要求 Node 22.20 或更高。
5. Claude Code 会在运行中的会话里发现新技能；如果会话启动时 `skills` 文件夹本身不存在，运行 `/reload-skills`。
6. 如需运行检查脚本，确保本机有 Chrome 或 Chromium，必要时设置 `CHROME_PATH`。

## 最小可用示例

在 Claude Code 中输入 `/anatomy` 并说明这张图要解释什么。README 给出的 Quick start 示例是：

```text
背景：我在用 Claude Code，已安装 Anatomy 技能（wheresryan22/anatomy）。
目标：请用 /anatomy 生成一张交互式等距图，解释令牌桶限流器（token bucket rate limiter）的工作原理。
要求：
1. 先收集真实数字（桶容量、令牌补充速率、请求速率等），再发明一个物理对象，让它的运转本身就是令牌桶机制。
2. 用 kit 构建几何：实心等距零件、四色明暗、从后往前绘制，放进带标题、提示和实时读数的卡片。
3. 让图形随鼠标和键盘平稳运动，并运行几何审计（node build.mjs --audit）确认没有零件互相穿透、每个端点都有支座。
4. 输出为独立 HTML 页面，浅色主题；如需火焰、水流等线条画不出的效果再用 WebGL。
5. 最后放大检查每个接合处，并读取你生成的每一张 PNG 截图。
```

README 还提到：你不必点名这个技能，当你要求等距插图、文档/博客/落地页的解释性图形或交互式讲解时，Claude 也会加载它。

## 验证方法

README 给出的可执行验证方式：

1. 构建示例并运行几何审计：`node examples/raptor-engine/build.mjs --audit`、`node examples/arcade-cabinet/build.mjs --audit`、`node examples/turning-dial/build.mjs --light --audit`。README 说明 3D 审计较慢，参见 `references/3d.md`。
2. 用无头 Chrome 脚本检查：`scripts/capture.mjs` 与 `scripts/drive.mjs` 生成截图、特写和慢放接触表；`scripts/lines.mjs` 会让任何悬空结束的线失败；`scripts/turn-check.mjs` 检查 3D 图形。这些脚本需要 Chrome 或 Chromium，可设置 `CHROME_PATH`。
3. 直接打开已提交的构建页面：README 说明 `examples/` 中的构建页面已提交，打开任意 `.html` 即可试用。
4. 技能本身要求 Claude 读取它生成的每一张 PNG。

## 风险与注意事项

- **不是图表库**：没有坐标轴、系列或数据绘图。数字只以模型驱动的实时读数和零件的真实尺寸与数量出现。
- **只画机器、仪器、工具和家具**：不画人，也不画精确地图。没有机制可搭的想法，出来的效果会更弱。
- **它故意很慢**：一张图需要很长的会话——零件清单、几何、审计，以及两种主题下每个接合处的特写。Raptor 的构建要几分钟，30 个零件的完整 3D 轨道审计要 15 到 20 分钟。
- **着色器需要 WebGL**：没有 WebGL 时 SVG 仍可阅读；在减少动态效果（reduced motion）下，所有图形静止。
- **3D 模式是 beta**：只在它的示例和一个测试图形上验证过，尚未在生产图形上验证。小型 3D 图形可跑 60 fps；380 零件的压力测试手在 1440 px 宽下约 20 fps，在节流的手机配置下为 13 到 15 fps（在负载很重的机器上测得）。
- **Node 版本**：构建与 kit 需要 Node 20.10+；skills CLI 1.7.1 要求 Node 22.20 或更高。在 Node 20 上浏览器脚本会用 `--experimental-websocket` 自行重启。
- README 未提供关于安全、隐私或数据外发的其他说明。

## 替代方案

README 未提供替代方案。README 中仅提到 Anatomy 是标准 Agent Skill、与 Agent Skills 兼容，并给出官网 `skills.wheresryan.sh/anatomy`、ZIP 下载与 MIT 许可证信息，未与其他工具做对比。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
