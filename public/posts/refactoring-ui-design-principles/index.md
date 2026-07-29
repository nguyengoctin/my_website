# Refactoring UI: Những Nguyên Tắc Thiết Kế Giao Diện Cho Developer


> *"Design không phải là làm cho thứ gì đó trông đẹp. Design là làm cho thứ gì đó hoạt động đúng cách."* — **Adam Wathan & Steve Schoger**

{{< admonition note "Nguồn tham khảo / Reference" >}}
Bài viết được tổng hợp và đúc kết từ cuốn sách **Refactoring UI** của **Adam Wathan & Steve Schoger**.
{{< /admonition >}}

Là lập trình viên, mỗi khi viết code chúng ta đều phải đưa ra các quyết định thiết kế hàng ngày — từ khoảng cách button, chọn màu badge, đến bố cục form. Dưới đây là bộ nguyên tắc cốt lõi giúp chúng ta tự tin đưa ra quyết định thiết kế chuẩn mực.

---

## 1. KHỞI ĐẦU THIẾT KẾ (STARTING FROM SCRATCH)

{{< admonition tip "Nguyên tắc 1: Khởi đầu từ tính năng cốt lõi" >}}
- **Bắt đầu từ Feature, không phải Layout:** Đừng vội vẽ Topnav hay Sidebar. Hãy tập trung thiết kế các phần tử cốt lõi của tính năng trước *(Điểm đi, điểm đến, ngày đi, nút Search)*.
- **Phác thảo bằng bút Sharpie / Grayscale:** 
  - Vẽ phác thảo trên giấy bằng bút nét to để ngăn bản thân sa lầy vào chi tiết quá sớm.
  - Thiết kế chỉ với 2 màu **Đen & Trắng (Grayscale)** để tập trung tối đa vào khoảng cách, kích thước và phân cấp thị giác trước khi phối màu.
- **Tập trung vào v1 đơn giản nhất:** Đừng cố thiết kế mọi trường hợp biên dựa trên tưởng tượng. Hãy xây dựng bản đơn giản nhất, kiểm chứng với dữ liệu thực rồi nâng cấp dần.
{{< /admonition >}}

---

## 2. HỆ THỐNG HÓA NGUYÊN LIỆU (DESIGNING WITH SYSTEMS)

{{< admonition info "Nguyên tắc 2: Định nghĩa Design System cố định" >}}
Đừng chọn màu hay font size một cách ngẫu hứng bằng color picker. Hãy định nghĩa sẵn một bộ số liệu cố định:
- **Hệ thống Spacing (Khoảng cách):** Định nghĩa sẵn bảng quy đổi cố định *(4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px)*.
- **Hệ thống Font Size:** Chọn sẵn 8-10 cỡ chữ cố định *(12px, 14px, 16px, 18px, 20px, 24px, 30px, 36px, 48px)*.
- **Hệ thống Màu sắc (Color Palette):**
  - **Grays:** 8-10 tông xám (từ xám cực sáng làm background đến xám đậm làm text).
  - **Primary Color:** 5-9 sắc độ màu chủ đạo (Primary 500 làm màu gốc, 100-400 cho hover/light background, 600-900 cho active/borders).
  - **Accent Colors:** Đỏ (Error), Xanh lá (Success), Vàng (Warning), Xanh dương (Info).
{{< /admonition >}}

---

## 3. PHÂN CẤP THỊ GIÁC (VISUAL HIERARCHY & TYPOGRAPHY)

{{< admonition abstract "Nguyên tắc 3: Phân cấp thị giác & Chữ viết" >}}
- **Phân cấp bằng Font Weight & Color (Không chỉ bằng Font Size):** Tránh việc mọi tiêu đề đều phải tăng kích thước chữ. Hãy dùng **Font Weight (Bold/Medium)** và **Màu xám tối (Dark gray)** thay vì đen tuyền (`#000000`) để phân biệt thông tin chính - phụ.
- **Nguyên tắc Tỉ lệ Nhược thị & Line-height:**
  - Chữ càng lớn (Headings) $\to$ Line-height càng nhỏ *(1.1 đến 1.25)*.
  - Chữ nhỏ (Body text) $\to$ Line-height rộng hơn *(1.5 đến 1.75)* để mắt dễ đọc.
  - **Độ dài dòng lý tưởng:** 45 - 75 ký tự mỗi dòng.
- **Quy tắc Khoảng cách (Proximity Principle):** Khoảng cách giữa các khối nội dung khác nhau luôn lớn hơn khoảng cách giữa các phần tử thuộc cùng một khối.
{{< /admonition >}}

---

## 4. MÀU SẮC & CHIỀU SÂU (COLOR & ELEVATION)

{{< admonition success "Nguyên tắc 4: Mô hình HSL & Chiều sâu giao diện" >}}
- **Phối màu theo mô hình HSL (Hue, Saturation, Lightness):**
  - Không tăng giảm độ sáng chỉ bằng mảng màu xám.
  - **Xoay Hue nhẹ khi điều chỉnh Lightness:** Khi làm sáng một màu, nhích nhẹ Hue về phía màu sáng (Vàng/Cyan). Khi làm tối một màu, nhích Hue về phía màu tối (Xanh lam/Tím).
- **Thay thế Border cứng bằng Chiều sâu:** Bề mặt giao diện phẳng quá nhiều Border sẽ làm mệt mắt. Hãy thay thế Border bằng:
  - **Box-shadow nhẹ:** Tạo độ nổi tinh tế ($y=2\text{px} \dots 8\text{px}$, blur lớn, opacity nhỏ).
  - **Background Color đối lập nhẹ:** Dùng 2 tông xám cạnh nhau (`#F9FAFB` và `#FFFFFF`).
  - **Khoảng trắng (Extra Spacing):** Dùng khoảng trống để chia ranh giới thay vì vẽ đường kẻ.
{{< /admonition >}}

---

## 5. BỐ CỤC & TƯƠNG TÁC (LAYOUT & UI DETAILS)

{{< admonition note "Nguyên tắc 5: Bố cục & Chi tiết tương tác" >}}
- **Empty States:** Khi ứng dụng chưa có dữ liệu, đừng để màn hình trắng trống trãi. Sử dụng minh họa (Illustration) hoặc hướng dẫn kèm nút Action để kích thích tương tác.
- **Table Design:** Căn lề trái cho Văn bản, căn lề phải cho Dữ liệu số (Financials/Metrics). Kết hợp thông tin liên quan chung 1 ô thay vì chia quá nhiều cột hẹp.
- **Overlapping Elements:** Tạo điểm nhấn thị giác bằng cách cho các phần tử đè lên nhau nhẹ *(VD: Avatar đè lên bìa Card, Badge đè lên góc ảnh)*.
{{< /admonition >}}

---

## BẢNG QUY TẮC VÀNG (QUICK CHEAT SHEET)

{{< admonition example "Bảng Quy Tắc Vàng Refactoring UI" >}}
1. **Text màu xám tối (`#111827`) luôn tạo cảm giác cao cấp hơn đen tuyền (`#000000`).**
2. **Line-height nhỏ cho Heading lớn, Line-height rộng cho Body text.**
3. **Khoảng cách giữa 2 group phần tử luôn rộng hơn khoảng cách bên trong 1 group.**
4. **Hạn chế vẽ Border — ưu tiên dùng Box-shadow mờ hoặc hai màu nền khác nhau.**
5. **Căn phải cho dữ liệu số, căn trái cho văn bản.**
{{< /admonition >}}

