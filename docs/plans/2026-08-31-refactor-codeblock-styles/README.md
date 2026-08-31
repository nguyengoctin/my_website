---
slug: 2026-08-31-refactor-codeblock-styles
auto: false
status: done
---

# Plan: Refactor toàn diện Codeblock Styles & UX (Hugo + LoveIt)

**Mode:** normal
**Created:** 2026-08-31
**Status:** DONE

## Context
Qua audit từ nghiên cứu cộng đồng và phân tích source code thực tế của theme LoveIt trên Hugo, hệ thống codeblock hiện tại gặp các hạn chế:
1. **Collapsible Header gây phiền toái:** Codeblock dài hơn 50 dòng bị đóng mặc định (`max-height: 0`), click vào dễ bị toggle nhầm làm biến mất code.
2. **Copy & Line Numbers UX:** Nút copy và số thứ tự dòng chưa tối ưu `user-select: none`, styling số dòng chưa có padding/border phân cách chuyên nghiệp.
3. **Typography & Wrapping Issue:** CSS gốc áp dụng `@include line-break(anywhere)` gây bẻ gãy từ vô tội vạ trên khối `pre code`.
4. **Dark/Light Theme Styling:** Chưa có module SCSS chuyên biệt chuẩn hóa theo hệ thống màu thương hiệu (Brand Colors) và JetBrains Mono font.

## Assumptions
- Giữ nguyên cơ chế build tĩnh của Hugo (Chroma `transform.Highlight`), không thêm JS runtime nặng.
- Không sửa trực tiếp vào thư mục theme gốc `themes/LoveIt/` (tuân thủ nguyên tắc Clean Architecture & Protected Area của Hugo) mà override thông qua `layouts/_partials/plugin/code-block.html` và module `assets/css/modules/_codeblock.scss`.

## Approach
1. **Module hóa CSS Codeblock:** Tạo file mới `assets/css/modules/_codeblock.scss` và import vào `assets/css/_override.scss`.
2. **Tối ưu Layouts Partial:** Override `layouts/_partials/plugin/code-block.html` trong project root để:
   - Mặc định luôn mở (`open` 100%), không tự động giấu code.
   - Header hiển thị tên ngôn ngữ rõ ràng, icon ngôn ngữ, và nút Copy luôn sẵn sàng ở vị trí thuận tiện.
3. **Cố định Typography & Scroll:**
   - Đảm bảo `pre code` dùng `white-space: pre`, `overflow-x: auto`, giữ nguyên khoảng cách thụt lề tab 2/4 spaces.
   - Cột số dòng có `user-select: none`, màu trung tính dịu mắt, border ngăn cách rõ ràng.
   - Hỗ trợ full Dark/Light theme đồng bộ bảng màu brand.

## Not Building
- Không cài thêm Client-side highlighting nặng (Prism.js / Highlight.js).
- Không can thiệp vào các shortcode đặc thù khác (Mermaid, Admonitions).

## Progress

| Status  | Phase   | Task |
| ------- | ------- | ---- |
| ✅ DONE | Phase 1 | Tạo module SCSS `_codeblock.scss` và tích hợp vào `_override.scss` |
| ✅ DONE | Phase 2 | Override partial `layouts/_partials/plugin/code-block.html` để hoàn thiện UX |
| ✅ DONE | Phase 3 | Thẩm định kiểm tra build Hugo và hiển thị Dark/Light mode |

## Tasks

#### Phase 1 [sequential]

1. **Tạo module `assets/css/modules/_codeblock.scss`**
   - Files: `assets/css/modules/_codeblock.scss`, `assets/css/_override.scss`
   - Thiết kế giao diện codeblock hiện đại (JetBrains Mono, rounded corners, subtle border, line numbers separator, copy button hover & feedback effect, scrollbar tinh tế).
   - Đảm bảo Dark/Light mode hỗ trợ hoàn hảo.
   - Verify: Chạy SCSS compilation qua Hugo không báo lỗi cú pháp.

2. **Override Template `layouts/_partials/plugin/code-block.html`**
   - Files: `layouts/_partials/plugin/code-block.html`
   - Cấu trúc lại DOM header codeblock (Language badge, Copy button với icon SVG/FontAwesome mượt mà).
   - Bỏ trạng thái auto-collapse phiền toái.
   - Verify: Kiểm tra DOM output render sạch sẽ, không trùng lặp class.

3. **Kiểm tra và Thẩm định Build (Definition of Done)**
   - Chạy lệnh `hugo --buildDrafts` để đảm bảo 100% build thành công không lỗi.
   - Verify: Kiểm tra các trang bài viết chứa codeblock (ví dụ bài viết về Claude MD / Prompt).

## Risks
- Xung đột CSS specificity với file `style.min.css` gốc của LoveIt: Giải quyết bằng cách viết selector có độ ưu tiên cao hoặc bọc trong scoping container `.single .content .code-block`.

## Next Steps
Sau khi phê duyệt plan: Thực thi Phase 1 & 2 → Verify build `hugo --buildDrafts` → `/cf-review` & `/cf-commit`.
