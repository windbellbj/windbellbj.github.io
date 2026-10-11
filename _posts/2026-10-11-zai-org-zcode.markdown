---
layout: post
title: "zai-org/ZCode"
subtitle: "Z.ai's coding agent harness. Powerful, intelligent, extensib"
date: 2026-10-11 22:25:57 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
---

- 仓库：https://github.com/zai-org/ZCode
- Stars：7670
- 语言：TypeScript
- 创建时间：2026-09-20
- 官方简介：Z.ai's coding agent harness. Powerful, intelligent, extensible.

---

> AI 生成服务本次不可用，以下内容由脚本按规则从 README 提取，可能不完整。

## 解决什么问题

Z.ai's coding agent harness. Powerful, intelligent, extensible.

## 核心概念

README 未提供专门的概念说明，请结合官方文档确认。

## 前置依赖

见下方 README 安装章节，或让 AI 助手协助确认。

## 安装与配置

# 使用测试环境
pnpm dev:desktop:test
```

`pnpm dev:desktop` 默认等同于 `pnpm dev:desktop:prod`，使用生产服务配置。启动脚本会准备本地运行资源、构建桌面 Agent，再启动 Electron 和源码监听。

需要独立开发数据目录时，可设置 `ZCODE_DATA_BASE_DIR`。例如在 macOS / Linux 中：

```bash
ZCODE_DATA_BASE_DIR="$HOME/.zcode-dev-home" pnpm dev:desktop:test
```

### 远程功能（SSH/WSL）

先执行 `pnpm bootstrap:with-remote` 准备远程资源（mock-cdn），再 `pnpm dev:desktop`；连接远程项目时资源选择「本地下载后上传」。开发态资源取自本地 `packages/desktop/mock-cdn` 和本地构建产物，经 SFTP 上传到远程，不访问 CDN。

### Web 开发

修改 Web 或后端源码时，使用开发模式：

```bash
pnpm dev:web

## 配置

根目录 [.env.example](.env.example) 提供服务地址与构建配置示例，可按需复制到 `.env`，本地覆盖放入 `.env.local`。Desktop 的开发环境通过 `dev:desktop:test` / `dev:desktop:prod` 选择。

| 配置                                 | 用途                                             |
| ------------------------------------ | ------------------------------------------------ |
| `ZCODE_DATA_BASE_DIR`                | 应用数据基目录，数据写入其下的 `.zcode/`         |
| `ZCODE_SERVER_WORKSPACE`             | Web 后端的工作区路径                             |
| `ZCODE_BUILTIN_PROVIDER_CONFIG_FILE` | 本地 Provider 配置文件路径；未设置时使用内置配置 |
| `ZCODE_DIST_BASE_URL`                | 命令行安装脚本使用的下载根地址                   |

运行时变量可在启动命令的环境中显式设置。随客户端发布的默认配置见 [config/README.md](config/README.md)。

# 已配置 ZCODE_DIST_BASE_URL 时
pnpm build:zcode

## 最小可用示例

将下面指令整段复制给任意 AI 助手，让它结合你的环境给出可执行步骤：

```text
你是一名资深工程师助手。我想在当前项目中了解并评估下面这个 AI 工具/技能：

名称：zai-org/ZCode
链接：https://github.com/zai-org/ZCode
官方简介：Z.ai's coding agent harness. Powerful, intelligent, extensible.
Stars：7670

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
