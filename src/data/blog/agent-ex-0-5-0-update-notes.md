---
title: AI 工作流｜agent-ex 更新：skill 安装优化
pubDatetime: 2026-11-13T09:30:00Z
description: agent-ex 连发三个版本：dispatch skill 打包进 npm 包，一条命令装好并链接到 17 家宿主。
draft: false
tags:
  - agent-ex
  - AI Agent
  - MCP
  - Skill
  - 工作流
categories:
  - 技术笔记
---

上一篇写 `agent-ex` 怎么用，那会儿装 dispatch skill 得两步：`npx skills add` 再给 WorkBuddy 手动 `ln -s`。才过一周，`agent-ex-mcp` 就发到了 `0.5.0`，skill 直接内置在 npm 包里。

## 一条命令装好 skill

```bash
npm i -g agent-ex-mcp@latest
agent-ex skill install
```

它把包里的 skill 拷到 `~/.agents/skills/agent-ex-dispatch`，写个 marker 记版本，再给本机各家宿主建软链。skill 跟着包发，版本永远和 CLI 对得上，升级后重跑一次就更新。

宿主表从 5 家扩到 17 家，除了 Claude Code、WorkBuddy、Trae CN，还多了 Cursor、Windsurf、Trae、GitHub Copilot、Gemini CLI、Droid、Amp、Qwen Code、MiniMax Code、CodeBuddy 等。

默认只链你本机装了的，也可以点名：

```bash
agent-ex skill install --agent cursor --agent claude-code   # id 和别名都认
agent-ex skill remove --agent cursor                        # 只卸这一家
agent-ex skill status                                       # 只读：装在哪、哪一版、哪些还没链
```

Codex、Cline、Zed 本来就读 `~/.agents/skills`，不用链，`status` 里会标 `no link needed`。原来那条手动 `ln -s` 可以删了，WorkBuddy 大部分安装自带桥接脚本，没有的话 `--agent workbuddy` 就行。

## 其他改动

- 派发前加模型存活预检。之前 profile 里配个下线的 model id，任务 1 秒内 failed，opencode 只回一句 `Unexpected server error. Check server logs for details.`，exit 还是 0，根本看不出是模型没了；现在确认模型下线就直接拒绝，不建任务。
- 飞书卡片脚注标出 profile 和实际跑起来的模型，任务挂了知道是哪个模型干的。
- `init` 收尾从 39 行压到 24 行，自动探测 node / npm / bun / git 并预填 worker 的 `path_dirs`。
- `agent_ex_status` 的 `include_finished` 会话重启后能认回上次派的任务（0.3.1）。

## 升级方法

```bash
npm i -g agent-ex-mcp@latest
agent-ex skill install
```

MCP server 是长驻进程，升完让主 agent 调一下 `agent_ex_restart`，再用 `agent_ex_version` 确认 `gitSha` 变了。

## 小结

还在用 agent-ex 的朋友值得顺手升个级，之后 skill 安装与升级都会方便些。祝大家 vibe coding 顺利。🙂
