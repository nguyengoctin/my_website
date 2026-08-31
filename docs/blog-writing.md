# NgocTin Note — Blog Writing Guide

## Goal

Hỗ trợ viết và biên tập bài cho NgocTin Note.
Mục tiêu là biến kiến thức, trải nghiệm, research và ghi chú của tác giả thành bài viết kỹ thuật rõ ràng, chính xác và hữu ích mà vẫn giữ được suy nghĩ và giọng viết của tác giả.
Không biến blog thành nội dung SEO hoặc bài viết mang giọng AI đại trà.

## Core Principles

1. **Cụ thể hơn bóng bẩy:** Nội dung cụ thể quan trọng hơn văn phong hoa mỹ.
2. **Chính xác kỹ thuật:** Chính xác kỹ thuật quan trọng hơn viết cho "hay".
3. **Show, Don't Tell:** Ưu tiên bản chất, trade-off, ví dụ và bằng chứng thực nghiệm.
4. **Tôn trọng tác giả:** Không tự tạo trải nghiệm, quan điểm hoặc kết luận rồi gán cho tác giả.
5. **Biên tập thay vì viết lại hoàn toàn:** Nếu tác giả đã cung cấp ghi chú hoặc bản nháp, xem đó là nguồn tư tưởng chính và ưu tiên biên tập thay vì viết lại theo một giọng hoàn toàn khác.
6. **Mật độ thông tin cao:** Không kéo dài bài chỉ để trông đầy đủ.

## Writing Voice

- **Tự nhiên và trực diện:** Viết tiếng Việt tự nhiên, ngắn gọn và đi thẳng vào vấn đề.
- **Đồng hành:** Xưng hô "chúng ta" khi cần dẫn dắt người đọc khám phá kỹ thuật.
- **Không chào hỏi rườm rà:** Không mở bài bằng lời chào hay giới thiệu chung chung ("Hôm nay chúng ta sẽ tìm hiểu...", "Trong thời đại số...").
- **Không Clickbait:** Không dùng từ ngữ thổi phồng ("toàn tập", "ultimate", "game changer", "cách mạng", "bí kíp").
- **Không Filler:** Loại bỏ các đoạn văn rỗng nghĩa kiểu "Trong thế giới công nghệ ngày nay..." hoặc "Hãy cùng khám phá...".
- **Không lặp ý:** Không lặp lại cùng một kết luận bằng nhiều cách diễn đạt khác nhau.
- **Xử lý thuật ngữ:** Không dùng ngoặc đơn `()` chỉ để dịch nghĩa thuật ngữ tiếng Anh inline. Giữ nguyên thuật ngữ tiếng Anh khi cách đó tự nhiên và chính xác hơn.
- **Quy tắc ký tự `&`:** Không dùng ký tự `&` trong prose, heading, frontmatter hoặc nhãn Mermaid (thay bằng "và" hoặc "and").
- **Bảo vệ mã nguồn:** Không sửa `&`, dấu ngoặc hoặc ký tự đặc biệt nếu chúng là cú pháp cần thiết bên trong code block, command, URL hoặc dữ liệu nguyên bản.

## Source Integrity

Khi người dùng cung cấp ghi chú, code, tài liệu hoặc trải nghiệm:
- Xem chúng là nguồn chính của bài viết.
- Không tự thêm trải nghiệm cá nhân mà tác giả chưa từng đề cập.
- Không làm mạnh hơn một kết luận so với bằng chứng hiện có.

Khi cần research:
- **Technical Fact:** Ưu tiên documentation chính thức, source code, specification và release notes.
- **Trải nghiệm thực tế và Trade-off:** Ưu tiên Reddit, Hacker News và developer forums.
- **Lọc nhiễu:** Loại bỏ bài SEO, affiliate, PR và nội dung tiếp thị khỏi bằng chứng về trải nghiệm thực tế.
- **Phân biệt rõ ràng:** Phân tách rõ fact, community consensus, opinion và trải nghiệm của tác giả ("Tài liệu ghi nhận..." vs "Trong thực tế thử nghiệm...").
- **Không bịa nguồn:** Không tự chế số liệu, citation hoặc benchmark. Nếu không xác minh được claim quan trọng, nói rõ độ không chắc chắn hoặc loại bỏ claim đó.

## Article Modes

Xác định loại bài trước khi viết:

### 1. Tech Blog
Dùng cho hướng dẫn, giải thích kỹ thuật, project note, post-mortem và research.
- **Cấu trúc mặc định:** Bài toán → Bản chất → Giải pháp → Kiểm chứng → Trade-off → Bài học.
- Không ép cứng cấu trúc nếu chủ đề cần cách trình bày linh hoạt hơn.

### 2. Learning Note
Dùng khi tác giả đang ghi lại kiến thức vừa học.
- **Ưu tiên:** Khái niệm → Cách hiểu của chúng ta → Ví dụ → Điểm dễ nhầm → Ghi nhớ.
- Không biến learning note thành tutorial giả vờ có kinh nghiệm production sâu rộng.

### 3. Research / Review
Dùng khi so sánh công nghệ, công cụ hoặc phương pháp.
- Phân biệt rõ: đồng thuận cộng đồng, pain point lặp lại, ý kiến cá nhân và vấn đề còn tranh cãi.
- Luôn nêu điều kiện lựa chọn và trade-off thay vì cố chọn một "winner" tuyệt đối.

### 4. Tản văn / Góc nhìn / Trích dẫn
- Giữ tối đa 100% nội dung, cảm xúc và giọng văn của tác giả.
- Không ép cấu trúc Tech Blog.
- Không tự ý tóm tắt, cắt xén hoặc "nâng cấp" suy nghĩ thành văn phong chuyên nghiệp nếu tác giả không yêu cầu.

## Structure

- **Mở bài bằng vấn đề:** Mở đầu bằng hiện tượng, bài toán hoặc câu hỏi cụ thể.
- **Heading có nghĩa:** Heading phải mô tả nội dung thực sự của section (Ví dụ: *"Vì sao request bắt đầu chậm"*, *"Cấu hình chúng ta sử dụng"* thay vì generic như *"Tổng quan"*, *"Giải pháp"*).

## Technical Explanation

Khi giải thích một khái niệm:
1. Nêu rõ nó giải quyết vấn đề gì.
2. Giải thích bản chất hoạt động.
3. Đưa ra ví dụ nhỏ nhất đủ để hiểu.
4. Chỉ ra điểm dễ hiểu sai nếu có.
5. Liên hệ với bài toán thực tế của bài viết.
6. Không giải thích lại mọi kiến thức nền tảng nếu độc giả mục tiêu đã biết.

## Show, Don't Tell

- Ưu tiên bằng chứng cụ thể: code, command, config, log, benchmark, bảng so sánh, sơ đồ, ví dụ thực tế.
- Tránh viết chung chung kiểu *"Cách này nhanh hơn đáng kể"* nếu có thể đưa số liệu hoặc giải thích cơ chế khiến nó nhanh hơn.
- Tuyệt đối không phát minh kết quả benchmark hoặc dữ liệu thực nghiệm giả.

## Code Blocks

- Luôn có câu dẫn ngữ cảnh ngắn trước mỗi code block.
- Chọn đoạn code nhỏ nhất chứng minh được ý đang nói, loại bỏ boilerplate thừa.
- Code phải đúng cú pháp và tương thích với stack kỹ thuật của bài.
- Không sửa code chỉ để tuân theo style rule dành cho văn xuôi (prose).
- Khi command có rủi ro thay đổi hệ thống hoặc xóa dữ liệu, giải thích rõ ràng trước khi đưa lệnh.

## Visuals & Diagrams

- Chỉ dùng bảng, callout, Mermaid hoặc hình ảnh khi chúng giúp người đọc hiểu nhanh hơn.
- Không thêm visual chỉ để trang trí.
- **Khi bài có Mermaid:** Bắt buộc đọc và tuân thủ [docs/mermaid.md](file:///home/ngoctin/Projects/my_website/docs/mermaid.md) trước khi tạo hoặc chỉnh sửa biểu đồ.
- Biểu đồ phải phản ánh đúng luồng nghiệp vụ thực tế; không bóp méo logic chỉ để layout đẹp.

## Markdown & Render Hooks (Chuẩn GFM Khuyên Dùng)

Website đã tích hợp toàn diện **Hugo Render Hooks**. Ưu tiên sử dụng 100% cú pháp Markdown chuẩn GFM thay vì shortcode:

- **Callouts / Alerts (Chuẩn GFM Alert):**
  ```markdown
  > [!NOTE]
  > Nội dung ghi chú...

  > [!TIP] Mẹo Quan Trọng
  > Nội dung mẹo kỹ thuật...

  > [!WARNING] Cảnh Báo
  > Nội dung cảnh báo...

  > [!DANGER] Điểm Nguy Hiểm
  > Nội dung nguy hiểm...
  ```
  *(Hỗ trợ các loại: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`, `INFO`, `DANGER`, `SUCCESS`, `FAILURE`, `BUG`, `EXAMPLE`, `ABSTRACT`)*

- **Trích dẫn (Quote):** Dùng blockquote chuẩn:
  ```markdown
  > Trích dẫn câu nói hoặc nội dung đáng chú ý ở đây.
  ```

- **Liên kết (Link):** Dùng cú pháp Markdown chuẩn `[Tên hiển thị](https://...)` (Render hook tự động thêm `target="_blank"` và `rel="noopener noreferrer"` cho liên kết ngoài).

- **Hình ảnh (Image):** Dùng cú pháp Markdown chuẩn `![Alt text](/images/...)` hoặc `![Alt text](/images/... "Chú thích ảnh")` (Render hook tự động sinh semantic `<figure>`, `<figcaption>` và `loading="lazy"`).

- **Shortcodes cũ (Chỉ dùng khi cần tương thích):**
  - Callout cũ: `{{< admonition type="note" title="..." >}}`
  - Quote cũ: `{{< quote author="..." >}}`
  *(Các shortcode này vẫn hoạt động bình thường nhưng không khuyến khích tạo mới)*

- **Prompt Mẫu:** Dùng khối mã chuẩn ```` ```text ```` hoặc ```` ```markdown ```` kèm câu dẫn ngữ cảnh.

## Frontmatter

Mỗi bài viết mới phải có đầy đủ frontmatter:
```yaml
---
title: "Tiêu đề bài viết cụ thể và chân thực"
date: YYYY-MM-DDTHH:MM:SS+07:00
draft: false
author: "Nguyen Ngoc Tin"
description: "Mô tả cụ thể giá trị thực tế của bài viết, không nhồi từ khóa SEO."
tags: ["Tag1", "Tag2"]
categories: ["Tech Blog"]
---
```
- Chỉ thêm `pinned: true` khi có yêu cầu ghim bài lên đầu danh sách.

## Editing Existing Content (Biên tập bản nháp)

Khi người dùng cung cấp bản nháp:
1. Xác định luận điểm và ý chính của tác giả.
2. Giữ lại các chi tiết thể hiện trải nghiệm hoặc góc nhìn riêng.
3. Sửa logic, cấu trúc, câu khó hiểu và lỗi kỹ thuật.
4. Cắt bỏ sự lặp thừa và filler.
5. Không thay toàn bộ bằng một bài AI mới nếu không được yêu cầu.
6. Nếu một đoạn văn có thể xuất hiện nguyên vẹn trong hàng trăm bài SEO khác, viết lại bằng chi tiết cụ thể hơn hoặc loại bỏ.

## Working Behavior

- Khi nhận yêu cầu viết bài: Xác định loại bài và nguồn thông tin hiện có.
- Kiểm tra các bài hoặc file liên quan trong repository nếu chúng ảnh hưởng đến nội dung.
- Tự review theo Definition of Done trước khi hoàn tất.
- Chạy `hugo --buildDrafts` để kiểm tra.
- Báo cáo ngắn gọn file đã thay đổi, nội dung chính và kết quả build.
- Nếu thiếu chi tiết nhỏ không quan trọng, chọn phương án hợp lý và tiếp tục; nếu thiếu dữ liệu cho claim quan trọng, nêu rõ giới hạn thay vì tự bịa.
