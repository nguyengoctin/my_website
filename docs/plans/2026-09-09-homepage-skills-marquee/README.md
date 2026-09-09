---
slug: 2026-09-09-homepage-skills-marquee
auto: false
status: in-progress
---

# Plan: Dual-Row Tech Stack Marquee with Icons for Homepage

**Mode:** normal

## Context

Trang chủ hiện có thông tin Bio, GitHub Activity, Timeline Kinh nghiệm và Học vấn. Người dùng muốn bổ sung dải tag kỹ năng "chạy chạy" (marquee) ở giữa phần About và Experience theo phong cách dải đôi (2 hàng ngược chiều nhau) kèm icon công nghệ (Tabler Icons), tối ưu theo các chuẩn tốt nhất của cộng đồng (Pure CSS 60fps, WCAG 2.2.2 Pause on hover/focus, Mask fade 2 mép, aria-hidden chống đọc trùng cho screen reader).

## Assumptions

- Sử dụng font icon Tabler Icons (`ti ti-*`) đã có sẵn trong theme LoveIt, không cần kéo thêm thư viện font ngoài để tránh tăng bundle size.
- Quản lý dữ liệu tập trung qua `data/tech_stack.yaml` để dễ dàng thêm bớt hoặc đổi icon mà không cần can thiệp vào code template.
- Tích hợp vào `content/_index.md` qua shortcode `{{< tech-marquee >}}` giúp giữ nguyên kiến trúc Markdown mà không phá vỡ template gốc của theme.

## Approach

Xây dựng component dải đôi kỹ năng (Dual-Row Tech Marquee) gồm:
1. `data/tech_stack.yaml`: Chứa danh sách 2 hàng công nghệ phân bổ đồng đều (Row 1: Backend, Cloud, AI; Row 2: Languages, Frontend, Database, DevOps) kèm tên và class icon Tabler.
2. `layouts/partials/home/tech-marquee.html` và `layouts/shortcodes/tech-marquee.html`: Render cấu trúc HTML ngữ nghĩa, mỗi hàng chứa 1 track nội dung chính và 1 track clone có `aria-hidden="true"` để loop vô tận.
3. `assets/css/modules/_marquee.scss`: Module SCSS chứa animation `@keyframes marquee-scroll-left` và `marquee-scroll-right` dựa trên `transform: translate3d()`, gradient fade mask ở 2 mép bằng `mask-image`, cơ chế pause trên `:hover` / `:focus-within`, và fallback `@media (prefers-reduced-motion: reduce)`.
4. Nhúng shortcode vào `content/_index.md` ngay trước mục Experience.
5. Kiểm thử biên dịch Hugo (`hugo --buildDrafts`).

## Not Building

- Không dùng JavaScript để điều khiển chuyển động cuộn (tránh layout thrashing và ngốn pin CPU).
- Không thêm link click trực tiếp vào từng tag chạy để tránh bẫy tiêu điểm (focus trap) và scroll jump khi di chuyển bằng phím Tab.

## Progress

| Status | Phase | Task |
| --- | --- | --- |
| ✅ DONE | Phase 1 | Task 1: Tạo file dữ liệu `data/tech_stack.yaml` với Devicon & SVG |
| ✅ DONE | Phase 1 | Task 2: Tạo module SCSS `assets/css/modules/_marquee.scss` và import vào `_custom.scss` |
| ✅ DONE | Phase 1 | Task 3: Tạo layout partial và shortcode `tech-marquee` trong Hugo |
| ✅ DONE | Phase 1 | Task 4: Nhúng shortcode `{{< tech-marquee >}}` vào `content/_index.md` và load Devicon CDN |
| ✅ DONE | Phase 1 | Task 5: Thẩm định biên dịch `hugo --buildDrafts` và kiểm tra toàn diện |

## Tasks

#### Phase 1 [sequential]

1. Tạo file dữ liệu `data/tech_stack.yaml` với Devicon & SVG
   - Files: `data/tech_stack.yaml`
   - Description: Định nghĩa 2 danh sách công nghệ (`row_1` và `row_2`), mỗi mục gồm `name` và `icon` (class Devicon chuẩn như `devicon-python-plain colored`, `devicon-fastapi-plain colored`, `devicon-docker-plain colored`...) hoặc `svg: "gemini"` cho Google Gemini.
   - Verify: File YAML hợp lệ, đọc được qua lệnh `python3 -c "import yaml; yaml.safe_load(open('data/tech_stack.yaml'))"`.

2. Tạo module SCSS `assets/css/modules/_marquee.scss` và import vào `_custom.scss`
   - Files: `assets/css/modules/_marquee.scss`, `assets/css/_custom.scss`
   - Description:
     - Định nghĩa container `.tech-marquee-wrapper` với `overflow: hidden`, `position: relative`, và gradient mask ở hai đầu (`mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent)`).
     - Tạo 2 hàng `.marquee-row` chạy ngược chiều: row 1 (`marquee-scroll-left`), row 2 (`marquee-scroll-right`).
     - Tốc độ chạy êm dịu (khoảng 30s-40s).
     - Định nghĩa `.tech-pill` dùng design tokens hiện có (`var(--clr-surface-3)`, `var(--clr-border)`, `var(--clr-text-2)`), đồng bộ với dark/light mode.
     - `@media (hover: hover)`: `.tech-marquee-wrapper:hover .marquee-track { animation-play-state: paused; }`.
     - `.tech-marquee-wrapper:focus-within .marquee-track { animation-play-state: paused; }`.
     - `@media (prefers-reduced-motion: reduce)`: Tắt animation, track clone ẩn (`display: none`), track chính hiển thị dạng static wrap.
   - Verify: Import không xung đột, biên dịch SCSS thông qua Hugo không lỗi cú pháp.

3. Tạo layout partial và shortcode `tech-marquee` trong Hugo
   - Files: `layouts/partials/home/tech-marquee.html`, `layouts/shortcodes/tech-marquee.html`
   - Description:
     - Partial đọc dữ liệu từ `site.Data.tech_stack`.
     - Render 2 hàng, mỗi hàng lặp 2 track (track 1 bình thường, track 2 có `aria-hidden="true"`).
     - Shortcode gọi partial `{{ partial "home/tech-marquee.html" . }}`.
   - Verify: File partial và shortcode tồn tại đúng đường dẫn.

4. Nhúng shortcode vào `content/_index.md`
   - Files: `content/_index.md`
   - Description: Đặt shortcode `{{< tech-marquee >}}` ở vị trí giữa phần GitHub Activity và thẻ phân cách `---` trước `## Experience`.
   - Verify: Vị trí xuất hiện tự nhiên, không làm vỡ các khối Markdown xung quanh.

5. Thẩm định biên dịch `hugo --buildDrafts` và kiểm tra toàn diện
   - Files: Kiểm tra toàn bộ trang chủ
   - Description: Chạy `hugo --buildDrafts`, kiểm tra HTML đầu ra trong `public/index.html` xem dải marquee có đầy đủ các tag, class và thuộc tính trợ năng (`role="region"`, `aria-label`, `aria-hidden="true"`).
   - Verify: Lệnh `hugo --buildDrafts` thoát với mã 0, không có warning hay shortcode error.

## Risks

- **Icon missing class:** Nếu class icon Tabler không khớp, icon có thể không hiển thị hoặc bị trống -> Giải pháp: Dùng các class Tabler phổ biến đã được kiểm tra (vd: `ti ti-brand-python`, `ti ti-brand-docker`, `ti ti-brand-aws`, `ti ti-brand-react`, `ti ti-database`, `ti ti-server`).
- **Glitches hoặc Stutter trên Safari/Mobile:** Do render subpixel hoặc transition -> Giải pháp: Sử dụng `transform: translate3d(..., 0, 0)` và `will-change: transform` để ép trình duyệt render qua GPU.
- **Horizontal scrollbar leakage:** Nếu container con tràn ra ngoài viewport -> Giải pháp: Đặt `overflow: hidden; width: 100%; max-width: 100%;` chặt chẽ trên wrapper.

## Next Steps

Sau khi kế hoạch được phê duyệt: kích hoạt `cf-tdd` để triển khai tuần tự theo checklist.
