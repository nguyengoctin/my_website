# Quy Tắc Viết Blog Chia Sẻ Kiến Thức

---

## 1. Triết Lý & Phong Cách Viết

- **Xưng hô "Chúng ta":** Dùng "chúng ta" khi khám phá khái niệm và chia sẻ hành trình học hỏi — người viết và người đọc cùng đồng hành. Tránh giọng dạy đời hay khoảng cách "tôi - bạn".
- **Tinh gọn & Mật độ thông tin:** Nếu nói được trong một đoạn văn, đừng dùng một trang A4. Không mở bài hay kết bài rườm rà.
- **Cấm ngoặc đơn dịch nghĩa:** TUYỆT ĐỐI KHÔNG dùng ngoặc đơn `()` để dịch từ inline. Dùng tiếng Việt tự nhiên hoặc giữ nguyên thuật ngữ tiếng Anh.
- **Cấu trúc rõ ràng & Dễ lướt:** Phân chia tiêu đề H2/H3 cụ thể. Trình bày bài toán trước, giải pháp và bài học thực tế theo sau.
- **Mở bài bằng bài toán, không phải bằng giới thiệu:** Câu đầu tiên phải khiến người đọc thấy ngay vấn đề đang được giải quyết. Không mở bằng "Biết đến X bao giờ chưa?" hay "Hôm nay chúng ta sẽ tìm hiểu…".
- **Đặt người đọc vào bối cảnh trước khi giải pháp:** Xác định rõ bài toán, ai sẽ gặp và tại sao nó khó. Đừng nhảy thẳng vào giải pháp khi người đọc chưa đồng cảm với vấn đề.
- **Tiêu đề mô tả cụ thể:** Tiêu đề phải phản ánh chính xác nội dung. Tránh tiêu đề mơ hồ — độc giả quyết định đọc hay không trong 3 giây.
- **Không dùng buzzwords hype:** Tránh tuyệt đối các từ "game-changer", "revolutionary", "blazing fast" hay các cụm từ marketing rỗng nghĩa.
- **Viết cho "bản thân quá khứ":** Chọn chủ đề từ những khái niệm mà bản thân từng bế tắc. Bài viết tốt nhất là bài viết bạn ước gì được đọc khi còn mới học.
- **Góc nhìn độc quyền:** Đừng viết lại tài liệu chính thức. Chia sẻ insight từ thực tế triển khai — sai lầm, edge case, và bài học "hidden gem" chỉ người có kinh nghiệm thực chiến mới biết.
- **Bằng chứng hơn tuyên bố:** Dùng ví dụ code, sơ đồ kiến trúc để minh họa thay vì chỉ khẳng định suông. "Show, don't tell."
- **Hiểu bản chất, đừng chỉ biết tên:** Diễn giải khái niệm bằng ngôn ngữ của mình — nếu chỉ lặp lại định nghĩa từ để biết cái tên, đó không phải hiểu.
- **Dạy cách tư duy, không chỉ đưa ra đáp án:** Mỗi bài viết nên trang bị cho người đọc một framework tư duy, không chỉ một giải pháp cụ thể để copy-paste.
- **Thất bại là dữ liệu:** Chia sẻ cả những gì đã không hoạt động và lý do tại sao — những bài học từ thất bại thường có giá trị hơn thành công.
- **Trích dẫn nguồn:** Khi tham khảo nghiên cứu hay quan điểm người khác, dẫn nguồn rõ ràng. Điều này xây dựng uy tín và tôn trọng người đọc.
- **Chấp nhận bài viết chưa hoàn hảo:** Strive to be right, but don't fear being wrong. Bài viết có lỗ hổng khi đăng vẫn có giá trị hơn không đăng. Cộng đồng sẽ giúp chỉnh sửa.

---

## 2. Cú Pháp Trình Bày Nội Dung

Các shortcodes sẵn có trong theme LoveIt và cách sử dụng chuẩn:

**Callout / Hộp chú thích:**
```
{{< admonition type="note|tip|warning|danger|info|success|question|failure|bug|example|abstract" title="Tiêu đề" >}}
Nội dung...
{{< /admonition >}}
```

**Trích dẫn:**
```
{{< quote author="Tên Tác Giả" >}}
Nội dung trích dẫn...
{{< /quote >}}
```
Nếu không ghi `author` sẽ tự động hiển thị `— Sưu tầm`.

**Khung Prompt mẫu:**
```
{{< prompt title="Prompt Mẫu: [Tiêu đề]" >}}
Nội dung prompt...
{{< /prompt >}}
```
Không dùng codeblock hay dấu ngoặc kép bên trong prompt.

**Hình ảnh với lightbox:**
```
{{< image src="/images/..." caption="Chú thích ảnh" alt="Mô tả alt" >}}
```

**Liên kết nội bộ:**
```
{{< link href="https://..." content="Tên hiển thị" title="Tooltip" >}}
```

**Sơ đồ Mermaid:**
```markdown
{{</* mermaid */>}}
flowchart LR
    A["Nhãn nút"] --> B["Nhãn nút khác"]
{{</* /mermaid */>}}
```
BẮT BUỘC dùng shortcode cặp `{{< mermaid >}} ... {{< /mermaid >}}` (KHÔNG dùng khối mã ```mermaid thô). Bọc nhãn nút trong dấu ngoặc kép `"..."`. TUYỆT ĐỐI KHÔNG dùng ngoặc đơn `()`, ngoặc vuông `[]` hay toán tử như `O(n²)` trong nhãn nút và nhãn mũi tên để tránh văng lỗi parser. Tách `subgraph` và `end` trên các dòng riêng biệt.

**Code Snippets:**
````
```ngôn_ngữ
// code ở đây
```
````
Luôn có câu giải thích ngắn gọn ngữ cảnh trước khi đưa ra mã nguồn.

**Shortcodes ít dùng (tham khảo khi cần):**
- `{{< typeit >}}` — Hiệu ứng gõ chữ từng ký tự
- `{{< echarts >}}` — Biểu đồ ECharts
- `{{< bilibili id="..." >}}` — Nhúng video Bilibili
- `{{< music >}}` — Nhúng trình phát nhạc
- `{{< gist >}}` — Nhúng GitHub Gist
- `{{< version >}}` — Đánh dấu phiên bản thay đổi
- `{{< style >}}` — CSS inline tùy chỉnh
- `{{< person >}}` — Thẻ giới thiệu người
- `{{< raw >}}` — HTML thô không qua sanitize
