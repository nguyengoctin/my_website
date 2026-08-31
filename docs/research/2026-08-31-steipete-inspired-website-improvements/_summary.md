# Research: Steipete-inspired Website Improvements

**Date:** 2026-08-31
**Scope:** So sánh source của `steipete.me` với website Hugo hiện tại để tìm pattern UI, information architecture và engineering có thể chuyển giao mà không sao chép framework hoặc nhận diện.

## Overview

Website hiện tại đã có typography editorial, dark mode, search mạnh và build khỏe. Vấn đề chính không phải thiếu polish mà là ba sản phẩm đang chia sẻ cùng một lớp điều hướng: portfolio, blog và knowledge hub. `steipete.me` tạo cảm giác clean bằng constraint rất rõ: ít destination cấp cao, list editorial thay cho card wall, một container đọc, metadata nhẹ và accessibility primitives nhất quán. Hướng phù hợp là giữ Hugo và áp một editorial shell lên knowledge hub, không migrate sang Astro.

## Key Findings

1. Site tham chiếu clean nhờ information hierarchy và giới hạn lựa chọn, không phải nhờ framework Astro.
2. Site hiện tại có hơn 400 content pages nhưng chỉ khoảng 26 posts, nên phải giữ roadmaps như một product surface riêng.
3. Design tokens hiện có đủ tốt, nhưng 4.542 dòng SCSS, khoảng 1.441 `!important`, duplicate templates và inline styles làm tăng chi phí thay đổi.
4. Header vừa được nâng cấp về behavior; vòng tiếp theo nên tập trung semantic HTML, keyboard state và focus-visible thay vì làm lại sticky/search.
5. Homepage nên ngắn hơn và chuyển từ full portfolio timeline sang identity, focus, selected work và recent writing.
6. Nên refactor theo vertical slice có rollback, không đại tu toàn bộ CSS một lần.

## Parts

| # | Document | Description |
| --- | --- | --- |
| 1 | [Reference architecture and UI](01-reference-architecture-and-ui.md) | Pattern từ source và live architecture của repo tham chiếu. |
| 2 | [Local codebase and UX audit](02-local-codebase-and-ux-audit.md) | Điểm mạnh, technical debt và accessibility gaps của Hugo site. |
| 3 | [Transferable principles and options](03-transferable-principles-and-options.md) | Ba hướng cải thiện và recommendation. |

## Open Questions

- Homepage nên ưu tiên recruiters và collaborators hay người đọc technical notes từ search?
- Có cho phép đổi primary navigation trong `hugo.toml` hay chỉ cải thiện layout với sitemap hiện tại?
- Experience và education đầy đủ nên giữ trên homepage, chuyển hoàn toàn sang `/cv/`, hay thu gọn bằng disclosure?
- Có cần thêm visual regression tooling, hay manual viewport checklist là đủ cho giai đoạn đầu?

## Recommended Next Steps

- Chọn Option B: editorial shell trên Hugo knowledge hub.
- Chốt primary audience và phạm vi navigation trước khi viết implementation plan.
- Triển khai theo bốn vertical slices: accessibility foundation, shared listing partials, homepage, article discovery.
- Với mỗi slice, chạy `hugo --buildDrafts`, production build và manual review desktop, tablet, mobile ở light và dark mode.

