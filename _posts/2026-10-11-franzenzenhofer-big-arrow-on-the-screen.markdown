---
layout: post
title: "bigarrow：让 AI 代理在 Mac 屏幕上画大箭头"
subtitle: "macOS 命令行工具 + Claude Code/Codex 技能，透明覆盖层指向界面元素，点击穿透、自动消失"
date: 2026-10-11 22:08:59 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
---

- 仓库：https://github.com/franzenzenhofer/big-arrow-on-the-screen
- Stars：611
- 语言：Swift
- 创建时间：2026-10-08
- 官方简介：Let your AI agents paint big arrows, boxes and text on your Mac screen. One CLI, click-through, gone by itself. Skill for Claude Code and Codex. MIT.

---

## 解决什么问题

AI 代理可以重构 monorepo、写迁移脚本、解释 monad，但当它需要你点一个按钮时，它只能把“请在对话框中点击 Allow”打印到一个你根本没在看的终端里。`bigarrow` 给了它一根手指。

`bigarrow` 是一个 macOS 命令行工具，外加一个面向 Claude Code 和 Codex 的技能（skill），能在所有窗口之上画出一个箭头和一块标牌。点击可以穿透，键盘焦点保持不变，箭头会自行移除。

README 明确说明它**不是**屏幕标注器、不是点击机器人、不是截图工具：它从不点击、从不输入、从不截屏，只负责“指”。

## 核心概念

- **箭头与标牌**：一个透明窗口覆盖在所有内容之上，覆盖每一块显示器、每一个 Space。绘制本身**不需要任何 macOS 权限**。
- **点击穿透**：除标牌和箭杆之外的所有区域点击都会穿透；点击标牌或箭杆会移除箭头（指针悬停时标牌会变暗以示提示）。
- **不抢焦点**：箭头位于屏幕保护程序层级，高于窗口、对话框和全屏应用，但永远不会成为活动窗口。
- **自动消失**：每个箭头都会自行结束。时限（`--duration`，`point` 默认 8 秒，`start` 默认 300 秒，`0` 表示无限制）、`stop`/`stop --all`、代理进程退出（`CLAUDE_PID` 或 `BIGARROW_OWNER_PID`）、人类回答（`bigarrow stop --hook` 作为 Claude Code 的 `UserPromptSubmit` 钩子）、人类关闭（`--close-button`，需显式开启）。
- **目标定位方式**：`--at X,Y`、`--rect X,Y,W,H`、`--mouse`、`--window App[:title]`、`--element Label --app App`、`--peekaboo ID --snapshot see.json`。坐标是全局左上角逻辑点，与 Accessibility 和 Peekaboo 报告的一致；`--display N` 使其相对于某一块显示器。
- **前置唤起**：`--app App[:窗口或标签页标题]`（或 `--window`）会先把该应用、窗口或 Chrome/Safari 标签页带到前台；`--no-raise` 可关闭该行为。若之后有其他应用遮挡目标，箭头会隐藏直到目标重新可见。
- **外观选项**：`--shape bend|straight|zigzag|spiral`、`--style arrow|ring|box`（ring 和 box 是轮廓，目标保持可见）、`--size S|M|L`、`--corners round|sharp`、`--color`（含 `#RRGGBB`）、`--border shadow|white-black|black`、`--border-color`、`--text-color`、`--edge-color`、`--close-color`、`--close-x-color`。
- **复制粘贴**：`--text` 中的 `{{value}}` 会变成一个复制按钮，点击即复制。
- **其他开关**：`--follow` 跟随窗口或元素移动、`--until-click` 在点击目标后结束、`--say` 朗读标牌文字、`--png` 直接渲染为 PNG、`--dry-run --json` 报告它“将会”指向哪里。
- **退出码**：0 成功，2 输入错误，3 目标未找到，4 缺少权限。每个命令都支持 `--json`。

## 前置依赖

- **操作系统**：macOS。README 的安装说明中，从源码构建要求 Xcode 16+、macOS 14+。README 未提供 `brew` 安装方式的最低系统版本。
- **安装方式**：Homebrew（`brew install franzenzenhofer/tap/bigarrow`）或从源码 `swift build -c release`。
- **权限**（README 以表格形式给出）：
  - `--at`、`--rect`、`--mouse`、`--window App`、`--peekaboo`、`--app App`：无需权限。
  - `--element`、`elements`、`--until-click`、`--app App:title`：需要辅助功能（Accessibility）权限。
  - `--window App:title`（macOS 26 隐藏窗口标题）：需要屏幕录制（Screen Recording）权限，外加辅助功能权限用于唤起（`--no-raise` 时不需要）。
  - macOS 把这些权限授予启动 `bigarrow` 的那个应用（Terminal、iTerm2、Ghostty、VS Code、Claude），而不是 `bigarrow` 本身。`bigarrow doctor` 会指出是哪个应用；缺少权限时以退出码 4 结束并给出应用名和设置面板。
- **技能安装**：`bigarrow install-skill` 会教 Claude Code（`~/.claude/skills`）和 Codex（`~/.agents/skills`）。
- **二进制说明**：二进制是纯 Swift；`scripts/` 只用于记录截图和运行测试。

## 安装与配置

本工具不直接作用于 Jekyll 博客站点本身。它是一个 macOS 桌面覆盖层工具，与 Jekyll 3.9.5 静态博客、GitHub Pages 部署、`scripts/` 下的 Python 标准库脚本以及 GitHub Actions 工作流都没有集成点。以下是在你的 Windows 10/11 本地开发机上试用的步骤。

需要先说明：README 只描述 macOS 行为，未提供任何 Windows 支持说明。因此在你当前的 Windows 开发机上，只能做“了解与准备”，实际运行需要一台 Mac。

1. **确认硬件条件**：准备一台 macOS 机器（README 的源码构建要求 macOS 14+ 与 Xcode 16+）。README 未提供 Windows 或 Linux 版本。
2. **在 Mac 上安装**：执行 `brew install franzenzenhofer/tap/bigarrow`。
3. **安装技能**：执行 `bigarrow install-skill`，它会写入 Claude Code 的 `~/.claude/skills` 与 Codex 的 `~/.agents/skills`。
4. **检查环境**：执行 `bigarrow doctor`，它会显示权限与显示器情况，并指出需要为哪个应用开启权限。
5. **按需授权**：如果你打算用 `--element` 按标签定位，需要在“系统设置”里为启动 `bigarrow` 的终端应用开启辅助功能权限；如果要用 `--window App:title`，还需要屏幕录制权限。
6. **在你的 Jekyll 项目里能做什么**：README 未提供任何与 Jekyll、GitHub Pages 或 Python 脚本集成的说明。若你希望在 Mac 上演示博客相关操作（例如在浏览器里指向某个标签页），README 给出的 `--app "Google Chrome:Sourdough"` 形式可以唤起并选中标签页，但这属于通用能力，不是针对 Jekyll 的集成。

## 最小可用示例

```text
背景：我在 macOS 上使用 Claude Code，需要你（AI 代理）在屏幕上用 bigarrow 指出一个界面元素，而不是只在终端里打印“请点击 Allow”。
目标：让 bigarrow 在“系统设置”窗口的 Allow 按钮上画一个带文字的箭头，并在我点击后自动消失。
要求：
1. 先运行 bigarrow doctor，确认权限与显示器状态；如果缺少辅助功能权限，告诉我需要为哪个应用开启，不要自行假设。
2. 使用按标签定位的方式：bigarrow point --element "Allow" --app "System Settings" --text "请点击 Allow"。
3. 如果目标未找到（退出码 3），改用 bigarrow elements --app "System Settings" 列出可匹配的元素名，再重试，不要编造元素名。
4. 如果缺少权限（退出码 4），把 README 中说明的权限归属告诉我：macOS 把权限授予启动 bigarrow 的应用，而不是 bigarrow 本身。
5. 全程不要点击、不要输入、不要截屏；bigarrow 只负责指。
6. 完成后告诉我实际执行的命令与退出码。
```

## 验证方法

README 提供了以下可执行的验证途径：

1. **环境自检**：运行 `bigarrow doctor`，查看权限与显示器状态。
2. **干跑定位**：用 `--dry-run --json` 查看它“将会”指向哪里，用于调试坐标。
3. **元素枚举**：运行 `bigarrow elements --app X`，列出 `--element` 可以匹配的内容。
4. **退出码判断**：0 表示成功，2 表示输入错误，3 表示目标未找到，4 表示缺少权限。
5. **官方测试证据**（README 陈述）：104 个自动化测试覆盖几何、摆放、接缝、黄金图像、复制按钮、录制的窗口服务器、Accessibility 与 Peekaboo 夹具，以及真实窗口服务器（点击穿透、焦点从不移动、停止计时）；CI 运行在 macOS 15，也在 macOS 26 和 27 上通过。另有 18 项干净 runner 上的行为检查（`visual.yml`）：点击 X、复制按钮（剪贴板持有该值且箭头保留）、`--until-click`、`--follow`、唤起与 `--no-raise`、被遮挡时隐藏、Chrome 标签页选择、属主退出、`stop --hook`、`--say`、全屏、Stage Manager、Spaces、第二块与 2x 显示器、箭头中途拔掉显示器、CPU。
6. **技能测试**：README 记录了一个只拿到技能和“给 Franz 指出 Chrome 里 Reload 按钮在哪”的新代理，按标签找到了它并构造出正确命令（见 `docs/skill-tests/2026-10-08-chrome-reload.md`）。

## 风险与注意事项

- **平台限制**：README 只描述 macOS。Windows 与 Linux 未提供。
- **权限归属容易搞错**：macOS 把辅助功能/屏幕录制权限授予启动 `bigarrow` 的应用（Terminal、iTerm2、Ghostty、VS Code、Claude），而不是 `bigarrow` 本身。
- **Chrome 网页内的 `--element` 有限制**：在 Electron 应用中可用；在 Chrome 中需要 `--force-renderer-accessibility`（或开启 VoiceOver），因为 Chrome 会忽略常规请求（README 称于 2026 年 10 月验证）。Chrome 自身的工具栏始终可用。否则需要指向页面坐标。
- **代理能否借此欺骗你**：README 的回答是“不会超出它已经能做的事”——一个能以你的身份运行 shell 命令的代理本来就能做更糟的事。README 列出若干由测试保障的约束：box 和 ring 是轮廓所以目标保持可见；标牌避开目标（或尽量少重叠）；点击标牌或箭杆会移除箭头；每个箭头都会自行结束；技能要求标牌写明你的点击会做什么。
- **CPU 开销**：README 称在 CI runner 上脉冲箭头占用 1.4%，由 Core Animation 在渲染服务器中完成。
- **Token 开销**：技能描述 182 tokens（代理始终可见的部分）；指令 1,528 tokens（Anthropic token-count API，Claude Opus 5.5），仅在它决定指向时加载；面板 id 与外观标志（另 1,118 tokens）仅在需要时加载。
- **README 未提供**：Windows 支持、与 Jekyll/GitHub Pages 的任何集成、数据收集或遥测细节（README 仅声明“无账号、无遥测”）、具体版本号。

## 替代方案

README 中提到的相关或替代方案：

- **屏幕标注应用**：README 的 FAQ 明确区分——“那些是给人用来在屏幕上画画的。这个是给程序从 shell 指向东西用的，带退出码。”README 称先检查了 26 个工具（见 `docs/research/`），没有一个做这件事。
- **Peekaboo**（https://github.com/openclaw/Peekaboo）与 **Nameplate**（https://github.com/steipete/Nameplate），作者 Peter Steinberger：README 称它们展示了覆盖层配方与技能打包方式，但两者都不会用带标签的箭头来指。`bigarrow` 可以读取 Peekaboo 的 `see --json` 作为目标来源。
- **图标来源**：复制与勾选图标来自 Feather（MIT）。

README 未提供其他同类竞品的对比清单或迁移指南。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
