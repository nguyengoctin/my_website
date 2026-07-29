# BỘ QUY TẮC VIẾT BLOG CÁ NHÂN (BLOG WRITING RULES)

> *"Writing is a shared learning experience for both the writer and the readers."* — **Huyen Chip**
> *"Nếu bạn có thể nói một vấn đề trong vòng một đoạn văn thì đừng nên dùng một trang A4 để giải thích cái vấn đề đó."* — **Phạm Huy Hoàng**

---

## 1. PHONG CÁCH VĂN PHONG & XƯNG HÔ (TONE & PERSPECTIVE)

- **Xưng hô "Chúng ta" (Shared Learning Experience):**
  Sử dụng "chúng ta" (người viết và người đọc cùng đồng hành) để tạo giọng văn chia sẻ, cùng học hỏi. Tránh giọng điệu dạy đời, xa cách hoặc xưng "tôi - bạn" cứng nhắc.
- **Tập trung vào bản chất bài toán:**
  Đến thẳng vấn đề, nêu rõ lý do tại sao kiến thức/kỹ thuật này quan trọng và ứng dụng thực tế ra sao.

---

## 2. NGUYÊN TẮC TINH GỌN & MẬT ĐỘ THÔNG TIN (CONCISENESS & DENSITY)

- **Nguyên tắc "Không trang A4 dư thừa":**
  Loại bỏ hoàn toàn các đoạn mở bài/kết bài hoa mỹ dài dòng, các câu từ cảm xúc lặp đi lặp lại.
- **Tối ưu hình thức trình bày:**
  - Dùng **Bảng so sánh (Tables)** cho các đối tượng so sánh.
  - Dùng **Danh sách đánh số (Numbered Lists)** cho các quy trình tuần tự.
  - Dùng **Phương trình toán LaTeX** cho công thức hiệu suất.
  - Dùng **Sơ đồ Mermaid / ASCII** cho kiến trúc hệ thống và luồng dữ liệu.

---

## 3. QUY TẮC NGÔN NGỮ & DỊCH THUẬT (NO PARENTHETICAL TRANSLATION)

- **TUYỆT ĐỐI KHÔNG dùng dấu ngoặc đơn `()` để dịch nghĩa tiếng Việt đi kèm:**
  - **SAI (Cấm):** `Spec-Driven Development (Phát triển dựa trên đặc tả)`, `hallucination (ảo giác)`, `nợ kỹ thuật (technical debt)`.
  - **ĐÚNG:** Diễn đạt câu tiếng Việt tự nhiên HOẶC giữ nguyên thuật ngữ chuyên ngành tiếng Anh mà không thêm ngoặc giải thích phía sau.
  - *Ví dụ đúng:* "Spec-Driven Development là phương pháp lấy tài liệu đặc tả làm Nguồn sự thật duy nhất."

---

## 4. ĐỊNH DẠNG PROMPT MẪU (PROMPT SHORTCODE)

- **Sử dụng shortcode `prompt` chuyên dụng:**
  ```markdown
  {{< prompt title="Prompt Mẫu: [Tên Prompt]" >}}
  Nội dung prompt ở đây...
  1. Mục 1
  2. Mục 2
  {{< /prompt >}}
  ```
- **Ưu điểm giao diện:**
  - Định dạng font chữ monospace chuyên dụng cho prompt.
  - **Không đánh số dòng** (no line numbers) để tránh rối mắt.
  - Tích hợp nút **Copy** 1-click góc trên bên phải.
  - Tự động xuống dòng chuẩn từng mục (1, 2, 3, 4, 5, 6, 7, 8).

---

## 5. ĐỊNH DẠNG QUOTE & TRÍCH DẪN (QUOTES)

- **Cú pháp Blockquote chuẩn:**
  ```markdown
  > *"Nội dung câu quote"* — **Tên Tác Giả**
  ```
- Các câu quote đầu bài viết hoặc trong bài sưu tầm quote phải trình bày đơn giản, cô đọng, không kèm các đoạn giải thích trang A4 rườm rà phía dưới.

---

## 6. QUY TẮC SƠ ĐỒ MERMAID (MERMAID DIAGRAMS IN HUGO LOVEIT)

- **Bọc sơ đồ bằng khối mã ` ```mermaid `:**
  ```markdown
  ```mermaid
  flowchart LR
      Step1["Bước 1: Hỏi và giải thích"] --> Step2["Bước 2: Tự tay triển khai"]
  ```
  ```
- **Lưu ý nhãn nút (Node Labels):**
  Bọc nhãn nút trong dấu ngoặc kép `"..."` và không bắt đầu nhãn bằng dạng `1. `, `2. ` để tránh lỗi `Unsupported markdown: list` của Mermaid 11.
