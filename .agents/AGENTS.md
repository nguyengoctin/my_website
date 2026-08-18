# AGENTS.md — Quy Chuẩn Vận Hành và Viết Blog

## 1. Core Commands

- **Dev Server:** `hugo server -D` (xem trực tiếp thay đổi trên môi trường local)
- **Kiểm tra Build:** `hugo --buildDrafts` (bắt buộc chạy để thẩm định cú pháp trước khi hoàn tất)
- **Build Production:** `hugo --gc --minify`

## 2. Definition of Done (Checklist Hoàn Thành)

Mỗi khi tạo mới hoặc chỉnh sửa bài viết/tính năng, bắt buộc phải thỏa mãn:
1. Lệnh `hugo --buildDrafts` biên dịch thành công 100%, không phát sinh lỗi render hay shortcode.
2. Tiêu đề và nội dung TUYỆT ĐỐI KHÔNG chứa ký tự `&` (phải thay bằng chữ "và" hoặc "and").
3. TUYỆT ĐỐI KHÔNG dùng ngoặc đơn `()` để dịch nghĩa inline (dùng tiếng Việt tự nhiên hoặc giữ nguyên thuật ngữ tiếng Anh gốc).
4. Xưng hô "chúng ta" xuyên suốt bài viết, giữ vai trò đồng hành cùng người đọc.
5. Frontmatter đầy đủ: `title`, `date`, `description`, `tags`, `categories`, `author`, `draft`.
6. Toàn bộ sơ đồ Mermaid và Shortcode tuân thủ đúng cú pháp quy định.

## 3. Vùng Cấm Can Thiệp (Protected Areas)

- Không tự ý sửa đổi file cấu hình `hugo.toml` hoặc cấu trúc theme gốc nếu không có yêu cầu cụ thể.
- Không tự ý chạy các lệnh Git can thiệp trực tiếp vào lịch sử commit (`git push`, `git reset --hard`).

## 4. Triết Lý và Cấu Trúc Bài Viết

- **Mở bài trực diện bằng bài toán:** Câu đầu tiên phải đưa người đọc vào vấn đề kỹ thuật hoặc bài toán thực tế cần giải quyết. Tuyệt đối không mở bài rườm rà hay chào hỏi thừa.
- **Bố cục chuẩn Tech Blog:**
  - Bài toán và bối cảnh thực tế $\to$ Bằng chứng số liệu và phân tích bản chất $\to$ Giải pháp và cấu hình mẫu $\to$ Bài học đúc kết.
- **Tiêu đề cụ thể, chân thực (Reddit Style):**
  - Không dùng từ thổi phồng, clickbait (Toàn tập, Bí kíp, Ultimate, Game-changer).
  - Định dạng chuẩn: *"Cách [Giải quyết bài toán cụ thể] bằng [Công nghệ]"* hoặc *"[Chủ đề]: Từ [Bản chất] đến [Giải pháp]"*.
  - Không dùng ngoặc đơn giải thích từ tiếng Anh ngay tiêu đề.
- **Show, Don't Tell:** Dùng ví dụ code, bảng dữ liệu, và sơ đồ trực quan thay vì chỉ khẳng định suông.
- **Phân loại bài viết:**
  - *Tech Blog (Kỹ thuật/Hướng dẫn):* Tinh gọn, đi thẳng vào bản chất kỹ thuật, tuân thủ cấu trúc bài toán $\to$ giải pháp.
  - *Tản văn / Góc nhìn / Trích dẫn (Mindset, Review):* Tôn trọng 100% nội dung, văn phong và cảm xúc bài gốc; chỉ dùng shortcodes để làm đẹp giao diện, không tự ý tóm tắt cắt xén.

## 5. Quy Chuẩn Shortcodes và Cú Pháp

- **Callout:** `{{< admonition type="note|tip|warning|danger|info|success|question|failure|bug|example|abstract" title="Tiêu đề" >}} Nội dung {{< /admonition >}}`
- **Quote:** `{{< quote author="Tên Tác Giả" >}} Nội dung {{< /quote >}}` — Không ghi author thì hiển thị `— Sưu tầm`
- **Prompt Mẫu:** `{{< prompt title="Prompt Mẫu: [Tên]" >}} Nội dung prompt không chứa codeblock lồng {{< /prompt >}}`
  - Chỉ sử dụng khung `prompt` cho các bộ câu lệnh hoàn chỉnh, đa bước hoặc có cấu trúc rõ ràng.
  - TUYỆT ĐỐI KHÔNG bọc các câu ngắn 1–2 dòng rời rạc vào khung prompt (dùng bullet point hoặc callout).
- **Link:** `{{< link href="https://..." content="Tên hiển thị" >}}`
- **Hình ảnh:** `{{< image src="/images/..." caption="Chú thích" alt="Alt text" >}}`
- **Ghim bài viết:** Thêm `pinned: true` vào frontmatter để tự động hiển thị biểu tượng ghim bên phải tiêu đề trên trang chủ và danh sách.
- **Typography & Heading:** Toàn bộ tiêu đề bài viết và heading dùng font `Lora` với độ đậm `font-weight: 500` (Medium) tinh gọn, thanh lịch.
- **Mermaid JS:** Bắt buộc dùng khối mã ` ```mermaid `:
  - **Khai báo loại biểu đồ:** Dòng đầu tiên là `flowchart TD`, `flowchart LR`, hoặc `sequenceDiagram` (nằm trên một dòng độc lập).
  - **Định dạng Node (Hộp văn bản):**
    - Hộp chữ nhật chuẩn: `NodeID["Nội dung tiếng Việt hoặc Unicode"]` (luôn dùng cặp ngoặc vuông `["..."]` bọc dấu nháy kép cho mọi node có dấu tiếng Việt hoặc khoảng trắng).
    - Nút hình thoi điều kiện: `NodeID{"Nội dung quyết định"}`.
    - `NodeID` bắt buộc là chuỗi ký tự ASCII đơn giản (ví dụ: `A`, `B`, `Step1`, `Node1`), TUYỆT ĐỐI KHÔNG dùng từ khóa hệ thống (như `end`, `subgraph`, `graph`).
  - **Nhãn trên mũi tên liên kết:**
    - Cú pháp chuẩn: `A -->|Nhãn văn bản thuần túy| B` (hoặc `A --> B` nếu không cần nhãn).
    - TUYỆT ĐỐI KHÔNG đặt dấu nháy kép `"` bên trong cặp thanh đứng `|...|` (ví dụ SAI: `-->|"Nhãn"|`, ĐÚNG: `-->|Nhãn|`).
    - TUYỆT ĐỐI KHÔNG dùng dấu phẩy `,`, dấu gạch chéo `/` trong nhãn mũi tên (dùng từ thay thế: `hoặc`, `và`, dấu gạch ngang `-`).
  - **TUYỆT ĐỐI KHÔNG để dòng trống (Empty Line) bên trong khối mã Mermaid:** Toàn bộ các dòng định nghĩa trong khối ` ```mermaid ` phải liên tục, không chèn dòng trống giữa các node hoặc giữa các `subgraph`.
  - **TUYỆT ĐỐI KHÔNG dùng ký tự `&` trong toàn bộ biểu đồ:** Thay bằng chữ "và" hoặc chữ "and".
  - **Quy tắc Subgraph:**
    - Khai báo: `subgraph ID ["Tên Hiển Thị"]` và `end` trên từng dòng độc lập.
    - Không nối mũi tên trực tiếp vào `ID` của subgraph; bắt buộc phải nối từ node con cụ thể bên trong.
- **Code Block:** Luôn có câu dẫn ngữ cảnh trước khi đưa khối mã ` ```ngôn_ngữ `. Toàn bộ các khối mã Markdown, Text, YAML tự động bẻ dòng theo chuẩn `white-space: pre-wrap`.
