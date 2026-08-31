# Phase 1: Dữ Liệu Nguồn và Template Typst

**Plan:** [README.md](./README.md)
**Type:** sequential

## Progress

| Status | Task |
| :--- | :--- |
| ✅ DONE | Task 1: Khởi tạo file dữ liệu `data/cv.yaml` chuẩn hóa |
| ✅ DONE | Task 2: Xây dựng template `cv/resume.typ` và script `scripts/build-cv.sh` |

## Tasks

1. **Khởi tạo file dữ liệu `data/cv.yaml` chuẩn hóa**
   - Files: `data/cv.yaml`
   - Description: Định nghĩa cấu trúc dữ liệu đầy đủ bao gồm thông tin cá nhân (`basics`), danh sách kỹ năng (`skills`), kinh nghiệm làm việc (`experience`), học vấn (`education`), dự án tiêu biểu (`projects`) và các chứng chỉ (`certifications`).
   - Verify: Chạy `hugo --buildDrafts` để kiểm tra Hugo parse dữ liệu YAML thành công không lỗi syntax.

2. **Xây dựng template `cv/resume.typ` và script `scripts/build-cv.sh`**
   - Files: `cv/resume.typ`, `scripts/build-cv.sh`
   - Description: Viết mã nguồn Typst thiết lập layout 1 cột chuẩn ATS, chia tỉ lệ lề A4, heading phân cấp rõ ràng và font chữ dễ đọc. Tạo script bash cho phép biên dịch cục bộ nhanh (`bash scripts/build-cv.sh`).
   - Verify: Chạy `bash scripts/build-cv.sh` (nếu có `typst` local) hoặc kiểm tra cú pháp Typst hợp lệ.
