#!/usr/bin/env python3
"""
Minimalist navigation script: only appends text links after ## References without breaking front matter.
"""

import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_DIR, ".roadmap-data", "all_nodes.json")
CONTENT_DIR = os.path.join(PROJECT_DIR, "content", "ai-engineer")


def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        nodes = json.load(f)

    lessons = []
    for node in nodes:
        cat = node.get('category', '01-introduction')
        slug = node.get('slug', '')
        label = node.get('label', '')
        file_path = os.path.join(CONTENT_DIR, cat, f"{slug}.md")
        rel_link = f"/ai-engineer/{cat}/{slug}/"
        
        if os.path.exists(file_path):
            lessons.append({
                'label': label,
                'cat': cat,
                'slug': slug,
                'path': file_path,
                'link': rel_link
            })

    for i, lesson in enumerate(lessons):
        weight = i + 1
        prev_item = lessons[i-1] if i > 0 else None
        next_item = lessons[i+1] if i < len(lessons) - 1 else None

        with open(lesson['path'], 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove previous nav block (anything after the last \n---\n following References or nav)
        # Split content into body and existing nav
        if '\n---\n\n[←' in content or '\n---\n\n|' in content or '\n---\n\n## 🧭' in content:
            content = content.split('\n---\n\n[←')[0].split('\n---\n\n|')[0].split('\n---\n\n## 🧭')[0].strip()

        # Build minimalist text navigation link line
        parts = []
        if prev_item:
            parts.append(f"[← {prev_item['label']}]({prev_item['link']})")
        parts.append("[AI Engineer Roadmap](/ai-engineer/)")
        if next_item:
            parts.append(f"[{next_item['label']} →]({next_item['link']})")

        nav_line = " · ".join(parts)

        nav_block = f"""

---

{nav_line}
"""

        # Update Front Matter
        prev_link = prev_item['link'] if prev_item else ""
        next_link = next_item['link'] if next_item else ""

        if 'weight:' not in content:
            content = re.sub(r'^(date:\s*[^\n]+)', r'\1\nweight: ' + str(weight), content, flags=re.MULTILINE)
        else:
            content = re.sub(r'^weight:\s*\d+', f'weight: {weight}', content, flags=re.MULTILINE)

        if 'prev:' not in content and prev_link:
            content = re.sub(r'^(weight:\s*\d+)', r'\1\nprev: "' + prev_link + '"', content, flags=re.MULTILINE)
        elif prev_link:
            content = re.sub(r'^prev:\s*"[^"]*"', f'prev: "{prev_link}"', content, flags=re.MULTILINE)

        if 'next:' not in content and next_link:
            content = re.sub(r'^(weight:\s*\d+)', r'\1\nnext: "' + next_link + '"', content, flags=re.MULTILINE)
        elif next_link:
            content = re.sub(r'^next:\s*"[^"]*"', f'next: "{next_link}"', content, flags=re.MULTILINE)

        final_content = content.strip() + nav_block

        with open(lesson['path'], 'w', encoding='utf-8') as f:
            f.write(final_content)

    print(f"Minimalist navigation applied to {len(lessons)} lessons.")


if __name__ == '__main__':
    main()
