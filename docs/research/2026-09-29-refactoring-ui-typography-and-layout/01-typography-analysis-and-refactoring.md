# Nghiên Cứu Chuyên Sâu: Typography (Thiết Kế Chữ Viết) Trong my_website Dựa Trên Refactoring UI

## Key Questions

- Hệ thống Font Size Scale của `my_website` được định nghĩa thế nào, có thỏa mãn quy tắc 8-10 cỡ chữ cố định không?
- Tỉ lệ giữa Line-height và Font Size có tuân thủ quy tắc tỉ lệ nghịch (text nhỏ giãn rộng, heading lớn thu hẹp) không?
- Các đơn vị đo lường font size có tránh được cạm bẫy cascading của đơn vị `em` không?
- Chiều rộng dòng văn bản (measure / line length) có đạt ngưỡng lý tưởng 45-75 ký tự không?
- Việc căn chỉnh baseline và xử lý `letter-spacing` cho chữ in hoa (all-caps) đã được tối ưu ra sao?

## Findings

### 1. Hệ thống Font Size Scale (Scale cố định vs Scale ngẫu nhiên)

Theo **Chương 2 và Chương 5 của Refactoring UI**:
- Developer không nên chọn font size tùy tiện hoặc phụ thuộc hoàn toàn vào Modular Scale hình thức (như Golden Ratio `1.618` vì dễ sinh số lẻ khó dùng).
- Khuyến nghị xây dựng thủ công một thang đo gồm **8-10 nấc cố định** để dễ dàng đưa ra quyết định thiết kế.

**Thực trạng trong codebase `assets/css/modules/_typography_and_nav.scss`:**
```scss
--fs-xs: 0.75rem;     // 12px
--fs-sm: 0.875rem;    // 14px (Meta, tags, caption)
--fs-base: 1.125rem;  // 18px (Body text)
--fs-md: 1.15rem;     // 18.4px (RẤT GẦN base)
--fs-lg: 1.25rem;     // 20px
--fs-xl: 1.35rem;     // 21.6px (RẤT GẦN lg)
--fs-2xl: 1.5rem;     // 24px
--fs-3xl: 2.15rem;    // 34.4px
--fs-h1: 2.125rem;    // 34px
--fs-h2: 1.475rem;    // 23.6px
--fs-h3: 1.25rem;     // 20px
--fs-h4: 1.125rem;    // 18px
```

*Đánh giá và Điểm vênh:*
- Dự án đã định nghĩa sẵn hệ thống token rõ ràng, không dùng số vãng lai trong style con.
- Tuy nhiên, tồn tại sự chồng lấn bước nhảy: `--fs-md` (18.4px) chỉ nhỉnh hơn `--fs-base` (18px) đúng 0.4px; `--fs-xl` (21.6px) chỉ hơn `--fs-lg` (20px) 1.6px. Mắt người hầu như không phân biệt được sự phân cấp này.
- **Giải pháp tối ưu hóa:** Rút gọn và giãn đều các nấc:
  - Level 1: `0.75rem` (12px)
  - Level 2: `0.875rem` (14px)
  - Level 3: `1rem` (16px)
  - Level 4: `1.125rem` (18px - Body base)
  - Level 5: `1.375rem` (22px - Subtitle / H3)
  - Level 6: `1.625rem` (26px - H2)
  - Level 7: `2.125rem` (34px - H1)

---

### 2. Tỉ lệ nghịch giữa Line-height và Font Size

Theo **Chương 5 của Refactoring UI**:
- **Text nhỏ (body, caption):** Cần line-height lớn (`1.5` đến `2.0`, tương đương `150% - 200%`) để mắt người đọc dễ dàng quay lại đầu dòng tiếp theo mà không bị nhảy dòng nhầm.
- **Heading lớn (H1, H2):** Chiều cao chữ đã lớn, nếu giữ line-height cao sẽ khiến heading trông như hai đoạn văn rời rạc. Cần giảm line-height xuống `1.1` đến `1.3`.

**Thực trạng trong codebase `assets/css/modules/_typography_and_nav.scss`:**
```scss
--lh-h1: 1.25;        // Heading 34px -> line-height 1.25 (Cực chuẩn)
--lh-h2: 1.32;        // Heading 23.6px -> line-height 1.32
--lh-h3: 1.4;         // Heading 20px -> line-height 1.4
--lh-h4: 1.45;        // Heading 18px -> line-height 1.45
--lh-normal: 1.6;     // UI text
--lh-relaxed: 1.76;   // Body prose 18px -> line-height 1.76
```

*Đánh giá:* **Xuất sắc 10/10**. Dự án áp dụng nguyên lý này một cách triệt để và khoa học. Khoảng cách dòng của body text font `Newsreader` đạt độ thoáng cao (1.76), trong khi H1 (1.25) rất gọn gàng, đậm chất báo chí/editorial.

---

### 3. Đơn vị đo lường: Loại bỏ hoàn toàn bẫy Cascading của `em`

Theo **Chương 5 của Refactoring UI**:
- Đơn vị `em` phụ thuộc vào font size của thẻ cha, dẫn đến việc lồng nhau (nested elements như `ul > li > ul > li` hoặc `span` trong `p`) làm font size bị co giãn ngoài tầm kiểm soát.
- Khuyên dùng `rem` hoặc `px` cho toàn bộ `font-size`.

**Thực trạng trong codebase:**
- Toàn bộ font size được khai báo bằng `rem` hoặc `px` (ví dụ: `font-size: var(--fs-base)`, `font-size: 1.15rem`, `font-size: 24px`).
- Một số ít trường hợp dùng `em` nhưng chỉ dành cho Icon: `font-size: 1.35em` cho Tabler icons để icon co giãn tự nhiên theo font size của text đi kèm.
*Đánh giá:* **Tuyệt đối an toàn và đúng chuẩn.**

---

### 4. Chiều rộng dòng lý tưởng (Optimal Reading Measure: 45-75 ký tự)

Theo **Chương 5 của Refactoring UI**:
- Dòng văn bản kéo dài từ mép trái sang mép phải màn hình máy tính gây mỏi cổ và mắt mệt mỏi khi lia dòng.
- Độ dài lý tưởng của một dòng văn bản nên nằm trong khoảng **45 đến 75 ký tự** (tương đương khoảng 600px - 750px với font 16px - 18px).

**Thực trạng trong codebase `assets/css/_custom.scss`:**
```scss
:root {
    --shell-width: 750px;
    --wide-width: 750px;
    --prose-width: 750px;
}
.page {
    width: 100% !important;
    max-width: var(--shell-width, 750px) !important;
    margin: 0 auto !important;
    padding-left: var(--gutter-desktop, 1.5rem) !important;
    padding-right: var(--gutter-desktop, 1.5rem) !important;
}
```

*Đánh giá:*
- Với container giới hạn 750px, trừ đi 2 mép padding `1.5rem` (48px) ➔ bề rộng vùng đọc thực tế là **702px**.
- Đối với font chữ `Newsreader` 18px, một dòng chứa trung bình **68 - 80 ký tự** tiếng Việt có dấu.
*Đánh giá:* **Rất vừa vặn**, tạo trải nghiệm đọc như trên một cuốn sách hoặc tạp chí in cao cấp.

---

### 5. Căn lề và Kerning / Letter-spacing cho chữ All-Caps

Theo **Chương 5 của Refactoring UI**:
- **Chữ All-Caps (In hoa toàn bộ):** Vì tất cả các ký tự in hoa đều có chung chiều cao (cap-height), chữ in hoa nhìn như một khối chữ nhật đồng dạng, rất khó phân biệt chữ nếu để letter-spacing mặc định. Luôn phải **tăng letter-spacing** cho chữ in hoa.
- **Headings lớn:** Ngược lại, headings kích thước lớn cần giảm nhẹ letter-spacing (optical kerning) để các chữ không bị thưa thớt.

**Thực trạng trong codebase:**
```scss
--ls-normal: 0.01em;
--ls-h1: -0.015em;    // Thu hẹp nhẹ kerning cho Heading lớn
--ls-h2: -0.008em;
--ls-caps: 0.05em;    // Mở rộng letter-spacing cho chữ in hoa

#toc-auto .toc-title {
  font-size: var(--fs-sm) !important;
  font-weight: var(--fw-bold) !important;
  letter-spacing: var(--ls-caps) !important;
  text-transform: uppercase !important;
}
```

*Đánh giá:* Áp dụng chính xác cả hai kỹ thuật: thu hẹp kerning của H1/H2 và nới rộng `0.05em` cho TOC Title in hoa.

## Code Examples

```scss
// Ví dụ tinh chỉnh hoàn thiện thang Font Size Token cho my_website
:root {
  --fs-xs:   0.75rem;   // 12px - Timestamps, code badges
  --fs-sm:   0.875rem;  // 14px - Meta data, caption, tags
  --fs-base: 1.125rem;  // 18px - Body editorial prose
  --fs-md:   1.35rem;   // 21.6px - Subheadings / H3
  --fs-lg:   1.625rem;  // 26px - Section title / H2
  --fs-xl:   2.125rem;  // 34px - Article title / H1
}
```

## Sources

- [Refactoring UI: Những Nguyên Tắc Thiết Kế Giao Diện Cho Developer](file:///home/ngoctin/Projects/my_website/content/posts/refactoring-ui-design-principles.md) — _primary_
- [Refactoring UI Book by Adam Wathan & Steve Schoger](https://www.refactoringui.com/) — _primary_
- Codebase source: `assets/css/modules/_typography_and_nav.scss` — _primary_

## Notes

- Token `--font-sans` hiện đang trỏ về `var(--font-serif)` (`Newsreader`). Điều này phản ánh chủ đích cá nhân của tác giả muốn tạo phong cách đọc thuần Editorial Book.
- Font tiếng Việt có dấu cần giữ `line-height >= 1.7` cho body text như dự án đang làm để tránh tình trạng các dấu mũ và dấu móc bị chạm vào dòng trên.
