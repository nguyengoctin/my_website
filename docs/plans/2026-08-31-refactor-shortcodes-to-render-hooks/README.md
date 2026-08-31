---
slug: 2026-08-31-refactor-shortcodes-to-render-hooks
auto: false
status: done
---

# Plan: Refactor Hệ Thống Shortcodes Sang Hugo Render Hooks & Chuẩn Hóa GFM UI/UX

**Mode:** normal
**Created:** 2026-08-31
**Status:** DONE

## Context
Dựa trên kết quả nghiên cứu (/cf-research) từ cộng đồng kỹ thuật (HN, Reddit, Hugo Discourse), việc lạm dụng shortcodes như `{{< admonition >}}`, `{{< quote >}}`, `{{< link >}}`, `{{< image >}}` gây ra các nhược điểm nghiêm trọng:
1. **Khóa chặt cú pháp (Vendor Lock-in):** File Markdown không thể xem hoặc render bình thường trên GitHub, VS Code, Obsidian hoặc khi chuyển sang SSG khác.
2. **UI/UX bất tiện:** LoveIt admonition mặc định là accordion đóng/mở khiến người đọc bị giấu thông tin; trích dẫn shortcode bị hardcode dấu ngoặc kép và dư thừa.
3. **Mục tiêu:** Chuyển dịch toàn diện sang **Hugo Markdown Render Hooks** chuẩn GFM, giữ tương thích ngược 100% cho bài cũ và hiện đại hóa giao diện Callout/Quote/Image/Link.

## Assumptions
- Sử dụng cơ chế native Markdown Render Hooks của Hugo v0.160+ (không cần plugin ngoài).
- Không phá vỡ (breaking change) các bài viết cũ đang dùng `{{< admonition >}}` hay `{{< quote >}}`.
- Không sửa trực tiếp vào thư mục gốc `themes/LoveIt/` mà override thông qua `layouts/` của project.

## Approach
1. **Triển khai Bộ Render Hooks (`layouts/_markup/`):**
   - `render-blockquote.html`: Tự động parse GFM Alerts (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) thành Callout Card hiện đại; các blockquote thường render thành trích dẫn chuẩn với font Lora thanh lịch.
   - `render-image.html`: Tự động sinh thẻ semantic `<figure>` và `<figcaption>`, thêm lazy loading & decoding async.
   - `render-link.html`: Tự động thêm `target="_blank"` và `rel="noopener noreferrer"` cho liên kết ngoài.
2. **Tối ưu Backward Compatibility cho Shortcode Cũ:**
   - Override partial `layouts/_partials/plugin/admonition.html` để loại bỏ accordion phiền toái, mở toàn bộ nội dung, làm phẳng UI.
   - Tối ưu `layouts/shortcodes/quote.html`.
3. **Cập nhật SCSS Styling:**
   - Hoàn thiện styling cho GFM Alert Callout trong Dark/Light mode.
4. **Cập nhật Tài liệu Quy Chuẩn:**
   - Chỉnh sửa `docs/blog-writing.md` hướng dẫn viết chuẩn Markdown GFM.

## Not Building
- Không can thiệp vào các shortcode nhúng đồ thị động chuyên biệt (Mermaid).
- Không tự động sửa hàng loạt toàn bộ file markdown cũ trong `content/posts/` nếu không cần thiết (để bảo toàn lịch sử git, vì render hooks và shortcode cũ sẽ cùng chạy mượt mà).

## Progress

| Status  | Phase   | Task |
| ------- | ------- | ---- |
| ✅ DONE | Phase 1 | Xây dựng bộ Markdown Render Hooks (`render-blockquote.html`, `render-image.html`, `render-link.html`) |
| ✅ DONE | Phase 2 | Tối ưu hóa giao diện Callout / Admonition & Quote trong SCSS và partial override |
| ✅ DONE | Phase 3 | Cập nhật tài liệu `docs/blog-writing.md` & Thẩm định nghiệm thu build |

## Tasks

#### Phase 1 [sequential]

1. **Tạo `layouts/_markup/render-blockquote.html`**
   - Files: `layouts/_markup/render-blockquote.html`
   - Nhận diện các cú pháp GFM Alert: `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`, `[!INFO]`, `[!DANGER]`, `[!SUCCESS]`, `[!FAILURE]`, `[!BUG]`, `[!EXAMPLE]`, `[!ABSTRACT]`.
   - Render ra Callout Card chuẩn semantics với icon và màu tương ứng. Nếu là blockquote thông thường thì render `<blockquote>`.
   - Verify: Viết thử đoạn Markdown chuẩn `> [!NOTE]` và kiểm tra HTML đầu ra.

2. **Tạo `layouts/_markup/render-image.html` & `layouts/_markup/render-link.html`**
   - Files: `layouts/_markup/render-image.html`, `layouts/_markup/render-link.html`
   - Image render hook: bọc `<figure>`, gán `loading="lazy"`, `decoding="async"`, sinh `<figcaption>` khi có title/caption.
   - Link render hook: kiểm tra `strings.HasPrefix .Destination "http"` để thêm bảo mật `rel="noopener noreferrer"` và mở tab mới cho external link.
   - Verify: Thử nghiệm link nội bộ vs link ngoài và ảnh Markdown chuẩn.

3. **Override Partial `layouts/_partials/plugin/admonition.html` & Tối ưu Shortcodes cũ**
   - Files: `layouts/_partials/plugin/admonition.html`, `layouts/shortcodes/quote.html`
   - Loại bỏ cấu trúc accordion, giữ nội dung luôn hiển thị 100% (luôn `open`), loại bỏ icon toggle phiền toái.
   - Verify: Kiểm tra các bài viết cũ đang dùng `{{< admonition >}}`.

4. **Tinh chỉnh CSS / SCSS Tokens**
   - Files: `assets/css/modules/_admonitions.scss`, `assets/css/_custom.scss`
   - Đảm bảo các class `.gfm-alert` và `.admonition` chia sẻ đồng bộ hệ thống màu Slate/Amber/Emerald/Rose/Cyan/Indigo cho cả Dark và Light mode.
   - Verify: Kiểm tra hiển thị responsive và chế độ tối/sáng.

5. **Cập nhật Tài liệu Hướng Dẫn `docs/blog-writing.md` & Kiểm tra Build**
   - Files: `docs/blog-writing.md`
   - Đưa cú pháp GFM (`> [!NOTE]`, standard markdown links/images) lên làm chuẩn mực ưu tiên hàng đầu, khuyến nghị hạn chế shortcodes.
   - Verify: Chạy `hugo --buildDrafts` đảm bảo 100% build pass không phát sinh lỗi hay warning.

## Risks
- Regex/String matching trong Hugo template khi parse GFM Alert: Hugo v0.160 hỗ trợ đầy đủ `strings.HasPrefix` và template functions mạnh mẽ. Cần viết template cẩn thận để hỗ trợ cả multiline và format markdown bên trong callout.

## Next Steps
Sau khi phê duyệt kế hoạch, tiến hành thực hiện tuần tự các bước và kiểm tra bằng `hugo --buildDrafts`.
