# Kỹ Thuật Layout Web và Print CSS Đạt Chuẩn A4 trong Hugo

## Key Questions

- Làm thế nào để trang `/cv` vừa hiển thị responsive đẹp mắt trên trình duyệt (hỗ trợ dark mode, liên kết tương tác) vừa xuất ra bản in A4 hoàn hảo khi người dùng bấm Print (`Ctrl + P`)?
- Các quy tắc CSS Paged Media nào là bắt buộc để ngăn chặn lỗi ngắt trang cắt đôi dòng chữ hoặc để lại tiêu đề lẻ loi (widows and orphans)?
- Cách xử lý triệt để việc ẩn các thành phần thừa của theme (header, navigation, footer, nút toggle dark mode) khi kích hoạt chế độ in?

## Findings

### Cơ chế CSS Paged Media và Quy Chuẩn Khổ Trang A4

Khi chuyển đổi một trang web HTML sang tài liệu in ấn hoặc PDF, trình duyệt tuân theo quy chuẩn CSS Paged Media:
1. **Khai báo `@page`:** Xác định kích thước khổ giấy tiêu chuẩn (`size: A4 portrait` hoặc `size: letter portrait`) và lề trang (`margin`).
2. **Kiểm soát ngắt trang (Page Breaking):**
   - Dùng thuộc tính hiện đại `break-inside: avoid` (kèm fallback `page-break-inside: avoid`) trên từng khối công việc (`.resume-item`), khối kỹ năng để đảm bảo trình duyệt không bao giờ cắt đôi một mục kinh nghiệm giữa hai trang giấy.
   - Dùng `break-after: avoid` trên các tiêu đề (`h2`, `h3`) để ngăn hiện tượng "tiêu đề mồ côi" (orphan heading) nằm ở cuối trang 1 trong khi nội dung nằm ở đầu trang 2.
3. **Typography cho In Ấn:**
   - Đơn vị đo lường: Khi in ấn, nên chuyển đổi đơn vị font từ `rem`/`px` sang `pt` (point) hoặc giữ tỉ lệ cân đối để văn bản sắc nét trên giấy (ví dụ: Body text 10pt - 10.5pt, Heading 12pt - 14pt, Name 18pt - 22pt).
   - Tối ưu màu sắc: Ép màu chữ về `#000` hoặc `#111` và nền trắng `#fff`, tắt toàn bộ gradient và background shadows để tránh tốn mực và giảm độ tương phản.

### Xử lý cô lập Layout trong Hugo

Để trang CV không bị ảnh hưởng bởi CSS phức tạp của toàn bộ blog:
- Sử dụng layout độc lập: Trong Hugo, có thể tạo `layouts/page/cv.html` hoặc `layouts/cv/single.html`.
- Nút Action trên Web: Thêm thanh công cụ nhỏ ở đầu trang (chỉ hiện trên màn hình, ẩn khi in) gồm nút "Tải bản PDF" và nút "In trang này" (`window.print()`).
- Tự động mở rộng URL khi in: CSS có thể tự động in kèm URL của các liên kết quan trọng bên cạnh text bằng pseudo-element `::after` nếu cần thiết, hoặc ẩn bớt các link rác.

## Code Examples

### Print Stylesheet Chuẩn Công Nghiệp (`assets/css/modules/_cv-print.scss`)

```scss
/* ==========================================================================
   CV Print and Layout Optimization
   ========================================================================== */

/* 1. Màn hình Web thông thường */
.resume-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  line-height: 1.5;
  color: var(--text-color, #1a202c);
  background-color: var(--bg-color, #ffffff);
}

.resume-toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-bottom: 2rem;

  .btn-print {
    padding: 0.5rem 1rem;
    font-weight: 500;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    background: #f8fafc;
    cursor: pointer;
    transition: background 0.2s ease;

    &:hover {
      background: #e2e8f0;
    }
  }
}

/* 2. Quy chuẩn khi In hoặc Xuất PDF (@media print) */
@media print {
  /* Thiết lập khổ giấy và lề trang */
  @page {
    size: A4 portrait;
    margin: 12mm 15mm 12mm 15mm;
  }

  /* Ẩn toàn bộ thành phần giao diện web */
  header.header,
  footer.footer,
  nav.navigation,
  .sidebar,
  .resume-toolbar,
  .theme-toggle,
  #back-to-top {
    display: none !important;
  }

  /* Reset layout và ép nền trắng chữ đen */
  body,
  main,
  .resume-container {
    margin: 0 !important;
    padding: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    background: #ffffff !important;
    color: #000000 !important;
    font-size: 10pt !important;
    line-height: 1.35 !important;
  }

  /* Tiêu đề chính */
  .resume-name {
    font-size: 18pt !important;
    margin-bottom: 2pt !important;
  }

  .resume-title {
    font-size: 11pt !important;
    color: #333333 !important;
  }

  /* Chống ngắt trang lỗi */
  h2, h3, .resume-section-title {
    break-after: avoid !important;
    page-break-after: avoid !important;
    font-size: 12pt !important;
    border-bottom: 1px solid #333333 !important;
    margin-top: 10pt !important;
    margin-bottom: 4pt !important;
  }

  .resume-item,
  .resume-section,
  .skills-grid {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
    margin-bottom: 8pt !important;
  }

  /* Giữ liên kết sạch sẽ */
  a {
    text-decoration: none !important;
    color: #000000 !important;
  }
}
```

### Script kích hoạt Print trên giao diện Web

```html
<div class="resume-toolbar">
  <a href="/cv.pdf" class="btn-print" download>Tải PDF Chuẩn</a>
  <button class="btn-print" onclick="window.print()">In hoặc Lưu PDF</button>
</div>
```

## Sources

- [MDN Web Docs: CSS Paged Media and @page](https://developer.mozilla.org/en-US/docs/Web/CSS/@page) — _primary_
- [MDN Web Docs: CSS break-inside property](https://developer.mozilla.org/en-US/docs/Web/CSS/break-inside) — _primary_
- [Designing For Print With CSS (Smashing Magazine)](https://www.smashingmagazine.com/2015/01/designing-for-print-with-css/) — _primary_
- [CSS-Tricks: A Guide to CSS Print Stylesheets](https://css-tricks.com/css-tricks-guides/guide-to-css-print/) — _secondary / background_

## Notes

- Trình duyệt Chromium (Chrome, Edge, Brave) hỗ trợ in ra PDF chính xác nhất theo chuẩn CSS `@page`. Firefox có một số sai lệch nhỏ về tính toán margin của `@page`.
- Thuộc tính `break-inside: avoid` là giải pháp thay thế chuẩn hiện đại cho `page-break-inside: avoid`, tuy nhiên chúng ta nên khai báo cả hai để đảm bảo tương thích ngược.
