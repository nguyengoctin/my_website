# Detected Design System

**Style**: Editorial Light and Airy kết hợp knowledge hub, có dark mode first cho nội dung kỹ thuật — độ tin cậy cao.

## Colors

- Brand primary: `#4d74eb`, hover `#1337a6`; dark mode `#60a5fa`, hover `#93c5fd`.
- Brand accent: `#ec4899`; dark mode `#f472b6`.
- Light background tiers: `#fdfdfd`, `#ffffff`, `#f8fafc`, `#f1f5f9`, `#e2e8f0`.
- Dark background tiers: `#1c1d22`, `#23252c`, `#2b2e38`, `#33363f`, `#3a3d48`.
- Primary text: `#111111`; dark mode `#e6e8ec`.
- Secondary text: `#475569`; dark mode `#a1a9b8`.
- Borders: `#e2e8f0`; dark mode `rgba(255,255,255,0.10)`.

## Typography

- Reading text and most navigation: `Lora`, Georgia, serif.
- Site wordmark and utility UI: system sans stack.
- Code: `JetBrains Mono` với fallback system monospace.
- Body article: `1.05rem`, line-height `1.75`.
- Headings: `h1` `1.75rem`, `h2` `1.35rem`, `h3` `1.15rem`; weights từ 500 đến 600.
- `h2` dùng uppercase và tracking `0.05em`, tạo nhịp gần technical documentation hơn editorial essay.

## Spacing

- Đơn vị nền gần `4px`, nhưng code hiện tại trộn rem, px và nhiều giá trị tùy biến.
- Container đọc chính và header cùng dùng `max-width: 850px`.
- Padding ngang: `15px` desktop, `12px` mobile.
- Section spacing phổ biến: `1.5rem` đến `2rem`.

## Shape and Depth

- Radius chính: `4px`, `5px`, `8px`, `14px`.
- Nội dung editorial ưu tiên border mảnh và shadow nhẹ.
- Search modal dùng radius `14px` và shadow sâu để biểu thị lớp phủ.
- Avatar dùng hình tròn với shadow rõ hơn các thành phần còn lại.

## Motion

- Hover và theme transition thường từ `120ms` đến `220ms`.
- Reading progress dùng `requestAnimationFrame` và transform.
- Search modal dùng scale, translate và opacity.
- Chưa có hệ thống `prefers-reduced-motion` nhất quán.

## Layout Patterns

- Header và content dùng cùng trục căn giữa `850px`.
- Bài viết là single-column editorial.
- Search desktop là command palette hai cột; mobile thu gọn thành một cột.
- Trang chủ dùng bio kết hợp timeline cho experience, education và projects.
- Archive nhóm bài theo tháng, có pinned posts.

## Components

- Buttons và chips: brand blue, radius nhỏ đến trung bình, nhiều biến thể riêng theo module.
- Tags: pill nhẹ, dùng surface và border.
- Cards: chủ yếu border nhẹ, ít shadow; một số module dùng shadow riêng.
- Code blocks: radius `8px`, border slate, copy action.
- Callouts: border-left theo semantic color.
- Navigation: text serif, active và hover bằng underline hoặc màu.

## Dark and Light Mode

- Theme được đồng bộ bằng thuộc tính `theme` trên `html` và `body`.
- Token màu cốt lõi đã có source of truth trong `_typography_and_nav.scss`.
- Nhiều module vẫn hard-code màu nên token chưa thực sự bao phủ toàn hệ thống.

## Notes

- Nền tảng thị giác nhất quán và có cá tính hơn một theme mặc định.
- Technical debt chính là 4.542 dòng SCSS, khoảng 1.441 lần dùng `!important`, selector lặp và style inline trong layout.
- Navigation đang phục vụ nhiều loại nội dung ngang cấp nên làm tăng cognitive load.
- Trang chủ kể câu chuyện portfolio khá đầy đủ nhưng làm yếu vai trò entry point cho blog.
- Accessibility primitives chưa đồng đều: thiếu skip link, mobile menu không dùng button semantic, trạng thái mở chưa được mô tả bằng `aria-expanded`, và focus-visible chưa có global rule.

