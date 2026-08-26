# Summary — Hugo Mermaid Best Practice Research

**Research ID**: `2026-08-26-hugo-mermaid-bestpractice`  
**Ngày**: 2026-08-26  
**Scope**: Codebase audit + Web research (Hugo docs, Mermaid v11 official docs)

---

## Tình trạng tổng quan

> **Nghiêm trọng**: 13/14 file có Mermaid vi phạm ít nhất 1 quy tắc cứng. Vấn đề phổ biến nhất là **dòng trống (empty line) trailing** cuối mỗi khối Mermaid.

---

## Kiến trúc template — Tốt ✅

Render hook + CSS dark mode GPU filter của dự án **đã đúng chuẩn** và nâng cao hơn pattern tối thiểu của Hugo docs. **Không cần refactor kiến trúc.**

---

## Phân loại vi phạm theo mức độ

### 🔴 NGHIÊM TRỌNG — Phải sửa ngay

| Vi phạm | File bị ảnh hưởng | Quy tắc |
|---------|-------------------|---------|
| **Empty lines** trong Mermaid block | 13/14 file (tất cả blocks) | Mermaid v11 + AGENTS.md |
| **Ampersand `&`** trong node label | `ky-nghe...agents.md` (B4:L3,L4), `lexi-ai...md` (B1:L8) | AGENTS.md §5 |

### 🟡 CẢNH BÁO — Nên sửa

| Vi phạm | File bị ảnh hưởng | Quy tắc |
|---------|-------------------|---------|
| **Diamond node quá dài** (`{}` > 20 ký tự) | `bep-di-6...md` (B2), `toan-tap...md` (B3,B4), `tu-duy...md` (B1,B2) | AGENTS.md §5 |

### 🟢 KHÔNG VI PHẠM

- Không file nào dùng `subgraph` ✅
- Không file nào dùng `|"..."|` trong arrow ✅
- Không file nào inject `%%{init}` ✅
- Không file nào dùng `1.` đầu label ✅ (dùng `(1)` thay thế — hợp lệ)
- Template `mermaid.html` + `_mermaid.scss` — hoàn toàn đúng chuẩn ✅

---

## Hành động đề xuất

### Immediate Fix — Dòng trống (13 file)

Mỗi dòng trống trailing (dòng cuối trong block trước ` ``` `) cần xóa. Đây là automated fix đơn giản.

**Script tự động**:
```bash
python3 scripts/fix_mermaid_empty_lines.py
```

### Manual Fix — Ampersand (2 file)

Trong `ky-nghe-phan-mem-ban-dia-ai-va-5-bai-hoc-lam-chu-ai-agents.md`:
- Block 4, L3: `Specify & Clarify` → `Specify và Clarify`
- Block 4, L4: `Plan & Tasks` → `Plan và Tasks`

Trong `lexi-ai-english-tutor.md`:
- Block 1, L8: `Controllers & Presenters` → `Controllers và Presenters`

### Optional Fix — Diamond nodes dài (3 file)

Rút ngắn nội dung diamond nodes xuống < 20 ký tự.

---

## Kết quả nghiên cứu quan trọng nhất

1. **Empty line là root cause chính** — Không phải lỗi render hook hay CSS. Mermaid v11 với `markdownAutoWrap: true` parse dòng trống như whitespace token, có thể trigger parse error ngẫu nhiên.

2. **Template hiện tại tốt hơn Hugo docs** — Pattern `data-content` + `patchMermaid()` của dự án nâng cao hơn pattern `<pre class="mermaid">` cơ bản. Không cần refactor.

3. **CSS dark mode là best practice** — Dùng GPU filter thay vì re-initialize là đúng trade-off cho site tĩnh.

4. **Vấn đề chỉ ở nội dung Markdown** — 100% vi phạm là trong file `.md`, không phải trong template/layout.

---

## Files

- [01-codebase-audit.md](./01-codebase-audit.md) — Audit chi tiết từng file, từng block
- [02-bestpractice-web.md](./02-bestpractice-web.md) — Best practice từ Hugo docs + Mermaid v11 official

---

## Next Step

Chạy `/cf-plan` để lập kế hoạch fix:
1. Script tự động xóa empty lines
2. Manual fix 3 ampersands
3. Optional shorten diamond nodes
4. Verify bằng `hugo --buildDrafts`
