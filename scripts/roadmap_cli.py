#!/usr/bin/env python3
"""
Generic Roadmap Automation CLI Tool (roadmap_cli.py)
Automates fetching, bilingual LLM chunking, indexing, and navigation
for ANY roadmap on roadmap.sh (e.g. backend, ai-engineer, devops, frontend).

Usage:
  python3 scripts/roadmap_cli.py fetch --slug backend
  python3 scripts/roadmap_cli.py process --slug backend --batch 1
  python3 scripts/roadmap_cli.py generate-index --slug backend
  python3 scripts/roadmap_cli.py add-navigation --slug backend
  python3 scripts/roadmap_cli.py run-all --slug backend
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
BASE_URL = "https://roadmap.sh"


def load_env():
    """Load environment variables from .env file."""
    env_vars = {}
    env_path = os.path.join(PROJECT_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"\'')
    return env_vars


_env = load_env()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or _env.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL") or _env.get("GEMINI_MODEL", "gemini-3.1-flash-lite")


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def fetch_json(url, retries=3, delay=1.5):
    """Fetch JSON from URL with retries."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; roadmap-fetcher/1.0)",
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"  Attempt {attempt+1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
    return None


def fetch_roadmap(slug):
    """Fetch all roadmap node data and group into chapters."""
    output_dir = os.path.join(PROJECT_DIR, ".roadmap-data", slug)
    os.makedirs(output_dir, exist_ok=True)

    print(f"=== FETCHING ROADMAP: {slug} ===")
    url = f"{BASE_URL}/{slug}.json"
    data = fetch_json(url)
    if not data:
        print(f"ERROR: Failed to fetch {url}")
        sys.exit(1)

    nodes = [n for n in data.get("nodes", []) if n.get("type") in ("topic", "subtopic")]
    sorted_nodes = sorted(
        nodes,
        key=lambda n: (
            n.get("position", {}).get("y", 0),
            n.get("position", {}).get("x", 0),
        ),
    )

    # Dynamic categorization algorithm
    # Custom category map file if provided: .roadmap-data/{slug}_categories.json
    custom_map_file = os.path.join(PROJECT_DIR, ".roadmap-data", f"{slug}_categories.json")
    custom_map = {}
    if os.path.exists(custom_map_file):
        with open(custom_map_file, "r", encoding="utf-8") as f:
            custom_map = json.load(f)

    chapter_idx = 0
    current_cat_dir = "01-general"
    category_titles = {}

    for n in sorted_nodes:
        ntype = n.get("type")
        label = n.get("data", {}).get("label", "").strip()

        if label in custom_map:
            n["category"] = custom_map[label]
        elif ntype == "topic":
            chapter_idx += 1
            cat_slug = slugify(label)
            current_cat_dir = f"{chapter_idx:02d}-{cat_slug}"
            n["category"] = current_cat_dir
            category_titles[current_cat_dir] = f"{chapter_idx:02d}. {label}"
        else:
            n["category"] = current_cat_dir

        n["label"] = label
        n["slug"] = slugify(label)

    print(f"Found {len(sorted_nodes)} nodes across chapters.")

    # Fetch detailed content for each node
    for i, node in enumerate(sorted_nodes):
        nid = node["id"]
        node_url = f"{BASE_URL}/{slug}/{nid}.json"
        print(f"  [{i+1}/{len(sorted_nodes)}] {node['label']}...", end=" ", flush=True)
        content_data = fetch_json(node_url)
        if content_data:
            node["description"] = content_data.get("description", "")
            node["resources"] = content_data.get("resources", [])
            node["updated_at"] = content_data.get("updatedAt", "")
            print(f"OK ({len(node['description'])} chars)")
        else:
            node["description"] = ""
            node["resources"] = []
            print("EMPTY")
        time.sleep(0.5)

    # Save output
    output_file = os.path.join(output_dir, "all_nodes.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sorted_nodes, f, ensure_ascii=False, indent=2)

    # Save metadata/category titles
    meta_file = os.path.join(output_dir, "metadata.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "title": data.get("title", slug.replace("-", " ").title()),
                "description": data.get("description", ""),
                "slug": slug,
                "total_nodes": len(sorted_nodes),
                "category_titles": category_titles,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Successfully saved {len(sorted_nodes)} nodes to {output_file}")


def call_gemini(prompt, max_retries=3):
    """Call Gemini API with prompt."""
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY not configured in .env or environment!")
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 65536},
    }
    data = json.dumps(payload).encode("utf-8")

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url, data=data, headers={"Content-Type": "application/json"}, method="POST"
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                candidates = res.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
            return ""
        except Exception as e:
            print(f"    Gemini API attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(3 * (attempt + 1))
    return None


def build_prompt(slug, batch, roadmap_title):
    """Build Gemini chunking prompt for a batch of lessons."""
    lessons_text = ""
    for i, lesson in enumerate(batch):
        desc = lesson.get("description", "").strip()
        if not desc:
            desc = f"# {lesson['label']}\n\nNo detailed content available for this topic."

        resources = lesson.get("resources", [])
        resources_text = ""
        if resources:
            resources_text = "\n\nRESOURCES:\n"
            for r in resources:
                resources_text += f"- [{r.get('title', '')}]({r.get('url', '')}) ({r.get('type', '')})\n"

        lessons_text += f"""
===LESSON_{i+1}_START===
LESSON_ID: {lesson['id']}
LESSON_LABEL: {lesson['label']}
LESSON_SLUG: {lesson['slug']}
LESSON_CATEGORY: {lesson['category']}

CONTENT:
{desc}
{resources_text}
===LESSON_{i+1}_END===
"""

    return f"""You are a bilingual content processor. Process the following {len(batch)} lessons from the {roadmap_title} Roadmap ({slug}).

For EACH lesson, you must:

1. Keep ALL original content - headings, paragraphs, lists, tables, code blocks. Do NOT summarize, paraphrase, or add anything.

2. Apply bilingual chunking to EVERY English paragraph and list item:
   - Split each sentence into semantic chunks of 3-6 words each
   - Split at: noun phrases, verb phrases, clauses, prepositional phrases, conjunctions
   - Do NOT split: verb+object, adjective+noun, compound nouns, prepositions from their phrases, idioms, phrasal verbs, collocations
   - Each line has 2-3 chunks separated by " | ", max 15 words per line
   - English line in **bold**, Vietnamese translation in *italic* directly below
   - Keep technical terms untranslated: API, HTTP, SQL, NoSQL, Git, CI/CD, LLM, Docker, Kubernetes, Linux, AWS, JSON, REST, etc.

3. Format:
**Chunk 1 | Chunk 2 | Chunk 3**

*Dịch chunk 1 | Dịch chunk 2 | Dịch chunk 3*

4. For headings: Keep original English heading as-is (## heading). Do NOT chunk headings.

5. For code blocks: Keep exactly as-is. Do NOT translate code.

6. Output format for EACH lesson - output complete markdown including front matter:

<<<LESSON_START>>>
LESSON_ID: [id]
LESSON_SLUG: [slug]
LESSON_CATEGORY: [category]

---
title: "[Original English Title]"
description: "[First sentence of content in English]"
summary: "[First sentence in Vietnamese]"
slug: "[slug]"
date: 2026-08-01
draft: false

categories:
  - {roadmap_title}

tags:
  - {slug}

toc: true
math: false
mermaid: false
---

[Chunked bilingual content here]

## Resources

[Resource links here]

## References

- https://roadmap.sh/{slug} (Node: [label])

<<<LESSON_END>>>

IMPORTANT:
- Output ALL lessons wrapped in <<<LESSON_START>>> and <<<LESSON_END>>>
- Keep 100% of original knowledge
- Vietnamese translation must be natural and accurate
- Every English paragraph must have chunked bilingual format

Here are the lessons to process:
{lessons_text}"""


def process_batch(slug, batch_num, batch_size=20, force=False):
    """Process a single batch using Gemini API."""
    data_dir = os.path.join(PROJECT_DIR, ".roadmap-data", slug)
    nodes_file = os.path.join(data_dir, "all_nodes.json")
    meta_file = os.path.join(data_dir, "metadata.json")

    if not os.path.exists(nodes_file):
        print(f"ERROR: {nodes_file} not found. Run fetch first!")
        sys.exit(1)

    with open(nodes_file, "r", encoding="utf-8") as f:
        all_nodes = json.load(f)

    roadmap_title = slug.replace("-", " ").title()
    if os.path.exists(meta_file):
        with open(meta_file, "r", encoding="utf-8") as f:
            roadmap_title = json.load(f).get("title", roadmap_title)

    total_batches = (len(all_nodes) + batch_size - 1) // batch_size
    if batch_num < 1 or batch_num > total_batches:
        print(f"ERROR: Invalid batch {batch_num}. Total batches: {total_batches}")
        sys.exit(1)

    start_idx = (batch_num - 1) * batch_size
    end_idx = min(start_idx + batch_size, len(all_nodes))
    batch = all_nodes[start_idx:end_idx]

    content_dir = os.path.join(PROJECT_DIR, "content", slug)

    print(f"\n=== PROCESSING BATCH {batch_num}/{total_batches} ({len(batch)} lessons) for {slug} ===")
    prompt = build_prompt(slug, batch, roadmap_title)
    print(f"  Prompt size: {len(prompt)} chars")
    print(f"  Calling Gemini API ({GEMINI_MODEL})...")

    start_time = time.time()
    response = call_gemini(prompt)
    elapsed = time.time() - start_time
    print(f"  Received response in {elapsed:.1f}s ({len(response) if response else 0} chars)")

    if not response:
        print("  ERROR: No response from Gemini API!")
        return 0

    # Parse response
    parts = re.split(r"<<<LESSON_START>>>", response)
    written_count = 0

    for part in parts[1:]:
        end_idx = part.find("<<<LESSON_END>>>")
        content = part[:end_idx].strip() if end_idx != -1 else part.strip()

        lesson_id, lesson_slug, lesson_cat = "", "", ""
        lines = content.split("\n")
        content_start = 0

        for j, line in enumerate(lines):
            if line.startswith("LESSON_ID:"):
                lesson_id = line.split(":", 1)[1].strip()
            elif line.startswith("LESSON_SLUG:"):
                lesson_slug = line.split(":", 1)[1].strip()
            elif line.startswith("LESSON_CATEGORY:"):
                lesson_cat = line.split(":", 1)[1].strip()
            elif line.startswith("---"):
                content_start = j
                break

        md_content = "\n".join(lines[content_start:]).strip()

        # Add 2 trailing spaces to English bold lines for Goldmark line break
        md_content = re.sub(r"(\*\*[^\n]+\*\*)$", r"\1  ", md_content, flags=re.MULTILINE)

        if lesson_slug and lesson_cat and md_content:
            target_dir = os.path.join(content_dir, lesson_cat)
            os.makedirs(target_dir, exist_ok=True)
            file_path = os.path.join(target_dir, f"{lesson_slug}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md_content + "\n")
            written_count += 1
            print(f"    Written: {file_path}")

    return written_count


def generate_index(slug):
    """Generate Hugo master _index.md and category _index.md files."""
    data_dir = os.path.join(PROJECT_DIR, ".roadmap-data", slug)
    nodes_file = os.path.join(data_dir, "all_nodes.json")
    meta_file = os.path.join(data_dir, "metadata.json")

    if not os.path.exists(nodes_file):
        print(f"ERROR: {nodes_file} not found.")
        return

    with open(nodes_file, "r", encoding="utf-8") as f:
        nodes = json.load(f)

    meta = {}
    if os.path.exists(meta_file):
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

    roadmap_title = meta.get("title", slug.replace("-", " ").title())
    content_dir = os.path.join(PROJECT_DIR, "content", slug)

    # Group nodes by category
    categories = {}
    for n in nodes:
        cat = n.get("category", "01-general")
        if cat not in categories:
            categories[cat] = []
        c_slug = n.get("slug")
        file_path = os.path.join(content_dir, cat, f"{c_slug}.md")
        if os.path.exists(file_path):
            categories[cat].append({
                "label": n.get("label"),
                "slug": c_slug,
                "link": f"/{slug}/{cat}/{c_slug}/"
            })

    # Master index content
    master_content = f"""---
title: "{roadmap_title} Roadmap"
description: "Lộ trình học tập {roadmap_title} được phân đoạn song ngữ Anh - Việt chuẩn SEO."
slug: "{slug}"
date: 2026-08-01
draft: false

categories:
  - {roadmap_title}

toc: true
math: false
mermaid: false
---

Lộ trình học tập {roadmap_title} được phân chia theo các chuyên mục tuần tự:

"""

    for cat_slug in sorted(categories.keys()):
        items = categories[cat_slug]
        if not items:
            continue
        cat_name = cat_slug.replace("-", " ").title()
        master_content += f"## {cat_name}\n\n"
        for item in items:
            master_content += f"- [{item['label']}]({item['link']})\n"
        master_content += "\n"

    master_path = os.path.join(content_dir, "_index.md")
    os.makedirs(content_dir, exist_ok=True)
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_content)
    print(f"Generated Master Index: {master_path}")

    # Category-level index files
    for cat_slug, items in categories.items():
        if not items:
            continue
        cat_dir = os.path.join(content_dir, cat_slug)
        os.makedirs(cat_dir, exist_ok=True)
        cat_index_path = os.path.join(cat_dir, "_index.md")
        cat_title = cat_slug.replace("-", " ").title()
        cat_content = f"""---
title: "{cat_title}"
description: "Các bài học thuộc chuyên mục {cat_title}."
date: 2026-08-01
draft: false

categories:
  - {roadmap_title}

toc: true
---

"""
        for item in items:
            cat_content += f"- [{item['label']}]({item['link']})\n"

        with open(cat_index_path, "w", encoding="utf-8") as f:
            cat_content += "\n"
            f.write(cat_content)
    print(f"Generated {len(categories)} category _index.md files.")


def add_navigation(slug):
    """Add sequential weights and prev/next links to all lesson files."""
    data_dir = os.path.join(PROJECT_DIR, ".roadmap-data", slug)
    nodes_file = os.path.join(data_dir, "all_nodes.json")

    if not os.path.exists(nodes_file):
        print(f"ERROR: {nodes_file} not found.")
        return

    with open(nodes_file, "r", encoding="utf-8") as f:
        nodes = json.load(f)

    content_dir = os.path.join(PROJECT_DIR, "content", slug)
    roadmap_title = slug.replace("-", " ").title()

    ordered_lessons = []
    seen = set()

    categories_sorted = sorted(list({n.get("category", "01-general") for n in nodes}))
    for cat in categories_sorted:
        cat_nodes = [n for n in nodes if n.get("category") == cat]
        for n in cat_nodes:
            c_slug = n.get("slug")
            file_path = os.path.join(content_dir, cat, f"{c_slug}.md")
            if os.path.exists(file_path) and file_path not in seen:
                seen.add(file_path)
                ordered_lessons.append({
                    "label": n.get("label"),
                    "cat": cat,
                    "slug": c_slug,
                    "path": file_path,
                    "link": f"/{slug}/{cat}/{c_slug}/"
                })

    print(f"Applying navigation to {len(ordered_lessons)} lesson files for {slug}...")

    for i, item in enumerate(ordered_lessons):
        weight = i + 1
        prev_item = ordered_lessons[i - 1] if i > 0 else None
        next_item = ordered_lessons[i + 1] if i < len(ordered_lessons) - 1 else None

        with open(item["path"], "r", encoding="utf-8") as f:
            content = f.read()

        # Clean existing navigation line
        content = re.sub(r"\n---\n\n\[.*roadmap.*\n?", "", content, flags=re.IGNORECASE)

        # Build bottom text navigation line
        parts = []
        if prev_item:
            parts.append(f"[← {prev_item['label']}]({prev_item['link']})")
        parts.append(f"[{roadmap_title} Roadmap](/{slug}/)")
        if next_item:
            parts.append(f"[{next_item['label']} →]({next_item['link']})")

        nav_block = "\n\n---\n\n" + " · ".join(parts) + "\n"

        prev_link = prev_item["link"] if prev_item else ""
        next_link = next_item["link"] if next_item else ""

        # Update weight in front matter
        if "weight:" not in content:
            content = re.sub(r"^(date:\s*[^\n]+)", r"\1\nweight: " + str(weight), content, flags=re.MULTILINE)
        else:
            content = re.sub(r"^weight:\s*\d+", f"weight: {weight}", content, flags=re.MULTILINE)

        # Update prev / next links
        if prev_link:
            if "prev:" not in content:
                content = re.sub(r"^(weight:\s*\d+)", r'\1\nprev: "' + prev_link + '"', content, flags=re.MULTILINE)
            else:
                content = re.sub(r'^prev:\s*"[^"]*"', f'prev: "{prev_link}"', content, flags=re.MULTILINE)

        if next_link:
            if "next:" not in content:
                content = re.sub(r"^(weight:\s*\d+)", r'\1\nnext: "' + next_link + '"', content, flags=re.MULTILINE)
            else:
                content = re.sub(r'^next:\s*"[^"]*"', f'next: "{next_link}"', content, flags=re.MULTILINE)

        final_content = content.strip() + nav_block
        with open(item["path"], "w", encoding="utf-8") as f:
            f.write(final_content)

    print(f"Successfully applied navigation to {len(ordered_lessons)} lessons!")


def main():
    parser = argparse.ArgumentParser(description="Generic Roadmap Automation CLI Tool")
    parser.add_argument("command", choices=["fetch", "process", "generate-index", "add-navigation", "run-all"])
    parser.add_argument("--slug", required=True, help="Roadmap slug (e.g. backend, devops, ai-engineer)")
    parser.add_argument("--batch", type=int, default=1, help="Batch number for process command")
    parser.add_argument("--batch-size", type=int, default=20, help="Batch size for LLM chunking")

    args = parser.parse_args()

    if args.command == "fetch":
        fetch_roadmap(args.slug)
    elif args.command == "process":
        process_batch(args.slug, args.batch, args.batch_size)
    elif args.command == "generate-index":
        generate_index(args.slug)
    elif args.command == "add-navigation":
        add_navigation(args.slug)
    elif args.command == "run-all":
        fetch_roadmap(args.slug)
        nodes_file = os.path.join(PROJECT_DIR, ".roadmap-data", args.slug, "all_nodes.json")
        if os.path.exists(nodes_file):
            with open(nodes_file, "r", encoding="utf-8") as f:
                nodes = json.load(f)
            total_batches = (len(nodes) + args.batch_size - 1) // args.batch_size
            for b in range(1, total_batches + 1):
                process_batch(args.slug, b, args.batch_size)
                time.sleep(2)
        generate_index(args.slug)
        add_navigation(args.slug)


if __name__ == "__main__":
    main()
