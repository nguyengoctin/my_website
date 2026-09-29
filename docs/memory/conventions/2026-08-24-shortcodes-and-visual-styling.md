---
title: "Quy Chuẩn Shortcodes và Trực Quan Hóa Sơ Đồ"
description: "Cú pháp Admonition, Quote, Audio, Code Block và quy tắc nhúng sơ đồ kỹ thuật vector SVG"
tags: [shortcodes, diagrams, svg, callouts, markdown]
created: 2026-08-24
updated: 2026-08-24
type: "preference"
importance: 3
source: scan
---

# Quy Chuẩn Shortcodes và Trực Quan Hóa Sơ Đồ

## Overview
Tập hợp các quy định về việc sử dụng shortcode giao diện và biểu đồ Mermaid trong toàn bộ bài viết nhằm bảo đảm hiển thị chuẩn xác trên cả Light và Dark mode.

## Key Points
- **Admonition (Callout):** `{{< admonition type="note|tip|warning|danger|info|success" title="Tiêu đề" >}} Nội dung {{< /admonition >}}`.
- **Quote Shortcode:** `{{< quote author="Tên Tác Giả" >}} Nội dung {{< /quote >}}` (nếu không có `author`, chỉ hiển thị khối trích dẫn). Font chữ sử dụng Lora 500 thanh lịch.
- **Audio Shortcode:** `{{< audio src="/audio/file.mp3" caption="Chú thích" >}}` dùng cho các bản tóm tắt âm thanh NotebookLM.
- **Khối mã (Code Blocks):** Luôn có câu dẫn ngữ cảnh trước code block. Các ngôn ngữ `text`, `markdown`, `yaml` tự động bẻ dòng `white-space: pre-wrap`.
- **Sơ đồ kỹ thuật Vector (Diagram Shortcode):**
  - Không dùng Mermaid JS runtime phía client.
  - Sử dụng shortcode `{{< diagram src="/diagrams/ten-so-do.svg" dark="/diagrams/ten-so-do-dark.svg" alt="Mô tả" >}}`.
  - Toàn bộ SVG được tạo trước bằng `fireworks-tech-graph`, hỗ trợ cả 2 theme Sáng / Tối.

## Related
- [.agents/AGENTS.md](file:///home/ngoctin/Projects/my_website/.agents/AGENTS.md)
- [docs/diagrams.md](file:///home/ngoctin/Projects/my_website/docs/diagrams.md)
- [layouts/shortcodes/diagram.html](file:///home/ngoctin/Projects/my_website/layouts/shortcodes/diagram.html)
- [layouts/shortcodes/quote.html](file:///home/ngoctin/Projects/my_website/layouts/shortcodes/quote.html)
- [layouts/_shortcodes/audio.html](file:///home/ngoctin/Projects/my_website/layouts/_shortcodes/audio.html)
