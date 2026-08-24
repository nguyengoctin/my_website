---
title: "Quy Chuẩn Shortcodes và Trực Quan Hóa Sơ Đồ"
description: "Cú pháp Admonition, Quote, Audio, Code Block và quy tắc phòng chống lỗi Mermaid SVG"
tags: [shortcodes, mermaid, diagrams, callouts, markdown]
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
- **Quy tắc vàng cho biểu đồ Mermaid (` ```mermaid `):**
  - **Không chèn `%%{init}%%` thủ công** vì hệ thống đã cấu hình theme indigo toàn cục tại `layouts/_partials/plugin/mermaid.html`.
  - **Dòng khai báo:** `flowchart TD`, `flowchart LR`, hoặc `sequenceDiagram` đứng riêng dòng 1.
  - **Node có dấu/khoảng trắng:** Luôn bọc trong cặp ngoặc vuông nháy kép `NodeID["Nội dung"]`.
  - **Không bắt đầu node bằng số kèm dấu chấm:** Không dùng `["1. Bước 1"]` vì gây lỗi Markdown parser của Mermaid 11+. Dùng `["(1) Bước 1"]` hoặc `["Bước 1: ..."]`.
  - **Không để dòng trống (empty line)** giữa các định nghĩa node hay subgraph.
  - **Chống bè ngang:** Khi có từ 4 node trở lên, bắt buộc chia thành các `subgraph` xếp dọc (`direction TB`) đặt cạnh nhau để không bị co chữ li ti.

## Related
- [.agents/AGENTS.md](file:///home/ngoctin/Projects/my_website/.agents/AGENTS.md)
- [docs/memory/conventions/2026-08-24-mermaid-diagram-rules.md](file:///home/ngoctin/Projects/my_website/docs/memory/conventions/2026-08-24-mermaid-diagram-rules.md)
- [docs/memory/bugs/2026-08-24-mermaid-svg-rendering-and-text-clipping-fix.md](file:///home/ngoctin/Projects/my_website/docs/memory/bugs/2026-08-24-mermaid-svg-rendering-and-text-clipping-fix.md)
- [layouts/shortcodes/quote.html](file:///home/ngoctin/Projects/my_website/layouts/shortcodes/quote.html)
- [layouts/_shortcodes/audio.html](file:///home/ngoctin/Projects/my_website/layouts/_shortcodes/audio.html)
