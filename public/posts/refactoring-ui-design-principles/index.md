# Refactoring UI: Những Nguyên Tắc Thiết Kế Giao Diện Mà Mọi Developer Nên Biết


> *"Design không phải là làm cho thứ gì đó trông đẹp. Design là làm cho thứ gì đó hoạt động đúng cách."*

{{< admonition note "Nguồn tham khảo / Reference" >}}
Bài viết này được tổng hợp và biên dịch dựa trên cuốn sách **Refactoring UI** của **Adam Wathan & Steve Schoger**. Nội dung gốc tham khảo từ bài viết của [tuananhhedspibk](https://github.com/tuananhhedspibk/tuananhhedspibk.github.io).
{{< /admonition >}}

Là một developer, tôi từng nghĩ thiết kế UI là lãnh địa riêng của designers. Nhưng thực tế là: **mọi người viết code đều phải đưa ra quyết định thiết kế hàng ngày** — từ việc đặt khoảng cách cho một button, chọn màu cho một badge, cho đến bố cục của một form đăng ký. Refactoring UI là cuốn sách giúp developers tư duy đúng về những quyết định đó.

---

## 1. STARTING FROM SCRATCH

### Bắt đầu từ Feature, không phải Layout

Khi bắt tay vào thiết kế một ứng dụng, hầu hết chúng ta đều nghĩ ngay đến:
- Ứng dụng trông sẽ như thế nào?
- Bố cục sẽ ra sao?
- Có cần top nav không?

Nhưng thực ra chúng ta đang chỉ nghĩ về **phần vỏ bên ngoài**. Một ứng dụng thực chất chỉ là tập hợp các *features*. Trước khi thiết kế một feature mà chưa có bất cứ thông tin gì về cách thức vận hành của nó, đây là công thức cho sự... mất phương hướng.

Thay vì bắt đầu ở phần vỏ, hãy bắt đầu với những thành phần thực sự của một feature.

**Ví dụ:** Với service booking flight, bắt đầu với feature "tìm kiếm chuyến bay". Giao diện cần:
- Fields cho điểm đi, điểm đến
- Fields cho ngày đi, ngày trở về
- Button thực thi chức năng search

Và chỉ vậy thôi. Không cần quan tâm đến navigation, sidebar, hay footer ở giai đoạn này.

### Chi tiết đến sau

Một tip hay: **Design trên giấy bằng bút Sharpie**.

![Phác thảo nhanh trên giấy với bút Sharpie thay vì lao vào tool ngay](/images/posts/refactoring-ui/61635785-48236e00-accf-11e9-9f91-2493f2c4fdac.png)

Việc vẽ chi tiết bằng bút Sharpie là điều không thể — nên đây là cách hay để bỏ thói quen đi quá sâu vào chi tiết ngay từ đầu thiết kế.

### Giữ màu Grayscale lúc đầu

Ban đầu nên thiết kế với 2 màu **đen, trắng (grayscale)** — điều này buộc bạn phải chú trọng vào **khoảng cách**, **tương phản**, **kích thước**. Kết quả là bạn sẽ có được giao diện với tính phân cấp tốt trước, rồi mới thêm màu sắc vào sau.

### Đừng đầu tư quá sớm

Build nhanh nhất có thể. Mục đích của bản thiết kế ban đầu là thể hiện ý tưởng — không phải là sản phẩm cuối. Khi đã có quyết định cuối cùng, hãy bỏ bản thô ban đầu và làm lại đúng cách.

{{< admonition tip "Đừng thiết kế quá nhiều" >}}
Không cần thiết kế toàn bộ feature trước khi triển khai. Việc tưởng tượng ra tất cả các trường hợp biên (edge cases) chỉ dựa trên trí tưởng tượng và design tool khiến công việc thiết kế trở nên nhàm chán và khó khăn một cách vô lý. **Hãy bắt đầu từ version đơn giản nhất** và mở rộng dần khi có dữ liệu thực.
{{< /admonition >}}

### Chọn tính cách (Personality) cho giao diện

Mỗi site nên có đặc điểm nhận dạng riêng. Những site liên quan đến ngân hàng hướng đến **bảo mật, tin cậy, chuyên nghiệp**, trong khi startup có thể mang lại hình ảnh **vui nhộn, tươi mới**.

Tính cách được quyết định bởi:

**Font choice:**
- Serif (có chân): sang trọng, cổ điển
- Rounded sans-serif (tròn): vui nhộn, trẻ trung
- Neutral sans-serif (không chân trung tính): đơn giản, hiện đại

**Màu sắc:**
- Xanh nước biển: an toàn, thân thiện
- Vàng kim: đắt đỏ, tinh vi
- Hồng: vui nhộn, không căng thẳng

**Border radius:**

![Border radius nhỏ — không ảnh hưởng nhiều, trang trọng](/images/posts/refactoring-ui/62029311-36851d80-b21d-11e9-885f-3c75d34f4c0d.png)

![Border radius lớn — năng động, thân thiện](/images/posts/refactoring-ui/62029366-5c122700-b21d-11e9-9939-cb35f110d841.png)

![Không có border radius — trang trọng, lịch sự](/images/posts/refactoring-ui/62049065-69450b00-b249-11e9-93a5-eeaf4a1743b0.png)

Điểm mấu chốt: **chỉ sử dụng một loại nút duy nhất** để tạo sự thống nhất.

### Giới hạn lựa chọn của bạn

Khi có quá nhiều lựa chọn (opacity 10% hay 15%? margin 18px hay 20px?), quyết định trở nên cực kỳ khó khăn dù không có lựa chọn nào thực sự tồi.

**Giải pháp: Xây dựng Design System từ trước.**

Đừng tìm màu mới mỗi khi thiết kế UI mới — hãy định nghĩa sẵn 8-10 màu chuẩn:

![Hệ thống màu chuẩn định nghĩa trước trong design system](/images/posts/refactoring-ui/62095587-d8f3de00-b2bb-11e9-9cd6-f45626cac2fb.png)

Đừng chỉnh từng pixel cho đến khi font chữ "hoàn hảo" — hãy tự thiết kế một hệ thống font size ngay từ đầu:

![Hệ thống font size chuẩn: 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72px](/images/posts/refactoring-ui/62095614-e9a45400-b2bb-11e9-8780-a4cdd54215b0.png)

Việc này mất thời gian lúc đầu, nhưng mỗi khi thêm UI mới, bạn sẽ không cần phải ra quyết định lại từ đầu.

---

## 2. HIERARCHY IS EVERYTHING

### Không phải mọi element đều bình đẳng

**Visual Hierarchy** là khái niệm chỉ sự phân cấp giữa các thành phần trong UI. Nếu không có sự phân cấp, mọi thứ cạnh tranh với nhau, tạo ra một bức tường thông tin rối rắm.

Đây là giao diện không có sự phân cấp:

![Giao diện không có Visual Hierarchy — mọi thứ có cùng trọng số](/images/posts/refactoring-ui/62106177-862c1d80-b2df-11e9-9ee3-62b3d5fc0875.png)

Và đây là giao diện đã có sự phân cấp thông tin — dù font chữ và tông màu không thay đổi gì:

![Giao diện đã có Visual Hierarchy — thông tin dễ nắm bắt hơn hẳn](/images/posts/refactoring-ui/62106272-cf7c6d00-b2df-11e9-9794-da144d8edb41.png)

### Kích thước không phải tất cả

Sai lầm phổ biến: *primary content phải có font size lớn, secondary content có font size nhỏ*. Nếu có 4-5 cấp phân cấp thì phải dùng 4-5 font size — nhưng trong một site chỉ nên dùng **tối đa 3 font sizes**.

Thay vào đó, kết hợp nhiều yếu tố:

![Kết hợp màu sắc và font weight để tạo phân cấp thay vì chỉ dùng font size](/images/posts/refactoring-ui/62119405-7110b800-b2fa-11e9-8314-baa62ee86753.png)

Trong một site chỉ cần:
- **2-3 màu:** Dark cho primary (tiêu đề), Grey cho secondary (ngày tháng), Lighter grey cho cấp 3 (copyright)
- **2 font weights:** 400-500 cho text thường, 600-700 cho nội dung muốn nhấn mạnh

### Đừng dùng grey text trên background màu

Light grey text trên background trắng hoạt động hoàn hảo. Nhưng điều này không đúng với background màu:

![Grey text trên background màu trông rất tệ](/images/posts/refactoring-ui/62131911-13d72f80-b317-11e9-9626-2927a427fc2d.png)

Cách đúng: dùng màu text gần với màu background (cùng tông):

![Màu text cùng tông với background — nhìn chuyên nghiệp hơn nhiều](/images/posts/refactoring-ui/62132108-63b5f680-b317-11e9-96d5-4b66e1db4282.png)

Chọn màu dựa theo background color rồi chỉnh độ sáng:

![Kỹ thuật chọn màu text cùng tông với background](/images/posts/refactoring-ui/62134048-d1175680-b31a-11e9-8612-363eb6336da4.png)

### Nhấn mạnh bằng cách làm mờ xung quanh

Đôi lúc muốn nhấn mạnh một item nhưng không thể làm nó nổi hơn được nữa:

![Active nav item không khác gì các inactive items](/images/posts/refactoring-ui/62177971-f7bca800-b381-11e9-97c0-e6fc82fe5d0b.png)

Thay vì cố làm active item nổi bật hơn, hãy **làm mờ (de-emphasize) các item xung quanh**:

![De-emphasize các items xung quanh để active item nổi bật hơn](/images/posts/refactoring-ui/62178091-7f0a1b80-b382-11e9-9268-e1262a3d2499.png)

Có thể áp dụng cho những phần UI lớn hơn — ví dụ bỏ background của sidebar để nội dung chính nổi bật:

![Bỏ background sidebar để nội dung chính của trang được nổi bật hơn](/images/posts/refactoring-ui/62178956-c34aeb00-b385-11e9-820a-5fde97997f5e.png)

### Label: Dùng khi thực sự cần

Hầu hết chúng ta mắc bẫy hiển thị dữ liệu theo format `label: value`. Điều này khiến người đọc khó nắm bắt thông tin vì không có bất cứ hệ thống phân cấp nào.

**Đôi khi không cần label:** `abc@mail.com` → ai cũng biết đó là email. Ngữ cảnh đã nói lên tất cả:

![Ngữ cảnh có thể thay thế label hoàn toàn](/images/posts/refactoring-ui/62182042-3bb6a980-b390-11e9-8a38-758bc7ce5848.png)

**Kết hợp label và value:** Thay vì "In stock: 12", hãy viết "12 in stock" — làm nổi bật value:

![Kết hợp label và value để làm nổi bật thông tin quan trọng](/images/posts/refactoring-ui/62185372-24ca8400-b39d-11e9-8eb0-27a7c7c0652f.png)

**Label là secondary:** Khi cần label (như dashboard), hãy coi label như supporting content — de-emphasize chúng, làm nổi bật dữ liệu:

![Label de-emphasized, dữ liệu nổi bật — đây là cách đúng đắn](/images/posts/refactoring-ui/62186062-c9e65c00-b39f-11e9-810d-1116b52b8329.png)

### Phân cấp thị giác ≠ Phân cấp tài liệu

Chúng ta được dạy rằng `<h1>`, `<h2>` phải có kích cỡ lớn. Nhưng trong nhiều trường hợp, title chỉ đóng **vai trò như label** — nội dung mới là thứ người ta cần đọc:

![Title đôi khi chỉ là label — không cần phải lớn hơn content](/images/posts/refactoring-ui/62189802-e76cf300-b3aa-11e9-84eb-837a008fbe06.png)

> Đừng để element đang sử dụng làm ảnh hưởng đến việc style cho thiết kế.

### Dùng Contrast để bù cho Weight

Khi kết hợp **text** và **icon**, icon thường nổi bật hơn text (đặc biệt solid icons). Cách xử lý: dùng màu nhạt hơn cho icon thay vì thay đổi weight:

![Giảm contrast của icon để cân bằng với text](/images/posts/refactoring-ui/62194093-19368780-b3b4-11e9-8088-17dcc7a779d8.png)

Tương tự, có thể tăng weight của border để bù cho contrast thấp. Border mỏng màu nhạt trông không có nghĩa, nhưng làm tối màu sẽ khiến người dùng tập trung vào border thay vì nội dung:

![Border mỏng, contrast thấp](/images/posts/refactoring-ui/62197592-13907000-b3bb-11e9-8e53-94865dbd9936.png)

![Tăng độ rộng border thay vì tăng độ tối](/images/posts/refactoring-ui/62197749-64a06400-b3bb-11e9-8c83-810b9064501a.png)

### Semantics là thứ yếu

Chúng ta hay mắc bẫy *thiết kế actions theo semantics* mà quên đi tính kế thừa. Trong trang web thường có 1 main action, 2 secondary actions, và một vài tertiary actions.

Nếu thiết kế theo semantics:

![Thiết kế button chỉ theo semantics — không có phân cấp rõ ràng](/images/posts/refactoring-ui/62200702-ee9efb80-b3c0-11e9-982a-5c92cc9bb22f.png)

Thiết kế đúng theo phân cấp:

![Thiết kế button theo phân cấp: Primary solid, Secondary outline, Tertiary link](/images/posts/refactoring-ui/62268151-d33bfb00-b469-11e9-98b8-c50a072b17d6.png)

- **Primary actions:** Background tương phản cao, solid
- **Secondary actions:** Outline style hoặc màu tương phản thấp
- **Tertiary actions:** Style như một link

{{< admonition warning "Destructive Actions" >}}
Actions liên quan đến xóa không có nghĩa là mặc nhiên **primary action**. Nếu không phải primary action, nút xóa nên là secondary hoặc tertiary — không phải lúc nào cũng cần background đỏ to tướng.

![Nút xóa không nhất thiết phải là primary action](/images/posts/refactoring-ui/62268618-590c7600-b46b-11e9-8353-1c69337a666b.png)

Chỉ khi nút xóa đi kèm với bước xác nhận thì nó mới nên là primary action.
{{< /admonition >}}

---

## 3. LAYOUT AND SPACING

### Bắt đầu với quá nhiều White Space

Một trong những cách đơn giản nhất để clean up thiết kế: **thêm nhiều không gian thở hơn cho các elements**.

![Giao diện với white space rộng rãi — thoáng hơn, dễ đọc hơn](/images/posts/refactoring-ui/62293414-84ab5280-b4a3-11e9-9c50-49d8208bc9b2.png)

### White space nên bị xóa, không phải được thêm

Khi thiết kế trông chật chội, chúng ta thường thêm margin/padding — nhưng không gian được thêm thường quá ít nên không cải thiện gì mấy.

Cách tiếp cận tốt hơn: **bắt đầu với thiết kế có nhiều khoảng trắng**, sau đó thu hẹp dần cho đến khi cảm thấy ổn:

![Bắt đầu với nhiều white space rồi thu hẹp dần](/images/posts/refactoring-ui/62293812-5b3ef680-b4a4-11e9-9796-f5e8ef36149e.png)

### Dense UIs cũng có chỗ đứng

Giao diện dashboard (Dense UI) mang lại cảm giác *bận rộn* nhất định — và đó không nhất thiết là xấu. Với những giao diện loại này, không cần quá nhiều khoảng trắng:

![Dashboard dense UI — nhiều thông tin trên một màn hình](/images/posts/refactoring-ui/62294271-8544e880-b4a5-11e9-8d12-79e0e06220a9.png)

### Xây dựng hệ thống Spacing

Thay vì căn chỉnh từng pixel một, hãy xây dựng hệ thống spacing từ trước.

**Tại sao linear scale không hoạt động?** Với elements nhỏ, thay đổi 2px cũng tạo ra sự khác biệt ~25%. Nhưng với elements lớn như card, thay đổi 20px chỉ tạo khác biệt ~2%.

![Với elements nhỏ, ngay cả 2px cũng tạo sự khác biệt đáng kể](/images/posts/refactoring-ui/62372149-b12da000-b571-11e9-8eca-3d55d0f6bbea.png)

**Xây dựng hệ thống:** Dùng base 16px (default font size của trình duyệt) làm cơ sở. Các kích cỡ lớn hơn là bội số của 16px:

![Hệ thống spacing dựa trên base 16px](/images/posts/refactoring-ui/62372718-2c438600-b573-11e9-90b0-8c313e4e358d.png)

Khi có hệ thống spacing, thiết kế sẽ nhất quán và trôi chảy hơn bao giờ hết:

![Áp dụng spacing system vào thực tế](/images/posts/refactoring-ui/62373927-cad0e680-b575-11e9-8566-04910f85ea38.png)

### Đừng cố lấp đầy toàn bộ màn hình

Hiện nay chúng ta thường dùng công cụ thiết kế có canvas rộng 1200-1400px. Nhưng có nhiều không gian không có nghĩa phải dùng hết:

![Element không cần phải full-width nếu content chỉ cần 600px](/images/posts/refactoring-ui/62588703-acfedb00-b901-11e9-9eee-87ebf001ca42.png)

Nếu element chỉ cần 600px thì hãy chỉ dùng 600px:

![Cho element khoảng không gian vừa đủ — không ép mọi thứ phải rộng như nhau](/images/posts/refactoring-ui/62588823-1a127080-b902-11e9-8c29-109449f00760.png)

Navigation full-width không có nghĩa là mọi element khác cũng phải vậy:

![Navigation rộng không đồng nghĩa content phải rộng tương đương](/images/posts/refactoring-ui/62588924-7a091700-b902-11e9-9c68-d69192bc0feb.png)

**Thu nhỏ canvas:** Nếu thiết kế web responsive, hãy bắt đầu từ mobile (400px). Khi hài lòng với mobile, tăng kích cỡ canvas và chỉnh sửa nhỏ:

![Mobile UI (400px)](/images/posts/refactoring-ui/62589508-7080ae80-b904-11e9-9b11-c4dea84d7c46.png)

![Web UI — mở rộng từ mobile design](/images/posts/refactoring-ui/62590319-e259f780-b906-11e9-812c-501b76ec81c8.png)

**Thinking in columns:** Khi thiết kế phù hợp màn hình nhỏ nhưng mất cân bằng trên màn hình rộng, hãy chia thành nhiều cột thay vì chỉ kéo rộng ra:

![Form cho màn hình hẹp](/images/posts/refactoring-ui/62591094-6f05b500-b909-11e9-9ab7-055a6aede993.png)

![Tách supporting text thành cột riêng trên màn hình rộng](/images/posts/refactoring-ui/62591107-80e75800-b909-11e9-8ea2-d33bd9ccb91b.png)

### Grid bị đánh giá quá cao

12-column grid rất phổ biến nhưng không phải lúc nào cũng phù hợp.

**Vấn đề với percentage-based grid:** Sidebar 25% + MainContent 75%. Khi resize màn hình, sidebar cũng resize theo — có thể rộng hơn cần thiết hoặc nhỏ đến mức text bị vỡ:

![Grid percentage gây vấn đề khi resize — sidebar quá rộng hoặc quá hẹp](/images/posts/refactoring-ui/62592516-5f3c9f80-b90e-11e9-97b3-c531a55f78f9.png)

**Giải pháp tốt hơn:** Sidebar dùng fixed width, MainContent flexible với internal grid:

![Fixed width sidebar — linh hoạt và kiểm soát tốt hơn](/images/posts/refactoring-ui/62593199-d7a46000-b910-11e9-93cf-9735a098e432.png)

**Don't force shrink:** Với login card, thay vì phụ thuộc vào grid (6/12 columns), hãy định nghĩa `max-width` và chỉ force shrink khi màn hình nhỏ hơn max-width:

![Login card với grid — shrink khi không cần thiết](/images/posts/refactoring-ui/62682025-13fdbc00-b9f6-11e9-9106-ed516b7e01fb.png)

![Login card với max-width — ổn định hơn](/images/posts/refactoring-ui/62682052-2677f580-b9f6-11e9-8f88-ee393bdd970f.png)

### Relative sizing không scale được

Giả sử: body font size 18px, title font size 45px → tỉ lệ 2.5. Liệu điều này có phù hợp khi màn hình nhỏ đi?

Với màn hình nhỏ (body 14px), nếu giữ nguyên tỉ lệ → title 35px:

![Title 35px trên màn hình nhỏ — quá lớn và không tự nhiên](/images/posts/refactoring-ui/62684281-4e1d8c80-b9fb-11e9-9c24-be924914df0c.png)

Nếu chỉnh title xuống 24px:

![Title 24px trên màn hình nhỏ — tự nhiên và phù hợp hơn nhiều](/images/posts/refactoring-ui/62684433-a94f7f00-b9fb-11e9-8197-f75f1abc03c6.png)

{{< admonition info "Quy tắc tổng quát" >}}
Các phần tử có kích cỡ lớn trên màn hình lớn sẽ bị thu nhỏ **nhanh hơn** là các phần tử có kích cỡ nhỏ khi kích cỡ màn hình bị thu nhỏ. Không có sự khác biệt quá nhiều giữa phần tử lớn và nhỏ ở màn hình có kích cỡ nhỏ. **Hãy scale mọi thứ độc lập với nhau.**
{{< /admonition >}}

Tương tự, với button: nếu giữ nguyên tỉ lệ padding/font-size khi scale:

![Button scale cứng nhắc theo tỉ lệ — không tự nhiên](/images/posts/refactoring-ui/62686010-ca659f00-b9fe-11e9-8da0-8f24856ce178.png)

Nếu thay đổi không theo tỉ lệ cứng:

![Button scale linh hoạt — nút nhỏ thật nhỏ, nút lớn thật lớn](/images/posts/refactoring-ui/62686530-e1f15780-b9ff-11e9-8966-44f4fe6915a7.png)

### Tránh Spacing mơ hồ

Khi thiết kế, spacing và separators là công cụ để phân biệt các *element groups* với nhau.

Khi margin giữa label với input bằng nhau — không có sự liên kết giữa label và input cùng group:

![Margin giữa input với label bằng nhau — không có sự liên kết rõ ràng](/images/posts/refactoring-ui/62750787-5083f300-ba9c-11e9-9663-90f46b2bf698.png)

Khi thay đổi khoảng cách giữa input với label phía dưới, mọi thứ có sự liên kết rõ ràng hơn:

![Khoảng cách khác nhau tạo ra sự liên kết giữa label và input cùng group](/images/posts/refactoring-ui/62750798-5bd71e80-ba9c-11e9-993c-1660df3e01ea.png)

Tương tự trong article: section heading cần khoảng cách phía trên đủ lớn:

![Section heading quá gần với nội dung phía trên — không rõ ràng thuộc section nào](/images/posts/refactoring-ui/62750960-df910b00-ba9c-11e9-9b57-30464b3cc6ae.png)

![Section heading có khoảng cách đủ lớn phía trên — rõ ràng hơn nhiều](/images/posts/refactoring-ui/62750974-eddf2700-ba9c-11e9-8ea7-9975bcd4366d.png)

Điều tương tự cũng xảy ra với các phần tử nằm ngang:

![Elements ngang cần spacing rõ ràng để phân biệt nhóm](/images/posts/refactoring-ui/62751024-2bdc4b00-ba9d-11e9-96c7-06e67e202770.png)

> Khoảng cách xung quanh group elements luôn phải **lớn hơn** khoảng cách bên trong group.

---

## 4. DESIGNING TEXT

### Thiết lập Type Scale

Không quá khó để tìm thấy một thiết kế có quá nhiều font-size:

![Quá nhiều font sizes — thiếu tính hệ thống và nhất quán](/images/posts/refactoring-ui/62755913-c7c38200-bab0-11e9-85c3-ae72c85dd55d.png)

Chọn font-size mà thiếu đi tính hệ thống là ý tưởng tồi vì:
1. Khiến giao diện thiếu tính thống nhất
2. Làm giảm tiến độ công việc

**Modular scales** (tính toán theo tỉ lệ như 4:5, 2:3, 1:1.618) nghe hay nhưng không thực tế: thường cho ra số phân số và không đủ font-sizes cần thiết cho interface design.

**Hand-crafted scales** mới là cách đúng — tự tạo hệ thống để chủ động kiểm soát:

![Hệ thống type scale được dùng phổ biến trong thực tế](/images/posts/refactoring-ui/62756782-01e25300-bab4-11e9-87e2-74bc70b0e80b.png)

![Áp dụng type scale vào interface thực tế](/images/posts/refactoring-ui/62756835-25a59900-bab4-11e9-9897-3edfd7dd70dc.png)

---

## 4. DESIGNING TEXT (tiếp theo)

### Tránh đơn vị em

Không nên dùng đơn vị `em` vì nó là giá trị mang tính tương đối — `em` của nested elements phụ thuộc vào element cha. Điều này dẫn đến việc tạo ra các giá trị ngoài ý muốn:

![em unit trên nested elements gây ra giá trị font size không mong muốn](/images/posts/refactoring-ui/66882296-d5433e00-f004-11e9-877e-ebfa5f6b8ca4.png)

> Hãy sử dụng `px` hoặc `rem` để bảo toàn những gì đang xây dựng cho giao diện.

### Chọn Font tốt

Một vài tricks để chọn fonts phù hợp:

- **Play it safe:** Sans-serif luôn là lựa chọn an toàn. Nếu không tin vào cảm nhận của bản thân, hãy dùng **system font stack**: `-apple-system`, `Segoe UI`, `Roboto`, `Noto Sans`, `Ubuntu`, `Cantarell`, `Helvetica Neue`.
- **Ignore typefaces với ít hơn 5 weights:** Fonts có nhiều weights thường được tạo ra cẩn thận hơn.
- **Optimize for legibility:** Fonts cho headlines có khoảng cách giữa các chữ hẹp hơn fonts cho text nhỏ.

![Chọn font theo mức độ phổ biến trên Google Fonts](/images/posts/refactoring-ui/69127501-b0535680-0aed-11ea-9ca8-05bc75aa8f88.png)

- **Steal from people who care:** Tìm một site bạn yêu thích, inspect để xem họ dùng font gì.

### Giữ Line Length trong tầm kiểm soát

Line length lý tưởng: **45-75 ký tự mỗi dòng**, tương đương chiều rộng **20-35em**.

![Paragraph quá rộng — khó theo dõi khi đọc](/images/posts/refactoring-ui/69203042-b2b5bf00-0b86-11ea-8298-284919f39ec9.png)

Khi kết hợp paragraph với ảnh hoặc components lớn, vẫn nên giữ chiều rộng của paragraph trong khoảng hợp lý dù layout rộng hơn:

![Paragraph giữ chiều rộng hợp lý dù layout rộng](/images/posts/refactoring-ui/69395990-38bb3c80-0d24-11ea-9c91-44a8a5c55003.png)

![Kết hợp paragraph hẹp với content lớn — thoáng và dễ đọc hơn](/images/posts/refactoring-ui/69396015-47095880-0d24-11ea-932a-980fdb40380a.png)

### Căn lề theo Baseline, không phải Center

Khi kết hợp nhiều font sizes trong cùng một dòng, căn lề dọc theo center sẽ trông vụng về:

![Căn giữa với nhiều font sizes — trông không tự nhiên](/images/posts/refactoring-ui/69507770-ff2e3f80-0f76-11ea-8e7d-fa17fa0817ee.png)

Thay vào đó, căn theo **baseline** (đường kẻ chân chữ):

![Căn theo baseline — tự nhiên và chuyên nghiệp hơn](/images/posts/refactoring-ui/69508196-6d273680-0f78-11ea-8372-90be8a761c6a.png)

### Line-height tỉ lệ nghịch với Font Size

Line-height 1.5 là điểm khởi đầu tốt, nhưng cần điều chỉnh theo:

**Chiều rộng dòng:** Paragraph hẹp cần `line-height: 1.5`, paragraph rộng cần `line-height: 2`.

![Line-height cần tỉ lệ thuận với chiều rộng paragraph](/images/posts/refactoring-ui/69515372-be8fef80-0f91-11ea-99ef-e9644450c262.png)

**Font size:** Font nhỏ cần line-height cao hơn, font lớn (headline) chỉ cần `line-height: 1`.

![Text nhỏ cần line-height cao, text lớn cần line-height thấp](/images/posts/refactoring-ui/69520419-03bb1e00-0fa0-11ea-8717-c90c986fdd42.png)

> Line-height và font size **tỉ lệ nghịch** với nhau.

### Không phải Link nào cũng cần màu sắc đặc biệt

Với giao diện chỉ toàn links, việc làm nổi bật bằng màu xanh truyền thống tạo ra sự gượng ép:

![Quá nhiều links màu xanh — giao diện khó nhìn](/images/posts/refactoring-ui/69525059-a4aed680-0faa-11ea-8f34-c51ac5153171.png)

Thay vào đó dùng font weight đậm hơn và màu tối hơn:

![Links nhấn mạnh bằng font weight và màu thay vì màu xanh](/images/posts/refactoring-ui/69525189-e9d30880-0faa-11ea-9b78-17add451e9f0.png)

Với những links không quan trọng, chỉ thêm underline hoặc màu khi hover.

### Căn lề có chủ đích

- **Căn giữa (center):** Tốt cho headlines hoặc text blocks ngắn độc lập.

![Center alignment phù hợp với headlines và text ngắn](/images/posts/refactoring-ui/69639107-529bad00-109f-11ea-9f44-c3b9b4b43948.png)

- **Đừng center long-form text:** Nếu text dài hơn 2-3 dòng, hãy căn trái.

![Long-form text căn trái — dễ đọc hơn căn giữa](/images/posts/refactoring-ui/69639202-7828b680-109f-11ea-92f6-04272e53ea19.png)

- **Căn phải số liệu trong bảng:** Giúp so sánh nhanh hơn.

![Số liệu căn phải trong bảng — so sánh dễ hơn](/images/posts/refactoring-ui/69639864-b2468800-10a0-11ea-801f-e785110cd605.png)

### Letter-spacing hiệu quả

- **Tightening headlines:** Nếu dùng font có letter-spacing rộng cho headline, hãy thu hẹp lại.
- **Improving all-caps:** Với text viết HOA toàn bộ, các chữ có cùng chiều cao nên **tăng letter-spacing** để dễ đọc hơn.

---

## 5. WORKING WITH COLOR

### Dùng HSL thay vì Hex

Hex và RGB không trực quan khi đọc code. **HSL** biểu diễn màu qua 3 thuộc tính gần với thị giác con người:
- **Hue (0-360°):** Vị trí trên bánh xe màu — 0° là đỏ, 120° là xanh lá
- **Saturation (0-100%):** 0% là xám, 100% là sống động
- **Lightness (0-100%):** 0% là đen thuần, 50% là màu hue nguyên chất, 100% là trắng

![HSL trực quan hơn nhiều so với Hex trong code](/images/posts/refactoring-ui/69786683-424e1400-11fe-11ea-8d6e-b184deeaebd8.png)

### Bạn cần nhiều màu hơn bạn nghĩ

Cách phổ biến là chọn 1 màu chủ đạo + palette generator tạo ra 4 màu thêm. Thực tế không đủ dùng.

Bạn cần chia bảng màu thành 3 nhóm:

**Grey (8-10 shades):** Cho text, backgrounds, panels, form controls. Bắt đầu từ dark grey thay vì true black:

![8-10 shades grey từ dark đến light](/images/posts/refactoring-ui/69809816-e00d0780-122d-11ea-9a9d-d6a8efa4816c.png)

**Primary color (5-10 shades):** Màu nhận diện thương hiệu. Ultra-light shades dùng cho alert backgrounds, darker shades dùng cho text:

![Primary color 5-10 shades cho các trường hợp sử dụng khác nhau](/images/posts/refactoring-ui/69810564-8e657c80-122f-11ea-862f-7f9404ad26a1.png)

**Accent colors:** Màu thu hút sự chú ý, plus màu cho các states:
- Đỏ cho destructive actions
- Vàng cho warnings
- Xanh cho positive trends

![Màu đỏ cho destructive actions](/images/posts/refactoring-ui/69935763-307bb200-1519-11ea-9482-7c6eaf8c764d.png)

### Xây dựng Shades từ trước

Đừng dùng các tên màu như "darker" hay "lighter" — sẽ tạo ra mớ bùng nhùng. Hãy tạo một tập cố định các shades (thường là 9 shades từ 100 đến 900):

1. Chọn **base color** phù hợp làm button background
2. Tìm **darkest shade** (dùng cho text) và **lightest shade** (dùng cho background)
3. Điền các shades ở giữa theo nguyên tắc tăng dần

![9 shades từ 100 đến 900 cho một màu hoàn chỉnh](/images/posts/refactoring-ui/69939287-d8e24400-1522-11ea-9f44-83ad6b04b888.png)

### Lightness làm mất Saturation

Trong HSL, khi lightness gần 0% hoặc 100%, ảnh hưởng của saturation giảm. Muốn shades lighter/darker trông rõ ràng, hãy **tăng saturation** khi lightness ra xa 50%.

Ngoài ra, có thể thay đổi độ sáng bằng cách **xoay hue** thay vì chỉ thay đổi lightness:
- Muốn màu sáng hơn: xoay về phía 60°, 180°, 300° (các hues sáng)
- Muốn màu tối hơn: xoay về phía 0°, 120°, 240° (các hues tối)

> Đừng xoay hue quá 20-30° nếu không muốn có một màu hoàn toàn khác.

### Grey không nhất thiết phải là Grey

Grey trong thực tế thường có saturation khá mạnh. Saturate grey với một chút màu tạo ra cảm giác ấm/mát:
- **Saturate với xanh:** Grey mát hơn, nhẹ nhàng hơn
- **Saturate với vàng/cam:** Grey ấm áp hơn

### Accessibility: Tương phản không nhất thiết phải xấu

Normal text (dưới 18px) cần tỉ lệ tương phản ít nhất **4.5:1**, text lớn cần **3:1**.

Khi cần đảm bảo tương phản mà không muốn dùng text trắng trên background tối, hãy **đảo ngược**: dùng text màu đậm trên background màu nhạt hơn.

Ngoài ra, **đừng chỉ dựa vào màu sắc** để truyền thông tin — thêm icons hoặc labels để hỗ trợ người dùng có thị giác màu kém.

---

## 6. CREATING DEPTH

### Mô phỏng nguồn sáng

Trong thực tế, **ánh sáng đến từ phía trên**. Hãy áp dụng nguyên tắc này vào thiết kế:

- **Raised elements (nổi lên):** Cạnh trên sáng hơn cạnh dưới, có box-shadow ngắn phía dưới.

![Button raised: cạnh trên sáng, box-shadow ngắn ở dưới](/images/posts/refactoring-ui/70967089-a3b82300-20d8-11ea-8314-b1796a6a60b3.png)

- **Inset elements (lõm xuống):** Dùng inset box-shadow phía trên và border sáng phía dưới.

![Input inset: inset shadow trên, border sáng dưới](/images/posts/refactoring-ui/70967784-b2073e80-20da-11ea-85a5-900442b18f5b.png)

### Dùng Shadow để diễn đạt độ cao (Elevation)

Shadow nhỏ → element chỉ cao hơn một chút. Shadow lớn → element gần người dùng hơn:

- **Small shadow:** Card bình thường
- **Medium shadow:** Dropdown, popover
- **Large shadow:** Dialog/Modal

Xây dựng **elevation system** với 5 levels shadow, tương tự như font/color system:

![5 levels shadow từ small đến large](/images/posts/refactoring-ui/71067774-7e9ae180-21b8-11ea-95d4-b6974a40fc04.png)

Shadow cũng có thể dùng để diễn đạt tương tác — item được kéo thả sẽ có shadow lớn hơn, button được nhấn sẽ có shadow nhỏ đi.

### Shadow thường có 2 phần

Shadow chuyên nghiệp thường gồm:
1. **Phần lớn:** blur lớn, mô phỏng shadow từ luồng sáng trực tiếp
2. **Phần nhỏ:** blur nhỏ hơn nhưng tối hơn, mô phỏng shadow vùng ánh sáng không chạm tới

![Shadow 2 phần kết hợp — trông tự nhiên hơn](/images/posts/refactoring-ui/71139593-f0733980-2251-11ea-9c5d-321b2c5340c3.png)

### Flat design cũng có chiều sâu

Ngay cả flat design cũng có thể tạo cảm giác chiều sâu:
- **Màu sáng hơn** → cảm giác gần người dùng hơn
- **Solid shadow** (không blur): tạo cảm giác nổi mà vẫn giữ tính phẳng

### Overlap Elements để tạo layers

Di chuyển card để nằm ở vùng chuyển giao giữa 2 backgrounds khác nhau sẽ tạo cảm giác đa tầng:

![Card overlap 2 backgrounds — cảm giác đa tầng](/images/posts/refactoring-ui/71140399-7db78d80-2254-11ea-8b09-7b9668922a3d.png)

---

## 7. WORKING WITH IMAGES

### Text cần Contrast nhất quán

Khi đặt text lên background là ảnh, vấn đề không nằm ở màu của text mà ở bức ảnh — ảnh có cả vùng sáng và vùng tối, text trắng sẽ bị chìm ở vùng sáng:

![Text trắng bị chìm trên vùng sáng của ảnh](/images/posts/refactoring-ui/71790813-bb4e5000-3075-11ea-8551-754ddefbd7ab.png)

Giải pháp:

- **Semi-transparent overlay:** Tráng lớp tối lên ảnh để giảm tương phản
- **Giảm contrast + tăng brightness:** Làm giảm tính sáng tối vốn có
- **Colorize ảnh:** Giảm contrast → desaturate → thêm solid fill với multiply blend mode
- **Text shadow:** Blur radius lớn, không có offset

### Icon không nên Scale up

Scale up SVG icon 3-4x so với intended size sẽ mất đi tính cân xứng. Thay vào đó, bao icon bởi một shape có background color phù hợp:

![Icon trong colored circle — giữ nguyên intended size](/images/posts/refactoring-ui/71959216-82f57000-3235-11ea-9b46-25a66339e630.png)

### Screenshot không nên Scale down

Thu nhỏ screenshot 70% khiến font size thực tế xuống còn 4px — người dùng phải nheo mắt. Giải pháp:
- Chụp ở layout nhỏ hơn (tablet)
- Chỉ chụp khu vực trung tâm của feature
- Tạo simplified version thay thế bằng cách thay text bằng lines đơn giản

### Beware User-Uploaded Content

- Dùng `background-size: cover` để kiểm soát tỉ lệ ảnh upload của người dùng
- Dùng **inner box-shadow nhẹ** thay vì border để tránh "bleed" khi ảnh cùng màu với background

---

## 8. FINISHING TOUCHES

### Supercharge the Defaults

Thay vì thêm chi tiết mới, hãy tận dụng tối đa những gì đang có:

- Bullet list → dùng icons thay vì dấu chấm
- Quote → tăng font size, thay đổi màu
- Links → font weight đậm hơn, underline style độc đáo
- Checkbox → dùng màu nhận diện thương hiệu thay vì màu mặc định browser

### Thêm màu bằng Accent Borders

Một trick đơn giản: thêm accent border màu sắc vào UI:
- `border-top` của Card
- `border-bottom` của active navigation item
- `border-left` của alert message
- Accent ngắn phía dưới headline

![Accent border top trên card — thêm màu sắc không phức tạp](/images/posts/refactoring-ui/72315627-cd179f00-36d6-11ea-8567-4e07340ee9ee.png)

### Trang trí Background

Nếu thiết kế trông đơn điệu dù hierarchy, spacing và typography đều tốt:
- **Thay đổi background color** cho một section
- **Gradient nhẹ:** Dùng 2 hues không khác nhau quá 30 độ
- **Repeating pattern:** Dùng [HeroPattern](http://www.heropatterns.com/)
- **Thêm geometric shapes/illustrations**

> Giữ độ tương phản giữa pattern và background ở mức thấp để đảm bảo tính dễ đọc.

### Đừng bỏ qua Empty States

Khi nội dung phụ thuộc vào dữ liệu từ người dùng, trang sẽ có lúc trống. Đừng để trống — dùng illustrations để thu hút và khuyến khích người dùng hành động:

> Empty state là tương tác đầu tiên của người dùng với sản phẩm. Hãy coi đó là cơ hội để tạo ấn tượng.

### Dùng ít Border hơn

Border làm người dùng tập trung vào nó thay vì nội dung. Thay thế bằng:
- **Box-shadow nhẹ:** Phân cách tinh tế
- **Hai background colors khác nhau:** Các phần tử cạnh nhau khác background color
- **Extra spacing:** Tăng khoảng cách giữa các group

### Think Outside the Box

Hãy phá vỡ "định kiến" về cách một component phải trông như thế nào:
- **Dropdown** có thể multi-column với icons thay vì list đơn giản
- **Table** có thể kết hợp columns liên quan, thêm ảnh/màu sắc
- **Radio buttons** có thể là selectable cards thay vì vòng tròn nhàm chán

---

## Lời Kết

Sau khi đọc hết Refactoring UI, tôi nhận ra **design là một kỹ năng có thể học được** — không phải tài năng bẩm sinh. Các quyết định thiết kế đều có thể tư duy hóa thành nguyên tắc rõ ràng:

- **Xây dựng hệ thống trước:** Màu, font, spacing — định nghĩa một lần, dùng mãi mãi
- **Visual Hierarchy** là nền tảng — không phải màu sắc hay animation
- **White space** là tài sản, không phải không gian lãng phí
- **Scale độc lập** — không có tỉ lệ nào là bất biến cho mọi màn hình
- **De-emphasize** đôi khi hiệu quả hơn emphasize
- **Ánh sáng và shadow** tạo ra chiều sâu — hãy mô phỏng vật lý thực tế
- **Đừng để màu sắc là thứ duy nhất truyền thông tin** — accessibility quan trọng
- **Phá vỡ định kiến** về cách components phải trông như thế nào

Đây là cuốn sách ngắn nhưng mỗi trang đều có thể áp dụng ngay vào dự án thực tế.

---

*Bài viết được tổng hợp từ: **Refactoring UI** — Adam Wathan & Steve Schoger (2019). Nội dung gốc tham khảo từ bài viết của [tuananhhedspibk](https://github.com/tuananhhedspibk/tuananhhedspibk.github.io).*

