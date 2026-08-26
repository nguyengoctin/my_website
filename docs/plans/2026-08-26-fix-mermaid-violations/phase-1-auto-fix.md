# Phase 1: Auto Fix — Empty Lines và Ampersands

**Plan:** README.md  
**Type:** sequential

## Progress

| Status | Task |
|--------|------|
| ⬜ TODO | Task 1: Chạy script fix tự động (live mode) |
| ⬜ TODO | Task 2: Verify nội dung sau fix bằng grep |

## Tasks

### Task 1: Chạy script `fix_mermaid_violations.py` ở live mode

- **File:** `scripts/fix_mermaid_violations.py`
- **Thay đổi:** Đổi `DRY_RUN = True` → `DRY_RUN = False` rồi chạy
- **Lệnh:**
  ```bash
  # Sửa DRY_RUN = False trong script, sau đó:
  python3 scripts/fix_mermaid_violations.py
  ```
- **Files bị sửa (13 files):**
  - `bep-di-6-zalo-mini-app-ordering-platform.md` — 2 empty lines
  - `bilingual-movie-learning-platform.md` — 1 empty line
  - `doc-sach-hoc-thuat-cung-ai.md` — 1 empty line
  - `he-thong-phuong-phap-doc-tai-lieu-it-ai-voi-ai-va-srs.md` — 1 empty line
  - `huong-dan-cau-hinh-mac-mini-headless-server.md` — 1 empty line
  - `ky-nghe-phan-mem-ban-dia-ai-va-5-bai-hoc-lam-chu-ai-agents.md` — 6 empty lines + 2 ampersands
  - `lap-trinh-web-ky-nguyen-ai-spec-driven-development.md` — 1 empty line
  - `lexi-ai-english-tutor.md` — 3 empty lines + 1 ampersand
  - `personal-hugo-technical-blog.md` — 1 empty line
  - `quy-trinh-thu-thap-va-chuyen-doi-ai-engineer-roadmap-song-ngu.md` — 1 empty line
  - `toan-tap-coding-friend-ai-engineering.md` — 6 empty lines
  - `tu-duy-viet-claudemd-thuc-chien.md` — 2 empty lines
  - `tu-prompt-engineering-den-graph-engineering.md` — 2 empty lines
- **Expected output:** "TOTAL FILES FIXED: 13, TOTAL EMPTY LINES REMOVED: 28, TOTAL AMPERSANDS FIXED: 3"
- **Verify:** Output khớp expected

### Task 2: Kiểm tra không còn vi phạm bằng grep

- **Lệnh:**
  ```bash
  python3 -c "
  import re, os
  posts = 'content/posts'
  issues = 0
  for f in os.listdir(posts):
      if not f.endswith('.md'): continue
      content = open(os.path.join(posts, f)).read()
      for m in re.finditer(r'\`\`\`mermaid\n(.*?)\`\`\`', content, re.DOTALL):
          block = m.group(1)
          if block.endswith('\n\n') or '\n\n' in block:
              print(f'STILL HAS EMPTY LINE: {f}')
              issues += 1
          for line in block.split('\n'):
              if ' & ' in line and '%' not in line:
                  print(f'STILL HAS AMP: {f}: {line[:50]}')
                  issues += 1
  print(f'Remaining issues: {issues}')
  "
  ```
- **Expected output:** "Remaining issues: 0"
- **Verify:** Output khớp expected
