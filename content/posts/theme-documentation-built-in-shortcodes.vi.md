---
title: "Hướng Dẫn & Demo Toàn Bộ Shortcodes Trên Giao Diện LoveIt"
date: 2026-07-29T18:40:00+07:00
draft: false
author: "Nguyen Ngoc Tin"
description: "Bài viết tổng hợp và demo thực tế toàn bộ 16 shortcodes tích hợp sẵn trên giao diện LoveIt của Hugo dành cho trang web cá nhân."
tags: ["Hugo", "LoveIt", "Shortcodes", "Web Development", "Documentation"]
categories: ["Tech Blog"]
---

> *"Các shortcodes của LoveIt giúp nâng cao trải nghiệm hiển thị nội dung phong phú mà không cần viết thêm mã HTML phức tạp."*

Giao diện **LoveIt** cung cấp một bộ công cụ shortcodes đa dạng giúp chúng ta dễ dàng trình bày bài viết chuẩn đẹp, tích hợp sơ đồ, âm nhạc, biểu đồ và các ô ghi chú ấn tượng. 

Dưới đây là tài liệu tổng hợp và demo trực quan toàn bộ 16 shortcodes có sẵn trong hệ thống.

---

## 1. THẺ GHI CHÚ ADMONITION

Shortcode `admonition` giúp tạo các hộp thông báo phân loại theo màu sắc và biểu tượng.

### Các loại Admonition hỗ trợ:
`note`, `abstract`, `info`, `tip`, `success`, `question`, `warning`, `failure`, `danger`, `bug`, `example`, `quote`.

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

## 2. SƠ ĐỒ ĐỘNG MERMAID

Sử dụng khối mã ```` ```mermaid ```` cho phép tạo sơ đồ quy trình, luồng dữ liệu hoặc biểu đồ trình tự trực quan.

```mermaid
flowchart LR
    Start[Khởi tạo] --> Process[Xử lý dữ liệu]
    Process --> Condition{Kiểm tra}
    Condition -- Hợp lệ --> Finish[Hoàn thành]
    Condition -- Lỗi --> Retry[Thử lại]
    Retry -.-> Process
```

### Cú pháp Markdown:
```markdown
```mermaid
flowchart LR
    Start[Khởi tạo] --> Process[Xử lý dữ liệu]
    Process --> Condition{Kiểm tra}
    Condition -- Hợp lệ --> Finish[Hoàn thành]
    Condition -- Lỗi --> Retry[Thử lại]
    Retry -.-> Process
```
```

---

## 3. TÙY CHỈNH KIỂU DÁNG CƠ BẢN STYLE

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

## 4. HIỆU ỨNG GÕ CHỮ TỰ ĐỘNG TYPEIT

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

## 5. THẺ PHIÊN BẢN VERSION

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

## 6. THẺ NHÂN VẬT PERSON

Shortcode `person` giúp tạo thẻ giới thiệu thông tin cá nhân hoặc tác giả dạng card.

{{< person url="https://github.com/ngoctinn" name="Nguyễn Ngọc Tín" text="Backend Engineer" picture="/images/avatar.jpg" >}}

### Cú pháp Markdown:
```markdown
{{</* person url="https://github.com/ngoctinn" name="Nguyễn Ngọc Tín" text="Backend Engineer" picture="/images/avatar.jpg" */>}}
```

---

## 7. LIÊN KẾT TÙY CHỈNH LINK

Shortcode `link` hỗ trợ tạo liên kết nâng cao kèm thuộc tính hiển thị.

{{< link href="https://github.com/ngoctinn" content="Truy cập GitHub cá nhân" title="Ghé thăm tài khoản GitHub" >}}

### Cú pháp Markdown:
```markdown
{{</* link href="https://github.com/ngoctinn" content="Nội dung hiển thị" title="Tiêu đề liên kết" */>}}
```

---

## 8. HÌNH ẢNH NÂNG CAO IMAGE

Shortcode `image` tạo hình ảnh có phản hồi kích thước, tự động làm lightbox xem ảnh phóng to và chú thích bên dưới.

{{< image src="/images/avatar.jpg" alt="Ảnh đại diện" caption="Ảnh đại diện Nguyễn Ngọc Tín" width="150px" >}}

### Cú pháp Markdown:
```markdown
{{</* image src="/images/avatar.jpg" alt="Mô tả ảnh" caption="Chú thích" width="150px" */>}}
```

---

## 9. BIỂU ĐỒ ECHARTS

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

## 10. TRÌNH PHÁT NHẠC MUSIC

Shortcode `music` nhúng trình phát nhạc trực tuyến MetingJS trên bài viết.

### Cú pháp Markdown:
```markdown
{{</* music url="/music/song.mp3" name="Tên bài hát" artist="Ca sĩ" cover="/images/cover.jpg" */>}}
```

---

## 11. BẢNG TỔNG HỢP DANH SÁCH 16 SHORTCODES

| Tên Shortcode | Chức năng chính | Ví dụ sử dụng tiêu biểu |
| :--- | :--- | :--- |
| **admonition** | Tạo khung thông báo phân loại | `{{</* admonition tip "Mẹo" */>}}...{{</* /admonition */>}}` |
| **mermaid** | Vẽ sơ đồ quy trình và trình tự | ` ```mermaid flowchart LR ... ``` ` |
| **style** | Định dạng CSS trực tiếp cho văn bản | `{{</* style "color: red;" p */>}}...{{</* /style */>}}` |
| **typeit** | Hiệu ứng gõ chữ hoạt hình | `{{</* typeit */>}}Hello World{{</* /typeit */>}}` |
| **version** | Huy hiệu đánh dấu phiên bản | `{{</* version 0.3.0 new */>}}` |
| **person** | Thẻ giới thiệu tác giả | `{{</* person name="Ngọc Tín" url="..." */>}}` |
| **link** | Liên kết tùy chỉnh | `{{</* link href="..." content="..." */>}}` |
| **image** | Hiển thị ảnh kèm chú thích & lightbox | `{{</* image src="..." caption="..." */>}}` |
| **echarts** | Vẽ biểu đồ thống kê dạng JSON | `{{</* echarts */>}} { ... } {{</* /echarts */>}}` |
| **music** | Nhúng trình phát nhạc APlayer | `{{</* music url="..." name="..." */>}}` |
| **gist** | Nhúng GitHub Gist snippet | `{{</* gist username gist_id */>}}` |
| **bilibili** | Nhúng video từ Bilibili | `{{</* bilibili bvid */>}}` |
| **mapbox** | Nhúng bản đồ tương tác Mapbox | `{{</* mapbox lng lat zoom */>}}` |
| **highlight** | Tô màu cú pháp mã nguồn | `{{</* highlight python */>}}...{{</* /highlight */>}}` |
| **raw** | Chèn trực tiếp mã HTML thô | `{{</* raw */>}}<div>HTML</div>{{</* /raw */>}}` |
| **script** | Thực thi đoạn mã JavaScript nội tuyến | `{{</* script */>}}console.log("OK"){{</* /script */>}}` |

---

## LỜI KẾT

Việc kết hợp linh hoạt các shortcodes sẵn có trên LoveIt giúp chúng ta tạo nên những bài viết kỹ thuật chuyên nghiệp, giàu hình ảnh và tối ưu trải nghiệm đọc cho người dùng.
