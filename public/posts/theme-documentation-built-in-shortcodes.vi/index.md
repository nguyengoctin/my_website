# Hướng Dẫn và Demo Toàn Bộ Shortcodes Trên Giao Diện LoveIt


{{< quote >}}
Các shortcodes giúp nâng cao trải nghiệm hiển thị nội dung phong phú mà không cần viết thêm mã HTML phức tạp.
{{< /quote >}}

Giao diện **LoveIt** cùng các tùy chỉnh nâng cao cung cấp bộ công cụ shortcodes đa dạng giúp chúng ta dễ dàng trình bày bài viết chuẩn đẹp, tích hợp sơ đồ, trích dẫn, biểu đồ, câu lệnh prompt và các ô ghi chú ấn tượng. 

Dưới đây là tài liệu tổng hợp và demo trực quan toàn bộ 17 shortcodes trong hệ thống.

---

## 1. THẺ GHI CHÚ ADMONITION

Shortcode `admonition` giúp tạo các hộp thông báo phân loại theo màu sắc và biểu tượng.

{{< admonition note "Admonition Ghi Chú (Note)" >}}
Đây là ô thông báo ghi chú mặc định dùng để cung cấp thông tin ngữ cảnh bổ sung cho bài viết.
{{< /admonition >}}

{{< admonition tip "Admonition Mẹo (Tip)" >}}
Đây là ô chứa các mẹo tối ưu hiệu năng hoặc lời khuyên hữu ích khi viết mã.
{{< /admonition >}}

{{< admonition warning "Admonition Cảnh Báo (Warning)" >}}
Đây là ô cảnh báo các rủi ro có thể gặp phải hoặc các thao tác nhạy cảm.
{{< /admonition >}}

{{< admonition example "Admonition Ví Dụ (Example)" >}}
Đây là ô trình bày ví dụ minh họa hoặc các câu lệnh mẫu thực thi.
{{< /admonition >}}

### Cú pháp Markdown:
```markdown
{{</* admonition type="tip" title="Tiêu đề thông báo" open=true */>}}
Nội dung bên trong ô thông báo...
{{</* /admonition */>}}
```

---

## 2. TRÍCH DẪN NÂNG CAO QUOTE

Shortcode `quote` tạo khối trích dẫn sang trọng với dải viền nổi bật và tên tác giả căn lề phải.

{{< quote author="Huyen Chip" >}}
I often use “we” in this book to mean you (the reader) and I. It’s a habit I got from my teaching days, as I saw writing as a shared learning experience for both the writer and the readers.
{{< /quote >}}

{{< quote author="Phạm Huy Hoàng" >}}
Nếu bạn có thể nói một vấn đề trong vòng một đoạn văn thì đừng nên dùng một trang A4 để giải thích cái vấn đề đó.
{{< /quote >}}

### Cú pháp Markdown:
```markdown
{{</* quote author="Tên Tác Giả" */>}}
Nội dung câu trích dẫn...
{{</* /quote */>}}
```

---


## 4. SƠ ĐỒ ĐỘNG MERMAID

Sử dụng khối mã ```` ```mermaid ```` cho phép tạo sơ đồ quy trình, luồng dữ liệu hoặc biểu đồ trình tự trực quan.

{{< mermaid >}}
flowchart LR
    Start["Khởi tạo"] --> Process["Xử lý dữ liệu"]
    Process --> Condition{"Kiểm tra"}
    Condition -->|"Hợp lệ"| Finish["Hoàn thành"]
    Condition -->|"Lỗi"| Retry["Thử lại"]
    Retry -.-> Process
{{< /mermaid >}}

### Cú pháp Shortcode:
```markdown
{{< mermaid >}}
flowchart LR
    Start["Khởi tạo"] --> Process["Xử lý dữ liệu"]
    Process --> Condition{"Kiểm tra"}
    Condition -->|"Hợp lệ"| Finish["Hoàn thành"]
    Condition -->|"Lỗi"| Retry["Thử lại"]
    Retry -.-> Process
{{< /mermaid >}}
```

---

## 5. TÙY CHỈNH KIỂU DÁNG CƠ BẢN STYLE

Shortcode `style` giúp chúng ta can thiệp trực tiếp các thuộc tính CSS cho một đoạn văn bản hoặc khối nội dung.

{{< style "color: #e74c3c; font-weight: bold; font-size: 1.1rem;" p >}}
Đoạn văn này được tùy chỉnh màu đỏ nổi bật và chữ in đậm thông qua shortcode style.
{{< /style >}}

### Cú pháp Markdown:
```markdown
{{</* style "color: #e74c3c; font-weight: bold;" p */>}}
Nội dung tùy chỉnh CSS...
{{</* /style */>}}
```

---

## 6. HIỆU ỨNG GÕ CHỮ TỰ ĐỘNG TYPEIT

Shortcode `typeit` tạo hiệu ứng gõ phím hoạt hình cho văn bản hoặc đoạn mã nguồn.

{{< typeit >}}
Chào mừng chúng ta đến với trang web cá nhân của Nguyễn Ngọc Tín!
{{< /typeit >}}

### Cú pháp Markdown:
```markdown
{{</* typeit */>}}
Nội dung hiển thị dạng gõ chữ tự động...
{{</* /typeit */>}}
```

---

## 7. THẺ PHIÊN BẢN VERSION

Shortcode `version` hiển thị các huy hiệu đánh dấu phiên bản cập nhật kèm màu sắc tương ứng.

- Phiên bản mới: {{< version 0.3.0 new >}}
- Phiên bản thay đổi: {{< version 0.2.5 changed >}}
- Phiên bản ngưng hỗ trợ: {{< version 0.1.0 deprecated >}}

### Cú pháp Markdown:
```markdown
{{</* version 0.3.0 new */>}}
{{</* version 0.2.5 changed */>}}
```

---

## 8. THẺ NHÂN VẬT PERSON

Shortcode `person` giúp tạo thẻ giới thiệu thông tin cá nhân hoặc tác giả dạng card.

{{< person url="https://github.com/ngoctinn" name="Nguyễn Ngọc Tín" text="Backend Engineer" picture="/images/avatar.webp" >}}

### Cú pháp Markdown:
```markdown
{{</* person url="https://github.com/ngoctinn" name="Nguyễn Ngọc Tín" text="Backend Engineer" picture="/images/avatar.webp" */>}}
```

---

## 9. LIÊN KẾT TÙY CHỈNH LINK

Shortcode `link` hỗ trợ tạo liên kết nâng cao kèm thuộc tính hiển thị.

{{< link href="https://github.com/ngoctinn" content="Truy cập GitHub cá nhân" title="Ghé thăm tài khoản GitHub" >}}

### Cú pháp Markdown:
```markdown
{{</* link href="https://github.com/ngoctinn" content="Nội dung hiển thị" title="Tiêu đề liên kết" */>}}
```

---

## 10. HÌNH ẢNH NÂNG CAO IMAGE

Shortcode `image` tạo hình ảnh có phản hồi kích thước, tự động làm lightbox xem ảnh phóng to và chú thích bên dưới.

{{< image src="/images/avatar.webp" alt="Ảnh đại diện" caption="Ảnh đại diện Nguyễn Ngọc Tín" width="150px" >}}

### Cú pháp Markdown:
```markdown
{{</* image src="/images/avatar.webp" alt="Mô tả ảnh" caption="Chú thích" width="150px" */>}}
```

---

## 11. BIỂU ĐỒ ECHARTS

Shortcode `echarts` render các biểu đồ thống kê trực quan dạng Bar, Line hoặc Pie bằng cấu trúc dữ liệu JSON.

{{< echarts >}}
{"title":{"text":"Thống kê mức độ sử dụng ngôn ngữ"},"tooltip":{},"xAxis":{"data":["Python","Java","TypeScript","SQL"]},"yAxis":{},"series":[{"name":"Tỷ lệ","type":"bar","data":[45,25,20,10]}]}
{{< /echarts >}}

### Cú pháp Markdown:
```markdown
{{</* echarts */>}}
{"title":{"text":"Thống kê"},"xAxis":{"data":["Python","Java","TypeScript"]},"yAxis":{},"series":[{"type":"bar","data":[40,30,30]}]}
{{</* /echarts */>}}
```

---

## 12. BẢNG TỔNG HỢP DANH SÁCH 17 SHORTCODES

| Tên Shortcode | Chức năng chính | Ví dụ sử dụng tiêu biểu |
| :--- | :--- | :--- |
| **admonition** | Tạo khung thông báo phân loại | `{{</* admonition tip "Mẹo" */>}}...{{</* /admonition */>}}` |
| **quote** | Khung trích dẫn sang trọng kèm tác giả | `{{</* quote author="Tên Tác Giả" */>}}...{{</* /quote */>}}` |
| **mermaid** | Vẽ sơ đồ quy trình và trình tự | ` {{< mermaid >}} flowchart LR ... {{< /mermaid >}} ` |
| **style** | Định dạng CSS trực tiếp cho văn bản | `{{</* style "color: red;" p */>}}...{{</* /style */>}}` |
| **typeit** | Hiệu ứng gõ chữ hoạt hình | `{{</* typeit */>}}Hello World{{</* /typeit */>}}` |
| **version** | Huy hiệu đánh dấu phiên bản | `{{</* version 0.3.0 new */>}}` |
| **person** | Thẻ giới thiệu tác giả | `{{</* person name="Ngọc Tín" picture="/images/avatar.webp" */>}}` |
| **link** | Liên kết tùy chỉnh | `{{</* link href="..." content="..." */>}}` |
| **image** | Hiển thị ảnh kèm chú thích và lightbox | `{{</* image src="..." caption="..." */>}}` |
| **echarts** | Vẽ biểu đồ thống kê dạng JSON | `{{</* echarts */>}} { ... } {{</* /echarts */>}}` |
| **music** | Nhúng trình phát nhạc APlayer | `{{</* music url="..." name="..." */>}}` |
| **gist** | Nhúng GitHub Gist snippet | `{{</* gist username gist_id */>}}` |
| **bilibili** | Nhúng video từ Bilibili | `{{</* bilibili bvid */>}}` |
| **mapbox** | Nhúng bản đồ tương tác Mapbox | `{{</* mapbox lng lat zoom */>}}` |
| **highlight** | Tô màu cú pháp mã nguồn | `{{</* highlight python */>}}...{{</* /highlight */>}}` |
| **raw** | Chèn trực tiếp mã HTML thô | `{{</* raw */>}}<div>HTML</div>{{</* /raw */>}}` |

---

## LỜI KẾT

Việc kết hợp linh hoạt các shortcodes sẵn có trên LoveIt giúp chúng ta tạo nên những bài viết kỹ thuật chuyên nghiệp, giàu hình ảnh và tối ưu trải nghiệm đọc cho người dùng.

