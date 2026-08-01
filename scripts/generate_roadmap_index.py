#!/usr/bin/env python3
"""
Generate Hugo section index files (_index.md) for the AI Engineer Roadmap.
Sequenced by Chapter 01 to 12. Clean header (no duplicate H1 in markdown body).
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_DIR, ".roadmap-data", "all_nodes.json")
CONTENT_DIR = os.path.join(PROJECT_DIR, "content", "ai-engineer")

CHAPTER_TITLES = {
    "01-introduction": "01. Introduction",
    "02-llm-fundamentals": "02. LLM Fundamentals",
    "03-prompt-engineering": "03. Prompt Engineering",
    "04-rag-and-vector-databases": "04. RAG & Vector Databases",
    "05-fine-tuning": "05. Fine-Tuning",
    "06-ai-agents": "06. AI Agents",
    "07-model-context-protocol-mcp": "07. Model Context Protocol (MCP)",
    "08-multimodal-ai": "08. Multimodal AI",
    "09-frameworks-and-tools": "09. Frameworks & Tools",
    "10-models-and-apis": "10. Models & APIs",
    "11-evaluation-safety-and-ethics": "11. Evaluation, Safety & Ethics",
    "12-applications-and-usecases": "12. Applications & Use Cases",
}

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        nodes = json.load(f)

    categories = {cat: [] for cat in CHAPTER_TITLES.keys()}

    seen_paths = set()
    for cat in CHAPTER_TITLES.keys():
        cat_nodes = [n for n in nodes if n.get('category') == cat]
        for node in cat_nodes:
            slug = node.get('slug', '')
            file_path = os.path.join(CONTENT_DIR, cat, f"{slug}.md")
            if os.path.exists(file_path) and file_path not in seen_paths:
                seen_paths.add(file_path)
                categories[cat].append({
                    'label': node.get('label', ''),
                    'slug': slug,
                    'link': f"/ai-engineer/{cat}/{slug}/"
                })

    # Master Index - Note: No H1 header in body because Hugo layout renders .Title in page header
    master_index_content = """---
title: "AI Engineer Roadmap"
description: "Lộ trình học tập AI Engineer năm 2026 với 174 bài học được phân đoạn song ngữ Anh - Việt."
slug: "ai-engineer"
date: 2026-08-01
draft: false

categories:
  - AI Engineer

toc: true
math: false
mermaid: false
---

Lộ trình học tập AI Engineer được phân chia theo 12 chuyên mục:

"""

    for cat_slug, cat_title in CHAPTER_TITLES.items():
        cat_nodes = categories.get(cat_slug, [])
        if not cat_nodes:
            continue
            
        master_index_content += f"## {cat_title}\n\n"
        for item in cat_nodes:
            master_index_content += f"- [{item['label']}]({item['link']})\n"
        master_index_content += "\n"

    master_index_path = os.path.join(CONTENT_DIR, "_index.md")
    with open(master_index_path, 'w', encoding='utf-8') as f:
        f.write(master_index_content)
    print("Updated Master Index (No duplicate H1 header).")

    # Category-level _index.md
    for cat_slug, cat_title in CHAPTER_TITLES.items():
        cat_nodes = categories.get(cat_slug, [])
        cat_dir = os.path.join(CONTENT_DIR, cat_slug)
        os.makedirs(cat_dir, exist_ok=True)
        
        cat_index_path = os.path.join(cat_dir, "_index.md")
        cat_content = f"""---
title: "{cat_title}"
description: "Các bài học thuộc chuyên mục {cat_title}."
date: 2026-08-01
draft: false

categories:
  - AI Engineer

toc: true
---

"""
        for item in cat_nodes:
            cat_content += f"- [{item['label']}]({item['link']})\n"

        with open(cat_index_path, 'w', encoding='utf-8') as f:
            f.write(cat_content)

if __name__ == '__main__':
    main()
