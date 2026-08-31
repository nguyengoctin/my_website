---
slug: 2026-08-31-refactor-mermaid-config-and-posts
auto: false
status: done
---

# Plan: Refactor Cấu Hình Mermaid JS và Tối Ưu Bố Cục Biểu Đồ Bài Viết

**Mode:** normal

## Context
Sơ đồ Mermaid trên hệ thống hiện tại xuất hiện hiện tượng khoảng cách và độ phồng quá lớn (do `nodePadding: 20`, `rankSpacing: 50`, `nodeSpacing: 50`, `fontSize: 15.5px`) và các nút hình thoi / chuỗi dọc trong bài viết bị rỗng lỗ hổng lớn.

## Assumptions
- Không sửa file `hugo.toml` hoặc can thiệp theme gốc.
- Mọi thay đổi tập trung vào `layouts/_partials/plugin/mermaid.html`, `assets/css/modules/_mermaid.scss` và bài viết Markdown.

## Approach
- Thu gọn các thông số sizing/spacing trong `_baseConfig` ở `mermaid.html`.
- Bổ sung bảo vệ `foreignObject` trong `_mermaid.scss`.
- Cập nhật cú pháp các khối Mermaid trong bài viết [content/posts/chuan-muc-viet-prompt-tu-yeu-cau-mo-ho-den-ban-dac-ta.md](file:///home/ngoctin/Projects/my_website/content/posts/chuan-muc-viet-prompt-tu-yeu-cau-mo-ho-den-ban-dac-ta.md) để biểu đồ gọn gàng, cân đối.

## Progress

| Status  | Phase   | Task |
| ------- | ------- | ---- |
| ✅ DONE | Phase 1 | Cập nhật cấu hình toàn cục tại `mermaid.html` & `_mermaid.scss` |
| ✅ DONE | Phase 1 | Tối ưu hóa các khối Mermaid trong bài viết prompt |
| ✅ DONE | Phase 1 | Thẩm định build `hugo --buildDrafts` và hiển thị thực tế |

## Tasks

#### Phase 1 [sequential]

1. Cập nhật `layouts/_partials/plugin/mermaid.html` và `assets/css/modules/_mermaid.scss`
   - Files: `layouts/_partials/plugin/mermaid.html`, `assets/css/modules/_mermaid.scss`
   - Verify: Chạy `hugo --buildDrafts` thành công.
2. Tinh chỉnh các sơ đồ Mermaid trong `content/posts/chuan-muc-viet-prompt-tu-yeu-cau-mo-ho-den-ban-dac-ta.md`
   - Files: `content/posts/chuan-muc-viet-prompt-tu-yeu-cau-mo-ho-den-ban-dac-ta.md`
   - Verify: `hugo --buildDrafts`
3. Kiểm tra tổng thể giao diện và render trên Hugo dev server
   - Verify: Kiểm tra console và log server, không có warning/error.

## Risks
- Tránh can thiệp `font-size` trực tiếp qua CSS ngoài lên SVG để không làm sai lệch bounding box.

## Next Steps
Sau khi hoàn thành: `/cf-review` → `/cf-commit`
