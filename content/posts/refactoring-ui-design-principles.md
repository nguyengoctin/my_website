---
title: "Refactoring UI: Những Nguyên Tắc Thiết Kế Giao Diện Cho Developer"
date: 2026-07-26T22:00:00+07:00
draft: false
author: "Nguyen Ngoc Tin"
tags: ["UI Design", "Refactoring UI", "UX", "Frontend", "Design System"]
categories: ["Tech Blog"]
description: "Toàn bộ những nguyên tắc thiết kế UI chuyên sâu từ cuốn sách Refactoring UI — kèm ảnh minh họa thực tế, dành cho developer muốn tự thiết kế giao diện mà không cần designer."
---

Là lập trình viên, mỗi lần phải đưa ra quyết định thiết kế — chọn màu button, căn khoảng cách, chọn font chữ — đều là một bài toán không có đáp án rõ ràng. Cuốn sách **Refactoring UI** của Adam Wathan & Steve Schoger được viết chính xác cho người như vậy.

{{< admonition note "Nguồn tham khảo" >}}
Tất cả nội dung và hình ảnh trong bài viết đều được tổng hợp từ cuốn sách **Refactoring UI** của **Adam Wathan & Steve Schoger**.
{{< /admonition >}}

---

## Chương 1 — Starting from scratch: Khởi đầu đúng hướng

### Bắt đầu từ feature, không phải layout

Khi bắt tay vào thiết kế một ứng dụng, phản xạ tự nhiên là nghĩ đến bố cục tổng thể: *"Có nên có top nav không? Sidebar bên trái hay bên phải?"* Đây là một cái bẫy — chúng ta đang nghĩ về phần **vỏ bên ngoài** thay vì tính năng thực sự.

Một ứng dụng thực chất chỉ là tập hợp của các feature. Thay vì bắt đầu ở layout, hãy chọn một feature cụ thể và thiết kế các phần tử cốt lõi của nó trước. Ví dụ với ứng dụng đặt vé máy bay, feature đầu tiên là "tìm kiếm chuyến bay" — giao diện chỉ cần field điểm đi, điểm đến, ngày đi và nút Search.

### Chi tiết đến sau

Đừng sa lầy vào icon, shadow, typeface ngay từ đầu. Một mẹo hay là **phác thảo trên giấy bằng bút Sharpie** — loại bút nét to khiến việc vẽ chi tiết nhỏ là điều không thể.

{{< image src="/images/posts/refactoring-ui/61635785-48236e00-accf-11e9-9f91-2493f2c4fdac.webp" caption="Phác thảo bằng bút Sharpie giúp tránh sa đà vào chi tiết sớm" alt="Phác thảo UI bằng bút Sharpie" >}}

### Thiết kế grayscale trước khi phối màu

Ban đầu chỉ thiết kế với **đen và trắng (grayscale)** — điều này buộc chúng ta phải chú trọng vào khoảng cách, tương phản và kích thước. Kết quả là một giao diện có tính phân cấp tốt, và màu sắc chỉ là lớp trang trí thêm vào sau.

### Chọn cá tính cho thiết kế

Mỗi site cần có đặc điểm nhận dạng riêng. Ngân hàng hướng tới sự bảo mật và chuyên nghiệp; startup thì vui nhộn và tươi mới. Cá tính này thể hiện qua:

- **Font:** serif cho sang trọng cổ điển, rounded sans-serif cho vui nhộn, neutral sans-serif cho đơn giản
- **Màu sắc:** xanh dương gợi an toàn thân thiện, vàng kim gợi đắt đỏ tinh vi, hồng gợi vui nhộn nhẹ nhàng
- **Border radius:** 3-4px hầu như không ảnh hưởng, lớn tạo năng động, không có tạo trang trọng

---

## Chương 2 — Limit your choices: Hệ thống hóa mọi quyết định

Khi có quá nhiều lựa chọn — opacity 10% hay 15%? margin-bottom 18px hay 20px? — việc quyết định trở nên cực kỳ mệt mỏi. Giải pháp là **xây dựng hệ thống ngay từ đầu** thay vì chọn từ thư viện vô tận.

Định nghĩa trước:
- **Font size scale:** 8-10 cỡ chữ cố định
- **Color palette:** 8-10 màu cho mỗi nhóm (grays, primary, accent)
- **Spacing system:** bảng khoảng cách dựa theo base 16px
- **Border radius, font weight, shadow levels**

{{< image src="/images/posts/refactoring-ui/62095587-d8f3de00-b2bb-11e9-9cd6-f45626cac2fb.webp" caption="Color palette cố định — không cần mở color picker mỗi lần thiết kế" alt="Color palette cố định" >}}

{{< image src="/images/posts/refactoring-ui/62095614-e9a45400-b2bb-11e9-8780-a4cdd54215b0.webp" caption="Font size scale cố định — thiết kế nhanh hơn và nhất quán hơn" alt="Font size scale" >}}

Khi lựa chọn từ một tập hạn chế, công việc trở nên dễ dàng hơn: chọn giá trị trung tâm, so sánh với 2 giá trị kề bên, chọn cái nào "cảm giác" đúng nhất rồi dừng lại.

---

## Chương 3 — Visual Hierarchy: Phân cấp thị giác là tất cả

### Không phải mọi phần tử đều bình đẳng

Nếu mọi phần tử trong giao diện đều cùng "ấn tượng" như nhau, thiết kế sẽ trở thành một bức tường nội dung — không truyền đạt được thông điệp gì. *Visual Hierarchy* là cách tạo ra liên hệ giữa các phần tử để người dùng biết đâu là quan trọng.

{{< image src="/images/posts/refactoring-ui/62106177-862c1d80-b2df-11e9-9ee3-62b3d5fc0875.webp" caption="Không có phân cấp thị giác — mọi thứ nặng như nhau" alt="Không có phân cấp" >}}

{{< image src="/images/posts/refactoring-ui/62106272-cf7c6d00-b2df-11e9-9794-da144d8edb41.webp" caption="Đã có phân cấp — mắt người biết nhìn vào đâu, dù font và màu không thay đổi" alt="Đã có phân cấp" >}}

### Font size không phải là vũ khí duy nhất

Nếu có 4-5 cấp độ thông tin, chúng ta sẽ cần 4-5 kích cỡ chữ — điều này bất hợp lý. Một site không nên dùng quá 3 font size. Thay vào đó, kết hợp **màu sắc** và **font weight**:

- Sử dụng 2-3 màu: màu tối cho nội dung chính, xám cho nội dung phụ, xám nhạt hơn cho cấp 3
- Sử dụng 2 font weight: 400-500 cho text thường, 600-700 cho nội dung cần nhấn mạnh

{{< image src="/images/posts/refactoring-ui/62119405-7110b800-b2fa-11e9-8314-baa62ee86753.webp" caption="Kết hợp màu và font weight để phân cấp thông tin hiệu quả" alt="Phân cấp bằng màu và font weight" >}}

Tránh dùng font weight dưới 400 cho các đoạn text nhỏ — chúng trông rất khó đọc.

### Đừng dùng text xám trên nền có màu

{{< image src="/images/posts/refactoring-ui/62131911-13d72f80-b317-11e9-9626-2927a427fc2d.webp" caption="Text xám trên nền có màu — tương phản kém, khó đọc" alt="Text xám trên nền có màu" >}}

Thay vào đó, hãy chọn màu text gần với tông màu của nền — cùng hue nhưng thay đổi saturation và lightness cho phù hợp:

{{< image src="/images/posts/refactoring-ui/62134048-d1175680-b31a-11e9-8612-363eb6336da4.webp" caption="Text cùng tông màu với nền — tương phản tự nhiên" alt="Text cùng tông màu" >}}

### Nhấn mạnh bằng cách làm mờ xung quanh

Đôi khi không thể làm item nổi bật hơn dù đã cố gắng. Trong tình huống đó, thay vì cố nhấn mạnh item chính, hãy **làm mờ các item xung quanh**:

{{< image src="/images/posts/refactoring-ui/62177971-f7bca800-b381-11e9-97c0-e6fc82fe5d0b.webp" caption="Active nav item không nổi bật dù đã được style" alt="Active nav item khó phân biệt" >}}

{{< image src="/images/posts/refactoring-ui/62178091-7f0a1b80-b382-11e9-9268-e1262a3d2499.webp" caption="Làm mờ các item không hoạt động — active item nổi lên tự nhiên" alt="De-emphasize để làm nổi active" >}}

Kỹ thuật này cũng áp dụng được cho layout lớn hơn: sidebar đang cạnh tranh sự chú ý với nội dung chính? Bỏ background của sidebar đi, để nội dung hiển thị thẳng lên background.

{{< image src="/images/posts/refactoring-ui/62178956-c34aeb00-b385-11e9-820a-5fde97997f5e.webp" caption="Sidebar không có background — nội dung chính nổi lên tự nhiên" alt="Sidebar không có background" >}}

### Khi nào cần label, khi nào không

Hiển thị dữ liệu theo kiểu `label: value` là cái bẫy phổ biến — format này không có phân cấp, mọi thứ đều trông như nhau.

Trong nhiều trường hợp không cần label vì nội dung đã tự nói lên: `abc@mail.com` hiển nhiên là email, `01923-12312` là số điện thoại. Ngữ cảnh có thể thay thế label.

{{< image src="/images/posts/refactoring-ui/62182042-3bb6a980-b390-11e9-8a38-758bc7ce5848.webp" caption="Ngữ cảnh thay thế label — giao diện gọn hơn, có phân cấp hơn" alt="Giao diện không cần label" >}}

Khi cần kết hợp label và value, ưu tiên làm nổi value: thay vì "In stock: 12", hãy nói "12 in stock":

{{< image src="/images/posts/refactoring-ui/62185372-24ca8400-b39d-11e9-8eb0-27a7c7c0652f.webp" caption="Value được đặt trước — người đọc nắm thông tin quan trọng ngay lập tức" alt="Value được nhấn mạnh" >}}

Khi thực sự cần label (như trong dashboard nhiều dữ liệu), hãy de-emphasize label và làm nổi value:

{{< image src="/images/posts/refactoring-ui/62186062-c9e65c00-b39f-11e9-810d-1116b52b8329.webp" caption="Label nhạt đi, value nổi lên — phân cấp rõ ràng hơn" alt="Label de-emphasized" >}}

### Cân bằng weight và contrast

Font bold nổi bật hơn regular vì chiếm nhiều diện tích hơn. Khi kết hợp text và icon, icon thường nổi bật hơn — nhưng không thể chỉnh weight của icon. Giải pháp: dùng **màu nhạt hơn cho icon**:

{{< image src="/images/posts/refactoring-ui/62194093-19368780-b3b4-11e9-8088-17dcc7a779d8.webp" caption="Icon nhạt màu hơn text — cân bằng tốt hơn dù icon nặng hơn về mặt thị giác" alt="Icon nhạt hơn text" >}}

Ngược lại, với border mỏng màu nhạt, có thể **tăng width của border** thay vì làm tối màu để giữ nguyên màu sắc mà vẫn tạo được sự phân cách:

{{< image src="/images/posts/refactoring-ui/62197749-64a06400-b3bb-11e9-8c83-810b9064501a.webp" caption="Tăng width border thay vì màu tối — giữ được tính nhẹ nhàng" alt="Tăng width border" >}}

### Phân cấp các action

Trong mỗi trang thường có 1 primary action, 2-3 secondary, và một số tertiary. Thiết kế theo ngữ nghĩa mà bỏ qua phân cấp sẽ tạo ra giao diện hỗn loạn:

- **Primary:** background tương phản cao, solid
- **Secondary:** outline hoặc màu tương phản thấp
- **Tertiary:** style như link, không có background

{{< image src="/images/posts/refactoring-ui/62268151-d33bfb00-b469-11e9-98b8-c50a072b17d6.webp" caption="Các action được phân cấp rõ — người dùng biết hành động nào ưu tiên" alt="Phân cấp action" >}}

Destructive action (xóa, hủy) không mặc nhiên là primary. Chỉ khi đi kèm với bước xác nhận thì nó mới nên là primary:

{{< image src="/images/posts/refactoring-ui/62268618-590c7600-b46b-11e9-8353-1c69337a666b.webp" caption="Destructive action không phải lúc nào cũng cần đỏ và nổi bật" alt="Destructive action phân cấp" >}}

---

## Chương 4 — Layout & Spacing: Bố cục và khoảng trắng

### Đừng ép element lấp đầy toàn màn hình

Màn hình rộng không có nghĩa phải dùng hết. Nếu element chỉ cần 600px, hãy chỉ dùng 600px và tạo khoảng không gian xung quanh:

{{< image src="/images/posts/refactoring-ui/62588703-acfedb00-b901-11e9-9eee-87ebf001ca42.webp" caption="Navigation full-width không có nghĩa các element khác cũng vậy" alt="Element không cần full width" >}}

{{< image src="/images/posts/refactoring-ui/62588924-7a091700-b902-11e9-9c68-d69192bc0feb.webp" caption="Cho element không gian vừa đủ — không nhiều hơn, không ít hơn" alt="Khoảng cách phù hợp" >}}

Khi cần responsive, bắt đầu từ mobile (400px) rồi tăng dần canvas. Với layout có sidebar, đặt sidebar **fixed width** và để MainContent thay đổi — tránh dùng % vì sidebar sẽ bị vỡ khi màn hình quá hẹp:

{{< image src="/images/posts/refactoring-ui/62593199-d7a46000-b910-11e9-93cf-9735a098e432.webp" caption="Sidebar fixed width, MainContent fluid — responsive tốt hơn" alt="Sidebar fixed width" >}}

### Sizing tương đối không tự động scale

Khi body text 18px và title 45px (tỉ lệ 2.5x) trên desktop, nếu áp dụng cứng tỉ lệ đó cho mobile (body 14px → title 35px), title sẽ quá lớn so với màn hình nhỏ. Thực tế title 24px sẽ phù hợp hơn nhiều — tỉ lệ thực là 1.7x:

{{< image src="/images/posts/refactoring-ui/62684281-4e1d8c80-b9fb-11e9-9c24-be924914df0c.webp" caption="Title 35px trên mobile theo tỉ lệ cố định — quá lớn" alt="Title quá lớn trên mobile" >}}

{{< image src="/images/posts/refactoring-ui/62684433-a94f7f00-b9fb-11e9-8197-f75f1abc03c6.webp" caption="Title 24px — tỉ lệ nhỏ hơn nhưng cảm giác phù hợp hơn cho màn hình nhỏ" alt="Title phù hợp trên mobile" >}}

### Bắt đầu với quá nhiều khoảng trắng

Khi thiết kế có cảm giác chật chội, thói quen là thêm margin — nhưng thường chỉ thêm được ít nên không cải thiện nhiều. Cách tốt hơn: **bắt đầu với rất nhiều khoảng trắng**, sau đó thu hẹp dần cho đến khi cảm thấy ổn.

{{< image src="/images/posts/refactoring-ui/62293812-5b3ef680-b4a4-11e9-9796-f5e8ef36149e.webp" caption="Bắt đầu với nhiều khoảng trắng — hơi nhiều thực ra rất gần với vừa đủ" alt="Nhiều khoảng trắng" >}}

### Hệ thống spacing thay vì căn từng pixel

Xây dựng hệ thống spacing dựa trên base 16px. Các kích cỡ nhỏ gần nhau, kích cỡ lớn cách xa nhau dần:

{{< image src="/images/posts/refactoring-ui/62372718-2c438600-b573-11e9-90b0-8c313e4e358d.webp" caption="Hệ thống spacing — thiết kế nhanh hơn và nhất quán hơn" alt="Hệ thống spacing" >}}

### Khoảng cách phải làm rõ mối liên hệ

Khi khoảng cách giữa label và input bằng nhau theo mọi hướng, người dùng không biết label nào thuộc về input nào:

{{< image src="/images/posts/refactoring-ui/62750787-5083f300-ba9c-11e9-9663-90f46b2bf698.webp" caption="Khoảng cách đều nhau — không có sự liên kết rõ ràng" alt="Khoảng cách không rõ ràng" >}}

{{< image src="/images/posts/refactoring-ui/62750798-5bd71e80-ba9c-11e9-993c-1660df3e01ea.webp" caption="Khoảng cách phía dưới input lớn hơn — label gắn chặt với input của nó" alt="Khoảng cách rõ ràng" >}}

{{< admonition tip "Quy tắc Proximity" >}}
Khoảng cách **xung quanh** một group elements luôn phải lớn hơn khoảng cách **bên trong** group đó.
{{< /admonition >}}

---

## Chương 5 — Typography: Thiết kế chữ viết

### Hệ thống font size

Quá nhiều font size trong một thiết kế khiến giao diện thiếu nhất quán. Không nên dùng modular scale (golden ratio...) vì thường cho kết quả phân số và thiếu các kích cỡ trung gian. Cách thực tế nhất là **tự tạo bằng tay** 8-10 kích cỡ phù hợp:

{{< image src="/images/posts/refactoring-ui/62756782-01e25300-bab4-11e9-87e2-74bc70b0e80b.webp" caption="Hệ thống font size — chọn từ tập cố định thay vì tuỳ hứng" alt="Hệ thống font size" >}}

### Tránh dùng đơn vị em cho font size

Đơn vị `em` là tương đối — phụ thuộc vào font size của element cha. Khi có nested elements, giá trị em sẽ cascade và tạo ra kết quả không mong muốn:

{{< image src="/images/posts/refactoring-ui/66882296-d5433e00-f004-11e9-877e-ebfa5f6b8ca4.webp" caption="Cascading với đơn vị em — phần tử con có font size 20px dù được khai báo 1em" alt="Vấn đề với đơn vị em" >}}

Hãy dùng `px` hoặc `rem` để bảo toàn thiết kế.

### Chiều rộng dòng lý tưởng: 45-75 ký tự

Khi styling paragraph, lỗi phổ biến là kéo text ra full width của container — dòng dài khó đọc. Chiều rộng lý tưởng là **45-75 ký tự**, tương đương **20-35em**:

{{< image src="/images/posts/refactoring-ui/69203042-b2b5bf00-0b86-11ea-8298-284919f39ec9.webp" caption="Dòng quá dài — mắt mệt mỏi khi theo dõi từ đầu sang cuối" alt="Dòng văn bản quá dài" >}}

### Line-height và font size tỉ lệ nghịch

- **Text nhỏ:** cần line-height cao (1.5-2.0) để mắt dễ tìm dòng tiếp theo
- **Heading lớn:** chỉ cần line-height thấp (1.0-1.25)

{{< image src="/images/posts/refactoring-ui/69518580-49291c80-0f9b-11ea-907a-769c4725db4b.webp" caption="Text nhỏ cần line-height rộng để dễ đọc" alt="Line-height cho text nhỏ" >}}

{{< image src="/images/posts/refactoring-ui/69520419-03bb1e00-0fa0-11ea-8717-c90c986fdd42.webp" caption="Text lớn chỉ cần line-height ngắn — line-height 1.0 là đủ" alt="Line-height cho heading" >}}

### Căn baseline khi kết hợp nhiều font size

Khi kết hợp nhiều cỡ chữ trong một dòng, căn giữa (vertical center) trông vụng về. Căn theo **baseline** — đường kẻ ngang làm chân đế của ký tự — tự nhiên hơn nhiều:

{{< image src="/images/posts/refactoring-ui/69508020-e5d9c300-0f77-11ea-812c-ce6d61ecbc7b.webp" caption="Căn baseline — nhiều font size cùng dòng nhưng vẫn liên kết tự nhiên" alt="Căn baseline" >}}

### Căn lề text đúng ngữ cảnh

- Center align: phù hợp với headline ngắn, text block độc lập — không dùng cho đoạn văn dài hơn 2-3 dòng
- Right align: dành riêng cho dữ liệu số trong bảng để dễ so sánh
- Left align: mặc định cho mọi nội dung văn bản

{{< image src="/images/posts/refactoring-ui/69639864-b2468800-10a0-11ea-801f-e785110cd605.webp" caption="Căn phải cho số liệu — so sánh giữa các hàng dễ dàng hơn nhiều" alt="Căn phải cho số liệu" >}}

### Tăng letter-spacing cho all-caps

Với text chỉ toàn chữ hoa, các ký tự có cùng chiều cao nên letter-spacing mặc định khiến việc đọc khó hơn. Hãy **tăng letter-spacing** để phân biệt giữa các ký tự:

{{< image src="/images/posts/refactoring-ui/69774326-ffc61080-11d8-11ea-848d-851b838bdb7d.webp" caption="All-caps với letter-spacing mặc định — khó đọc" alt="All-caps khó đọc" >}}

{{< image src="/images/posts/refactoring-ui/69774508-72cf8700-11d9-11ea-96ff-13841f130901.webp" caption="All-caps với letter-spacing tăng — dễ đọc hơn nhiều" alt="All-caps dễ đọc" >}}

---

## Chương 6 — Working with Color: Làm chủ màu sắc

### Chuyển sang HSL thay vì hex

Hex code (`#3d5af1`) không trực quan. HSL hiển thị màu theo cách mắt người cảm nhận:

- **Hue:** vị trí trên bánh xe màu (0° = đỏ, 120° = xanh lá, 240° = xanh dương)
- **Saturation:** mức độ sống động (0% = xám, 100% = sống động)
- **Lightness:** mức độ sáng tối (0% = đen, 50% = màu thuần, 100% = trắng)

### Cần nhiều màu hơn bạn nghĩ

Bảng màu thực dụng cần ít nhất 3 loại:

**Grays** — dùng cho text, background, panel. Cần 8-10 sắc độ:

{{< image src="/images/posts/refactoring-ui/69809672-8c9ab980-122d-11ea-8d14-8a54dfdd42bb.webp" caption="Bảng màu gray đầy đủ — từ background sáng đến text tối" alt="Bảng màu gray" >}}

**Primary color(s)** — màu nhận diện thương hiệu, cần 5-10 sắc độ (ultra-light cho background alert, darker cho text):

{{< image src="/images/posts/refactoring-ui/69810564-8e657c80-122f-11ea-862f-7f9404ad26a1.webp" caption="Primary color với nhiều sắc độ — đủ dùng cho mọi ngữ cảnh" alt="Primary color palette" >}}

**Accent colors** — màu trạng thái: đỏ cho xóa/hủy, vàng cho warning, xanh lá cho thành công. Mỗi accent cũng cần 5-10 sắc độ.

### Xây dựng palette màu đúng cách

Hãy tạo **9 shades** từ 100 đến 900:

1. Chọn màu base (phù hợp làm button background)
2. Chọn shade tối nhất (dùng cho text) và sáng nhất (dùng cho background)
3. Điền các shade trung gian sao cho chúng dung hòa với 2 biên

{{< image src="/images/posts/refactoring-ui/69939287-d8e24400-1522-11ea-9f44-83ad6b04b888.webp" caption="9 shades từ 100-900 — đủ dùng mà không bị giới hạn" alt="9 shades palette" >}}

### Giữ saturation khi điều chỉnh lightness

Trong HSL, khi lightness tiến về 0% hoặc 100%, saturation mất dần ảnh hưởng. Để các sắc độ lighter/darker vẫn giữ được màu sống động, hãy **tăng saturation** khi lightness ra xa 50%:

{{< image src="/images/posts/refactoring-ui/69962246-ef06f900-1550-11ea-99cd-e8f730741df3.webp" caption="Tăng saturation khi lightness ra xa 50% — màu giữ được độ sống động" alt="Tăng saturation" >}}

### Thay đổi độ sáng bằng cách xoay hue

Chỉ thay đổi lightness sẽ khiến màu trở nên trắng hoặc đen hơn, làm mất cường độ màu. Thay vào đó, **xoay hue**:
- Để làm sáng: xoay hue về phía 60°, 180°, hoặc 300°
- Để làm tối: xoay hue về phía 0°, 120°, hoặc 240°

{{< image src="/images/posts/refactoring-ui/70026345-e3fca900-15e2-11ea-8cc4-b6b1b1c68ef2.webp" caption="Kết hợp xoay hue và đổi lightness — màu vẫn sống động ở cả sắc độ tối và sáng" alt="Xoay hue để thay đổi độ sáng" >}}

Đừng xoay hue quá 20-30° nếu không muốn có màu hoàn toàn khác.

### Gray cũng có thể có màu

True grey có saturation 0% — không có màu thực sự. Trong thực tế, grey có thể "ấm" hơn bằng cách thêm một chút vàng/cam, hoặc "mát" hơn bằng cách thêm một chút xanh dương:

{{< image src="/images/posts/refactoring-ui/70028156-39d35000-15e7-11ea-837f-a8ec1e842da8.png" caption="Grey với chút blue saturation — cảm giác mát và hiện đại hơn" alt="Cool grey" >}}

### Đừng chỉ dựa vào màu sắc

Với người dùng có thị giác màu kém, giao diện phụ thuộc hoàn toàn vào màu sẽ không truyền đạt được thông tin. Hãy thêm các yếu tố phụ như mũi tên lên/xuống cho trend, icon để phân biệt trạng thái:

{{< image src="/images/posts/refactoring-ui/70105579-920c5f80-1684-11ea-96df-efee655227a0.webp" caption="Thêm mũi tên để hỗ trợ người dùng mù màu phân biệt trend" alt="Hỗ trợ người dùng mù màu" >}}

---

## Chương 7 — Creating Depth: Tạo chiều sâu

### Giả lập nguồn sáng từ trên xuống

Ánh sáng luôn đến từ phía trên. Để tạo hiệu ứng "nổi" hay "chìm", hãy mô phỏng nguyên tắc này:

- **Raised elements (nổi):** cạnh trên sáng hơn, có bóng nhỏ phía dưới
- **Inset elements (chìm):** inset shadow từ trên, bottom border sáng nhạt

{{< image src="/images/posts/refactoring-ui/70967089-a3b82300-20d8-11ea-8314-b1796a6a60b3.webp" caption="Button raised — ánh sáng từ trên, bóng đổ xuống dưới" alt="Raised button" >}}

{{< image src="/images/posts/refactoring-ui/70967784-b2073e80-20da-11ea-85a5-900442b18f5b.webp" caption="Input inset — ánh sáng phía dưới, bóng đổ vào trong từ trên" alt="Inset input" >}}

### Dùng shadow để biểu thị khoảng cách trục Z

Shadow nhỏ + blur nhẹ = element chỉ cao hơn bề mặt một chút. Shadow lớn + blur mạnh = element gần người dùng hơn. Hãy xây dựng sẵn **5 mức shadow** từ nhỏ đến lớn:

{{< image src="/images/posts/refactoring-ui/70968836-af5a1880-20dd-11ea-8cd1-a2049694b9e9.webp" caption="Hệ thống shadow từ nhỏ đến lớn — tương ứng với khoảng cách trục Z" alt="Hệ thống shadow" >}}

Shadow cũng phản ánh tương tác — item đang drag có shadow lớn hơn, button khi nhấn giảm shadow:

{{< image src="/images/posts/refactoring-ui/71068624-73e14c00-21ba-11ea-90ae-29212f8ed38a.webp" caption="Shadow giảm khi button được nhấn — phản ánh tương tác vật lý" alt="Shadow khi nhấn button" >}}

### Shadow có thể có 2 tầng

Trong thực tế, shadows thường có 2 phần:
- **Tầng 1:** lớn hơn, blur lớn hơn — mô phỏng shadow từ nguồn sáng trực tiếp
- **Tầng 2:** nhỏ hơn, tối hơn, blur nhỏ hơn — shadow phía dưới object

{{< image src="/images/posts/refactoring-ui/71139593-f0733980-2251-11ea-9c5d-321b2c5340c3.webp" caption="Shadow 2 tầng — tự nhiên và chiều sâu hơn so với shadow đơn" alt="Shadow 2 tầng" >}}

### Tạo chiều sâu bằng cách xếp chồng element

Di chuyển card để nằm ở vùng chuyển giao giữa 2 background khác nhau — tạo cảm giác "đa tầng":

{{< image src="/images/posts/refactoring-ui/71140399-7db78d80-2254-11ea-8b09-7b9668922a3d.webp" caption="Card overlap 2 background — tạo cảm giác đa tầng tự nhiên" alt="Card overlap background" >}}

---

## Chương 8 — Finishing Touches: Đánh bóng thiết kế

### Tận dụng tối đa những gì đang có

Trước khi thêm element mới, hãy khai thác những gì đã có:

- Thay bullet list bằng icon phù hợp ngữ cảnh (khóa cho bảo mật, check cho tính năng...)
- Tạo quote block với font size lớn hơn và màu khác để làm điểm nhấn
- Style custom checkbox, radio button với màu nhận diện thay vì màu browser mặc định

{{< image src="/images/posts/refactoring-ui/72050581-d387ce80-3304-11ea-8bbe-42e0080d954e.webp" caption="Quote được style nổi bật — cùng nội dung nhưng tạo ấn tượng tốt hơn" alt="Quote được style" >}}

### Dùng accent border thêm màu sắc

Thêm **colored accent border** vào các phần tử để tạo điểm nhấn mà không thay đổi nhiều thiết kế — `border-top` của card, `border-bottom` của active nav item, cạnh trái của alert message:

{{< image src="/images/posts/refactoring-ui/72315627-cd179f00-36d6-11ea-8567-4e07340ee9ee.webp" caption="Accent border-top trên card — thêm màu sắc mà không tốn thêm không gian" alt="Accent border trên card" >}}

### Hạn chế dùng border — có 3 lựa chọn tốt hơn

Border tạo ra sự phân mảnh và thu hút sự chú ý không cần thiết. Thay vào đó:

1. **Box-shadow nhẹ** — phân cách tinh tế
2. **Hai background color khác nhau** — element cạnh nhau có nền xám nhạt và trắng
3. **Thêm khoảng cách** — khoảng trắng đủ lớn tự tạo ra ranh giới

{{< image src="/images/posts/refactoring-ui/73656483-8f090c00-46d3-11ea-8a6e-837e60f969f5.webp" caption="Hai background color khác nhau — phân cách rõ mà không cần border" alt="Hai background color để phân cách" >}}

### Thiết kế empty states

Empty state là **tương tác đầu tiên** của người dùng với một feature mới — đây là cơ hội tạo ấn tượng tốt. Đừng để màn hình trống rỗng, hãy thêm illustration và call-to-action rõ ràng:

{{< image src="/images/posts/refactoring-ui/73608938-ffe4f100-460b-11ea-8e7c-d3b708cc361e.webp" caption="Empty state với illustration và call-to-action — khuyến khích người dùng bắt đầu" alt="Empty state tốt" >}}

### Thoát ra khỏi khuôn mẫu

Hầu như chúng ta đều có định kiến về cách một component phải trông như thế nào. Dropdown phải là danh sách thẳng? Radio button phải là vòng tròn nhàm chán? Hãy thử phá vỡ quy ước:

{{< image src="/images/posts/refactoring-ui/73657518-c8db1200-46d5-11ea-9691-a4f5392b6a09.webp" caption="Dropdown multi-column với icon — phong phú hơn mà vẫn dễ dùng" alt="Dropdown phong phú" >}}

{{< image src="/images/posts/refactoring-ui/73658545-db564b00-46d7-11ea-86fd-53b15e939483.webp" caption="Selectable card thay cho radio button — trực quan và hấp dẫn hơn" alt="Selectable card thay radio button" >}}

### Leveling up — Cách trau dồi thêm

Khi bắt gặp một thiết kế đẹp, hãy tự hỏi: *"Designer đã thực hiện điều gì mà mình có thể sẽ không bao giờ làm?"* Ví dụ: thêm background color cho date-picker, đặt button bên trong text input, dùng 2 màu chữ cho headline.

Cách tốt nhất để chú ý đến chi tiết là **xây dựng lại thiết kế đó từ đầu** — khi nhận ra sự khác biệt, chúng ta sẽ khám phá ra những tricks như giảm line-height cho heading, tăng letter-spacing cho uppercase, kết hợp nhiều box-shadow.

{{< image src="/images/posts/refactoring-ui/73660185-07270000-46db-11ea-9e6c-b25a1e40842d.webp" caption="Rebuild một thiết kế đẹp từ đầu — cách học hiệu quả nhất" alt="Rebuild thiết kế" >}}
