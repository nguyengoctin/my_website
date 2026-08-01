#!/usr/bin/env python3
"""
Order all AI Engineer Roadmap lessons sequentially by Chapter (01 -> 12).
Update weight, prev/next links in Front Matter AND minimalist bottom navigation.
"""

import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_DIR, ".roadmap-data", "all_nodes.json")
CONTENT_DIR = os.path.join(PROJECT_DIR, "content", "ai-engineer")

# Chapters in exact chronological roadmap order
CHAPTER_ORDER = [
    '01-introduction',
    '02-llm-fundamentals',
    '03-prompt-engineering',
    '04-rag-and-vector-databases',
    '05-fine-tuning',
    '06-ai-agents',
    '07-model-context-protocol-mcp',
    '08-multimodal-ai',
    '09-frameworks-and-tools',
    '10-models-and-apis',
    '11-evaluation-safety-and-ethics',
    '12-applications-and-usecases'
]


def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        nodes = json.load(f)

    # Group and order nodes chapter by chapter
    seen_paths = set()
    ordered_lessons = []

    for c in CHAPTER_ORDER:
        cat_nodes = [n for n in nodes if n.get('category') == c]
        for n in cat_nodes:
            slug = n.get('slug', '')
            file_path = os.path.join(CONTENT_DIR, c, f"{slug}.md")
            if os.path.exists(file_path) and file_path not in seen_paths:
                seen_paths.add(file_path)
                ordered_lessons.append({
                    'label': n.get('label', ''),
                    'cat': c,
                    'slug': slug,
                    'path': file_path,
                    'link': f"/ai-engineer/{c}/{slug}/"
                })

    print(f"Processing {len(ordered_lessons)} lessons in exact Chapter sequence (01 -> 12)...")

    # Update each lesson with correct sequential navigation
    for i, lesson in enumerate(ordered_lessons):
        weight = i + 1
        prev_item = ordered_lessons[i-1] if i > 0 else None
        next_item = ordered_lessons[i+1] if i < len(ordered_lessons) - 1 else None

        with open(lesson['path'], 'r', encoding='utf-8') as f:
            content = f.read()

        # Clean existing bottom navigation text if present
        if '\n---\n\n[←' in content or '\n---\n\n[AI Engineer Roadmap]' in content:
            content = content.split('\n---\n\n[←')[0].split('\n---\n\n[AI Engineer Roadmap]')[0].strip()

        # Build minimalist text navigation line
        parts = []
        if prev_item:
            parts.append(f"[← {prev_item['label']}]({prev_item['link']})")
        parts.append("[AI Engineer Roadmap](/ai-engineer/)")
        if next_item:
            parts.append(f"[{next_item['label']} →]({next_item['link']})")

        nav_line = " · ".join(parts)
        nav_block = f"\n\n---\n\n{nav_line}\n"

        # Update Front Matter fields
        prev_link = prev_item['link'] if prev_item else ""
        next_link = next_item['link'] if next_item else ""

        # Update weight
        if 'weight:' not in content:
            content = re.sub(r'^(date:\s*[^\n]+)', r'\1\nweight: ' + str(weight), content, flags=re.MULTILINE)
        else:
            content = re.sub(r'^weight:\s*\d+', f'weight: {weight}', content, flags=re.MULTILINE)

        # Update prev link
        if 'prev:' not in content and prev_link:
            content = re.sub(r'^(weight:\s*\d+)', r'\1\nprev: "' + prev_link + '"', content, flags=re.MULTILINE)
        elif prev_link:
            content = re.sub(r'^prev:\s*"[^"]*"', f'prev: "{prev_link}"', content, flags=re.MULTILINE)
        elif not prev_link and 'prev:' in content:
            content = re.sub(r'^prev:\s*"[^"]*"\n?', '', content, flags=re.MULTILINE)

        # Update next link
        if 'next:' not in content and next_link:
            content = re.sub(r'^(weight:\s*\d+)', r'\1\nnext: "' + next_link + '"', content, flags=re.MULTILINE)
        elif next_link:
            content = re.sub(r'^next:\s*"[^"]*"', f'next: "{next_link}"', content, flags=re.MULTILINE)
        elif not next_link and 'next:' in content:
            content = re.sub(r'^next:\s*"[^"]*"\n?', '', content, flags=re.MULTILINE)

        final_content = content.strip() + nav_block

        with open(lesson['path'], 'w', encoding='utf-8') as f:
            f.write(final_content)

    print(f"Successfully applied Chapter-by-Chapter sequential navigation to {len(ordered_lessons)} lesson files!")


if __name__ == '__main__':
    main()
