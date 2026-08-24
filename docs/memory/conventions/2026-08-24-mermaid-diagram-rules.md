---
title: "Quy Chuẩn Viết Sơ Đồ Mermaid và Xử Lý Lỗi SVG Hugo"
description: "Tổng hợp toàn bộ quy tắc viết sơ đồ Mermaid JS trong Hugo, cách chống lỗi list và tối ưu layout 2 cột"
tags: [mermaid, hugo, frontend, conventions, best-practices]
created: 2026-08-24
updated: 2026-08-24
type: "preference"
importance: 3
source: conversation
---

# Quy Chuẩn Viết Sơ Đồ Mermaid và Xử Lý Lỗi SVG Trong Hugo

## Overview
Bộ quy chuẩn toàn diện để thiết kế sơ đồ Mermaid JS đẹp mắt, rõ ràng, không bị lỗi cú pháp Markdown và tối ưu tỷ lệ hiển thị trên mọi kích thước màn hình trong Hugo blog.

## Key Points
- **Cấu hình theme toàn cục:** Đã inject theme Indigo và hỗ trợ Dark Mode tự động tại `layouts/_partials/plugin/mermaid.html`. Tuyệt đối không chèn `%%{init}%%` thủ công trong bài viết.
- **Tránh lỗi `Unsupported markdown: list`:** Tuyệt đối không bắt đầu nội dung node bằng số thứ tự kèm dấu chấm (như `["1. Bước một"]`). Phải đổi thành `["Lớp 1: Bước một"]`, `["Nhóm 1: Bước một"]` hoặc `["(1) Bước một"]`.
- **Tránh tràn góc nhọn hình thoi:** Nút điều kiện `{...}` chỉ chứa câu hỏi ngắn gọn dưới 20 ký tự (ví dụ: `Check{"Có --add-tests?"}`). Chi tiết điều kiện đưa lên nhãn mũi tên `-->|Có: Chu trình TDD|`.
- **Chống bè ngang và chống thu nhỏ chữ (Scale down):** Không tỏa ra quá 3 node con nằm ngang từ 1 node cha. Với sơ đồ từ 4 node trở lên, bắt buộc chia thành các `subgraph` xếp dọc (`direction TB`) đặt cạnh nhau để tạo bố cục 2 cột cân đối.
- **Tránh cắt chữ mép phải (Text Clipping):** Thêm `<br/>` ngắt dòng thông minh để nội dung node vuông vắn. CSS container đã có `foreignObject { overflow: visible !important; }`.
- **CSS SVG internals:** Tuyệt đối không dùng CSS ép `font-size !important` vào thẻ `text` bên trong SVG vì sẽ làm sai lệch bounding box của Mermaid JS.

## Related
- `.agents/AGENTS.md`
- `layouts/_partials/plugin/mermaid.html`
- `assets/css/_override.scss`
