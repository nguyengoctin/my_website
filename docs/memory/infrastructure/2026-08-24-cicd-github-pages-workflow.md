---
title: "Quy Trình Build và CI/CD GitHub Pages"
description: "Pipeline tự động build Hugo Extended và triển khai lên GitHub Pages"
tags: [infrastructure, cicd, github-actions, github-pages, hugo-build]
created: 2026-08-24
updated: 2026-08-24
type: "procedure"
importance: 3
source: scan
---

# Quy Trình Build và CI/CD GitHub Pages

## Overview
Dự án được cấu hình quy trình CI/CD hoàn toàn tự động thông qua GitHub Actions (`.github/workflows/gh-pages.yml`) để biên dịch static files và xuất bản lên GitHub Pages khi có commit mới trên nhánh `main`.

## Key Points
- **Lệnh Kiểm Tra Cục Bộ (Bắt buộc trước khi commit):**
  - Chạy dev server: `hugo server -D`
  - Kiểm tra build nháp và kiểm duyệt shortcode/layout: `hugo --buildDrafts`
  - Thử nghiệm build production: `hugo --gc --minify`
- **GitHub Actions Workflow (`.github/workflows/gh-pages.yml`):**
  - **Trigger:** Tự động chạy khi có sự kiện `push` vào nhánh `main`.
  - **Runner:** `ubuntu-latest`.
  - **Action Steps:**
    1. `actions/checkout@v4` với `submodules: recursive` và `fetch-depth: 0`.
    2. `peaceiris/actions-hugo@v3` cài đặt Hugo bản mới nhất kèm cờ `extended: true`.
    3. Chạy `hugo --gc --minify` để dọn rác và nén tối ưu assets vào thư mục `public/`.
    4. `actions/upload-pages-artifact@v3` tải gói thư mục `public/`.
    5. `actions/deploy-pages@v4` xuất bản lên môi trường `github-pages`.
- **Concurrency:** Cấu hình nhóm `concurrency: group: "pages"` và `cancel-in-progress: false` để đảm bảo thứ tự deploy tuần tự và an toàn.

## State Machine
```
[Local Changes] ──(hugo --buildDrafts)──> [Git Commit & Push main]
                                                     │
                                                     ▼
                                          [GitHub Actions Triggered]
                                                     │
                                                     ▼
                                          [Hugo --gc --minify Build]
                                                     │
                                                     ▼
                                          [Deploy to GitHub Pages]
```

## Related
- [.github/workflows/gh-pages.yml](file:///home/ngoctin/Projects/my_website/.github/workflows/gh-pages.yml)
- [hugo.toml](file:///home/ngoctin/Projects/my_website/hugo.toml)
- [.agents/AGENTS.md](file:///home/ngoctin/Projects/my_website/.agents/AGENTS.md)
