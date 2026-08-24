---
title: "Sửa Lỗi Render Mermaid SVG, Text Clipping Và Markdown List Trong Hugo"
description: "Phân tích nguyên nhân gốc rễ và giải pháp 4 pha xử lý lỗi render Mermaid JS trên Hugo LoveIt"
tags: [mermaid, bug-fix, svg, css, hugo]
created: 2026-08-24
updated: 2026-08-24
type: episode
importance: 4
source: conversation
---

# Báo Cáo Phân Tích Lỗi Hệ Thống: Mermaid JS SVG Rendering & Text Clipping (/cf-sys-debug)

## 1. Overview
Trong quá trình hiển thị các sơ đồ Mermaid JS trên blog Hugo (theme LoveIt), hệ thống xuất hiện đồng thời 4 lỗi nghiêm trọng:
1. Chữ bị cắt cụt mép phải trong các node.
2. Sơ đồ nhiều nhánh bị bóp méo, thu nhỏ chữ li ti không đọc được.
3. Xuất hiện dòng chữ `Unsupported markdown: list` thay cho nội dung thực tế.
4. Text bị tràn ra 4 góc nhọn của nút hình thoi điều kiện `{...}`.

---

## 2. Root Cause Investigation (Nguyên Nhân Gốc Rễ)

### A. Lỗi `Unsupported markdown: list`
- **Root cause:** Từ Mermaid 11+, nhãn trong node `["..."]` mặc định được phân giải cú pháp Markdown. Khi nhãn bắt đầu bằng số thứ tự kèm dấu chấm (như `["1. Khám phá"]`, `["2. Lập kế hoạch"]`), parser nhận diện nhầm đây là cú pháp Ordered List (danh sách có thứ tự) mà Mermaid chưa hỗ trợ render bên trong node $\to$ Gây crash và ném ngoại lệ `Unsupported markdown: list`.

### B. Lỗi Text Clipping (Mất Chữ Mép Phải)
- **Root cause:** Mermaid JS tính toán bounding box độ rộng thẻ `<foreignObject>` bằng font canvas mặc định. Khi render lên web, font chữ thực tế (với tiếng Việt có dấu) có độ rộng glyph nhỉnh hơn độ rộng canvas vài pixel, làm text thực tế vượt qua chiều rộng tính toán $\to$ Trình duyệt áp dụng cơ chế overflow clipping mặc định của SVG, cắt xén mất các chữ cái ở đuôi node (`/c`, `đa`, `hành`, `H`...).

### C. Lỗi Sơ Đồ Bè Ngang & Thu Nhỏ Li Ti (Scale Down)
- **Root cause:** 1 node gốc tỏa ra 5–7 node con dàn hàng ngang làm chiều rộng của SVG đạt tới 1100–1200px. Khi co vào container hiển thị (~750px), CSS `max-width: 100%` bắt buộc trình duyệt phải scale down cả biểu đồ xuống ~50-60%, khiến chữ bị thu nhỏ như hạt gạo.

---

## 3. Hệ Thống Giải Pháp 4 Pha Đã Triển Khai (The Fix)

1. **Khắc phục Text Clipping (CSS Toàn Cục):**
   - Thêm quy tắc tại `assets/css/_override.scss`:
     ```scss
     .mermaid svg foreignObject {
       overflow: visible !important;
       div { overflow: visible !important; }
     }
     ```
2. **Khắc phục Lỗi List & Bố Cục (Markdown Refactoring):**
   - Xóa bỏ toàn bộ tiền tố số `1. `, `2. ` trong node, thay bằng `Nhóm 1: `, `Lớp 1: `.
   - Chuyển các sơ đồ nhiều nhánh (sơ đồ 26 Skills, sơ đồ Review 5 lớp) sang cấu trúc **2 Subgraph xếp dọc song song (`direction TB`)**.
3. **Cấu Hình Theme Toàn Cục Tự Động:**
   - Override template tại `layouts/_partials/plugin/mermaid.html` để tự động inject Indigo theme cho Light Mode và Dark Mode chuẩn, loại bỏ hoàn toàn `%%{init}%%` thủ công.
4. **Quy Chuẩn Hóa:**
   - Đã ghi nhận toàn bộ quy tắc vào `.agents/AGENTS.md` và `docs/memory/conventions/`.

---

## 4. Prevention (Cách Phòng Ngừa Tương Lai)
- Luôn chia Subgraph 2 cột dọc khi sơ đồ có từ 4 node trở lên.
- Không bao giờ đặt số thứ tự kèm dấu chấm ở đầu tên node.
- Giữ câu hỏi trong nút hình thoi `{...}` ngắn dưới 20 ký tự.
