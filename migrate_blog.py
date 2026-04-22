#!/usr/bin/env python3
"""迁移 Hexo 博客到 Astro Paper"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

HEXO_DIR = Path.home() / "workspace/hexo_blog/source/_posts"
BLOG_DIR = Path.home() / "workspace/stardust-blog/src/data/blog"

def parse_hexo_frontmatter(content: str) -> dict:
    """解析 Hexo frontmatter"""
    frontmatter = {}
    
    # 提取 title
    match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
    if match:
        frontmatter['title'] = match.group(1).strip().strip('"').strip("'")
    
    # 提取 date
    match = re.search(r'^date:\s*(.+)$', content, re.MULTILINE)
    if match:
        date_str = match.group(1).strip()
        try:
            # 尝试解析各种日期格式
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    frontmatter['pubDatetime'] = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
                    break
                except:
                    continue
        except:
            pass
    
    # 提取 categories
    match = re.search(r'^categories:\s*$((?:\s+-\s+.+\n?)+)', content, re.MULTILINE)
    if match:
        cats = re.findall(r'-\s+(.+)', match.group(1))
        frontmatter['categories'] = cats
    
    # 提取 tags
    match = re.search(r'^tags:\s*$((?:\s+-\s+.+\n?)+)', content, re.MULTILINE)
    if match:
        tags = re.findall(r'-\s+(.+)', match.group(1))
        frontmatter['tags'] = tags
    
    # 提取 index_img 作为 heroImage
    match = re.search(r'^index_img:\s*(.+)$', content, re.MULTILINE)
    if match:
        frontmatter['heroImage'] = match.group(1).strip()
    
    return frontmatter

def convert_hexo_to_astropaper(hexo_file: Path) -> str:
    """转换 Hexo 文章到 Astro Paper 格式"""
    content = hexo_file.read_text(encoding='utf-8')
    
    # 分离 frontmatter 和正文
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            hexo_frontmatter = parts[1]
            body = parts[2]
        else:
            hexo_frontmatter = ''
            body = content
    else:
        hexo_frontmatter = ''
        body = content
    
    # 解析 frontmatter
    fm = parse_hexo_frontmatter(hexo_frontmatter)
    
    # 生成 slug
    slug = hexo_file.stem
    
    # 构建新的 frontmatter
    new_fm = []
    new_fm.append('---')
    new_fm.append(f"title: {fm.get('title', slug)}")
    
    if 'pubDatetime' in fm:
        new_fm.append(f"pubDatetime: {fm['pubDatetime']}")
        new_fm.append(f"modDatetime: {fm['pubDatetime']}")
    
    if 'heroImage' in fm:
        new_fm.append(f"heroImage: {fm['heroImage']}")
    
    new_fm.append('draft: false')
    
    if 'tags' in fm and fm['tags']:
        new_fm.append('tags:')
        for tag in fm['tags']:
            new_fm.append(f"  - {tag}")
    
    if 'categories' in fm and fm['categories']:
        new_fm.append('categories:')
        for cat in fm['categories']:
            new_fm.append(f"  - {cat}")
    
    new_fm.append('---')
    new_fm.append('')
    
    # 清理正文中的 Hexo 特定标记
    body = body.strip()
    
    return '\n'.join(new_fm) + body

def main():
    print(f"源目录: {HEXO_DIR}")
    print(f"目标目录: {BLOG_DIR}")
    
    if not HEXO_DIR.exists():
        print(f"错误: 源目录不存在 {HEXO_DIR}")
        return
    
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # 获取所有 md 文件
    md_files = list(HEXO_DIR.glob("*.md"))
    print(f"找到 {len(md_files)} 篇文章")
    
    success = 0
    for hexo_file in md_files:
        try:
            # 转换内容
            new_content = convert_hexo_to_astropaper(hexo_file)
            
            # 生成新文件名
            new_file = BLOG_DIR / hexo_file.name
            
            # 写入
            new_file.write_text(new_content, encoding='utf-8')
            success += 1
            print(f"✓ {hexo_file.name}")
        except Exception as e:
            print(f"✗ {hexo_file.name}: {e}")
    
    print(f"\n完成! 成功迁移 {success}/{len(md_files)} 篇")

if __name__ == '__main__':
    main()
