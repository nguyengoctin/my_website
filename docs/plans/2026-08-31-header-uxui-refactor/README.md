---
slug: 2026-08-31-header-uxui-refactor
auto: false
status: done
---

# Plan: Header UX/UI Refactor - Smart Sticky, Search Hotkey & Mobile Drawer Polish

**Mode:** normal
**Created:** 2026-08-31
**Status:** DONE

## Context

Dựa trên kết quả đánh giá UX/UI cộng đồng cho Header của website cá nhân/kỹ thuật, Header hiện tại sử dụng chế độ `fixed` (chiếm không gian dọc khi đọc bài) và thanh tìm kiếm thiếu phím tắt chuẩn (`Cmd+K`/`Ctrl+K`). Kế hoạch này tối ưu hóa Header sang Smart Sticky (tự ẩn khi cuộn xuống, hiện khi cuộn lên), tích hợp phím tắt tìm kiếm và cải tiến Mobile Drawer.

## Assumptions

- Hugo LoveIt theme hỗ trợ sẵn `data-header-desktop="auto"` trong `theme.js` khi cấu hình `desktopMode = "auto"`.
- Layout tùy biến `layouts/partials/header.html` cho phép nhúng script xử lý sự kiện phím tắt và toggle mà không phá vỡ tính năng Lunr search.
- Các quy chuẩn trong `AGENTS.md` (không dùng `&` trong prose, không dịch inline tiếng Anh) được tuân thủ nghiêm ngặt.

## Approach

1. **Cấu hình `hugo.toml`:** Đổi `desktopMode` từ `"fixed"` sang `"auto"` để kích hoạt Smart Sticky header.
2. **Nâng cấp `layouts/partials/header.html`:**
   - Bổ sung huy hiệu phím tắt trực quan (`kbd` badge `⌘K` / `Ctrl+K`) cho nút tìm kiếm.
   - Thêm bộ lắng nghe sự kiện phím tắt toàn cục (`Cmd+K`, `Ctrl+K`, `/` và `Escape`) để mở/đóng ô tìm kiếm mượt mà.
   - Bổ sung logic khóa cuộn `body` khi mở menu mobile.
3. **Hoàn thiện giao diện tại `assets/css/_custom.scss`:**
   - Tinh chỉnh CSS cho huy hiệu phím tắt (badge) trong thanh search.
   - Chuẩn hóa khoảng đệm (touch target >= 44px) và hiệu ứng hover/active cho menu links trên cả desktop và mobile.
   - Tối ưu transition và backdrop blur cho mobile menu.

## Not Building

- Không thay thế Lunr search bằng Algolia/Pagefind (giữ nguyên hạ tầng Lunr hiện tại).
- Không chuyển đổi sang Bottom Navigation bar trên mobile (giữ chuẩn Header top navigation).

## Progress

| Status  | Phase   | Task                                                        |
| ------- | ------- | ----------------------------------------------------------- |
| ✅ DONE | Phase 1 | Cấu hình Smart Sticky trong `hugo.toml`                     |
| ✅ DONE | Phase 1 | Tích hợp phím tắt tìm kiếm và xử lý khóa cuộn mobile        |
| ✅ DONE | Phase 1 | Tinh chỉnh SCSS cho Header, Search Badge và Mobile Drawer   |
| ✅ DONE | Phase 1 | Kiểm tra build Hugo và nghiệm thu giao diện                 |

## Tasks

#### Phase 1 [sequential]

1. **Cấu hình Smart Sticky**
   - Files: `hugo.toml`
   - Action: Cập nhật `params.header.desktopMode = "auto"`.
   - Verify: Chạy `hugo --buildDrafts` thành công, kiểm tra thuộc tính `data-header-desktop` trên thẻ `<body>`.

2. **Cập nhật Template Header và Phím tắt**
   - Files: `layouts/partials/header.html`
   - Action:
     - Thêm huy hiệu phím tắt `<kbd class="search-kbd">⌘K</kbd>` cạnh icon search.
     - Bổ sung JavaScript bắt sự kiện bàn phím `keydown` (`(e.metaKey || e.ctrlKey) && e.key === 'k'` và `e.key === '/'`) để kích hoạt mở và focus ô search; phím `Escape` để đóng search.
     - Đồng bộ class khóa cuộn `body.menu-open` khi toggle mobile menu.
   - Verify: Nhấn `Cmd+K` / `Ctrl+K` / `/` trên trang desktop mở ngay input search; nhấn `Escape` đóng lại.

3. **Cải tiến SCSS cho Header và Mobile Drawer**
   - Files: `assets/css/_custom.scss`
   - Action:
     - Thêm style cho `.search-kbd` (nhỏ gọn, bo góc, tinh tế ở cả dark và light mode).
     - Đảm bảo menu item padding và tap target tối thiểu 44px trên mobile.
     - Thêm rule `body.blur { overflow: hidden; }` chống cuộn nền khi mở drawer.
   - Verify: Kiểm tra layout không bị tràn, giao diện hiển thị sắc nét trên cả desktop và mobile.

4. **Kiểm thử nghiệm thu**
   - Files: Kiểm tra toàn bộ website qua Hugo server.
   - Action: Chạy `hugo --buildDrafts` kiểm tra không lỗi syntax, kiểm tra hiệu năng và hoạt động thực tế.
   - Verify: `hugo --buildDrafts` trả về exit code 0.

## Risks

- **Xung đột phím tắt khi đang gõ text:** Phím `/` có thể kích hoạt ngoài ý muốn nếu đang gõ trong textarea hoặc input khác.
  - *Giải pháp:* Chỉ kích hoạt phím tắt khi phần tử đang focus không phải là `input`, `textarea`, `select` hoặc `contenteditable`.

## Next Steps

Sau khi hoàn tất: `/cf-review` → `/cf-commit`
