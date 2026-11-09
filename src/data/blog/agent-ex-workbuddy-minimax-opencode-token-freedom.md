---
title: AI 工作流｜agent-ex：给你的 AI 找个免费“外援”
pubDatetime: 2026-10-26T18:30:00Z
description: 七个月前被 token 周限搞出了焦虑，于是买了 MiniMax plan，结果便宜的 token 买不来会做方案的脑子。后来我就转向了 WorkBuddy/Trae，配合 MiniMax，一个写 spec、一个 review——agent-ex 就是整条流水线上的桥。
draft: false
tags:
  - agent-ex
  - WorkBuddy
  - MiniMax
  - OpenCode
  - MCP
  - AI Agent
  - 工作流
  - 穷鬼
  - 免费 token
categories:
  - 技术笔记
---

![人走了，活还在跑](/images/agent-ex-hero.webp)

## 前情背景

大概七个月前，MiniMax M2.7 刚发布的时候，我被一句「token 周限」的宣传搞出焦虑来了，于是就买了 MiniMax 的 token plan，放弃了同期 GLM 和 Kimi，结果发现，便宜是真便宜，但拉也是真的拉完了。

M2.7 越用越觉得菜，写个方案 spec + plan 真是要老命了，纯属鸡肋，每天都得激情开骂。DeepSeek V4 强一些，但没有 token plan，用多了也肉疼。

那会儿 Trae Solo 出来没多久，后来又出来了 WorkBuddy，都支持手机连接电脑，所以很长一段时间内我的工作方式就是 cc-connect + 飞书 + Claude Code 用 MiniMax 写 spec，然后让 Trae/WorkBuddy 里 GLM/DeepSeek 去 review，或者反过来。

我作为两个 agent 工具中的“接头人”，两边传话实在有点累，于是，就有了这个“穷鬼工作流”——`agent-ex`。

## `agent-ex` 能做什么

简单来讲，就是让 `主 agent` 和 `外部 agent` 合作去完成一项任务。通过 `agent-ex-dispatch` skill 调用 MCP 的能力分配任务给外部 agent，通过 `agent-ex wait` 等待任务完成后，进行后续轮次的操作，直到任务完成。

这个工作流的好处在于，可以极大程度地利用**不同 agent 工具**和**不同模型能力**的差异，从不同角度去分析、解决当前面临的问题，让产出的质量更高。

总体上，我还是推荐使用 `superpowers` 或者 `spec-kit` 这种 SDD（spec 驱动）的方式去解决问题，也是我常用的两个工作场景：**spec/plan 文档的创建**、**tasks 的执行与验收**。

### 1. spec/plan 的撰写过程

`spec` 是一个任务的核心需求与验收指标，`plan` 是任务细节的具体拆分。

在 spec 创建的过程中，我通常会和 `主 agent` 沟通几轮，确定大概需求/任务的方向，使用 `superpowers` 的能力产出第一份 `spec` 文档，然后就可以派发任务了：“派发 agent-ex 任务，loop 合作完成这份 spec，产出一份你俩都认可的方案”。

同样的，`plan` 文件的撰写也是相同流程，派发后就可以去做别的事情了，等待 WorkBuddy 任务完成。skill 里规定了，如果在方案制定过程中出现了两个 agent 都无法确认的问题，就会抛回给用户去拍板。

### 2. tasks 的执行与验收

这个步骤是 loop 的主战场，上一步骤产出的 plan 会把任务拆分好，后续的执行其实就更适合交给**便宜的 worker 模型**去执行了：“请派发 agent-ex 任务进行开发，loop 执行”。

整体上是个**串行开发 + 验证**的流程，串行是为了避免任务之间改动同一个工作区文件相互影响（可以支持 `git worktree`，暂时没做），外部 agent 执行完成后，主 agent 进行验收验证，然后再派下一个任务。验收的过程有几档置信度标准以及验收闸门，并不是轻易地接受外部 agent 结论。

### `loop` 的前提

这里需要特别注意，loop 的实现需要依赖 `主 agent` 支持 **「后台任务完成能触发新 turn」** 的能力，WorkBuddy 实测可以，Trae 有些问题，不支持后台任务，前台任务等待也有另一个小问题，所以，这里更推荐 WorkBuddy。

其实 MiniMax Code 最新版本迭代也很快，后台任务能力实现的体感更好一些，但是考虑到主模型能力越强越好，更推荐 WorkBuddy 按需切换 GLM 或者 DeepSeek。

## `agent-ex` 怎么用

### MCP + Skill 两层

简单讲，就是 agent-ex CLI 工具提供任务派发、执行、管理、存储的 **MCP server** 能力，需要配置到 `主 agent` 设置中去，同时还提供了 `agent-ex wait` 等待任务完成的能力，这是 loop 的核心。**dispatch skill** 规范了任务派发方式和派发时机，提供了任务 prompt 示例，以及任务验收标准。

### 安装与配置

前置条件：需要安装 Claude Code 或者 OpenCode 其中之一。

#### 1. 安装 npm 包

`npm i -g agent-ex-mcp`

#### 2. 初始化配置

`agent-ex init`

初始化的过程会读取已有 Claude 或者 OpenCode 配置（不联网不上传），本地解析后生成新 `~/.agent-ex/config.json`。初始化引导的过程中，如果选择使用 OpenCode，还支持生成 OpenCode 免费模型配置文件。

最终，初始化完成会给出一份 MCP 配置文件，配到你使用的 `主 agent` MCP 或者 连接器 配置里即可，可能需要手动在设置里点击“信任”或者类似开关，有些应用需要重启 app 后生效。

```
{
  "mcpServers": {
    "agent-ex": {
      "command": "/Users/xxxx/.nvm/versions/node/v24.14.0/bin/node",
      "args": [
        "/Users/xxxx/.nvm/versions/node/v24.14.0/lib/node_modules/agent-ex-mcp/dist/server.js"
      ]
    }
  }
}
```

> ⚠️ 注意：这里绝对路径是因为 MCP 客户端拉起 server 时很可能**不继承你的 shell `PATH`**，而不同 agent 会有沙箱设计的问题，导致 npm 路径无法识别到。

#### 3. 安装 skills

`npx skills add wuruofan/agent-ex --skill agent-ex-dispatch -g -y`

WorkBuddy 有个问题比较烦，不识别通用的 `.agents/` 配置目录，`npx skills` 安装后需要手动链接一下。

`ln -s ~/.agents/skills/agent-ex-dispatch ~/.workbuddy/skills/agent-ex-dispatch`

> ⚠️ 注意：链接之前先保证目录 `~/.workbuddy/skills/` 存在，**`ln` 对已存在的同名目录不会报错**，它会把软链塞进那个目录里，看着成功、实际没生效。

#### 4. 更新方法

`npm i -g agent-ex-mcp@latest`，skill 那边是实体副本，得单独更新：`npx skills update -g`。

> ⚠️ 注意：WorkBuddy/Trae 更新后可能需要 MCP server 重启，可以让主 agent 调用 `agent_ex_restart` 重启，但有些 agent 工具有限制，需要手动去设置里关闭然后再重新开启 MCP。

#### 5. 一句话安装

也可以把下面这段直接丢给你在用的 `主 agent`：

```
帮我装一下 agent-ex，按顺序来：
1. npm i -g agent-ex-mcp
2. 跑 agent-ex init，用我本机已有的 claude 或 opencode，密钥写进 ~/.agent-ex/.env
3. 把它打印的 MCP 注册片段（绝对路径那份）写进你的 MCP 设置里
4. npx skills add wuruofan/agent-ex --skill agent-ex-dispatch -g -y
5. 补一条软链：ln -s ~/.agents/skills/agent-ex-dispatch ~/.workbuddy/skills/agent-ex-dispatch
6. 重启 MCP server，用 agent_ex_version 确认工具都在，把版本号报给我
```

#### 6. 飞书 webhook 配置（可选）

1. 新建飞书群，然后进入群，`设置 → 群机器人 → 添加机器人 → 自定义机器人`，建完复制那串 `https://open.feishu.cn/open-apis/bot/v2/hook/...`。
2. 安全设置只勾「自定义关键词」，词填 `agent-ex`。
3. 把第 1 步复制的字符串发给 agent 工具：“帮我配置下 agent-ex 的 `FEISHU_WEBHOOK_URL`，xxxxx”。

![飞书机器人设置](/images/agent-ex-feishu-bot-setting.png)

## ⭐️ 如何充分地薅免费 token

整体思路就是 **WorkBuddy/Trae** 这种自带积分的 agent 工具 + **OpenCode Zen 免费模型**，前者负责“想”，后者负责“干”。

- WorkBuddy 的积分：写 spec、拆 plan、拍板、看复核结论。
- OpenCode Zen 的免费模型：具体的任务执行。

`agent-ex` 内置了免费模型的配置，如果 init 的时候没有创建，也可以使用 `agent-ex profile create opencode-zen-free --use` 一键创建并使用。

> ⚠️ 注意：OpenCode Zen 免费模型会变，已经预置了优先级和轮换顺序，每次执行任务之前会拉取最新模型清单，按照预置的 `ZEN_FREE_PREFER` 优先级顺序（`deepseek`、`glm`、`mimo`）去使用。

## 🤬吐槽

关于 Trae 曾经我用得最多，手机端会话同步得很快，用起来也很流畅，但是在 `agent-ex` 开发过程中发现很多问题，最重要的就是 Trae 本身**没有后台任务触发新 turn 的能力**，尝试过用定时器轮询去绕开，但是定时器任务没法继承会话上下文；如果选择前台任务等待的话，还会遇到前台任务超时转后台任务的问题。

Trae 还有一个问题，**本地 stdio MCP server 重启时不会自动重连**，而且界面上没有任何报错提示，只能电脑端去设置里点击重启 MCP，给 Trae 的产品和开发反馈过，但开发人员不认为是问题，反馈了好久也没给解决。

另外，Trae Solo 一开始改名 TraeWork，中间团队被豆包合并，有几周模型列表都不更新了，最近又改名回 Trae，直到现在手机 app 还没有深色模式，晚上睡觉前布置个任务眼都要瞎了，反正最近是拉完了。

而 WorkBuddy 也有自己的问题，手机登录同步电脑端会话的时候总是需要重新拉取会话信息，会话缓存做的是一坨，拉取会话历史和加载都很慢，还容易出错。WorkBuddy 不识别通用的 `.agents/` 配置目录，`npx skills` 安装后需要手动链接一下，比较烦躁。

但 WorkBuddy 更新频率比较高，模型上线速度较快，后台任务支持较好，**总的来说，还是首推使用 WorkBuddy**。

该说不说，最近 MiniMax Code 迭代速度比较快，后台任务做得很好，很多次执行过程中，会主动在当前会话里启动后台定时任务去等待，应该是提示词里有专门的优化。

## 最后

还是推荐大家试一试，尤其是 token 不够用的朋友。

祝大家 vibe coding 顺利，少生气。🙂
