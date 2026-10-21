---
layout: post
title: "WhatsApp MCP：在 Cloudflare 上免费读取聊天记录"
subtitle: "只读 MCP 服务，让 AI 代理搜索个人 WhatsApp 消息；与 Java 开发无关，可跳过"
date: 2026-10-22 04:26:15 +0800
author: ""
header-img: "img/post-bg-ai-news.svg"
tags:
    - AI新资讯
    - MCP服务
news_category: mcp
---

- 来源：Hacker News Show HN
- 项目链接：https://github.com/finereli/whatsapp-mcp
- HN 讨论：https://news.ycombinator.com/item?id=50145715（157 points）

---

# WhatsApp MCP：在 Cloudflare 上免费读取聊天记录

> 一个**只读**的 MCP 服务：把个人 WhatsApp 账号链接到你自己的 Cloudflare 账号，让任意 MCP 客户端（Claude Code、Claude Desktop 等）搜索和阅读你的聊天记录。适合想把私人聊天接进 AI 代理的个人用户；**与 Java 后端开发、AI 辅助编码无关，Java 程序员可跳过**。

## 它是什么

作者想要「手机上的 Claude 能读我的 WhatsApp 消息」，但现有方案要么需要 WhatsApp Business，要么得自己架服务器跑 Baileys。于是他做了这个项目：

- **运行在你自己的 Cloudflare 账号里**，不是第三方托管服务；
- 像 WhatsApp Web 一样**扫码链接一次手机**，之后任何支持 MCP 的客户端都能搜索、阅读聊天；
- **只能读，不能发**；可以记住你给手机号起的名字；
- 会同时连接 Google 账号，用来补全 WhatsApp 联系人姓名——否则很多联系人只有号码，搜索效果很差；
- 作者明确说明这是**单用户安装**，因为「既处于灰色地带，又非常私密」，建议直接把仓库地址交给代理，让它帮你完成配置。

## 怎么工作

- 手机始终是数据源头，服务只是一个「已链接设备」；
- 它**不保持长连接**：代理发起请求时、以及每天一次，才连上 WhatsApp，收取排队消息，写入自己的数据库后断开；手机照常使用和收通知；
- 消息存在你 Cloudflare 账号内 Durable Object 的 SQLite 数据库里，项目页称「不会流向别处」。

<!-- asset:blog-1 start -->
![只读链接设备的工作方式](/img/ai-news/hn-whatsapp-mcp-running-free-on-cloudflare-145715/blog-1.png)

*图：只读链接设备的工作方式*
<!-- asset:blog-1 end -->


## 社区怎么看

HN 讨论（157 points）几乎全部集中在**隐私**上，且以质疑为主：

- 有人讽刺：「Cloudflare 本来就在嗅探大半个互联网的流量，不如顺便让它看看我们的私信？」
- 核心担忧：把对话的另一方也暴露给第三方 AI 公司，对方**从未同意**；
- 反驳观点：通讯录被上传早已发生多年，元数据和对话内容不是一回事；
- 也有人认为「这艘船早就开走了」——你永远不知道对方在用什么样的第三方工具处理通信；
- 还有观点认为，对话「安全」本就取决于对方如何处理，现实中的安全性一直是种表演。

**没有看到针对功能、稳定性或代码质量的正反面评价**，讨论基本是隐私立场之争。

<!-- asset:blog-2 start -->
![HN 讨论聚焦隐私质疑](/img/ai-news/hn-whatsapp-mcp-running-free-on-cloudflare-145715/blog-2.png)

*图：HN 讨论聚焦隐私质疑*
<!-- asset:blog-2 end -->


## 怎么开始试用

前置条件：Cloudflare 账号（需 **Workers Paid** 计划，项目页说明导入大量历史时默认 CPU 限制不够用）、Node 20 或以上、你的手机。

1. 克隆仓库并安装依赖：`git clone https://github.com/finereli/whatsapp-mcp`，进入目录后 `npm install`；
2. 创建 KV 命名空间：`npx wrangler kv namespace create OAUTH_KV`，把打印出的 id 填进 `wrangler.jsonc`；
3. 设置链接页密码（12 位以上）：`npx wrangler secret put OWNER_PASSWORD`；
4. 部署：`npm run deploy`，Wrangler 会给出形如 `https://whatsapp-mcp.your-name.workers.dev` 的地址；
5. 打开该地址，按页面提示**扫码链接 WhatsApp**（设置 → 已链接设备 → 链接设备），首次会导入历史，页面显示进度，可以关掉；
6. 连接代理，例如 Claude Code：`claude mcp add --transport http whatsapp https://your-url/mcp`，然后输入 `/mcp` 并用密码登录；其他客户端指向同一个 `/mcp` 地址即可。

想用自己的域名，见 `wrangler.jsonc` 底部的注释。

<!-- asset:code-1 start -->
```powershell
git clone https://github.com/finereli/whatsapp-mcp
npm install
npx wrangler kv namespace create OAUTH_KV
npx wrangler secret put OWNER_PASSWORD
npm run deploy
claude mcp add --transport http whatsapp https://your-url/mcp
```
<!-- asset:code-1 end -->


## 对 Trae Work 用户的价值判断

坦白说：**这条新品与 AI 辅助软件开发无关**。它是个人通讯数据的只读检索工具，不产出代码、不增强编码代理，也不解决 Java/Spring 开发中的任何问题。

如果你只是想在 Trae Work 里提升编码效率，**可以直接跳过**。若你出于个人兴趣想在自己的 Cloudflare 账号里搭一个只读聊天检索服务，可以按上面的步骤试；但请先想清楚：聊天另一方的隐私并不由你一个人决定。

```text
背景：我在 Windows 上用 Trae Work 做 Java/Spring 后端开发，看到 GitHub 项目 finereli/whatsapp-mcp——一个跑在 Cloudflare Workers 上的只读 MCP 服务，可让 MCP 客户端搜索、阅读个人 WhatsApp 聊天记录，需 Workers Paid 计划，单用户安装，作者称消息只存在自己账号的 Durable Object SQLite 中。
目标：帮我判断这个项目是否值得我花时间试用，以及如果试用，如何在我的环境里安全地完成部署与接入。
要求：
1. 先明确结论：它对我的 Java 开发工作流是否有实际价值；若基本无关，请直接说明并给出理由。
2. 梳理部署前置条件与关键步骤（Cloudflare 账号与套餐、Node 版本、KV、密码、部署、扫码链接、MCP 客户端接入），指出容易卡住的环节。
3. 从隐私与合规角度列出主要风险点（对话另一方未同意、第三方 AI 训练数据、Cloudflare 可见性等），并给出降低风险的建议。
4. 对比「自建 Cloudflare 方案」与「本地导出后检索」两种思路的取舍。
5. 不要编造项目未公开的信息，缺失处标注「官方未公开说明」。
```

---

> 本文由 AI 综合Show HN 原帖与社区讨论撰写，已要求其仅依据公开资料成文；关键命令请以官方文档为准。
