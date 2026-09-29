# Research: Đối Chiếu Hệ Thống Typography & Layout/Spacing Của my_website Với Cuốn Sách Refactoring UI

**Date:** 2026-09-29
**Scope:** Khảo sát, phân tích toàn diện mã nguồn CSS/SCSS và các thành phần giao diện của dự án `my_website` dựa trên hệ thống nguyên tắc thiết kế từ cuốn sách *Refactoring UI* (Adam Wathan & Steve Schoger), tập trung vào hai mảng cốt lõi: Thiết kế chữ viết (Typography) và Bố cục & Khoảng trắng (Layout and Spacing).

## Overview

Dự án `my_website` sở hữu nền tảng kiến trúc CSS được tổ chức rất chặt chẽ, áp dụng hầu như triệt để các triết lý thiết kế hiện đại của *Refactoring UI*. Hệ sinh thái giao diện nổi bật với kiến trúc "Single Shell" 750px nhất quán từ Header đến Footer, luật Gestalt Proximity thể hiện qua tỉ lệ margin đỉnh/đáy 3:1 ở các thẻ Heading, nguyên lý tỉ lệ nghịch giữa Font Size và Line-height, cùng việc dùng Accent Border và Tinted Background thay cho việc lạm dụng Border đóng hộp. Điểm cần hoàn thiện duy nhất nằm ở việc tinh chỉnh các bước nhảy trong thang Font Size Scale và làm tròn các token khoảng cách lẻ theo chuẩn Grid 8px/16px.

## Key Findings

1. **Tuân thủ xuất sắc luật Gestalt Proximity (Chương 4):** Khoảng cách từ Heading đến đoạn văn bên dưới (đáy) luôn nhỏ hơn khoảng cách từ đoạn văn bên trên đến Heading (đỉnh) theo tỉ lệ xấp xỉ 3:1 (H2: top 40px / bottom 13.6px; H3: top 28px / bottom 8px). Điều này tạo liên kết thị giác tự nhiên và loại bỏ cảm giác trôi nổi của tiêu đề.
2. **Áp dụng chuẩn xác tỉ lệ nghịch giữa Font Size và Line-height (Chương 5):** Text nhỏ có line-height lớn (Body text `Newsreader` 18px đạt line-height `1.76` rất thoáng), trong khi Heading lớn thu hẹp line-height về `1.25` (H1) và `1.32` (H2), giữ cho tiêu đề không bị vỡ vụn.
3. **Độ rộng dòng đọc lý tưởng (Optimal Measure: 45-75 ký tự):** Kiến trúc Shell cố định 750px (vùng nội dung thực 702px sau padding) tạo ra dòng văn bản trung bình 68-80 ký tự, mang lại trải nghiệm đọc sách cao cấp, không bị căng mắt trên màn hình lớn.
4. **Cơ chế Responsive linh hoạt:** Khi chuyển từ Desktop sang Mobile, tỉ lệ phóng đại của Heading được hạ bớt (từ 1.88x xuống 1.64x) và khoảng cách đỉnh thu hẹp từ 40px xuống 29.6px, tối ưu không gian hiển thị cho màn hình hẹp.
5. **Cơ hội cải tiến (Gaps):** Token `--fs-md` (18.4px) quá sát `--fs-base` (18px) và `--space-p: 1.45rem` (23.2px) có thể được chuẩn hóa về Grid 8px (`1.5rem` = 24px) để đạt độ nhất quán tuyệt đối.

## Parts

| # | Document | Description |
|---|----------|-------------|
| 1 | [01-typography-analysis-and-refactoring.md](01-typography-analysis-and-refactoring.md) | Phân tích hệ thống Font Size Scale, tỉ lệ Line-height, đơn vị Rem vs Em, độ dài dòng văn bản và Kerning All-Caps. |
| 2 | [02-layout-spacing-and-visual-hierarchy.md](02-layout-spacing-and-visual-hierarchy.md) | Phân tích kiến trúc Single Shell 750px, luật Proximity 3:1, hệ thống Spacing Grid 8px/16px và cách phân tách khối không dùng border. |

## Open Questions

- Liệu có nên bổ sung một phông chữ Sans-serif trung tính (Neutral Sans-serif như Inter hoặc Geist) cho các khối dữ liệu kỹ thuật/bảng biểu, hay tiếp tục duy trì 100% Serif (`Newsreader`) cho toàn bộ site theo định hướng Editorial?
- Có nên áp dụng thêm fluid typography (sử dụng hàm `clamp()`) cho Heading H1/H2 để chuyển đổi mượt mà giữa các kích thước màn hình thay vì ngắt đột ngột tại breakpoint 768px?

## Recommended Next Steps

- **Chuẩn hóa token thang Font Size:** Loại bỏ sự chồng lấn giữa `--fs-base` (18px) và `--fs-md` (18.4px) trong `_typography_and_nav.scss`.
- **Làm tròn Spacing Tokens theo Base 8px:** Cập nhật `--space-p: 1.5rem` (24px) và `--space-h2-bottom: 0.75rem` (12px).
- **Khởi chạy `/cf-plan`:** Nếu muốn bắt tay triển khai chuẩn hóa các token này mà không làm ảnh hưởng đến giao diện hiện tại.
