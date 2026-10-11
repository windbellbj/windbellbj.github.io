---
layout: post
title: "Herald OS：以 Hermes Agent 为界面的智能体原生操作系统"
subtitle: "README 解读：安装方式、权限分级、系统工具桥接与在 Windows 开发机上的试用路径"
date: 2026-10-11 22:08:59 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
---

- 仓库：https://github.com/iamlukethedev/Herald-OS
- Stars：416
- 语言：TypeScript
- 创建时间：2026-10-06
- 官方简介：An agent-native operating system, with Hermes Agent as the interface. Independent project, not affiliated with Nous Research.

---

## 解决什么问题

Herald OS 是一个围绕 AI 智能体构建的操作系统。README 的描述是：你不再自己翻菜单和文件夹，而是通过语音或文字与 Hermes 对话，由它跨整台机器工作——打开应用、查找和整理文件、观察正在运行的程序、记住对你重要的事情、按计划运行例程，并在你眼前构建软件。

它的核心主张是：每一个会改变系统状态的操作，都要经过一套由你控制的权限系统。README 中明确写到，Hermes 的系统工具分为四个层级，`read`（系统信息、文件搜索）和 `act`（打开应用）直接执行并记录日志，`mutate`（创建、移动、重命名）会先询问，`destructive`（停止进程、把文件移入回收站）每次都要询问；`~/.ssh`、钥匙串和 Hermes 自己的凭据等位置始终拒绝访问。

README 同时强调：Herald OS 是 Luke The Dev 的独立项目，不是 Hermes 或 Nous Research 的官方产品，也未获得 Nous Research 的关联、赞助或背书；它运行在 Nous Research 发布的开源智能体 Hermes Agent 之上，Hermes Agent 与它一起安装。README 还标注当前状态为 alpha (0.1)，并提醒对任何让智能体接触的东西保留备份。

## 核心概念

- **Hermes 在中心**：README 列出 Overview、Hermes、Missions、Memory、Files、Automations、Connections 和 Settings 等页面，外加 Terminal、System monitor 和浮动聊天窗口。
- **系统工具桥接（herald-os-bridge）**：Herald OS 不 fork Hermes，而是运行标准 Hermes Agent 安装，并把系统能力作为一个常规 Hermes 插件加入。该插件被链接到 `~/.hermes/plugins/herald-os-bridge`，加入 `plugins.enabled`，并把 `cli` 平台的工具集列表写入 `herald_os`。README 说明这些工具只在 Herald OS 启动的会话中运行，Telegram、Discord、cron 和 `hermes` CLI 永远拿不到它们。
- **权限分级与审计**：四层工具权限，Settings > Privacy 展示策略和审计日志（`~/.hermes/herald-os/audit.jsonl`）。
- **接续上次工作**：打开 Herald OS 或休息后回来时，Hermes 查看最近文档、项目文件夹（含 git 状态）、对话和今天的日历，在 Overview 上最多放三条工作线索。README 说明该功能默认关闭，需从 Overview 打开；它只读取名称和日期（最近文件和文件夹、项目分支和提交信息、对话标题、今日事件标题、打开的应用），绝不读取文件内容、窗口标题或屏幕，并把这些发送给你的 Hermes 模型提供方来生成建议。
- **Herald OS Linux 是操作系统本身**：Fedora 提供内核、驱动和软件包，你看到的一切都是 Herald；niri 合成器排列窗口，Herald 绘制菜单栏、dock、通知、应用启动器和系统菜单。
- **在 Arch Linux 和 Omarchy 上**，Herald OS 是一个软件包：从登录界面进入完整会话，或作为 Hyprland 与 Omarchy 内的应用。
- **在 Mac 上**，Herald OS 全屏覆盖在 macOS 之上，同一套界面、智能体和工具，由 macOS 处理硬件和你的 Mac 应用。
- **Herald OS 的其它能力**：命令栏、语音（按语音键或说 “hey Hermes”）、Studio（说 “build a website for a hair salon” 并观看过程）、崩溃帮助、Herald Canvas 图像编辑器、Herald Office（Docs、Sheets、Slides）、十二套主题（两套浅色）、沙箱化小组件、屏幕取词与取色、用量统计、自动化与钩子脚本。

## 前置依赖

README 按不同安装路径给出了不同依赖，没有一份统一的依赖清单：

- **macOS 应用**：macOS 13 (Ventura) 或更高版本，且为 Apple Silicon。
- **从源码在 macOS 上运行**：macOS 13 (Ventura) 或更高版本、Apple Silicon（Intel Mac 未测试，README 说 Herald OS 在 macOS 26 上开发）；Node.js 22.12 或更高版本；Git 和 Xcode Command Line Tools（`xcode-select --install`，用于原生模块）；Hermes Agent 0.21.3 或更高版本，并配置好模型提供方。
- **Herald OS Linux 在虚拟机构建**：Apple Silicon Mac、Homebrew、约 20 GB 空闲磁盘空间；虚拟机分配 4 核和 8 GB 内存，若 Mac 总共只有 8 GB，需在命令前加 `MEM=4096`。
- **模型提供方**：无论选哪种方式，Hermes 都需要一个模型提供方——Nous Portal 账号，或 Hermes 支持的提供方（OpenRouter、OpenAI、Anthropic、本地模型等）的 API key。
- **完整会话（Linux）**：需要 niri 及其菜单栏和面板所用的工具，Fedora 的包名在 `linux/image/packages.txt`。

README 未提供在 Windows 上直接安装或运行 Herald OS 的路径。

## 安装与配置

本工具不直接作用于 Jekyll 博客站点本身。Herald OS 是一个操作系统/桌面应用（TypeScript + Electron，另有 Fedora 系统镜像与 Arch 包），与 Jekyll 3.9.5 静态博客、`scripts/` 下的 Python 标准库脚本以及 GitHub Actions 工作流没有直接集成点。README 未提供 Windows 安装方式，因此下面给出的是在你这台 Windows 10/11 开发机上可行的试用路径，以及在你已有环境中的注意事项。

**路径一：在 Windows 上先了解与评估（不改动你的机器）**

1. 打开仓库的 releases 页面（README 中所有下载都在 releases 页面），查看当前发布的构件类型：macOS 的 `HeraldOS-<version>-mac-arm64.dmg`、Linux 安装镜像 `herald-os-<version>-x86_64.iso.part0` 与 `.part1`、Linux tarball `herald-os-<version>-linux-x64.tar.gz`（ARM 为 `arm64`）、以及虚拟机磁盘 `herald-os-<version>-aarch64.qcow2.zst.part0` 与 `.part1`。
2. 阅读 README 指向的文档：`docs/ARCHITECTURE.md`、`docs/SYSTEM-BRIDGE.md`、`docs/VOICE.md`、`docs/LINUX.md` 和 `docs/manual/README.md`。

**路径二：在 Windows 上准备安装介质（README 给出了 Windows 命令）**

1. 从 releases 页面下载 `herald-os-<version>-x86_64.iso.part0` 和 `.part1`（README 说明 GitHub 单文件上限 2 GB，所以镜像分两部分）。
2. 在 Windows 上合并：README 给出的命令是 `copy /b herald-os-<version>-x86_64.iso.part0 + herald-os-<version>-x86_64.iso.part1 herald-os-<version>-x86_64.iso`。
3. 用 Fedora Media Writer 或 balenaEtcher 把 ISO 写入 8 GB 或更大的 U 盘。
4. 从 U 盘启动目标 PC 并按安装程序操作。README 说明磁盘界面可以擦除磁盘或与 Windows 并存安装，并可以加密，Secure Boot 可以保持开启。
5. 首次启动会先设置 Hermes Agent，然后 Herald OS 询问你的名字、密码和 Wi-Fi。

**路径三：在 Windows 上用虚拟机试（README 未提供 Windows 上的虚拟机步骤）**

README 只描述了在 Apple Silicon Mac 上用 `bash linux/vm/try.sh` 一条命令下载并启动虚拟机，以及把 qcow2 导入 UTM。README 未提供 Windows 上的虚拟机操作步骤，因此这里只能给出 README 中可复用的部分：下载 `herald-os-<version>-aarch64.qcow2.zst.part0` 和 `.part1`，用 `cat` 合并、用 `zstd -d` 解压。README 未说明 Windows 上应使用哪个虚拟机软件。

**如果你要在自己的机器上从源码构建（README 只支持 macOS 与 Linux）**

README 的构建步骤全部基于 macOS 或 Linux：`npm run bootstrap`、`npm run dev`、`npm run dist:mac`、`npm run dist:linux --workspace apps/desktop`。README 未提供 Windows 上的构建步骤。你机器上已有的 Python 3.12 与 Ruby 在 README 中未被提及为 Herald OS 的依赖。

**安装后需要知道的配置位置（README 表格）**

- Herald OS 偏好：`~/.hermes/herald-os/prefs.json`（在 Settings 中编辑）。
- 审计日志与控制套接字：`~/.hermes/herald-os/`。
- 日志文件：`~/.hermes/logs/herald-os.log`。
- Hermes 配置、记忆、会话、凭据：`~/.hermes/`，由 Hermes 管理。
- 少量选项来自环境变量，主要用于开发：在 macOS 上以窗口模式启动（`HERALD_OS_WINDOWED=1`）、使用不同的 Hermes 检出（`HERALD_OS_HERMES_ROOT`）、使用一次性的 Hermes home（`HERMES_HOME=/tmp/herald-test`）。README 指向 `.env.example` 列出全部。

**Herald OS 会改动你 Hermes 的哪些设置（README 明确列出）**

- 系统桥接插件被链接进 `~/.hermes/plugins/herald-os-bridge`，加入 `plugins.enabled`，并把 `cli` 平台的工具集列表写入 `herald_os`。
- 工具搜索被关闭（`tools.tool_search.enabled: off`），以便 Hermes 直接调用系统工具；原值保存在 `~/.hermes/herald-os/tool-search-before`，可在 Settings > Hermes & agents > Tool search 重新打开。
- 你的主题会成为 Hermes 的皮肤（`display.skin: herald-os`），除非你选了别的。
- 语音会在原有提供方无法运行时把语音转文字切到 `local` 或文字转语音切到 `edge`（`stt.provider`、`tts.provider`），并会告知你。
- 在 Linux 上撤销用 `herald-os setup --undo`；macOS 上的步骤在 `docs/SYSTEM-BRIDGE.md`。

## 最小可用示例

下面这段指令可以整段复制给任意 AI 编程助手，用来在你这台 Windows 开发机上规划一次 Herald OS 试用，同时不破坏现有的 Jekyll 博客仓库与自动化脚本。

```text
背景：我在 Windows 10/11 本地开发机上工作，已安装 Python 3.12 与 Ruby。我的项目是一个 Jekyll 3.9.5 静态博客（GitHub Pages 部署，仓库 windbellbj/windbellbj.github.io），仓库里有 scripts/ 目录下的 Python 标准库自动化脚本，以及 GitHub Actions 工作流。

目标：帮我评估并准备试用 Herald OS（https://github.com/iamlukethedev/Herald-OS）。它是一个以 Hermes Agent 为界面的智能体原生操作系统，README 标注状态为 alpha (0.1)，且明确说明 README 未提供 Windows 安装方式。

要求：
1. 先确认 Herald OS 与我的 Jekyll 博客没有直接集成点，不要修改博客仓库的任何文件、脚本或工作流。
2. 基于 README 事实，列出在 Windows 上可行的路径：一是只阅读文档与 releases 页面做评估；二是按 README 给出的 Windows 命令合并 herald-os-<version>-x86_64.iso.part0 与 .part1，并用 Fedora Media Writer 或 balenaEtcher 写入 8 GB 以上 U 盘，用于在另一台 PC 上安装。
3. 明确告诉我 README 未提供的内容：Windows 上的虚拟机步骤、Windows 上的源码构建步骤、以及任何 Windows 原生安装包。
4. 提醒我 README 中的风险点：alpha 状态、对智能体接触的文件保留备份、权限四层级（read/act 直接执行并记录，mutate 先询问，destructive 每次询问）、以及 ~/.ssh、钥匙串和 Hermes 凭据始终拒绝访问。
5. 输出一份分步骤的检查清单，每一步注明依据来自 README 的哪一部分，不要编造版本号、命令或结论。
```

## 验证方法

README 在“从源码在 macOS 上运行”一节给出了明确的验证步骤，可作为功能是否正常的判断依据：

1. **Hermes 能回答**：打开 Hermes 页面（`Cmd+2`）并提问。如果它要求你登录，使用它显示的卡片，或再次运行 `hermes setup`。
2. **系统工具可用**：问 “what is using the most memory right now?”。README 说 Hermes 应当用 `system_processes` 工具回答，而不是用 shell 命令。再让它移动一个文件，应当先出现一张批准卡片。
3. **语音可用（可选）**：按 `Alt+Space`，并在 macOS 询问时允许麦克风访问。Settings > Voice 里有 “Say hello” 和 “Start talking” 按钮用于测试。

在安装 Herald OS 之前，README 还建议先单独确认 Hermes 本身可用：运行 `hermes doctor`，再运行 `hermes` 打个招呼，然后用 `Ctrl+D` 退出。

在 Linux 上，README 说明每个热键和菜单项都是一个 `herald-os` 命令，`herald-os commands` 会列出全部命令，可用于核对命令是否可用。

对于 Windows 环境，README 未提供验证方法。

## 风险与注意事项

- **alpha 状态**：README 明确标注 “Status: alpha (0.1). Expect rough edges, and keep backups of anything you let an agent touch.”（预期会有粗糙之处，对任何让智能体接触的东西保留备份）。
- **非官方项目**：README 声明 Herald OS 是 Luke The Dev 的独立项目，不是 Hermes 或 Nous Research 的官方产品，未获 Nous Research 关联、赞助或背书。
- **权限模型**：`read` 和 `act` 直接执行并记录日志；`mutate` 先询问，可允许本次会话或始终允许；`destructive` 每次询问；`~/.ssh`、钥匙串和 Hermes 自己的凭据等位置始终拒绝。Hermes 自己的终端工具仍遵循 Hermes 的批准设置。
- **接续上次工作会发送数据**：该功能默认关闭，开启后会把最近文件和文件夹、项目分支和提交信息、对话标题、今日事件标题、打开的应用的名称和日期发送给你的 Hermes 模型提供方；README 强调它不读取文件内容、窗口标题或屏幕，并可在 Settings > Privacy 关闭及设置排除的文件夹和词。
- **会改动你已有的 Hermes 配置**：包括插件启用、工具搜索开关、皮肤和语音提供方，详见上文“安装与配置”一节；Linux 上可用 `herald-os setup --undo` 撤销。
- **macOS 构建未公证**：README 说明该构建尚未经 Apple 公证，macOS 首次会阻止它，需运行 `xattr -dr com.apple.quarantine "/Applications/Herald OS.app"`。本地构建同样未公证；macOS 通知需要代码签名的构建才能在你处于其它应用时送达。
- **Intel Mac 无现成构建**：README 说明没有 Intel 版 Mac 应用（`npm run dist:mac` 只为 Apple Silicon 构建），现成的虚拟机（`linux/vm/try.sh`）也需要 Apple Silicon。
- **Arch 包不在 AUR**：README 明确说该包尚未进入 AUR。
- **Omarchy 支持未在真机测试**：README 说它已针对 Omarchy 4 自身的配置和脚本测试，但尚未在 Omarchy 机器上测试，欢迎提交报告。
- **切换到 bootc 系统会替换系统**：README 提醒，已经在 Fedora Silverblue 或其它 bootc 系统上时，可以就地切换到 Herald OS 镜像，这会替换你运行的系统并新增一个免密码登录的账户，建议在备用机器或虚拟机中尝试。
- **README 未提供**：Windows 上的安装、构建与验证方法；除 README 所述之外的其它安全审计结论。

## 替代方案

README 未提供替代方案。README 中与“替代”相关的唯一表述是：Herald OS 不 fork Hermes，而是运行标准 Hermes Agent 安装并添加 `herald-os-bridge` 插件；以及在 Arch Linux 与 Omarchy 上，Herald OS 既可以作为完整会话，也可以作为现有桌面内的一个应用运行，在 macOS 上则全屏覆盖在 macOS 之上。这些是 Herald OS 自身的运行形态，不是竞品替代方案。

---

> 本文由 AI 阅读官方素材（GitHub README）后生成，已要求其仅依据素材撰写；关键命令请以官方文档为准。
