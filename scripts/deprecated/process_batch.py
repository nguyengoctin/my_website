#!/usr/bin/env python3
"""
Process AI Engineer Roadmap lessons in batches of 20.
Uses Gemini API for chunking and translation.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import re
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, ".roadmap-data")
CONTENT_DIR = os.path.join(PROJECT_DIR, "content", "ai-engineer")
BATCH_SIZE = 20

# Config - Load from .env or environment
def load_env():
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

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found in environment or .env file.")
    sys.exit(1)

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"


def call_gemini(prompt, max_retries=3):
    """Call Gemini API with a prompt."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 65536,
        }
    }

    data = json.dumps(payload).encode('utf-8')

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                GEMINI_URL,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                candidates = result.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        return parts[0].get('text', '')
            return ''
        except Exception as e:
            print(f"    Gemini API attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(3 * (attempt + 1))
    return None


def build_chunk_prompt(lessons_batch):
    """Build a prompt for Gemini to chunk and translate a batch of lessons."""

    lessons_text = ""
    for i, lesson in enumerate(lessons_batch):
        desc = lesson.get('description', '').strip()
        if not desc:
            desc = f"# {lesson['label']}\n\nNo content available for this topic."

        resources = lesson.get('resources', [])
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

    prompt = f"""You are a bilingual content processor. Process the following {len(lessons_batch)} lessons from the AI Engineer Roadmap.

For EACH lesson, you must:

1. Keep ALL original content - headings, paragraphs, lists, tables, code blocks. Do NOT summarize, paraphrase, or add anything.

2. Apply bilingual chunking to EVERY English paragraph and list item:
   - Split each sentence into semantic chunks of 3-6 words each
   - Split at: noun phrases, verb phrases, clauses, prepositional phrases, conjunctions
   - Do NOT split: verb+object, adjective+noun, compound nouns, prepositions from their phrases, idioms, phrasal verbs, collocations
   - Each line has 2-3 chunks separated by " | ", max 15 words per line
   - English line in **bold**, Vietnamese translation in *italic* directly below
   - Keep technical terms untranslated: AI, ML, LLM, Transformer, Embedding, Fine-tuning, Vector Database, Prompt Engineering, Deep Learning, RAG, API, SDK, MCP, GPU, CPU, NLP, etc.

3. Format:
**Chunk 1 | Chunk 2 | Chunk 3**

*Dịch chunk 1 | Dịch chunk 2 | Dịch chunk 3*

4. For headings: Keep the original English heading as-is (## heading). Do NOT chunk headings.

5. For code blocks: Keep exactly as-is. Do NOT translate code.

6. For lists: Apply chunking to each list item text.

7. For Resources section: Keep links as-is, just list them under ## Resources heading.

8. Output format for EACH lesson - output the COMPLETE markdown file content including front matter:

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
  - AI Engineer

tags:
  - [relevant tags based on category]

toc: true
math: false
mermaid: false
---

[Chunked bilingual content here]

## Resources

[Resource links here]

## References

- https://roadmap.sh/ai-engineer (Node: [label])

<<<LESSON_END>>>

IMPORTANT:
- Output ALL lessons, one after another
- Each lesson MUST be wrapped in <<<LESSON_START>>> and <<<LESSON_END>>> markers
- Include LESSON_ID, LESSON_SLUG, LESSON_CATEGORY on separate lines after <<<LESSON_START>>>
- Keep 100% of original knowledge - no summarization
- Vietnamese translation must be accurate and natural
- Every English paragraph must have chunked bilingual format

Here are the lessons to process:

{lessons_text}"""

    return prompt


def parse_gemini_response(response_text, lessons_batch):
    """Parse Gemini response into individual lesson files."""
    results = []

    # Split by lesson markers
    parts = re.split(r'<<<LESSON_START>>>', response_text)

    for part in parts[1:]:  # Skip first empty part
        end_idx = part.find('<<<LESSON_END>>>')
        if end_idx == -1:
            content = part.strip()
        else:
            content = part[:end_idx].strip()

        # Extract metadata
        lesson_id = ""
        lesson_slug = ""
        lesson_category = ""

        lines = content.split('\n')
        content_start = 0
        for j, line in enumerate(lines):
            if line.startswith('LESSON_ID:'):
                lesson_id = line.split(':', 1)[1].strip()
            elif line.startswith('LESSON_SLUG:'):
                lesson_slug = line.split(':', 1)[1].strip()
            elif line.startswith('LESSON_CATEGORY:'):
                lesson_category = line.split(':', 1)[1].strip()
            elif line.startswith('---'):
                content_start = j
                break

        md_content = '\n'.join(lines[content_start:]).strip()

        if lesson_id and md_content:
            results.append({
                'id': lesson_id,
                'slug': lesson_slug,
                'category': lesson_category,
                'content': md_content,
            })

    return results


def write_lesson_file(lesson_data):
    """Write a single lesson markdown file."""
    category = lesson_data['category']
    slug = lesson_data['slug']
    content = lesson_data['content']

    # Post-process content: add 2 trailing spaces to English bold lines for Hugo line break
    content = re.sub(r'(\*\*[^\n]+\*\*)$', r'\1  ', content, flags=re.MULTILINE)

    # Create directory
    dir_path = os.path.join(CONTENT_DIR, category)
    os.makedirs(dir_path, exist_ok=True)

    # Write file
    file_path = os.path.join(dir_path, f"{slug}.md")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        if not content.endswith('\n'):
            f.write('\n')

    return file_path


def process_batch(batch_num, lessons_batch):
    """Process a single batch of lessons."""
    start = (batch_num - 1) * BATCH_SIZE + 1
    end = start + len(lessons_batch) - 1
    print(f"\n{'='*60}")
    print(f"BATCH {batch_num}: Lessons {start}-{end} ({len(lessons_batch)} lessons)")
    print(f"{'='*60}")

    # Build prompt
    prompt = build_chunk_prompt(lessons_batch)
    print(f"  Prompt size: {len(prompt)} chars")

    # Call Gemini
    print(f"  Calling Gemini API ({GEMINI_MODEL})...")
    start_time = time.time()
    response = call_gemini(prompt)
    elapsed = time.time() - start_time
    print(f"  Response received in {elapsed:.1f}s ({len(response) if response else 0} chars)")

    if not response:
        print(f"  ERROR: No response from Gemini API!")
        return []

    # Parse response
    results = parse_gemini_response(response, lessons_batch)
    print(f"  Parsed {len(results)} lessons from response")

    # Write files
    written = []
    for r in results:
        path = write_lesson_file(r)
        written.append(path)
        print(f"    Written: {path}")

    # Check for missing lessons
    result_ids = {r['id'] for r in results}
    for lesson in lessons_batch:
        if lesson['id'] not in result_ids:
            print(f"  WARNING: Missing lesson: {lesson['label']} ({lesson['id']})")

    return written


def main():
    # Load fetched data
    data_file = os.path.join(DATA_DIR, "all_nodes.json")
    if not os.path.exists(data_file):
        print(f"ERROR: {data_file} not found. Run fetch_roadmap_data.py first.")
        sys.exit(1)

    with open(data_file, 'r', encoding='utf-8') as f:
        all_nodes = json.load(f)

    # Filter nodes with content
    nodes_with_content = [n for n in all_nodes if n.get('description', '').strip()]
    nodes_empty = [n for n in all_nodes if not n.get('description', '').strip()]

    print(f"Total nodes: {len(all_nodes)}")
    print(f"With content: {len(nodes_with_content)}")
    print(f"Empty (will create stub): {len(nodes_empty)}")

    # Determine which batch to process
    batch_num = 1
    if len(sys.argv) > 1:
        batch_num = int(sys.argv[1])

    # Calculate batches
    total_batches = (len(all_nodes) + BATCH_SIZE - 1) // BATCH_SIZE

    if batch_num < 1 or batch_num > total_batches:
        print(f"Invalid batch number. Valid: 1-{total_batches}")
        sys.exit(1)

    start_idx = (batch_num - 1) * BATCH_SIZE
    end_idx = min(start_idx + BATCH_SIZE, len(all_nodes))
    batch = all_nodes[start_idx:end_idx]

    print(f"\nProcessing batch {batch_num}/{total_batches}")
    print(f"Lessons {start_idx+1}-{end_idx}")
    for n in batch:
        has = "✓" if n.get('description', '').strip() else "✗"
        print(f"  {has} {n['label']} -> {n['category']}/{n['slug']}.md")

    written = process_batch(batch_num, batch)

    print(f"\n{'='*60}")
    print(f"BATCH {batch_num} COMPLETE: {len(written)} files written")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
