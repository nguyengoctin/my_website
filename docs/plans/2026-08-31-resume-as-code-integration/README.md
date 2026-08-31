---
slug: 2026-08-31-resume-as-code-integration
auto: false
status: done
---

# Plan: Tích Hợp Resume as Code vào Website Hugo và Typst CI/CD

**Mode:** normal
**Created:** 2026-08-31
**Status:** DONE

## Overview

Chuyển đổi trang `/cv/` từ cơ chế hiển thị static PDF (qua PDF.js canvas) sang kiến trúc **Resume as Code** hiện đại. Toàn bộ nội dung CV được quản lý trực tiếp trong mã nguồn thông qua `data/cv.yaml` và `cv/resume.typ`, render giao diện web Native Semantic HTML mượt mà hỗ trợ Dark Mode và Print CSS khổ A4, đồng thời tự động hóa xuất file PDF chất lượng cao thông qua Typst trong GitHub Actions.

## Not Building

- Không xây dựng các form chỉnh sửa CV trực quan (WYSIWYG editor) trên giao diện web người dùng.
- Không sử dụng các CDN script bên ngoài (như PDF.js) để tránh làm chậm tốc độ tải trang.

## Progress

| Status | Phase | File | Tasks |
| :--- | :--- | :--- | :--- |
| ✅ DONE | Phase 1: Dữ Liệu Nguồn và Template Typst | [phase-1-data-and-typst.md](./phase-1-data-and-typst.md) | 2 tasks |
| ✅ DONE | Phase 2: Web Layout và Print CSS Engineering | [phase-2-web-layout-and-print-css.md](./phase-2-web-layout-and-print-css.md) | 2 tasks |
| ✅ DONE | Phase 3: CI/CD Pipeline và Thẩm Định Build | [phase-3-cicd-and-verification.md](./phase-3-cicd-and-verification.md) | 2 tasks |

## Assumptions

- Dữ liệu `data/cv.yaml` đóng vai trò Single Source of Truth cho giao diện web Hugo, kết hợp hàm `markdownify` để format bold/links trong highlights.
- Typst là công cụ biên dịch PDF độc lập, chạy trực tiếp trong GitHub Actions bằng action `enter-at/setup-typst` mà không yêu cầu cài đặt TeX Live.

## Risks

- **Khác biệt font chữ khi xuất PDF:** Môi trường Ubuntu của GitHub Actions có thể thiếu một số font độc quyền nếu không cấu hình font dự phòng.
  - *Giảm thiểu rủi ro:* Sử dụng font hệ thống mã nguồn mở tiêu chuẩn (`Liberation Sans` / `DejaVu Sans` hoặc bundle font `Inter` trong repo).
- **Lệch ngắt trang khi người dùng in trực tiếp từ trình duyệt:** Các trình duyệt khác nhau có thể tính toán margin lệch nhau vài pixel.
  - *Giảm thiểu rủi ro:* Sử dụng `break-inside: avoid` trên từng `.cv-item` và cố định `@page { size: A4; margin: 12mm 15mm; }`.

## Next Steps

Sau khi hoàn tất triển khai: `/cf-review` → `/cf-commit`
