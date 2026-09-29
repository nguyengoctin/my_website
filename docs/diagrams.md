# Quy Chuẩn Thiết Kế và Quản Lý Sơ Đồ Vector (Diagrams)

Tài liệu này quy định chi tiết quy chuẩn tạo, lưu trữ và nhúng sơ đồ kỹ thuật vector tĩnh vào các bài viết trên hệ thống Hugo.

## 1. Triết Lý Thiết Kế
- **Không dùng Mermaid JS runtime:** Loại bỏ hoàn toàn việc phụ thuộc vào thư viện JS cồng kềnh render ở phía client.
- **Pure SVG Vector Tĩnh:** Tất cả sơ đồ được render trước thành file `.svg` chuẩn, lưu trữ tại `static/diagrams/`.
- **Hỗ trợ Sáng / Tối Song Song (Dual-Theme):** Mỗi sơ đồ luôn đi kèm 2 phiên bản:
  - `ten-so-do.svg` (Theme Sáng - Coral Zinc Light)
  - `ten-so-do-dark.svg` (Theme Tối - Coral Zinc Dark)

## 2. Công Cụ Tạo Sơ Đồ
Sử dụng AI Skill **`fireworks-tech-graph`** (hoặc script tại `scripts/generate_all_diagrams.py`) để chuyển đổi ý tưởng / luồng logic thành các file SVG chất lượng cao:
- Font chữ: `ui-sans-serif, system-ui` hoặc `IBM Plex Mono` cho mã / token.
- Node bo góc tinh tế (`rx="6"`), viền sắc sảo (`stroke-width="1.5"`).
- Màu nhấn (Accent): `#ea580c` (Cam Coral sáng) / `#fb923c` (Cam Coral tối).

## 3. Cú Pháp Nhúng vào Bài Viết
Bắt buộc sử dụng shortcode `diagram`:

```markdown
{{</* diagram src="/diagrams/ten-so-do.svg" dark="/diagrams/ten-so-do-dark.svg" alt="Mô tả sơ đồ" */>}}
```

Có thể thêm chú thích dưới hình bằng tham số `caption`:
```markdown
{{</* diagram src="/diagrams/ten-so-do.svg" dark="/diagrams/ten-so-do-dark.svg" alt="Mô tả sơ đồ" caption="Hình 1: Luồng xử lý dữ liệu" */>}}
```
