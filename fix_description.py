#!/usr/bin/env python3
"""批量添加 description 到博客文章"""

import re
from pathlib import Path

BLOG_DIR = Path(__file__).parent / "src/data/blog"

def add_description(file_path: Path):
    content = file_path.read_text(encoding='utf-8')
    
    # 检查是否已有 description
    if re.search(r'^description:', content, re.MULTILINE):
        return False
    
    # 提取标题
    match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
    title = match.group(1).strip() if match else "文章"
    
    # 在 heroImage 后添加 description，如果没有 heroImage 就在 title 后添加
    if re.search(r'^heroImage:', content, re.MULTILINE):
        content = re.sub(
            r'^(heroImage:.+)$',
            r'\1\ndescription: ' + title,
            content,
            flags=re.MULTILINE
        )
    else:
        content = re.sub(
            r'^(title:.+)$',
            r'\1\ndescription: ' + title,
            content,
            flags=re.MULTILINE
        )
    
    file_path.write_text(content, encoding='utf-8')
    return True

def main():
    count = 0
    for md_file in BLOG_DIR.glob("*.md"):
        if add_description(md_file):
            print(f"Fixed: {md_file.name}")
            count += 1
    print(f"\nDone! Fixed {count} files.")

if __name__ == '__main__':
    main()
