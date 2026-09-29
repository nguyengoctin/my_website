---
slug: 2026-09-29-refactoring-ui-token-alignment
auto: false
commitPerTask: false
status: done
---

# Plan: Chuẩn Hóa Typography & Spacing Tokens Theo Refactoring UI

**Mode:** normal
**Created:** 2026-09-29
**Status:** DONE

## Context

Dựa trên kết quả từ `/cf-review` và nghiên cứu chuyên sâu `/cf-research` (`docs/research/2026-09-29-refactoring-ui-typography-and-layout/`), kiến trúc CSS của `my_website` hiện rất tốt nhưng có 2 điểm cần chuẩn hóa:
1. Thang Font Size Scale có nấc `--fs-md` (18.4px) quá sát `--fs-base` (18px) và `--fs-xl` (21.6px) quá sát `--fs-lg` (20px).
2. Spacing tokens (`--space-p: 1.45rem` = 23.2px, `--space-h2-bottom: 0.85rem` = 13.6px) mang giá trị lẻ, chưa khớp tròn theo hệ thống Grid Base 8px/16px.

## Assumptions

- Các thành phần phụ thuộc vào `--fs-md` (như quote footer) và `--space-p` (khoảng cách đoạn văn) sẽ tự động nhận giá trị đồng bộ và đẹp mắt hơn mà không gây vỡ bố cục.
- Độ rộng toàn site vẫn giữ nguyên `--shell-width: 750px` (chuẩn Single Shell đã kiểm chứng).

## Approach

- Chuẩn hóa lại các biến token CSS trong `assets/css/modules/_typography_and_nav.scss`.
- Giữ nguyên các giá trị H1, H2, H3, H4 hiện tại để bảo toàn cấu trúc editorial, chỉ chỉnh lại thang bậc font-size trung gian (`--fs-md`, `--fs-lg`, `--fs-xl`) và làm tròn các token khoảng cách.
- Thẩm định bằng lệnh `hugo --buildDrafts`.

## Not Building

- Không thay đổi phông chữ gốc (`Newsreader` serif và `IBM Plex Mono`).
- Không can thiệp vào các shortcode hay render hooks đã ổn định.

## Progress

| Status  | Phase   | Task                                                               |
| ------- | ------- | ------------------------------------------------------------------ |
| 🟩 DONE | Phase 1 | Chuẩn hóa Font Size Scale Tokens trong `_typography_and_nav.scss` |
| 🟩 DONE | Phase 1 | Chuẩn hóa Spacing Tokens theo Base Grid 8px/16px                   |
| 🟩 DONE | Phase 1 | Kiểm tra độ tương thích và xác minh bản build Hugo                  |

## Tasks

#### Phase 1 [sequential]

1. **Chuẩn hóa Font Size Scale Tokens**
   - Files: [`assets/css/modules/_typography_and_nav.scss`](assets/css/modules/_typography_and_nav.scss)
   - Điều chỉnh:
     - `--fs-md: 1.25rem;` (20px - thay cho 1.15rem, tạo bước đệm rõ rệt trên base 18px)
     - `--fs-lg: 1.375rem;` (22px - thay cho 1.25rem)
     - `--fs-xl: 1.5rem;` (24px - thay cho 1.35rem)
     - `--fs-2xl: 1.75rem;` (28px - thay cho 1.5rem)
     - `--fs-3xl: 2.125rem;` (34px - đồng bộ với `--fs-h1`)
   - Outcome: Thang font size có các nấc nhảy thị giác rõ ràng, loại bỏ tình trạng 2 cỡ chữ cách nhau < 1px.
   - Verify: `grep -n -- '--fs-' assets/css/modules/_typography_and_nav.scss`

2. **Chuẩn hóa Spacing Tokens theo Base Grid 8px/16px**
   - Files: [`assets/css/modules/_typography_and_nav.scss`](assets/css/modules/_typography_and_nav.scss)
   - Điều chỉnh:
     - `--space-p: 1.5rem;` (24px - thay cho 1.45rem = 23.2px lẻ)
     - `--space-h2-bottom: 0.75rem;` (12px - thay cho 0.85rem = 13.6px; tỉ lệ top:bottom là `2.5rem` : `0.75rem` = `40px` : `12px` ~ 3.33:1, chuẩn Gestalt Proximity)
     - Mobile: `--space-h2-top: 2rem;` (32px) và `--space-h2-bottom: 0.75rem;` (12px)
   - Outcome: Khoảng cách giữa các đoạn văn và tiêu đề tròn theo nhịp 8px grid.
   - Verify: `grep -n -- '--space-' assets/css/modules/_typography_and_nav.scss`

3. **Kiểm tra độ tương thích và xác minh bản build Hugo**
   - Files: Toàn bộ site
   - Outcome: Biên dịch sạch sẽ 100%, không phát sinh lỗi render.
   - Verify: `hugo --buildDrafts`

## Risks

- Thay đổi `--space-p` từ 1.45rem (23.2px) sang 1.5rem (24px) tăng thêm 0.8px cho mỗi đoạn văn; thay đổi này rất tinh tế, tăng nhẹ độ thoáng mà không làm thay đổi cảm quan tổng thể.
- Thay đổi `--space-h2-bottom` từ 0.85rem (13.6px) xuống 0.75rem (12px) giúp Heading gắn chặt hơn 1.6px với đoạn văn bên dưới, củng cố thêm luật Gestalt Proximity.

## Next Steps

Sau khi người dùng duyệt kế hoạch: Triển khai chỉnh sửa → chạy `hugo --buildDrafts` → `/cf-review` → `/cf-commit`.
