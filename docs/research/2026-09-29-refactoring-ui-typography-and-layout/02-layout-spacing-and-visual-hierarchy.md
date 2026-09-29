# Nghiên Cứu Chuyên Sâu: Layout, Spacing & Visual Hierarchy Trong my_website Dựa Trên Refactoring UI

## Key Questions

- Bố cục container của `my_website` có tuân thủ nguyên tắc "Đừng ép element lấp đầy màn hình" của Refactoring UI không?
- Hệ thống Spacing của trang có dựa trên Base Grid 8px/16px hay tồn tại các giá trị tùy tiện?
- Quy tắc Proximity (Khoảng cách bao quanh nhóm luôn lớn hơn khoảng cách bên trong nhóm) được triển khai thế nào giữa Headings, Đoạn văn và Khối nội dung?
- Việc xây dựng phân cấp thị giác (Visual Hierarchy) bằng màu sắc, trọng lượng và nền (thay vì lạm dụng đường viền - borders) được áp dụng ra sao?
- Kích thước phần tử và khoảng cách có scale mượt mà và hợp lý trên thiết bị di động (Responsive Scaling) không?

## Findings

### 1. Không ép element lấp đầy màn hình (Give elements room to breathe)

Theo **Chương 4 của Refactoring UI**:
- Màn hình rộng không đồng nghĩa với việc nội dung phải căng tràn toàn bộ không gian.
- Nếu một thành phần chỉ cần 600px - 750px để đọc tốt nhất, hãy cố định độ rộng đó và để không gian hai bên tự do (whitespace).
- Điều này tạo cảm giác thư thái, loại bỏ cảm giác căng thẳng, rối rắm cho người dùng.

**Thực trạng trong codebase `assets/css/_custom.scss`:**
```scss
:root {
    --shell-width: 750px;
    --wide-width: 750px;
    --prose-width: 750px;
    --gutter-desktop: 1.5rem;
    --gutter-mobile: 1rem;
}

.page.single,
.page.home,
.page.archive,
.page.categories {
    max-width: var(--shell-width, 750px) !important;
}

#header-desktop .header-wrapper,
.custom-footer-wrapper {
    max-width: var(--shell-width, 750px) !important;
}
```

*Đánh giá:* **Xuất sắc 10/10**. Dự án áp dụng triết lý "Single Shell Architecture" duy nhất một độ rộng 750px từ Header ➔ Content ➔ Footer. Cho dù người dùng mở trang web trên màn hình Ultra-wide 4K, nội dung vẫn được căn giữa thanh lịch, không bị dãn bè gây vỡ bố cục.

---

### 2. Quy tắc Proximity (Luật Gestalt về Khoảng cách gần)

Theo **Chương 4 của Refactoring UI**:
- **Nguyên tắc vàng:** Khoảng cách **xung quanh một nhóm** luôn phải lớn hơn khoảng cách **bên trong nhóm** đó.
- Điển hình nhất là Tiêu đề (Headings): Khoảng cách từ Heading đến đoạn văn bên dưới (đoạn văn thuộc về nó) phải **nhỏ hơn rất nhiều** so với khoảng cách từ đoạn văn bên trên tới Heading đó. Nếu hai khoảng cách này bằng nhau, người đọc sẽ cảm thấy Heading lơ lửng ở giữa không gian chết.

**Thực trạng trong codebase `assets/css/modules/_typography_and_nav.scss`:**
```scss
--space-h2-top: 2.5rem;     // 40px - Khoảng cách đỉnh H2
--space-h2-bottom: 0.85rem; // 13.6px - Khoảng cách đáy H2 (Tỉ lệ xấp xỉ 3:1)

h2 {
  margin-top: var(--space-h2-top) !important;
  margin-bottom: var(--space-h2-bottom) !important;
}

h3 {
  margin-top: 1.75rem !important; // 28px
  margin-bottom: 0.5rem !important;  // 8px (Tỉ lệ 3.5:1)
}

h4 {
  margin-top: 1.4rem !important;
  margin-bottom: 0.45rem !important;
}

// Xóa bỏ khoảng cách chết khi có đường kẻ ngang đứng trước Heading
hr + h2, hr + h3, hr + h4 {
  margin-top: 0.25rem !important;
}
```

*Đánh giá:* **Điểm sáng vượt trội**. `my_website` cài đặt tỉ lệ margin đỉnh / đáy của H2, H3 theo tỉ lệ `3:1` và `3.5:1`. Đặc biệt, luật xử lý `hr + h2 { margin-top: 0.25rem }` triệt tiêu khoảng trắng thừa khi đã có ranh giới `hr`, thể hiện sự thấu hiểu sâu sắc về Gestalt Proximity.

---

### 3. Hệ thống Spacing Grid (Bội số 8px/16px)

Theo **Chương 2 và Chương 4 của Refactoring UI**:
- Mọi quyết định khoảng cách (margin, padding, gap) nên được lấy từ một bảng Spacing cố định (thường là thang 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px).
- Việc dùng các số lẻ (như 17px, 23px) khiến giao diện mất đi nhịp điệu thị giác (visual rhythm).

**Thực trạng trong codebase:**
- Các khoảng cách cơ bản dùng hệ đơn vị `rem` (với base font-size 16px):
  - Gutter desktop: `1.5rem` = 24px (Chuẩn)
  - Gutter mobile: `1rem` = 16px (Chuẩn)
  - Margin code block, table, video: `1.5rem` = 24px (Chuẩn)
  - Header padding: `0.75rem` (12px), `1.25rem` (20px)
- **Điểm cần tinh chỉnh:**
  - `--space-p: 1.45rem` = 23.2px (Số lẻ)
  - `--space-h2-bottom: 0.85rem` = 13.6px (Số lẻ)
- **Khuyến nghị chuẩn hóa:**
  - Đổi `--space-p` thành `1.5rem` (24px)
  - Đổi `--space-h2-bottom` thành `0.75rem` (12px) hoặc `1rem` (16px)

---

### 4. Phân tách phần tử mà không lạm dụng Border (Chương 8)

Theo **Chương 8 của Refactoring UI**:
- Border dày đặc tạo ra cảm giác tù túng, đóng hộp và khiến giao diện như bị chia nhỏ thành nhiều mảnh vụn.
- Thay vì dùng border 4 phía, có 3 cách thay thế tinh tế hơn:
  1. **Nền màu nhạt (Tinted Backgrounds):** Dùng màu nền hơi lệch tone (ví dụ xám rất nhạt `#f8fafc`).
  2. **Bóng đổ nhẹ (Subtle Box-Shadow):** Tạo chiều sâu tách lớp.
  3. **Khoảng cách trắng (Generous Spacing):** Tự khoảng trắng sẽ tạo ranh giới tự nhiên.
  4. **Accent Border:** Chỉ viền 1 cạnh (border-left hoặc border-top) để làm điểm nhấn.

**Thực trạng trong codebase `assets/css/modules/_admonitions.scss` & `_custom.scss`:**
```scss
// Admonitions / Callouts:
.admonition {
  border-radius: 8px !important;
  border-left-width: 3px !important; // Chỉ viền trái (Accent border)
  border-left-style: solid !important;
  border-top: none; border-right: none; border-bottom: none;
  background-color: #f8faff !important; // Nền sáng êm dịu
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
}

// Blockquotes:
blockquote {
  border: none !important;
  border-left: 3px solid #cbd5e1 !important;
  background-color: transparent !important;
}
```

*Đánh giá:* **Rất đúng tinh thần Refactoring UI**. Giao diện bài viết và các khối thông báo hoàn toàn không có cảm giác "đóng hộp", mắt người lướt qua rất nhẹ nhàng.

---

### 5. Responsive Sizing: Tỉ lệ co giãn thông minh trên Mobile

Theo **Chương 4 của Refactoring UI**:
- Không bao giờ giữ nguyên tỉ lệ font size hay spacing của Desktop đem xuống Mobile.
- Ví dụ: Trên Desktop, Title 45px / Body 18px (tỉ lệ 2.5x) là đẹp. Nhưng trên Mobile (body 14px - 17px), nếu nhân cứng 2.5x thì Title sẽ thành 35px - 42px ➔ Title chiếm nửa màn hình điện thoại. Thực tế Title 24px - 28px sẽ tự nhiên hơn rất nhiều.

**Thực trạng trong codebase `assets/css/modules/_typography_and_nav.scss`:**
```scss
// Desktop:
--fs-base: 1.125rem;  // 18px
--fs-h1: 2.125rem;    // 34px -> Tỉ lệ ~ 1.88x
--space-h2-top: 2.5rem;

// Mobile (@media max-width: 768px):
--fs-base: 1.0625rem; // 17px
--fs-h1: 1.75rem;     // 28px -> Tỉ lệ hạ xuống ~ 1.64x
--space-h2-top: 1.85rem; // Giảm khoảng cách đỉnh heading để tiết kiệm diện tích cuộn
```

*Đánh giá:* Thực hiện rất khéo léo. Tỉ lệ H1 trên mobile được chủ động hạ xuống mức `1.64x`, đồng thời khoảng cách giữa các phần tử cũng co gọn lại để người dùng không phải cuộn quá nhiều trang trắng vô nghĩa.

## Code Examples

```scss
// Đề xuất chuẩn hóa Spacing Tokens cho my_website theo Base 8px/16px Grid
:root {
  --space-1: 0.25rem; // 4px
  --space-2: 0.5rem;  // 8px
  --space-3: 0.75rem; // 12px
  --space-4: 1rem;    // 16px - Base unit
  --space-5: 1.5rem;  // 24px - Paragraph spacing & container gutter
  --space-6: 2rem;    // 32px
  --space-7: 2.5rem;  // 40px - H2 top margin
  --space-8: 3rem;    // 48px

  // Spacing semantic mappings
  --space-p: var(--space-5);         // 1.5rem (24px)
  --space-h2-top: var(--space-7);    // 2.5rem (40px)
  --space-h2-bottom: var(--space-3); // 0.75rem (12px) - Tỉ lệ hoàn hảo ~3.33 : 1
}
```

## Sources

- [Refactoring UI: Những Nguyên Tắc Thiết Kế Giao Diện Cho Developer](file:///home/ngoctin/Projects/my_website/content/posts/refactoring-ui-design-principles.md) — _primary_
- [Refactoring UI Book by Adam Wathan & Steve Schoger](https://www.refactoringui.com/) — _primary_
- Codebase sources: `assets/css/_custom.scss` và `assets/css/modules/_typography_and_nav.scss` — _primary_

## Notes

- Giao diện có độ hoàn thiện rất cao, áp dụng hầu như triệt để các triết lý thiết kế UI cho developer.
- Việc căn chỉnh lại vài biến token lẻ sẽ giúp codebase đạt mức độ "Pixel Perfect" theo hệ thống Grid 8px.
