---
title: "Pipeline Tự Động Hóa Lộ Trình Học Tập"
description: "Cơ chế kéo dữ liệu roadmap.sh, chunking bằng Gemini LLM và sinh cấu trúc thư mục tự động"
tags: [features, roadmap-cli, python, automation, gemini-api]
created: 2026-08-24
updated: 2026-08-24
type: "fact"
importance: 3
source: scan
---

# Pipeline Tự Động Hóa Lộ Trình Học Tập

## Overview
Dự án tích hợp công cụ CLI Python (`scripts/roadmap_cli.py`) để đồng bộ hóa và tạo tài liệu học tập chi tiết cho các chuyên ngành (Backend, AI Engineer, DevOps...) trực tiếp từ hệ thống `roadmap.sh`.

## Key Points
- **Pipeline các bước thực thi:**
  1. `fetch`: Tải cấu trúc node JSON từ `roadmap.sh/{slug}.json` và nhóm vào các chương trong `.roadmap-data/{slug}/`.
  2. `process`: Gửi dữ liệu chi tiết của từng chủ đề qua Gemini LLM API (sử dụng model cấu hình như `gemini-3.1-flash-lite`) để sinh nội dung song ngữ, giải thích kỹ thuật và code ví dụ.
  3. `generate-index`: Tự động tạo trang `_index.md` cho các chương với danh sách bài đọc được sắp xếp chuẩn xác.
  4. `add-navigation`: Bổ sung điều hướng Next/Previous bài học vào cuối từng file Markdown.
  5. `run-all`: Chạy toàn bộ chu trình hoàn chỉnh cho một roadmap slug.
- **Quản lý biến môi trường:** Hỗ trợ load `.env` để đọc `GEMINI_API_KEY` và `GEMINI_MODEL`.

## State Machine
```
[roadmap.sh API]
       │ (fetch)
       ▼
[.roadmap-data/ JSON Nodes]
       │ (process with Gemini LLM)
       ▼
[content/{slug}/ Markdown Chunks]
       │ (generate-index & add-navigation)
       ▼
[Hugo Content Pages ready to render]
```

## Related
- [scripts/roadmap_cli.py](file:///home/ngoctin/Projects/my_website/scripts/roadmap_cli.py)
- [content/ai-engineer/](file:///home/ngoctin/Projects/my_website/content/ai-engineer)
- [content/backend/](file:///home/ngoctin/Projects/my_website/content/backend)
