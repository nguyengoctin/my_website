---
title: "Quy Chuẩn Viết Bài và Định Dạng Nội Dung"
description: "Quy chuẩn giọng văn, frontmatter, cấm dùng &, quy tắc tiêu đề và danh mục bài viết"
tags: [conventions, content-writing, style-guide, agents-rule]
created: 2026-08-24
updated: 2026-08-24
type: "preference"
importance: 3
source: scan
---

# Quy Chuẩn Viết Bài và Định Dạng Nội Dung

## Overview
Dự án áp dụng bộ quy chuẩn viết blog kỹ thuật nghiêm ngặt (định nghĩa tại `AGENTS.md` và `BLOG_WRITING_RULES.md`) để duy trì chất lượng học thuật, độ mạch lạc và tính thẩm mỹ cao.

## Key Points
- **Xưng hô:** Sử dụng đại từ "chúng ta" xuyên suốt bài viết để đóng vai trò đồng hành cùng bạn đọc.
- **Tiêu đề (Reddit Style):** Cụ thể, chân thực, nêu rõ bài toán và công nghệ. Tuyệt đối không dùng từ thổi phồng/clickbait ("Toàn tập", "Bí kíp", "Game-changer").
- **Mở bài:** Đi thẳng vào bài toán kỹ thuật hoặc bối cảnh thực tế ở câu đầu tiên, không chào hỏi rườm rà.
- **Quy tắc cấm kỵ (Zero Tolerance):**
  - Tuyệt đối không dùng ký tự `&` trong tiêu đề, nội dung và biểu đồ (bắt buộc thay bằng "và" hoặc "and").
  - Tuyệt đối không dùng ngoặc đơn `()` để dịch nghĩa tiếng Anh inline (dùng tiếng Việt tự nhiên hoặc giữ nguyên thuật ngữ kỹ thuật gốc).
- **Cấu trúc Tech Blog:** Bài toán thực tế $\to$ Dữ liệu/phân tích bản chất $\to$ Giải pháp/cấu hình mẫu $\to$ Bài học đúc kết.
- **Frontmatter bắt buộc:** `title`, `date`, `description`, `tags`, `categories`, `author`, `draft` (và tùy chọn `pinned: true`).

## Related
- [.agents/AGENTS.md](file:///home/ngoctin/Projects/my_website/.agents/AGENTS.md)
- [BLOG_WRITING_RULES.md](file:///home/ngoctin/Projects/my_website/BLOG_WRITING_RULES.md)
- [archetypes/default.md](file:///home/ngoctin/Projects/my_website/archetypes/default.md)
