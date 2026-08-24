---
title: "Kiến Trúc Dự Án Hugo Static Site"
description: "Tổng quan kiến trúc Hugo Extended, LoveIt Theme, module mounts và cơ chế quản lý nội dung"
tags: [architecture, hugo, static-site, loveit, layouts]
created: 2026-08-24
updated: 2026-08-24
type: "fact"
importance: 3
source: scan
---

# Kiến Trúc Dự Án Hugo Static Site

## Overview
Dự án là một blog kỹ thuật và nền tảng lộ trình học tập cá nhân, được xây dựng trên nền tảng **Hugo Extended** kết hợp theme **LoveIt** được tùy biến sâu ở tầng layout và SCSS.

## Key Points
- **Framework:** Hugo (Extended version với hỗ trợ SCSS/Sass và Goldmark Markdown renderer).
- **Theme & Layouts:** Theme LoveIt được ghi đè thông qua thư mục `layouts/` cục bộ (custom taxonomy, section, shortcodes, partials) và `assets/css/_custom.scss`.
- **Hệ thống phân mục nội dung:**
  - `content/posts/`: Các bài viết kỹ thuật sâu, ghi chép và tản văn.
  - `content/ai-engineer/` và `content/backend/`: Cấu trúc lộ trình chi tiết theo từng chương/module.
  - `content/roadmaps/`, `content/cheatsheets/`, `content/listen.md`, `content/cv.md`: Các trang tính năng đặc thù.
- **Tùy biến Asset Pipeline:** Cấu hình `module.mounts` trong `hugo.toml` liên kết `static/images` sang `assets/images` để xử lý hình ảnh trực tiếp qua Hugo Pipes.
- **Tự động hóa dữ liệu:** Sử dụng script Python `scripts/roadmap_cli.py` để kéo và đồng bộ dữ liệu lộ trình từ roadmap.sh, phân chia theo chương với LLM chunking.

## State Machine (Vòng đời nội dung)
- **Bản nháp (Draft):** `draft: true` $\to$ chỉ xuất hiện khi chạy `hugo server -D` hoặc `hugo --buildDrafts`.
- **Biên dịch (Build):** `draft: false` $\to$ Hugo biên dịch mã nguồn sang `public/` qua Goldmark Markdown, SCSS compiler và Lunr index generator.
- **Triển khai (Deploy):** Git push lên branch `main` kích hoạt GitHub Actions chạy `hugo --gc --minify` và deploy lên GitHub Pages.

## Related
- [hugo.toml](file:///home/ngoctin/Projects/my_website/hugo.toml)
- [layouts/](file:///home/ngoctin/Projects/my_website/layouts)
- [assets/css/_custom.scss](file:///home/ngoctin/Projects/my_website/assets/css/_custom.scss)
- [content/](file:///home/ngoctin/Projects/my_website/content)
- [scripts/roadmap_cli.py](file:///home/ngoctin/Projects/my_website/scripts/roadmap_cli.py)
