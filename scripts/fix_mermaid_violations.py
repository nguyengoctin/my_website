#!/usr/bin/env python3
"""
Audit và fix toàn bộ vi phạm Mermaid best-practice:
1. EMPTY_LINES: Xóa dòng trống cuối mỗi khối Mermaid (trước ```)
2. AMPERSAND: Thay & -> và trong node labels
"""
import re
import os

POSTS_DIR = "content/posts"
DRY_RUN = True  # Set False để thực sự sửa

# Thống kê
stats = {"files_fixed": 0, "empty_lines_removed": 0, "amp_fixed": 0}


def fix_mermaid_block(block_content: str) -> tuple[str, int, int]:
    """
    Fix một khối Mermaid:
    - Xóa dòng trống ở cuối block (trailing empty lines)
    - Thay & -> và trong toàn block
    Returns: (fixed_content, empty_lines_removed, amp_fixed)
    """
    empty_removed = 0
    amp_fixed = 0

    # Split thành lines
    lines = block_content.split("\n")

    # Xóa trailing empty lines (dòng trống cuối block)
    while lines and lines[-1].strip() == "":
        lines.pop()
        empty_removed += 1

    # Thay & -> và trong node labels (chỉ trong labels, không phải comments)
    # & trong Mermaid chỉ xuất hiện trong node label "[...]" hoặc "{...}"
    fixed_lines = []
    for line in lines:
        # Chỉ thay & bên trong cặp ["..."] hoặc {...} - không thay & trong comments %% 
        if "%" not in line and "&" in line:
            fixed_line = line.replace(" & ", " và ")
            if fixed_line != line:
                amp_fixed += 1
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)

    return "\n".join(fixed_lines), empty_removed, amp_fixed


def fix_file(filepath: str) -> dict:
    """Fix một file Markdown, trả về thống kê."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    result = {"empty_removed": 0, "amp_fixed": 0, "blocks_fixed": 0}
    new_content = content
    offset = 0

    # Tìm tất cả khối mermaid
    pattern = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)

    for match in pattern.finditer(content):
        block_inner = match.group(1)
        fixed_inner, empty_rm, amp_fix = fix_mermaid_block(block_inner)

        if fixed_inner != block_inner:
            # Thay thế trong new_content
            original_block = f"```mermaid\n{block_inner}```"
            fixed_block = f"```mermaid\n{fixed_inner}\n```"

            # Tìm và thay trong new_content (chỉ lần đầu để tránh collision)
            new_content = new_content.replace(original_block, fixed_block, 1)

            result["empty_removed"] += empty_rm
            result["amp_fixed"] += amp_fix
            if empty_rm > 0 or amp_fix > 0:
                result["blocks_fixed"] += 1

    if new_content != content:
        if not DRY_RUN:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
        return result
    return result


def main():
    print(f"{'DRY RUN' if DRY_RUN else 'LIVE RUN'} — Mermaid Best Practice Fixer")
    print("=" * 60)

    for fname in sorted(os.listdir(POSTS_DIR)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(POSTS_DIR, fname)

        with open(fpath, "r") as f:
            content = f.read()

        # Quick check: has mermaid?
        if "```mermaid" not in content:
            continue

        result = fix_file(fpath)

        if result["blocks_fixed"] > 0 or result["empty_removed"] > 0 or result["amp_fixed"] > 0:
            print(f"\n[{fname}]")
            print(f"  Blocks fixed: {result['blocks_fixed']}")
            print(f"  Empty lines removed: {result['empty_removed']}")
            print(f"  Ampersands fixed: {result['amp_fixed']}")
            stats["files_fixed"] += 1
            stats["empty_lines_removed"] += result["empty_removed"]
            stats["amp_fixed"] += result["amp_fixed"]

    print("\n" + "=" * 60)
    print(f"TOTAL FILES FIXED: {stats['files_fixed']}")
    print(f"TOTAL EMPTY LINES REMOVED: {stats['empty_lines_removed']}")
    print(f"TOTAL AMPERSANDS FIXED: {stats['amp_fixed']}")

    if DRY_RUN:
        print("\n⚠️  DRY RUN — no files modified. Set DRY_RUN=False to apply.")


if __name__ == "__main__":
    main()
