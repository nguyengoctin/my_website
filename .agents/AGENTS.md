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
  - Bài toán và bối cảnh thực tế → Bằng chứng số liệu và phân tích bản chất → Giải pháp và cấu hình mẫu → Bài học đúc kết.
- **Tiêu đề cụ thể, chân thực (Reddit Style):**
  - Không dùng từ thổi phồng, clickbait (Toàn tập, Bí kíp, Ultimate, Game-changer).
  - Định dạng chuẩn: *"Cách [Giải quyết bài toán cụ thể] bằng [Công nghệ]"* hoặc *"[Chủ đề]: Từ [Bản chất] đến [Giải pháp]"*.
  - Không dùng ngoặc đơn giải thích từ tiếng Anh ngay tiêu đề.
- **Show, Don't Tell:** Dùng ví dụ code, bảng dữ liệu, và sơ đồ trực quan thay vì chỉ khẳng định suông.
- **Phân loại bài viết:**
  - *Tech Blog (Kỹ thuật/Hướng dẫn):* Tinh gọn, đi thẳng vào bản chất kỹ thuật, tuân thủ cấu trúc bài toán → giải pháp.
  - *Tản văn / Góc nhìn / Trích dẫn (Mindset, Review):* Tôn trọng 100% nội dung, văn phong và cảm xúc bài gốc; chỉ dùng shortcodes để làm đẹp giao diện, không tự ý tóm tắt cắt xén.

## 5. Quy Chuẩn Shortcodes và Cú Pháp

- **Callout:** `{{< admonition type="note|tip|warning|danger|info|success|question|failure|bug|example|abstract" title="Tiêu đề" >}} Nội dung {{< /admonition >}}`
- **Quote:** `{{< quote author="Tên Tác Giả" >}} Nội dung {{< /quote >}}` — Nếu không ghi `author` thì chỉ hiển thị trích dẫn (không hiển thị dòng tác giả)
- **Prompt Mẫu:** Sử dụng khối mã Markdown chuẩn ```` ```text ```` (hoặc ```` ```markdown ````), luôn có câu dẫn ngữ cảnh rõ ràng trước khối mã. Không dùng shortcode riêng biệt cho prompt.
- **Link:** `{{< link href="https://..." content="Tên hiển thị" >}}`
- **Hình ảnh:** `{{< image src="/images/..." caption="Chú thích" alt="Alt text" >}}`
- **Ghim bài viết:** Thêm `pinned: true` vào frontmatter để tự động hiển thị biểu tượng ghim bên phải tiêu đề trên trang chủ và danh sách.
- **Typography & Heading:** Toàn bộ tiêu đề bài viết và heading dùng font `Lora` với độ đậm `font-weight: 500` (Medium) tinh gọn, thanh lịch.
- **Mermaid JS:** Bắt buộc dùng khối mã ` ```mermaid `:
  - **Cấu hình Theme Toàn Cục:** Hệ thống đã tự động inject theme indigo và cấu hình `themeVariables` toàn cục (light/dark mode) tại `layouts/_partials/plugin/mermaid.html`. TUYỆT ĐỐI KHÔNG chèn thủ công `%%{init}%%` vào bài viết để tránh trùng lặp và xung đột dark mode.
  - **Khai báo loại biểu đồ:** Dòng đầu tiên trong khối ` ```mermaid ` là `flowchart TD`, `flowchart LR`, hoặc `sequenceDiagram` (nằm trên một dòng độc lập).
  - **Định dạng Node (Hộp văn bản):**
    - Hộp chữ nhật chuẩn: `NodeID["Nội dung tiếng Việt hoặc Unicode"]` (luôn dùng cặp ngoặc vuông `["..."]` bọc dấu nháy kép cho mọi node có dấu tiếng Việt hoặc khoảng trắng).
    - **TUYỆT ĐỐI KHÔNG bắt đầu nội dung node bằng số kèm dấu chấm** (ví dụ SAI: `["1. Bước một"]`, `["2. Bước hai"]` sẽ gây lỗi `Unsupported markdown: list` của Mermaid 11+. ĐÚNG: `["Lớp 1: Bước một"]`, `["Nhóm 1: Bước một"]` hoặc `["(1) Bước một"]`).
    - **Tiến trình (Bước, Pha, Nhóm, Lớp) BẮT BUỘC dùng `<br/>` để xuống dòng:** Đối với các node có tiền tố tiến trình như `Bước X:`, `Pha X:`, `Nhóm X:`, `Lớp X:` hoặc nội dung dài, bắt buộc chèn `<br/>` ngay sau dấu hai chấm (ví dụ: `NodeID["`Bước 1:<br/>Quét tri thức`"]`) để hộp node hiển thị vuông vắn, không bị kéo bè ngang hoặc tràn khung trên mobile.
    - Nút hình thoi điều kiện: `NodeID{"Câu hỏi ngắn gọn"}`. TUYỆT ĐỐI chỉ để câu hỏi ngắn dưới 20 ký tự (ví dụ: `Check{"Có --add-tests?"}`), không nhét cả câu văn dài vào nút hình thoi để tránh bị đè tràn góc nhọn.
    - `NodeID` bắt buộc là chuỗi ký tự ASCII đơn giản (ví dụ: `A`, `B`, `Step1`, `Node1`), TUYỆT ĐỐI KHÔNG dùng từ khóa hệ thống (như `end`, `subgraph`, `graph`).
  - **Nhãn trên mũi tên liên kết:**
    - Cú pháp chuẩn: `A -->|Nhãn văn bản thuần túy| B` (hoặc `A --> B` nếu không cần nhãn).
    - TUYỆT ĐỐI KHÔNG đặt dấu nháy kép `"` bên trong cặp thanh đứng `|...|` (ví dụ SAI: `-->|"Nhãn"|`, ĐÚNG: `-->|Nhãn|`).
    - TUYỆT ĐỐI KHÔNG dùng dấu phẩy `,`, dấu gạch chéo `/` trong nhãn mũi tên (dùng từ thay thế: `hoặc`, `và`, dấu gạch ngang `-`).
  - **TUYỆT ĐỐI KHÔNG để dòng trống (Empty Line) bên trong khối mã Mermaid:** Toàn bộ các dòng định nghĩa trong khối ` ```mermaid ` phải liên tục, không chèn dòng trống giữa các node hoặc giữa các `subgraph`.
  - **TUYỆT ĐỐI KHÔNG dùng ký tự `&` trong toàn bộ biểu đồ:** Thay bằng chữ "và" hoặc chữ "and".
  - **Quy tắc Bố Cục Cân Đối (Tối thiểu 2 node / hàng):**
    - **TUYỆT ĐỐI KHÔNG xếp luồng đơn điệu 1 hàng dọc từ trên xuống dưới** (tạo cảm giác sơ đồ dài lê thê và trống trải hai bên).
    - Bắt buộc chia nhánh cân đối (`A --> B` và `A --> C`), tạo cấu trúc 2 cột hoặc đa nhánh để mỗi tầng luôn có tối thiểu 2 node nằm song song.
  - **Quy tắc Bố Cục và Liên Kết Node (KHÔNG ĐÓNG KHUNG NHÓM SUBGRAPH):**
    - **TUYỆT ĐỐI KHÔNG dùng `subgraph` đóng khung nhóm** (gây sinh ra các đường viền bao quanh khổng lồ và làm lệch bố cục).
    - Tạo bố cục tự nhiên bằng các liên kết trực tiếp giữa các node (`A --> B`, `A --> C`, `B --> D...`).
    - Nối các node theo chiều dọc hoặc chia luồng nhánh cân đối để sơ đồ hiển thị gọn gàng, tự nhiên và không bị phình to.
- **CSS Mermaid — Quy tắc cứng:** CSS chỉ được kiểm soát `.mermaid` container (display, overflow, margin). TUYỆT ĐỐI KHÔNG ghi đè `font-size`, `font-weight`, `font-family` vào các thẻ `text`, `.nodeLabel`, `.edgeLabel` bên trong SVG — vì Mermaid JS tính toán bounding box trước khi render; can thiệp CSS sau đó sẽ làm chữ lệch và bị cắt xén khỏi viền node.
- **Code Block:** Luôn có câu dẫn ngữ cảnh trước khi đưa khối mã ` ```ngôn_ngữ `. Toàn bộ các khối mã Markdown, Text, YAML tự động bẻ dòng theo chuẩn `white-space: pre-wrap`.
