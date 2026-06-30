---
title: 踩坑记录｜被 A 畜 Claude Code 气到心塞
pubDatetime: 2026-06-27T15:30:00Z
modDatetime: 2026-06-27T16:00:00Z
cover: /images/cover-claude-code-2-1-186-billing-pitfall.png
description: Claude Code v2.1.186 的 first-party auth gate 导致
  auto-compact 对三方 API 失效，我的 MiniMax 1M 上下文会话
  一路涨到 2.4M tokens，5 小时额度直接爆掉。
draft: false
tags:
  - OpenClaw
  - Claude Code
  - minimax
  - 踩坑记录
  - 草台
  - 反向工程
categories:
  - 随笔
---

> 我这两天快被气死，Anthropic A 畜的名号果然名不虚传。
> Claude Code 请不要升级到 v2.1.150 以上！！第三方 API 自动压缩会失效！！

事情的背景是最近两天 MiniMax M3 正式上线了 1M 上下文，之前都是 512K 上下文接口，1M 的计费要比 512K 贵一倍，而碰巧的是我这两天又把一直用的 cc-connect 和 claude code 都给更新了，悲剧就发生了。

## 奇怪的 token 消耗变快

cc-connect 是一个可以把本地 agent 消息转发到飞书或者微信会话的本地服务，配合 cc 这个组合我用了很久了一直没问题，直到昨天早上，我发现 token 消耗的变快很多，一个任务 5 小时限额就耗完了。

一开始我只是以为是 M3 1M 上下文上线导致的，看了飞书里返回的上下文百分比信息，大概都是 53%\~57%，就很亏，于是检查了 cc-connect 环境变量的配置，限制了 cc 的最大 context 512K 和自动压缩比例 80%。

可下午实践了下感觉还是消耗快，翻了下 cc-connect 的消息，没有看到自动压缩相关信息。我以为是 M3 API 兼容性有问题，不认 cc 最大 context 的设置项还是按 1M 上下文去处理，只好限制 40% 自动压缩。

## 悲剧上演

![minimax 账单 5h 限额 + 飞书 429 报错](/images/claude-code-2-1-186-billing-screenshot.jpg)
*左：minimax 套餐页面，5h 限额 + 7778 赠送积分；右：cc-connect 飞书，Claude Code 报 429 · ctx 100%*

我昨晚 23 点零几分用 cc-connect 给 claude code 下了个不复杂的任务，那时候我看了眼网站上套餐用量，还剩 80%呢，我想着肯定没问题，就让 cc 去调研一个功能，顺便再验证下 40%自动压缩是否生效。

结果半个小时之后，我就傻眼了，任务没完成，告诉我 "API Error: Request rejected (429)．已达到 Token Plan 用量上限：请升级 Token Plan 套餐或购买积分补充用量。(2056)"，我一查网站，5 小时限额冲爆，而且 7778 积分也花完了。😱😱😲😲😲😲

## 真相只有一个

熬过 12 点额度重置之后，让我的 openclaw 帮我定位下原因，尾酱🦊翻了下日志，发现 23:44:02 停止的那次运行 turn，输入 input 2.4M，远超 M3 1M 上下文限制！！shit！

![cc-connect 飞书 429 错误卡片，关键数字已用粉色框线标注](/images/claude-code-2-1-186-cc-error-annotated.jpg)
*cc-connect 飞书：Claude Code 报 429 · ctx 100% · cache_read 635K · output 42K*

```
input_tokens = 2,425,177 - 2.4M!
output_tokens = 42,043
turn_duration=35m21s
tools = 175
```

现在该配置的都配置了，尾酱🦊说检查了进程 cc-connect 的环境变量生效了，但是 cc 没处理！

查了一圈，终于找到了原因，A 畜果然是 A 畜！早该就应该怀疑是它的问题！

[GitHub Issue #6558](https://github.com/anthropics/claude-code/issues/65585) 说的很详细， "Auto-compact stopped working for third-party API providers since v2.1.161"，从 v2.1.161 起，Anthropic 在 auto-compact 链路中加了一个 first-party auth gate，导致三方 API 用户 auto-compact 永远不会触发。

```
ANTHROPIC_BASE_URL != api.anthropic.com
 → Z7() = false (not firstParty)
 → dGL() = true → LC() = true → Au() = false
 → GrowthBook 不可用
 → tengu_sepia_moth feature flag 返回默认值 false
 → auto-compact 永远不触发
```

说实话，这个 gate 位置加得太故意了——专门把第三方 provider 的自动压缩功能关掉。isFirstPartyAnthropicBaseUrl() 这个检查完全没有任何技术必要性，显然就是有意为之。

## 更多线索

按 issue 作者所说 150 版本还是好的，但我公司电脑 claude code 版本号 159，还是可以自动压缩的，跑了下逆向，果然又发现了些线索：

代码里能找到"Autocompact buffer"字符串，说明自动压缩功能本身还在；与此同时， 完整的 GrowthBook 系统（用于区分和第一方和第三方接口的代码）在 159 中也已存在，例如
isGrowthBookEnabled 、initializeGrowthBook、refreshGrowthBookFeatures 等完整 GrowthBook 链路，以及 isLegacyOpusFirstParty、firstPartyNameToCanonical、preferThirdPartyAuthentication 等类型检查方法。

但是真正导致 auto compact 功能失效的 tengu_sepia_moth feature 判断标志 flag 在 159 中完全不存在，其他 tengu_\* flags 倒是很丰富（如 tengu_velvet_moth、tengu_dunw ich_bell 等）。

简单来说，目前的逆向结果表明，150\~159 版本自动压缩直接触发，三方 API 正常用，161 之后，自动压缩被"开关化"了，三方 API 用户被直接排除。

这就说明一件事，A 畜并不是"不小心弄坏了"，而是主动把自动压缩从基础功能降级成了"官方专属功能"。💩💩💩

## 坑中之坑

![狐狸沮丧地看着燃烧的 2.4M tokens 账单](/images/claude-code-2-1-186-fox-sad-2-4m.png)
*降级到 v2.1.150 后，旧 session 还在——任何操作都会把 7.44MB 整个 context 喂给 minimax，账单继续爆*

于是我果断降级到 150 版本，你以为这样就完了？当我后面想再次继续之前那个任务的时候，另一个坑出现了。

由于之前是报错中断了，不确定任务进行到什么地步，我尝试 cc-connect 选中之前那个会话，发送"继续"，结果发现没有处理压缩，赶紧 `/stop`，执行 `/compact`，提示"没有活跃的会话可以压缩。请先发送一条消息。"

我于是又发了一条消息"继续，先压缩"，这个时候我反应过来不对劲了，赶紧停止，一看帐单，两条消息就把 5 小时额度干到 64%了。

其实我应该能想到的，compact 压缩上下文这件事情其实是 agent 工具管理会话的一部分，需要 agent 工具自己主动的去调用 API 总结历史消息，把总结结果代替之前的消息发送给 LLM API，而我那个 186 版本创建的超大会话文件中，根本没有 summary 总结信息，所以无论哪个版本的 cc 都会把整个文件作为输入传给 MiniMax 的 API，这是一个无解的死局了。🌚🌚🌚

我让尾酱🦊帮我再次调查了下，果然，那个会话文件 7.44MB 大小，任何"加载＋发送"都会把整个上下文当 input 吐给 minimax，而且我严重怀疑 MiniMax 草台班子的 API 就是按 input 去算计费的，而不是按实际能处理的 1M 去计费。😮‍💨😮‍💨😮‍💨

## 最后

唉，反正一坑接一坑，最后我让尾酱🦊把历史两个超大会话备份之后清除了，同时也清除了 cc-connect 的历史记录，世界终于又恢复和平了。

折腾了两天，浪费了好些 token，也算是对 cc 的会话存储有了进一步的理解，当然理解更深的还是 A 畜这个公司的本性。🤬🤬🤬

还得加把劲，我的 motelet agent 还差一些才能用。💪⛽️

最后的最后，重要事情说三遍，**不要升级Claude Code！不要升级Claude Code！不要升级Claude Code！**

## 推荐操作

### 1. 锁版本

```bash
npm install -g @anthropic-ai/claude-code@2.1.150
```

⚠️ 注意全局 npm 安装路径：`source ~/.nvm/nvm.sh && nvm use` 之后再装，避免装到 `/usr/local/lib` 和 `.nvm/.../lib` 分裂。

### 2. 加配置

编辑 `~/.claude/settings.json`：

```json
{
  "env": {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "40",
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=40`：40% 触发自动压缩，三方 API 也能生效
- `DISABLE_AUTOUPDATER=1`：v2.1.150 才识别的环境变量，阻止 cc 自己偷偷升级回坏版本

### 3. 删旧大 session

如果之前 v2.1.186 留下了超大的 session jsonl（>5MB），建议直接删掉，不然降级后任何操作都会把整个 context 喂给 API 继续爆账单。`~/.claude/projects/` 下找 `*.jsonl` 文件按大小排，大的直接砍。
