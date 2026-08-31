# Tổng Quan Nghiên Cứu: Kiến Trúc Resume as Code Tích Hợp Vào Hugo

**Date:** 2026-08-31
**Scope:** Nghiên cứu toàn diện các phương án quản lý và hiển thị CV bằng mã nguồn trong Hugo, kết hợp giữa hiển thị web tương tác và tự động hóa xuất PDF đạt chuẩn ATS công nghiệp.

## Overview

Nghiên cứu này khảo sát các phương thức quản lý CV dạng "Resume as Code" được cộng đồng kỹ thuật đánh giá cao nhất. Giải pháp tối ưu cho website Hugo bao gồm việc thiết lập dữ liệu nguồn duy nhất trong `data/cv.yaml` hoặc `cv/resume.typ`, render giao diện web chuẩn responsive tại đường dẫn `/cv`, và tích hợp quy trình tự động xuất PDF (thông qua Typst hoặc Print CSS) để cung cấp file tải trực tiếp cho nhà tuyển dụng với độ tương thích ATS tuyệt đối.

## Key Findings

1. **Dữ liệu cấu trúc (YAML) là nền tảng linh hoạt nhất trong Hugo:** Lưu thông tin CV tại `data/cv.yaml` (kết hợp `markdownify` cho các mô tả công việc) giúp dữ liệu độc lập với giao diện, dễ bảo trì và có thể tái sử dụng cho nhiều template hoặc script xuất dữ liệu.
2. **Quy chuẩn Print CSS xử lý trọn vẹn bài toán in ấn web:** Sử dụng CSS `@media print` với `@page { size: A4; margin: 12mm 15mm; }` và `break-inside: avoid` giải quyết triệt để lỗi cắt đôi dòng chữ hoặc để lại tiêu đề mồ côi (orphans/widows) khi in trực tiếp từ trình duyệt.
3. **Typst là công cụ thay thế vượt trội cho LaTeX:** Với kích thước siêu nhẹ (~30MB binary), tốc độ build 30ms và cú pháp trực quan, Typst là lựa chọn hàng đầu để tích hợp vào GitHub Actions CI/CD nhằm tự động build ra file `static/cv.pdf` mỗi khi push code.
4. **Chuẩn ATS bắt buộc bố cục 1 cột tuyến tính:** File PDF nộp đơn phải là dạng 1 cột (single-column), sử dụng font chữ chuẩn có nhúng bảng Unicode, không dùng bảng (table) hoặc đồ họa thanh kỹ năng để đảm bảo tỷ lệ trích xuất text đạt 100%.

## Parts

| # | Document | Description |
| :--- | :--- | :--- |
| 1 | [Kiến Trúc Dữ Liệu Nguồn: Markdown và YAML](01-data-architecture-markdown-vs-yaml.md) | So sánh các mô hình lưu trữ dữ liệu nguồn, ưu nhược điểm của JSON Resume và cấu trúc file `data/cv.yaml` tối ưu trong Hugo. |
| 2 | [Kỹ Thuật Layout Web và Print CSS](02-hugo-web-layout-and-print-css-engineering.md) | Xây dựng layout `/cv`, bộ quy tắc CSS Paged Media `@page`, chống ngắt trang lỗi và tối ưu trải nghiệm in ấn A4. |
| 3 | [Tự Động Hóa Xuất PDF: Typst và CI/CD](03-typst-and-ci-cd-pdf-automation.md) | So sánh Typst với Headless Chrome/LaTeX, kèm mã nguồn template Typst tinh gọn và file cấu hình GitHub Actions tự động hóa. |
| 4 | [Tiêu Chuẩn Tối Ưu ATS và Định Dạng Công Nghiệp](04-ats-optimization-and-industry-standards.md) | Cơ chế trích xuất của hệ thống ATS, các lỗi bố cục thường gặp và câu lệnh CLI kiểm tra chất lượng PDF. |

## Open Questions

- Dự án sẽ ưu tiên chọn **Phương án 1 (Hugo Data + Print CSS trực tiếp trên web)** để tối giản toolchain, hay **Phương án 2 (Typst song song trong CI/CD)** để đạt chất lượng ấn bản PDF cao nhất?

## Recommended Next Steps

1. Kích hoạt lệnh `/cf-plan` để lập kế hoạch triển khai cụ thể các thành phần (file dữ liệu, template layout, SCSS print styles và CI workflow) vào mã nguồn website hiện tại.
2. Thiết lập cấu trúc `data/cv.yaml` với đầy đủ thông tin cá nhân và kinh nghiệm thực tế.
