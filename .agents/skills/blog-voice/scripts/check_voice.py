#!/usr/bin/env python3
"""blog-voice 的机械门禁：只报告，不改稿。

用法：
    python3 check_voice.py src/data/blog/<新文>.md
    python3 check_voice.py src/data/blog/<新文>.md --base <旧稿.md>
    python3 check_voice.py --corpus            # 复算 SKILL.md 里的统计口径

检查项：
  1. frontmatter 是否齐全（title / description / pubDatetime）
  2. 段落长度：中位数是否 40–110，>180 字的段落占比
  3. 独占行加粗：是否 ≤8 字 + 冒号的标签；成串的论点句直接判错
  4. emoji：是否在语料白名单内，连写是否 >6
  5. 语料 0 次的词
  6. --base：数字与行内代码片段是否被改动
"""

import argparse
import glob
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
CORPUS_GLOB = str(REPO / "src/data/blog/*.md")

EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2705\u26A0\u2728\u274C\u2757\u2753\u2B50\u2764]\uFE0F?")
BOLD_ONLY = re.compile(r"^\*\*([^*]+)\*\*$")
# 「**把任务派出去。**」这一类：短、单句、句号收尾的独占行加粗
BOLD_SLOGAN = re.compile(r"^\*\*([^，。；：,.;:]{2,20})。\*\*$")
INLINE_CODE = re.compile(r"`[^`\n]+`")
NUMBER = re.compile(r"\d+(?:\.\d+)?(?:%|MB|GB|KB|M|K)?")
LABEL_HINTS = ("现象", "原因", "修复", "影响", "结局", "目标", "现状", "约束", "验收", "结论")

# 语料 0 次，用了就是「像但不是」
BANNED = ["白嫖", "卧槽", "牛逼", "手动挡", "综上所述", "赋能", "抓手", "本质就一件事"]
# 语料里只有 1 次，别当常用词
RARE = {"说白了": 1, "闭环": 1, "一坨": 1, "要老命": 1, "拉完了": 2}


def split_frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    return {"raw": m.group(1)}, text[m.end():]


def body_paragraphs(body):
    """只取正文段落：跳过标题、列表、代码、引用、表格、图片、HTML。

    markdown 行尾双空格是硬换行，旧文里等于分段，先归一成空行再切。
    """
    body = re.sub(r"[ \t]{2,}\n", "\n\n", body)
    out = []
    for block in re.split(r"\n\s*\n", body):
        p = block.strip()
        if not p:
            continue
        if p.startswith(("#", "-", "*", ">", "|", "`", "![", "<", "---")) or re.match(r"^\d+\.", p):
            continue
        out.append(p)
    return out


def char_len(p):
    s = re.sub(r"[*`\[\]()!|]", "", p).replace("\n", "")
    return len(s)


_CACHE = {}


def corpus_stats():
    if "stats" in _CACHE:
        return _CACHE["stats"]
    files = sorted(glob.glob(CORPUS_GLOB))
    if not files:
        sys.exit(f"找不到语料：{CORPUS_GLOB}")
    emo = Counter()
    per_file = []
    anchors = Counter()
    for f in files:
        text = Path(f).read_text(encoding="utf-8")
        _, body = split_frontmatter(text)
        clean = re.sub(r"```.*?```", "", text, flags=re.S)
        for m in EMOJI.finditer(clean):
            emo[m.group()] += 1
        for line in body.split("\n"):
            m = BOLD_ONLY.match(line.strip())
            if m:
                anchors[m.group(1)] += 1
        lens = [char_len(p) for p in body_paragraphs(body)]
        if lens:
            per_file.append((Path(f).name, round(statistics.mean(lens), 1), statistics.median(lens), len(lens)))
    allv = sorted(char_len(p) for f in files for p in body_paragraphs(split_frontmatter(Path(f).read_text(encoding="utf-8"))[1]))
    _CACHE["stats"] = (files, emo, per_file, anchors, allv)
    return _CACHE["stats"]


def check(path, base=None):
    text = Path(path).read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    problems, warnings = [], []

    # 1. frontmatter
    raw = fm.get("raw", "")
    if not raw:
        problems.append("没有 frontmatter")
    for key in ("title", "description", "pubDatetime"):
        if not re.search(rf"^{key}:", raw, re.M):
            problems.append(f"frontmatter 缺 {key}")

    # 2. 段落
    paras = body_paragraphs(body)
    lens = [char_len(p) for p in paras]
    if lens:
        med = statistics.median(lens)
        long = [(char_len(p), p[:40].replace("\n", " ")) for p in paras if char_len(p) > 180]
        print(f"段落：{len(lens)} 段，中位数 {med} 字，均值 {round(statistics.mean(lens), 1)}，最长 {max(lens)}")
        if not 40 <= med <= 110:
            warnings.append(f"段落中位数 {med}，语料区间是 40–110")
        if len(long) / len(lens) > 0.25:
            problems.append(f">180 字的段落 {len(long)}/{len(lens)}，超过 25%（样本中位 3%，命令密集的操作文能到 21%）")
        for n, head in long:
            warnings.append(f"超长段（{n} 字）：{head}…")
    else:
        warnings.append("没解析出正文段落")

    # 3. 独占行加粗：标签可以，短句口号成串判错
    bold_lines, slogans = [], []
    for i, line in enumerate(body.split("\n"), 1):
        s = line.strip()
        m = BOLD_ONLY.match(s)
        if m:
            bold_lines.append((i, m.group(1).strip()))
        if BOLD_SLOGAN.match(s):
            slogans.append((i, BOLD_SLOGAN.match(s).group(1)))
    print(f"独占行加粗：{len(bold_lines)} 行，其中短句口号 {len(slogans)}")
    if len(slogans) >= 3:
        problems.append(
            f"短句口号独占行成串（{len(slogans)} 处），这是排比加粗小标题："
            + "；".join(f"L{i}:{t[:14]}" for i, t in slogans[:4])
        )
    elif slogans:
        warnings.append(f"短句口号独占行 L{slogans[0][0]}：{slogans[0][1][:20]}（1–2 处可接受）")
    for i, label in bold_lines:
        if len(label) > 10 and not any(h in label for h in LABEL_HINTS) and not EMOJI.search(label):
            warnings.append(f"长句独占行加粗 L{i}：{label[:20]}…（确认它是标签，不是论点）")

    # 4. emoji
    files, emo, _, _, _ = corpus_stats()
    clean = re.sub(r"```.*?```", "", body, flags=re.S)
    used = Counter(m.group() for m in EMOJI.finditer(clean))
    if used:
        unknown = {k: v for k, v in used.items() if k not in emo}
        print("emoji：" + "、".join(f"{k}{v}" for k, v in used.most_common()))
        if unknown:
            problems.append("语料里没出现过的 emoji：" + "、".join(unknown))
        for m in re.finditer(r"(?:[\U0001F000-\U0001FAFF\u2600-\u27BF]){7,}", clean):
            problems.append(f"emoji 连写超过 6 个：{m.group()}")
    else:
        print("emoji：0")

    # 5. 禁用词
    for w in BANNED:
        if w in body:
            problems.append(f"语料 0 次的词：{w}")
    for w, cap in RARE.items():
        n = body.count(w)
        if n > max(cap * 2, 2):
            warnings.append(f"「{w}」语料全文仅 {cap} 次，这篇用了 {n} 次")

    # 6. 与旧稿对比
    if base:
        old = Path(base).read_text(encoding="utf-8")
        _, old_body = split_frontmatter(old)
        old_nums = Counter(NUMBER.findall(old_body))
        new_nums = Counter(NUMBER.findall(body))
        lost = old_nums - new_nums
        added = new_nums - old_nums
        old_code = set(INLINE_CODE.findall(old_body))
        new_code = set(INLINE_CODE.findall(body))
        if lost:
            problems.append("数字被改动或消失：" + "、".join(f"{k}×{v}" for k, v in lost.items()))
        if added:
            warnings.append("新增数字（确认不是编的）：" + "、".join(f"{k}×{v}" for k, v in added.items()))
        if old_code - new_code:
            problems.append("行内代码片段消失：" + "、".join(sorted(old_code - new_code)[:5]))
        if new_code - old_code:
            warnings.append("新增行内代码：" + "、".join(sorted(new_code - old_code)[:5]))

    print()
    for w in warnings:
        print(f"  warn  {w}")
    for p in problems:
        print(f"  FAIL  {p}")
    if not problems:
        print("  门禁通过（剩下的人工四项见 SKILL.md）")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--base", help="改写前的旧稿，用于比对数字与代码片段")
    ap.add_argument("--corpus", action="store_true", help="打印语料统计")
    a = ap.parse_args()

    if a.corpus:
        files, emo, per_file, anchors, allv = corpus_stats()
        print(f"语料：{len(files)} 篇")
        print("emoji：" + "、".join(f"{k}{v}" for k, v in emo.most_common(18)))
        print(f"\n段落（中文字符，正文段）：p10={allv[len(allv)//10]} p50={allv[len(allv)//2]} p90={allv[9*len(allv)//10]} n={len(allv)}")
        print("\n各篇段落 均值/中位数/段数：")
        for name, mean, med, n in per_file:
            print(f"  {name[:46]:48s} {mean:>6} / {med:>4} / {n}")
        print("\n独占行加粗 top：")
        for k, v in anchors.most_common(12):
            print(f"  {k[:20]:22s} {v}")
        return 0

    if not a.file:
        sys.exit("给个文件，或用 --corpus")
    return check(a.file, a.base)


if __name__ == "__main__":
    sys.exit(main())
