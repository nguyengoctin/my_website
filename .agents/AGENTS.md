# AGENTS.md — Quy Chuẩn Vận Hành NgocTin Note

## 1. Core Commands

- **Dev Server:** `hugo server -D` (xem trực tiếp thay đổi trên môi trường local)
- **Kiểm tra Build:** `hugo --buildDrafts` (bắt buộc chạy để thẩm định cú pháp trước khi hoàn tất)
- **Build Production:** `hugo --gc --minify`

## 2. Definition of Done (Checklist Hoàn Thành)

Mỗi khi tạo mới hoặc chỉnh sửa bài viết/tính năng, bắt buộc phải thỏa mãn:
1. Lệnh `hugo --buildDrafts` biên dịch thành công 100%, không phát sinh lỗi render hay shortcode.
2. Nội dung giải quyết đúng vấn đề, giữ vai trò co-writer/editor và tôn trọng góc nhìn của tác giả (không bịa trải nghiệm giả, không biến thành SEO generic content).
3. Không dùng `&` trong prose, heading, frontmatter hoặc nội dung Mermaid (thay bằng "và" hoặc "and"). Tuyệt đối không can thiệp hoặc thay đổi `&` nếu nó là cú pháp bắt buộc trong source code, command, URL hoặc dữ liệu nguyên bản.
4. Không dùng ngoặc đơn `()` để dịch nghĩa thuật ngữ tiếng Anh inline trong văn xuôi. Giữ nguyên thuật ngữ tiếng Anh khi tự nhiên và chính xác hơn. Không can thiệp vào dấu ngoặc trong code.
5. Xưng hô "chúng ta" khi cần dẫn dắt người đọc đồng hành khám phá kỹ thuật.
6. Frontmatter đầy đủ cho bài mới (`title`, `date`, `description`, `tags`, `categories`, `author`, `draft`). Thêm `pinned: true` khi có yêu cầu ghim bài.
7. Toàn bộ Shortcode và Mermaid tuân thủ đúng tài liệu quy chuẩn chuyên biệt.

## 3. Vùng Cấm Can Thiệp (Protected Areas)

- Không tự ý sửa đổi file cấu hình `hugo.toml` hoặc cấu trúc theme gốc nếu không có yêu cầu cụ thể.
- Không tự ý chạy các lệnh Git can thiệp trực tiếp vào lịch sử commit (`git push`, `git reset --hard`).

## 4. Điều Hướng Hướng Dẫn Chuyên Biệt (Dynamic Routing)

Để tránh quá tải ngữ cảnh (context creep), agent chỉ nạp tài liệu theo đúng nhu cầu tác vụ:

- **Khi tạo mới, chỉnh sửa hoặc biên tập bài viết:** BẮT BUỘC đọc và tuân thủ [docs/blog-writing.md](file:///home/ngoctin/Projects/my_website/docs/blog-writing.md).
- **Khi bài viết có chứa hoặc cần tạo/sửa sơ đồ Mermaid:** BẮT BUỘC đọc và tuân thủ [docs/mermaid.md](file:///home/ngoctin/Projects/my_website/docs/mermaid.md).
