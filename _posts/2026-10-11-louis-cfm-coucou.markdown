---
layout: post
title: "Louis-CFM/coucou"
subtitle: "A tiny friend in your Mac's notch and on your iPhone that ke"
date: 2026-10-11 22:25:57 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
---

- 仓库：https://github.com/Louis-CFM/coucou
- Stars：4763
- 语言：Swift
- 创建时间：2026-09-27
- 官方简介：A tiny friend in your Mac's notch and on your iPhone that keeps an eye on your AI coding agents: Claude Code, Codex, Cursor, Gemini CLI, Antigravity and more. Approve from the notch or your Lock Screen.

---

> AI 生成服务本次不可用，以下内容由脚本按规则从 README 提取，可能不完整。

## 解决什么问题

A tiny friend in your Mac's notch and on your iPhone that keeps an eye on your AI coding agents: Claude Code, Codex, Cursor, Gemini CLI, Antigravity and more. Approve from the notch or your Lock Screen.

## 核心概念

README 未提供专门的概念说明，请结合官方文档确认。

## 前置依赖

见下方 README 安装章节，或让 AI 助手协助确认。

## 安装与配置

## Install

### App Store

Coucou is coming to the **Mac App Store** and the **iPhone App Store**: one click to install, automatic updates, and the iPhone app pairs with your Mac through your iCloud account, with nothing to configure. The links will be here as soon as Apple publishes them.

The App Store build of the Mac app runs in Apple's sandbox, so a few features stay in the GitHub build: Claude plan usage, the Apple Music pill and attaching the front window to the chat.

### iPhone

1. **Install Coucou on your iPhone** (iOS 18 or later): install [TestFlight](https://apps.apple.com/app/testflight/id899247664) from the App Store, then [Join the TestFlight beta](https://testflight.apple.com/join/3GpeHv2b). The beta is free; Apple limits it to 10,000 testers. The App Store version is coming soon.
   *Apple is reviewing the beta: it opens within a day or two — if the link isn't accepting testers yet, check back soon.*
2. **On your Mac**, with Coucou 0.1.9 or later: **Settings… → General → iPhone**, turn on **Show my agent sessions on my iPhone**, and **Move Mochi to my iPhone's Dynamic Island when my Mac is locked** for the Lock Screen.
3. **Same Apple Account** in iCloud on the Mac and the iPhone. That's the whole link: no account, no pairing code.
4. Open Coucou on the iPhone, allow notifications, and start a Claude Code session on the Mac.

Everything else, troubleshooting included, is in [docs/IPHONE.md](docs/IPHONE.md).

### Android

The first signed APK is on its way. Until then:

1. **Build the app** from [`android/`](android/) (see [Build from source](#build-from-source)) and install it on your phone (Android 11 or later).
2. **On your computer**, install Coucou **0.4.0 or later** for [Windows](#windows) or [Linux](#linux): **Settings → Android phone**, turn on **Phone link**. If Windows asks about the firewall, allow Coucou on private networks.
3. **Show pairing code** and scan it with the app. The phone and the computer must be on the same Wi-Fi.

Everything else, troubleshooting included, is in [`android/README.md`](android/README.md).

### Download for macOS

1. Grab the latest `Coucou.zip` from [Releases](https://github.com/Louis-CFM/coucou/releases).
2. Unzip and move **Coucou.app** to `/Applications`.
3. Launch it, and click **Open** when macOS asks you to confirm. Updating from 0.1.0? macOS may ask you, once for each key you saved, to let Coucou use it: enter your Mac password and click **Always Allow**.

### Windows

Download **[Coucou-Windows.msi](https://github.com/Louis-CFM/coucou/releases/download/windows-latest/Coucou-Windows.msi)** or **[Coucou-Windows-setup.exe](https://github.com/Louis-CFM/coucou/releases/download/windows-latest/Coucou-Windows-setup.exe)** (Windows 10/11, always the newest version) and run it. You can also [build it from source](#build-from-source).

**Windows will show a warning the first time — that's expected.** The installer isn't code-signed yet, so SmartScreen doesn't know the publisher:

1. A **"Windows protected your PC"** screen appears, with *Publisher: Unknown publisher*.
2. Click **More info** (*Informations complémentaires* in French). This reveals a **Run anyway** button.
3. Click **Run anyway** (*Exécuter quand même*). The installer starts normally.

This is only because the app isn't signed with a paid certificate yet. Coucou is open source, and Microsoft Defender scans the installer as clean.

**Windows and Linux 0.4.0** pair with [Coucou for Android](#coucou-for-android): approve, answer and chat from your Android phone (Settings → Android phone, off by default). 0.3.0 added open on hover, your own sounds, a colour of your own for each Mochi and the Mochi-to-desktop shortcut; on Linux, the Spotify pill with Mochi dancing to it, global shortcuts on Wayland and "Open terminal" that brings the terminal forward. 0.2.0 caught up with the Mac: Codex, Copilot CLI, Muse Code and six more agents with approvals from the island, answers to Claude's questions, live diffs, GitHub pull requests and CI, plan usage, local models, the wardrobe, Mochi on the desktop, keyboard shortcuts, the weekly recap and 10 languages. See the [changelog](CHANGELOG.md).

There is no notch on a PC, so the island slides out of the top edge of the screen
instead of hiding inside one. See [`windows/README.md`](windows/README.md) for the
rest of the differences.

### Linux

**Coucou for Linux 0.4.0** is out (x86_64): [AppImage](https://github.com/Louis-CFM/coucou/releases/download/linux-v0.4.0/Coucou-Linux-0.4.0-x86_64.AppImage) · [.deb](https://github.com/Louis-CFM/coucou/releases/download/linux-v0.4.0/Coucou-Linux-0.4.0-amd64.deb) · [.rpm](https://github.com/Louis-CFM/coucou/releases/download/linux-v0.4.0/Coucou-Linux-0.4.0-x86_64.rpm) · [all files and checksums](https://github.com/Louis-CFM/coucou/releases/tag/linux-v0.4.0). The newest AppImage is always at [`linux-latest`](https://github.com/Louis-CFM/coucou/releases/download/linux-latest/Coucou-Linux-x86_64.AppImage).

- **AppImage** (any distribution): `chmod +x Coucou-Linux-*.AppImage`, then run it.
- **Debian / Ubuntu**: `sudo apt install ./Coucou-Linux-*.deb`
- **Fedora / openSUSE**: `sudo dnf install ./Coucou-Linux-*.rpm`

Check a download with `sha256sum -c SHA256SUMS --ignore-missing`. On Arch Linux, build it with the [PKGBUILD](linux/arch/PKGBUILD).

The island sits on the top edge on compositors with layer-shell — COSMIC, KDE
Plasma, Hyprland, Sway and other wlroots compositors. GNOME has no layer-shell,
so there it runs through XWayland as a dock window at the top of the screen. See [`windows/README.md`](windows/README.md#linux).

### Build from source

**macOS** — requirements: macOS 15+, Xcode 16+, [XcodeGen](https://github.com/yonaskolb/XcodeGen).

```bash
brew install xcodegen
git clone https://github.com/Louis-CFM/coucou.git
cd coucou/NotchBuddy
xcodegen
open NotchBuddy.xcodeproj   # then ⌘R
```

**Windows** — requirements: [Rust](https://rustup.rs), Node 20+, MSVC build tools.

```powershell
git clone https://github.com/Louis-CFM/coucou.git
cd coucou/windows
npm install
npm run pack                # installer lands in windows/release/
```

**Linux** — requirements: [Rust](https://rustup.rs), Node 20+, and the WebKitGTK,
gtk-layer-shell and appindicator development packages (Debian/Ubuntu names below).

```bash
sudo apt install build-essential pkg-config \
  libwebkit2gtk-4.1-dev libgtk-layer-shell-dev libayatana-appindicator3-dev \
  librsvg2-dev libssl-dev libdbus-1-dev patchelf \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good
git clone https://github.com/Louis-CFM/coucou.git
cd coucou/windows
npm install
npm run pack                # AppImage, .deb and .rpm land in windows/release/
```

**Android** — requirements: JDK 17 and the Android SDK (platform 35).

```bash
git clone https://github.com/Louis-CFM/coucou.git
cd coucou/android
./gradlew assembleDebug      # the APK lands in app/build/outputs/apk/debug/
```

## Setup

Click the Coucou icon in the menu bar (macOS) or in the system tray (Windows, Linux) → **Settings…**

| What | Why | Where the key goes |
|---|---|---|
| **Claude Code hooks** | live sessions and approvals | **Install hooks** — Coucou backs up `~/.claude/settings.json`, merges its hooks and shows you the diff before writing anything |
| **Claude plan** *(macOS, GitHub build)* | Plan usage gauge in the notch header | **Install relay** in Settings → Agents → Plan usage, then enable "Show in the notch" |
| **Gemini CLI hooks** *(macOS)* | Gemini CLI sessions in the island | **Install hooks** in Settings → Gemini CLI — backs up `~/.gemini/settings.json` |
| **Antigravity (agy) hooks** *(macOS)* | agy sessions in the island | **Install hooks** in Settings → Antigravity — backs up `~/.gemini/config/hooks.json` |
| **Anthropic API key** | chat and questions about files | Settings → Anthropic API · Keychain / Windows Credential Manager / Secret Service |
| **Google AI API key** *(macOS)* | chat with Google AI (Gemini) | Settings → Chat — 

（章节内容较长，已截取）

## 最小可用示例

将下面指令整段复制给任意 AI 助手，让它结合你的环境给出可执行步骤：

```text
你是一名资深工程师助手。我想在当前项目中了解并评估下面这个 AI 工具/技能：

名称：Louis-CFM/coucou
链接：https://github.com/Louis-CFM/coucou
官方简介：A tiny friend in your Mac's notch and on your iPhone that keeps an eye on your AI coding agents: Claude Code, Codex, Cursor, Gemini CLI, Antigravity and more. Approve from the notch or your Lock Screen.
Stars：4763

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
