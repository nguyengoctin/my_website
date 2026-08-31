# Hugo Codeblock Styling & Architecture Research Summary

## Tổng quan
Nghiên cứu tổng hợp từ cộng đồng kỹ thuật thực tế (Hugo Discourse, Hacker News, Reddit r/webdev, GitHub Issues) về tối ưu hóa hiển thị codeblock, giải quyết triệt để vấn đề xung đột CSS, bôi đen copy dính số dòng, giật lag gập mở và wrap code sai quy chuẩn.

## Tài liệu chi tiết
- [01-community-consensus-and-painpoints.md](file:///home/ngoctin/Projects/my_website/docs/research/2026-08-31-hugo-codeblock-style-audit-best-practices/01-community-consensus-and-painpoints.md): Đánh giá chi tiết sự đồng thuận và điểm đau của cộng đồng kỹ thuật.
- [02-hugo-chroma-architecture-and-overrides.md](file:///home/ngoctin/Projects/my_website/docs/research/2026-08-31-hugo-codeblock-style-audit-best-practices/02-hugo-chroma-architecture-and-overrides.md): Audit xung đột giữa config Hugo và CSS theme LoveIt cùng chiến lược override module hóa.

## Kết luận & Khuyến nghị chính
1. **Server-side Highlighting (Chroma) + `noClasses = false`** là giải pháp vàng về hiệu năng và tùy biến theme.
2. **Line Numbers dạng Table (`lineNumbersInTable = true`)** vượt trội về UX chống copy dính số dòng khi được kết hợp với `user-select: none`.
3. **Phân tách rành mạch:** Inline code cần `break-word`, trong khi Block code (`pre code`) bắt buộc giữ `white-space: pre` và `overflow-x: auto`.
4. **Loại bỏ animation gập mở bắt buộc** trên codeblock thông thường để tránh cản trở thao tác đọc và sao chép của lập trình viên.
