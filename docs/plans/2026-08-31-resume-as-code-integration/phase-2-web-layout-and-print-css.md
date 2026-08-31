# Phase 2: Web Layout và Print CSS Engineering

**Plan:** [README.md](./README.md)
**Type:** sequential

## Progress

| Status | Task |
| :--- | :--- |
| ✅ DONE | Task 3: Xây dựng module SCSS `_cv.scss` và import vào theme |
| ✅ DONE | Task 4: Refactor `layouts/cv/single.html` sang Native Semantic HTML |

## Tasks

1. **Xây dựng module SCSS `_cv.scss` và import vào theme**
   - Files: `assets/css/modules/_cv.scss`, `assets/css/_override.scss`
   - Description: Thiết kế hệ thống styles hoàn chỉnh cho trang CV:
     - Giao diện web responsive: Thẻ container dạng card sang trọng, hiệu ứng hover tinh tế, Dark Mode tự động theo biến theme của LoveIt.
     - Toolbar: Nút tải file PDF (`/cv/Nguyen_Ngoc_Tin-CV.pdf`) và nút in trực tiếp (`window.print()`).
     - Print CSS `@media print`: Ẩn hoàn toàn header/footer/sidebar, căn chỉnh lề `@page` A4, `break-inside: avoid` cho từng mục kinh nghiệm để tránh ngắt trang lỗi.
   - Verify: Kiểm tra file SCSS compile thành công qua Hugo pipeline.

2. **Refactor `layouts/cv/single.html` sang Native Semantic HTML**
   - Files: `layouts/cv/single.html`
   - Description: Loại bỏ hoàn toàn thư viện bên ngoài PDF.js và canvas, thay thế bằng template Go HTML render trực tiếp từ `data/cv.yaml`. Áp dụng `markdownify` cho các bullet points để hỗ trợ định dạng bold/links.
   - Verify: Truy cập trang `/cv/` trên local server xem giao diện hiển thị tức thì (0ms loading), font chữ sắc nét và text selectable 100%.
