# Part 01 — Codebase Audit: Mermaid trong Hugo Site

## Mục tiêu

Kiểm tra toàn bộ file Markdown và template liên quan đến Mermaid trong dự án, phân loại vi phạm, đánh giá mức độ nghiêm trọng.

---

## Kiến trúc hiện tại

### `layouts/_partials/plugin/mermaid.html`

- **Render hook**: Hugo Goldmark render hook (`layouts/_default/_markup/render-codeblock-mermaid.html`) chuyển khối ` ```mermaid ` thành `<div class="mermaid" id="..." data-content="...">`.
- **Theme config**: Inject `<script>` một lần duy nhất (`mermaidThemePatchInjected`), dùng `theme: 'base'` với `themeVariables` indigo.
- **Dark mode**: Xử lý bằng CSS GPU filter (`invert(0.93) hue-rotate(180deg)`) — zero JS, tức thì.
- **Init**: `startOnLoad: false`, dùng `patchMermaid()` monkey-patch `m.initialize`.
- **htmlLabels**: `false` — quan trọng, vì `true` sẽ kích hoạt Markdown parser trong nhãn.

### `assets/css/modules/_mermaid.scss`

- Container: `display: flex`, `overflow-x: auto`, `width: 100%`.
- SVG: `max-width: 80%`, `height: auto`.
- Dark: `[theme=dark] .mermaid svg { filter: invert(0.93)... }`.
- **Không ghi đè** `font-size`, `font-family`, `font-weight` trong SVG — đúng chuẩn.

---

## Kết quả Audit — 14 file có Mermaid

### Tổng hợp vi phạm

| File | Số Block | EMPTY_LINE | AMPERSAND (&) | LONG_DIAMOND | Ghi chú |
|------|----------|------------|---------------|--------------|---------|
| `ky-nghe-phan-mem-ban-dia-ai-va-5-bai-hoc-lam-chu-ai-agents.md` | 6 | B1,B2,B3,B4,B5,B6 | B4:L3,L4 | — | Nghiêm trọng nhất |
| `toan-tap-coding-friend-ai-engineering.md` | 6 | B1,B2,B3,B4,B5,B6 | — | B3,B4 | |
| `lexi-ai-english-tutor.md` | 3 | B1,B2,B3 | B1:L8 | — | |
| `bep-di-6-zalo-mini-app-ordering-platform.md` | 2 | B1,B2 | — | B2 | |
| `tu-duy-viet-claudemd-thuc-chien.md` | 2 | B1,B2 | — | B1,B2 | |
| `tu-prompt-engineering-den-graph-engineering.md` | 2 | B1,B2 | — | — | |
| `bilingual-movie-learning-platform.md` | 1 | B1 | — | — | |
| `doc-sach-hoc-thuat-cung-ai.md` | 1 | B1 | — | — | |
| `he-thong-phuong-phap-doc-tai-lieu-it-ai-voi-ai-va-srs.md` | 1 | B1 | — | — | |
| `huong-dan-cau-hinh-mac-mini-headless-server.md` | 1 | B1 | — | — | |
| `lap-trinh-web-ky-nguyen-ai-spec-driven-development.md` | 1 | B1 | — | — | |
| `personal-hugo-technical-blog.md` | 1 | B1 | — | — | |
| `quy-trinh-thu-thap-va-chuyen-doi-ai-engineer-roadmap-song-ngu.md` | 1 | B1 | — | — | |
| `theme-documentation-built-in-shortcodes.vi.md` | — | — | — | — | Docs mẫu, bỏ qua |

### Chi tiết vi phạm

#### 1. EMPTY_LINE (Dòng trống trong khối Mermaid)
**Tất cả 13/14 file bị ảnh hưởng.**

Khi Mermaid parser gặp dòng trống, hành vi phụ thuộc phiên bản:
- Mermaid v9-: thường bỏ qua, vô hại.
- Mermaid v10+: có thể trigger "Parse error: Newline expected" với một số cấu trúc.
- Mermaid v11 (đang dùng): `markdownAutoWrap: true` có thể parse dòng trống như token xuống dòng, gây lỗi ngẫu nhiên.

**Mức độ**: CAO — tất cả block đều có 1 dòng trống trailing (dòng cuối trước ` ``` `). Đây là dòng trống cuối khối, không phải giữa các node, nên thực tế ít gây lỗi hơn nhưng vẫn vi phạm quy chuẩn.

#### 2. AMPERSAND (&) 
**2 file**: `ky-nghe-phan-mem-ban-dia-ai-va-5-bai-hoc-lam-chu-ai-agents.md`, `lexi-ai-english-tutor.md`.

Ký tự `&` trong Mermaid v11 với `htmlLabels: false` không bị HTML-escaped bởi browser, nhưng khi Goldmark render hook dùng `htmlUnescape` rồi đưa vào `data-content`, `&` thành `&amp;` gây mismatch giữa raw content và parsed. Dùng "và" hoặc "and" thay thế.

**Mức độ**: NGHIÊM TRỌNG — vi phạm quy chuẩn cứng trong AGENTS.md.

#### 3. LONG_DIAMOND ({...} > 30 ký tự)
**3 file**: `bep-di-6-zalo-mini-app-ordering-platform.md`, `toan-tap-coding-friend-ai-engineering.md`, `tu-duy-viet-claudemd-thuc-chien.md`.

Node hình thoi với nội dung dài bị Mermaid ép co chữ hoặc tràn góc. Nội dung tối đa ~20 ký tự cho node `{}`.

**Mức độ**: TRUNG BÌNH — ảnh hưởng thẩm mỹ, không gây crash.

---

## Kiến trúc hiện tại — Đánh giá

| Thành phần | Trạng thái | Ghi chú |
|------------|------------|---------|
| Render hook (Goldmark) | ✅ Đúng | `htmlUnescape` + `data-content` đúng chuẩn |
| Theme injection (one-shot) | ✅ Đúng | `mermaidThemePatchInjected` guard |
| Dark mode (CSS filter) | ✅ Đúng | 0ms, no re-render |
| `htmlLabels: false` | ✅ Đúng | Tránh Markdown parser trong label |
| `startOnLoad: false` | ✅ Đúng | Kiểm soát timing |
| CSS — không ghi đè SVG font | ✅ Đúng | Tránh bounding box lệch |
| Empty lines trong MD blocks | ❌ Vi phạm | 13/14 file |
| Ampersand trong labels | ❌ Vi phạm | 2 file |
| Long diamond nodes | ⚠️ Cảnh báo | 3 file |
