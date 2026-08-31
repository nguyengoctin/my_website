# Local Codebase and UX Audit

## Key Questions

- Website hiện tại đã có những điểm mạnh nào nên giữ?
- Những yếu tố nào làm UI kém clean dù từng component được chăm chút?
- Đâu là rủi ro kỹ thuật nếu tiếp tục thêm override?

## Findings

### Website là knowledge hub, blog và portfolio cùng lúc

Site có hơn 400 Markdown pages, trong đó phần lớn thuộc AI Engineer và Backend roadmaps. Chỉ khoảng 26 file nằm trong `content/posts`. Vì vậy navigation và homepage không thể được đánh giá như một blog thuần túy.

`content/_index.md` dùng homepage để trình bày bio, experience, education và projects. Đây là nội dung portfolio có giá trị, nhưng độ dài làm recent writing và đường vào knowledge base bị đẩy xuống sâu. Người đọc mới phải tự suy luận vai trò chính của website.

### Design system đã hình thành nhưng chưa được cưỡng chế

`assets/css/modules/_typography_and_nav.scss` định nghĩa token light và dark khá rõ. Tuy nhiên nhiều module khác hard-code lại các màu slate, brand blue và border alpha. Radius dao động từ `4px` đến `14px`; spacing trộn px và rem.

Toàn bộ custom SCSS khoảng 4.542 dòng và chứa khoảng 1.441 `!important`. `_custom.scss` vẫn giữ nhiều rule mà các module mới cũng định nghĩa lại. Điều này tạo cascade khó dự đoán, làm mỗi thay đổi UI cần thêm specificity thay vì dùng token và component contract.

### Layout duplication làm tăng blast radius

`layouts/section.html`, `layouts/_default/section.html` và `layouts/posts/section.html` gần như cùng một pattern. Summary cũng tồn tại ở nhiều vị trí. Style của archive description, pinned label và icon nằm inline trong template.

Khi đổi archive card hoặc spacing, nhiều file phải được đồng bộ thủ công. Đây là chỗ nên dùng partial dùng chung trước khi tinh chỉnh hình thức.

### Header vừa được cải thiện nhưng còn semantic gap

Smart sticky, search hotkey và mobile drawer đã được triển khai trong kế hoạch trước. Không nên làm lại tính năng này. Phần còn thiếu là semantic HTML và keyboard state:

- Mobile toggle đang là `div`, không phải `button`.
- Không có `aria-expanded` và `aria-controls` trên mobile toggle.
- Search và theme desktop dùng anchor với `javascript:void(0)`.
- Không có skip link tới main content.
- Focus-visible chưa có quy tắc toàn cục tương đương hover.

### Search mạnh nhưng nặng hơn nhu cầu entry point

Command palette hai cột, hỗ trợ tiếng Việt không dấu và keyboard navigation là điểm khác biệt tốt. Nên giữ. Tuy nhiên search modal có một design language riêng với nhiều token hard-code và file SCSS gần 700 dòng. Cần chuẩn hóa về token chung, focus trap và restore focus thay vì thay search engine chỉ để giống reference.

### Typography đọc tốt nhưng hierarchy hơi đồng nhất

Lora cho toàn body, nav, article và phần lớn UI tạo cá tính editorial. Mặt trái là các lớp thông tin utility, metadata, chip và nav không tách rõ khỏi reading voice. Hướng hợp lý là giữ Lora cho article và identity, dùng system sans cho UI metadata, không đổi toàn site sang font của reference.

### Baseline kỹ thuật khỏe

`hugo --buildDrafts` hoàn tất trong khoảng 3 giây với 1.337 pages, 173 processed images và exit code 0. Cảnh báo duy nhất là `.Site.Data` đã deprecated từ Hugo `0.156.0`. Điều này xác nhận không có lý do kỹ thuật để replatform.

## Code Examples

```scss
:root {
  --clr-bg: #fdfdfd;
  --clr-surface: #ffffff;
  --clr-text: #111111;
  --clr-text-2: #475569;
}
```

Token hiện có đủ làm foundation. Công việc tiếp theo là thay hard-coded values bằng token và giảm duplicate selectors.

## Sources

- `hugo.toml` — cấu trúc menu, search, theme và page features.
- `content/_index.md` — homepage portfolio hiện tại.
- `layouts/partials/header.html` — desktop và mobile navigation.
- `layouts/partials/search-modal.html` — search dialog structure.
- `assets/js/search-modal.js` — search behavior và keyboard flow.
- `assets/css/_custom.scss` và `assets/css/modules/*.scss` — design implementation.
- `docs/plans/2026-08-31-header-uxui-refactor/README.md` — cải thiện header đã hoàn tất.

## Notes

- Chưa có visual browser screenshot vì runtime điều khiển trình duyệt không khả dụng trong phiên này. Kết luận UI dựa trên source, generated markup và build output.
- Cần manual viewport review trước khi merge thay đổi giao diện.

