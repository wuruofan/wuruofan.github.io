---
title: 🦞养虾日记｜OpenClaw 升级踩坑记录：2026.3.13 ~ 2026.5.22
pubDatetime: 2026-06-01T05:20:00Z
modDatetime: 2026-06-01T05:30:00Z
cover: /images/cover-openclaw-upgrade-pitfalls.jpg
description: OpenClaw 升级踩坑全记录：install.sh 和 npm 双轨并行、Session Lock 大坑、LaunchAgent 被覆盖——这些坑我都替你踩过了
draft: false
tags:
  - 养虾日记
  - OpenClaw
  - AI Agent
  - 踩坑记录
  - Claude Code
  - 升级
categories:
  - 随笔
---

## 前情摘要

我之前在旧笔记本上装了 OpenClaw，有段时间没更新了，日常也就用来干一些杂活，陪我读书记笔记。

养过小龙虾的可能都有体会，这东西记忆很差，隔天的事情就忘记了，你还得提醒它去翻自己记录，很恼火。看着现在新 Hermes Agent 出现，OpenClaw 好像也更新了记忆的一些能力，我就想着…要不更新看看？

其实我是有预想过会有坑的，我想着这不万事有 Claude Code 嘛，也研究过推荐的 `openclaw doctor --fix` 方案，但是万万没想到…结果开启了一场跨越 `2026.3.13` → `2026.5.18` → `2026.5.22` 的 debugging 之旅。

本文适合每一个被 OpenClaw 升级折腾到头秃的人类…如果你也准备升级，建议先看完这篇，也能帮你省下 2 小时和一把头发。

---

## 坑一：双轨制安装 — `install.sh` 与 `npm install -g` 的平行宇宙

我最早用官方 `install.sh` 一键安装，这次就打算让 Claude Code 帮我升级，然后我就一头掉进第一个坑里了。🙂🙃🙂🙃🙂

**现象：**

Claude Code 说更新成功了，版本号 2026.05.18。于是，我让虾自己重启 gateway 之后，问它版本号，居然还是 2026.03.13，明明升级了，版本号却纹丝不动。

我又去问 Claude Code，为啥？它说确实升级成功了啊，它自己去试了下，也说好奇怪，OpenClaw tui 是新版本，gateway 却是旧版本。

**原因：**

这其实是安装方式和升级方式差异导致的。

最开始官方 `install.sh` 脚本把二进制写进了 `/usr/local/bin` 和 `/usr/local/lib/node_modules` 目录；但是 CC 选择了用 `npm install -g` 的方式更新，而 CC 本身是用的 nvm 环境，就导致新版装进了 `~/.nvm/versions/...`。

而 shell PATH 里 `/usr/local/bin` 优先级高于 nvm，所以每次敲 `openclaw`，调用的都是 `install.sh` 留下的"古董"，而且 gateway 启动方式 LaunchAgent plist 里写的路径也是 nvm 下的路径。

问题是发现了，但修复方案 CC 选择了一个治标不治本的方法，由于 CC 启动 tui 永远都是 nvm 的最新版本，所以它就只把 LaunchAgents 里的路径改了，这样 gateway 启动的就是最新版的了，这也给我后面更新 05.22 版本又埋了个坑。😓😓😓

**正确的修复方法：**

```bash
sudo rm /usr/local/bin/openclaw
sudo rm -rf /usr/local/lib/node_modules/openclaw
```

然后确认 `which openclaw` 指向 nvm 路径。不要用 `sudo npm uninstall -g`，因为那会误删 nvm 里的新版。

---

## 坑二：5.18 的 Session Lock 大坑💩💩

**现象：**

gateway 重启成功，但是飞书渠道完全不可用，除了说你好，其它每条消息都执行个几分钟，然后报错：

> `EmbeddedAttemptSessionTakeoverError:`
> `session file changed while embedded prompt lock was released`

到处找不到解决方法，没办法，我后来去扒了源码，发现是新版本**新增的 session 指纹机制**导致的，但奇怪的是这部分**既不在 `openclaw` 主仓库里**，也不在它依赖的 `pi-agent-core` 代码仓库里——它存在于 **OpenClaw 打包 patch 的那部分代码**中。

OpenClaw 底层其实维护着一个**本地大幅修改的 pi 核心代码的 fork 版本**（那时候仓库还叫 `pi-mono`，npm 包名也和现在不一样）。这个 `EmbeddedAttemptSessionTakeoverError` 的指纹检查（用 `mtimeNs` 纳秒级精度检测 `.jsonl` 是否被篡改）就是在这个 fork 的 patch 里引入的。

问题出在：这套指纹机制无法区分"外部劫持"和"自己人写的"。当 embedded runner 释放锁让 LLM 处理 prompt 时，如果内部 session hook 或 trajectory writer 顺手写了一点东西到 `.jsonl`，指纹就对不上了，直接抛异常。

**这相当于你打开门拿个快递的时候，家里猫蹭了下门边边，结果门禁就报警说「有人入侵」，然后把你锁在门口了。** 🌚🌚🌚

**影响范围：**

- 所有现有 session 和新 session（`/new` 也救不了）
- 飞书 WebSocket 渠道 100% 复现
- `compaction.mode: off` 无效

**结局：**

提了 **Issue #84059**：《EmbeddedAttemptSessionTakeoverError: session file changed while embedded prompt lock was released》

GitHub 链接：https://github.com/openclaw/openclaw/issues/84059

然后发现很多人回复我，并不是我一个人遇到这个问题。最终，问题大概一周后在 `2026.5.22` 版本修复。

---

## 坑三：LaunchAgents 被 `doctor --fix` 覆盖，配置兼容性连环报错

还记得之前为了绕过路径问题吗？CC 手动修改了 `~/Library/LaunchAgents/ai.openclaw.gateway.plist`，它之前把 `ProgramArguments` 指向了 nvm 里的新版二进制，绕开了问题，后来我自己更新 05.22 的时候又踩坑了。

**现象：**

那天我自己用 npm 更新完，运行 `openclaw doctor --fix` 之后，gateway 启动总说配置错误问题。查了下才发现还是 OpenClaw 路径优先找到最早 install.sh 安装的旧版本，导致 doctor 也是旧的，fix 之后的 gateway 也是旧版本，加载新版本配置文件就失败报错了。

```bash
- plugins: Unrecognized key: "bundledDiscovery"
- plugins.allow: plugin not found: minimax
```

**修复方法：**

先按照**坑一**的解决方法，统一安装路径，移除不需要的旧版本二进制文件，删除无效配置，启动新版本 gateway 即可。

```bash
# 删除无效插件配置
openclaw config delete plugins.entries.minimax

# 清理 bundledDiscovery（新版会自动重建）
# 手动编辑 ~/.openclaw/openclaw.json 删除即可
```

---

## 坑四：端口占用 — 旧进程赖着不走

**现象：**

旧版本二进制文件删除，但是启动 gateway 还是报错：

> `Gateway restart failed: Error: gateway port 18789 is still busy`
> `pid 94619 meow: openclaw (127.0.0.1:18789)`

这是因为旧版本 gateway 是 LaunchAgents 启动的，没退出，新服务起不来。macOS 的 `launchctl bootstrap` 不会自动杀旧进程。

**修复方法：**

```bash
# 找到进程号（刚才报错信息里有）
kill 94619
# 或者更彻底
launchctl bootout gui/$UID ~/Library/LaunchAgents/ai.openclaw.gateway.plist
openclaw gateway restart
```

---

## 正确的升级姿势（2026.5.22 及以后）

如果你也经历了 `install.sh` → nvm 的混乱，建议按这个顺序清理：

```bash
# 1. 清理系统全局的旧安装
sudo rm /usr/local/bin/openclaw
sudo rm -rf /usr/local/lib/node_modules/openclaw

# 2. 用 nvm 的 npm 安装最新版
/Users/meow/.nvm/versions/node/v22.22.1/bin/npm install -g openclaw@latest

# 3. 确认版本一致
which openclaw # 应该指向 nvm
openclaw --version # 应该 >= 2026.5.22

# 4. 重装 LaunchAgent（因为二进制路径变了）
openclaw gateway install --force

# 5. 清理无效配置
openclaw doctor --fix

# 6. 重启
openclaw gateway restart
```

---

## 最后

OpenClaw 这一波升级真是折腾的够呛，新特性用不上多少，以后还是稳定养老为主了，05.18 这版本坑太大，这世界就是个巨大的草台班子。🤕🤕🤕
