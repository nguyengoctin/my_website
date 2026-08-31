# Quy Chuẩn Kỹ Thuật và Bố Cục Sơ Đồ Mermaid

Tài liệu này quy định chi tiết cú pháp, bố cục và kỹ thuật render Mermaid JS trên hệ thống Hugo của repository.

## 1. Triết lý và Nguyên tắc

- **Mermaid là công cụ, không phải KPI:** Chỉ thêm sơ đồ khi nó giúp làm rõ một luồng dữ liệu, kiến trúc hoặc tiến trình phức tạp. Không thêm sơ đồ chỉ để trang trí.
- **Semantic Truth:** Biểu đồ phải phản ánh chính xác 100% bản chất luồng dữ liệu hoặc tiến trình thực tế. TUYỆT ĐỐI KHÔNG tự ý nối chéo các node nhân tạo chỉ để ép layout thành lưới làm sai lệch bản chất logic.

## 2. Kiến Trúc Render và Cấu Hình Hệ Thống

1. **Khối mã chuẩn Markdown:** Bắt buộc dùng khối mã ` ```mermaid ` (Hugo Goldmark tự động biên dịch thành `<div class="mermaid" id="..." data-content="...">` qua Render Hook `layouts/_default/_markup/render-codeblock-mermaid.html`).
2. **Khởi tạo và Token màu:** Đã được cấu hình tự động qua partial `layouts/_partials/plugin/mermaid.html` (chứa `theme: 'base'`, `securityLevel: 'loose'`, `themeVariables` indigo). **TUYỆT ĐỐI KHÔNG** chèn thủ công `%%{init}%%` vào bài viết.
3. **Dark Mode & Render Timing:** Hệ thống sử dụng bộ lọc CSS GPU Filter trên container `.mermaid svg` để đổi màu tức thì 0ms khi chuyển theme sáng/tối, không re-render lại SVG làm giật lag giao diện.
4. **Quy tắc CSS Mermaid:** CSS chỉ được kiểm soát `.mermaid` container (display, overflow, margin). **TUYỆT ĐỐI KHÔNG** ghi đè `font-size`, `font-weight`, `font-family` vào các thẻ `text`, `.nodeLabel`, `.edgeLabel` bên trong SVG — vì Mermaid JS tính toán bounding box trước khi render; can thiệp CSS sau đó sẽ làm chữ lệch và bị cắt xén khỏi viền node.

## 3. Quy Chuẩn Cú Pháp và Định Dạng Node

- **Khai báo loại biểu đồ:** Dòng đầu tiên trong khối ` ```mermaid ` là `flowchart TD`, `flowchart LR`, hoặc `sequenceDiagram` (nằm trên một dòng độc lập).
- **Hộp chữ nhật chuẩn:** BẮT BUỘC dùng cú pháp `NodeID["Nội dung tiếng Việt hoặc Unicode"]` (luôn dùng cặp ngoặc vuông `["..."]` bọc dấu nháy kép cho mọi node có dấu tiếng Việt hoặc khoảng trắng).
- **Cấm số kèm dấu chấm:** TUYỆT ĐỐI KHÔNG bắt đầu nội dung node bằng số kèm dấu chấm (Ví dụ SAI: `["1. Bước một"]`, `["2. Bước hai"]` sẽ gây lỗi `Unsupported markdown: list` của Mermaid 11+. ĐÚNG: `["Lớp 1: Bước một"]`, `["Nhóm 1: Bước một"]` hoặc `["(1) Bước một"]`).
- **Tiến trình bắt buộc dùng `<br/>`:** Đối với các node có tiền tố tiến trình như `Bước X:`, `Pha X:`, `Nhóm X:`, `Lớp X:` hoặc nội dung dài, bắt buộc chèn `<br/>` ngay sau dấu hai chấm (Ví dụ: `NodeID["Bước 1:<br/>Quét tri thức"]`) để hộp node hiển thị vuông vắn, không bị kéo bè ngang hoặc tràn khung trên màn hình di động.
- **Nút hình thoi điều kiện:** `NodeID{"Câu hỏi ngắn gọn"}`. TUYỆT ĐỐI chỉ để câu hỏi ngắn dưới 20 ký tự (Ví dụ: `Check{"Có --add-tests?"}`), không nhét cả câu văn dài vào nút hình thoi để tránh bị đè tràn góc nhọn.
- **NodeID chuẩn ASCII:** `NodeID` bắt buộc là chuỗi ký tự ASCII đơn giản (ví dụ: `A`, `B`, `Step1`, `Node1`), TUYỆT ĐỐI KHÔNG dùng từ khóa hệ thống (như `end`, `subgraph`, `graph`).

## 4. Nhãn Mũi Tên và Liên Kết

- **Cú pháp chuẩn:** `A -->|Nhãn văn bản thuần túy| B` (hoặc `A --> B` nếu không cần nhãn).
- **Cấm dấu nháy kép trong nhãn mũi tên:** TUYỆT ĐỐI KHÔNG đặt dấu nháy kép `"` bên trong cặp thanh đứng `|...|` (Ví dụ SAI: `-->|"Nhãn"|`, ĐÚNG: `-->|Nhãn|`).
- **Ký tự đặc biệt trên nhãn mũi tên:** TUYỆT ĐỐI KHÔNG dùng dấu phẩy `,`, dấu gạch chéo `/` trong nhãn mũi tên (dùng từ thay thế: `hoặc`, `và`, dấu gạch ngang `-`).

## 5. Quy Tắc Bố Cục và Định Dạng Toàn Cục

- **Không dòng trống:** TUYỆT ĐỐI KHÔNG để dòng trống (Empty Line) bên trong khối mã ` ```mermaid `. Toàn bộ các dòng định nghĩa phải liên tục.
- **Quy tắc ký tự `&`:** TUYỆT ĐỐI KHÔNG dùng ký tự `&` trong toàn bộ biểu đồ (thay bằng chữ "và" hoặc "and").
- **Cấm dùng `subgraph`:** TUYỆT ĐỐI KHÔNG dùng `subgraph` đóng khung nhóm (gây sinh ra các đường viền bao quanh khổng lồ và làm lệch bố cục).
- **Bố cục theo luồng:**
  - **Quy trình tuần tự tuyến tính:** Nối đúng theo thứ tự logic liên tục `A --> B --> C --> D --> E...` hoặc dùng `flowchart LR` (trái sang phải) nếu muốn dàn hàng ngang gọn gàng.
  - **Quy trình phân nhánh / Kiến trúc đa tầng:** Thể hiện rõ các nhánh song song, hội tụ hoặc cây phân cấp thực tế (`A --> B`, `A --> C`, `B --> D`, `C --> D...`).
