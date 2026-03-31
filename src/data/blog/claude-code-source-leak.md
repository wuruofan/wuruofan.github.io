---
title: 一次意外的"开源"：Claude Code 源码泄露事件始末
pubDatetime: 2026-03-31T12:00:00Z
modDatetime: 2026-03-31T12:00:00Z
cover: /images/cover-claude-code-leak.jpg
description: 从 Twitter 上的一条动态开始，聊聊 Claude Code 源码泄露事件，以及 Source Map 技术的科普
draft: false
tags:
  - Claude Code
  - AI 编程
  - 开源
  - 技术事件
categories:
  - 技术
---

![封面图](/images/cover-claude-code-leak.jpg)

## Twitter 上的震动

3月31日，Twitter 上有条动态突然引发关注：

> **[@Fried_rice](https://x.com/Fried_rice/status/2038894956459290963)**: "Claude Code 源代码通过 npm 包的 .map 文件泄露了！"

事情经过大概是：Claude Code 发布到 npm 的时候，包里带了一个 `.map` 文件。这个 map 文件是 **Source Map**，用来把压缩混淆后的代码还原成原始 TypeScript，方便调试。

问题出在这个 map 文件指向的路径——它指向了 Anthropic 内部的 R2 存储桶，而这个桶居然是公开可访问的。结果就是：任何人都能下载到完整的原始 TypeScript 源码。

Anthropic 后来把访问权限关掉了，但已经有人把源码扒下来做成了 GitHub 仓库：

👉 https://github.com/instructkr/claude-code

（就在我写这篇公众号文章配图的功夫，这个仓库已经飙到 **1万+ Star** 了 😱😱）

---

## 什么是 Source Map？

前端代码在上线前，通常会被压缩混淆。举个例子，你写的 `function helloWorld()` 压缩后可能变成 `function a()`，读都读不懂。

但这样一来，线上出了 Bug，调试的时候就傻眼了。

**Source Map 就是来解决这个问题的。**

它是一个 `.map` 文件，里面记录着"压缩后的代码"和"原始源码"的对应关系：

![Source Map 原理图](/images/source-map-diagram.png)

```
压缩后的代码 (cli.js)
    ↓
Source Map (cli.js.map)  ← 映射关系
    ↓
原始源码 (TypeScript)
```

现在前端开发工具都支持 Source Map，Chrome DevTools 里可以直接看原始源码调试，就是靠的这个。

---

## 这个仓库里有什么？

仓库 README 写得很清楚：**仅供教育和安全研究使用**。

![Claude Code 目录结构](/images/claude-code-structure.png)

```
src/
├── main.tsx           # 入口，804KB
├── commands/           # 103 个 slash 命令
├── tools/             # ~40 个工具实现
├── components/         # 146 个 UI 组件
├── skills/            # 技能系统
├── plugins/           # 插件系统
└── ...
```

数据：
- 📦 **1884 个 TypeScript 文件**
- 📊 **512,000+ 行代码**
- 🏗️ **完整的前后端架构**

---

## 源码可见 ≠ 源码可用

先说结论：**这不算开源。**

README 明确写了：

> "This repository does not claim ownership of the original code, and it should not be interpreted as an official Anthropic repository."

你拿到了代码，但依然受 Anthropic 的商业条款约束，不能自由使用、修改或分发。

就像你路过工地捡到了一份施工图纸，不代表你有权拿着图纸去盖楼。

---

## 一点思考

我 clone 看了那份源码，Claude Code 的架构确实挺好的，模块化清晰，工具注册、命令注册、插件系统都挺有条理。

左手 OpenClaw，右手 Claude Code，都是值得学习借鉴的榜样。等我的 Gateway + TUI 架构实现完，不知道能达到什么样的效果呢？

不过有一点可以肯定：**一个月内，国产 Trae、CodeBuddy 之类的编程工具一定会突飞猛进**。

我们一直说 Claude Code 是业内最强，但当 Agent 能力平权之后，Opus 模型和国产模型的差距到底如何？值得持续跟进关注。

---

## 最后的最后

小黑整理完文章准备截图的时候，发！现！[instructkr/claude-code](https://github.com/instructkr/claude-code) 已经变了，变成 **Claude Code Python Porting** 了！还好当时赶紧 fork + clone 了一份！

---

好了，今天就聊这么多。

下次再见(¯▽¯)/~~

---

**吴小黑♠️ with 尾酱🦊 ✨**
