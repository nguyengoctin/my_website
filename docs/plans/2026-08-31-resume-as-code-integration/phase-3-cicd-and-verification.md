# Phase 3: CI/CD Pipeline và Thẩm Định Build

**Plan:** [README.md](./README.md)
**Type:** sequential

## Progress

| Status | Task |
| :--- | :--- |
| ✅ DONE | Task 5: Cập nhật workflow GitHub Actions `.github/workflows/gh-pages.yml` |
| ✅ DONE | Task 6: Thẩm định toàn diện (Build, Responsive, Print layout và ATS) |

## Tasks

1. **Cập nhật workflow GitHub Actions `.github/workflows/gh-pages.yml`**
   - Files: `.github/workflows/gh-pages.yml`
   - Description: Bổ sung bước cài đặt Typst qua action `enter-at/setup-typst` và lệnh biên dịch `typst compile cv/resume.typ static/cv/Nguyen_Ngoc_Tin-CV.pdf` trước khi chạy `hugo --gc --minify`.
   - Verify: Kiểm tra cú pháp YAML của file workflow.

2. **Thẩm định toàn diện (Build, Responsive, Print layout và ATS)**
   - Files: Kiểm tra toàn bộ website
   - Description: Chạy `hugo --buildDrafts`, kiểm tra render trang `/cv/`, kiểm tra chế độ Print Preview trên trình duyệt để xác nhận ngắt trang mượt mà không lỗi.
   - Verify: `hugo --buildDrafts` kết thúc với mã lỗi 0 (exit code 0).
