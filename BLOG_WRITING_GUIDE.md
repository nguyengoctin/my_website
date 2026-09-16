# NgocTin Note — Blog Writing Guide

## Goal

Hỗ trợ viết và biên tập bài cho NgocTin Note. Mục tiêu là biến kiến thức, trải nghiệm, research và reference note của tác giả thành bài viết kỹ thuật rõ ràng, chính xác và hữu ích mà vẫn giữ được suy nghĩ và giọng viết của tác giả.

Không biến blog thành nội dung SEO hoặc bài viết mang giọng AI đại trà. Không phải mọi reference note đều cần trở thành bài blog.

## Core Principles

1. **Cụ thể hơn bóng bẩy:** Nội dung cụ thể quan trọng hơn văn phong hoa mỹ.
2. **Chính xác kỹ thuật:** Chính xác kỹ thuật quan trọng hơn viết cho "hay".
3. **Show, don't tell:** Ưu tiên cơ chế, trade-off, ví dụ và evidence thực tế.
4. **Tôn trọng provenance:** Không tự tạo trải nghiệm, quan điểm, benchmark, kết quả hoặc kết luận rồi gán cho tác giả.
5. **Biên tập trước, viết lại sau:** Nếu đã có note hoặc draft, xem đó là nguồn tư tưởng chính và ưu tiên biên tập, sắp xếp và làm rõ.
6. **Mật độ thông tin cao:** Không kéo dài bài chỉ để trông đầy đủ.
7. **Đứng độc lập:** Người đọc không được giả định biết conversation, project history hoặc note nội bộ.
8. **Không public mọi note:** Chỉ phát triển thành bài khi material có insight chuyển giao được cho người khác.

## Reader and Voice

- Dùng **"tôi"** khi mô tả trải nghiệm, observation, decision hoặc kết quả thực sự của tác giả.
- Dùng **"bạn"** khi hướng dẫn hoặc nói trực tiếp với người đọc.
- Chỉ dùng **"chúng ta"** khi thực sự đang dẫn người đọc cùng suy luận qua một cơ chế hoặc ví dụ; không dùng như giọng mặc định.
- Viết tiếng Việt tự nhiên, trực diện và cụ thể.
- Không mở bài bằng lời chào hoặc intro chung chung như "Hôm nay chúng ta sẽ...", "Trong thời đại số...", "Hãy cùng khám phá...".
- Không clickbait và không dùng từ thổi phồng như "toàn tập", "ultimate", "game changer", "cách mạng", "bí kíp" nếu evidence không thực sự biện minh.
- Không lặp lại cùng một kết luận bằng nhiều cách diễn đạt khác nhau.
- Không dùng ngoặc đơn chỉ để dịch thuật ngữ tiếng Anh inline. Giữ thuật ngữ tiếng Anh khi đó là cách tự nhiên và chính xác hơn.
- Không dùng ký tự `&` làm conjunction trong prose, heading, frontmatter hoặc nhãn Mermaid. Dùng "và" hoặc "and". Không sửa `&` khi nó là syntax cần thiết trong code block, command, URL hoặc dữ liệu nguyên bản.

## Source Integrity

Khi người dùng cung cấp note, code, tài liệu hoặc trải nghiệm:

- Xem chúng là nguồn chính của bài viết.
- Không tự thêm trải nghiệm cá nhân mà tác giả chưa từng đề cập.
- Không làm mạnh hơn kết luận so với evidence hiện có.
- Phân biệt điều tác giả trực tiếp làm hoặc quan sát với fact từ documentation, community experience và inference.
- Nếu claim còn uncertainty có ý nghĩa, giữ uncertainty thay vì viết lại thành fact.

Khi cần research:

- **Technical fact:** ưu tiên documentation chính thức, source code, specification và release notes.
- **Claim về hiệu quả:** ưu tiên dữ liệu hoặc benchmark phù hợp, không dùng benchmark không cùng workload để suy rộng.
- **Trải nghiệm thực tế và trade-off:** ưu tiên first-hand evidence từ Reddit, Hacker News, GitHub Issues hoặc developer forums phù hợp.
- **Lọc nhiễu:** không dùng SEO, affiliate, PR hoặc marketing làm bằng chứng cho trải nghiệm thực tế.
- **Không bịa nguồn:** không tự chế số liệu, citation hoặc benchmark. Nếu không xác minh được claim quan trọng, giảm mức khẳng định, nêu uncertainty hoặc loại bỏ claim.

## Article Modes

Xác định loại bài theo material thay vì ép mọi bài vào cùng một template.

### Tech Blog

Dùng cho hướng dẫn, giải thích kỹ thuật, project note, post-mortem và problem-solving.

Một bài dạng này thường tự nhiên đi qua: vấn đề → hiểu cơ chế → evidence hoặc investigation → solution → verification → điều đáng nhớ. Chỉ dùng những phần thực sự phục vụ câu chuyện kỹ thuật.

### Learning Note

Dùng khi tác giả đang ghi lại kiến thức vừa học.

Ưu tiên mental model, cách hiểu, ví dụ, điểm dễ nhầm và điều cần nhớ. Không biến learning note thành tutorial giả vờ có kinh nghiệm production sâu rộng.

### Research / Review

Dùng khi so sánh công nghệ, công cụ hoặc phương pháp.

Phân biệt fact, community pattern, pain point lặp lại, opinion và vấn đề còn tranh cãi. Nêu điều kiện lựa chọn và trade-off thay vì cố tạo một winner tuyệt đối.

### Tản văn / Góc nhìn / Trích dẫn

Giữ tối đa nội dung, cảm xúc và giọng văn của tác giả. Không ép cấu trúc Tech Blog và không tự nâng cấp suy nghĩ thành văn phong chuyên nghiệp nếu tác giả không yêu cầu.

## Information Structure

- Mở bài bằng vấn đề, hiện tượng, observation hoặc câu hỏi kỹ thuật cụ thể.
- Mỗi paragraph nên tập trung vào một ý chính và đặt thông tin quan trọng gần đầu.
- Heading phải mô tả nội dung thật của section. Ưu tiên *"Vì sao request bắt đầu chậm"* thay vì *"Tổng quan"* hoặc *"Giải pháp"*.
- Dùng sentence case cho heading.
- Không dùng Heading H1 trong body; title đã nằm trong frontmatter.
- Không đánh số heading chỉ để tạo cảm giác tutorial. Chỉ dùng numbered list khi sequence thực sự là semantics.
- Không tạo section chỉ để hoàn thành một template.
- Ưu tiên prose tự nhiên. Không biến mọi nội dung thành list, callout, card hoặc visual.

## No Tables

- Không dùng Markdown table trong bài viết.
- Với comparison hoặc structured information, ưu tiên prose ngắn, bullet list hoặc subsection riêng cho từng lựa chọn.
- Nếu dữ liệu bản chất là một ma trận lớn và chuyển thành prose sẽ làm mất thông tin đáng kể, dùng visual phù hợp hoặc dẫn tới data hoặc reference riêng thay vì ép vào table.

Đây là house style của NgocTin Note, không phải quy tắc kỹ thuật phổ quát cho mọi tài liệu.

## Technical Explanation

Khi giải thích một khái niệm, ưu tiên những phần thực sự cần để người đọc hiểu:

- nó giải quyết vấn đề gì;
- cơ chế hoặc mental model cốt lõi;
- ví dụ nhỏ nhất đủ để thấy behavior;
- điểm dễ hiểu sai hoặc assumption quan trọng;
- liên hệ với bài toán thực tế của bài viết.

Không giải thích lại mọi prerequisite nếu độc giả mục tiêu đã biết. Nếu thiếu một prerequisite sẽ làm người đọc hiểu sai procedure, nêu nó rõ ràng.

## Show, Don't Tell

- Ưu tiên evidence cụ thể: code, command, config, log, measurement, before hoặc after behavior, sơ đồ và ví dụ thực tế.
- Tránh claim như "nhanh hơn đáng kể", "ổn định hơn", "nhẹ hơn" hoặc "tối ưu" nếu không có measurement hoặc explanation về cơ chế.
- Không phát minh benchmark hoặc dữ liệu thực nghiệm.
- Không mô tả command, code hoặc kết quả như đã được chạy hoặc verify nếu source không chứng minh điều đó.
- Với claim phụ thuộc version, thời điểm hoặc environment, đặt context đó gần claim.

## Code Blocks and Commands

- Luôn có câu dẫn ngữ cảnh ngắn trước code block.
- Chọn đoạn code nhỏ nhất chứng minh được ý đang nói và loại boilerplate không liên quan.
- Khi code được trình bày như ví dụ có thể chạy, dependency, prerequisite và assumption quan trọng phải đủ rõ.
- Khi hữu ích, nêu expected behavior hoặc output để người đọc có thể tự kiểm chứng.
- Không sửa code thực tế chỉ để tuân theo style rule dành cho prose.
- Khi command có thể thay đổi hệ thống, xóa dữ liệu hoặc khó rollback, giải thích rủi ro trước lệnh.

## Callouts and Visuals

- Callout là ngoại lệ, không phải decoration. Chỉ dùng cho warning, caveat, constraint hoặc insight cần được tách khỏi flow chính.
- Không dùng nhiều callout liên tiếp.
- Mermaid, screenshot và hình ảnh phải làm rõ state, flow, architecture, comparison hoặc evidence cụ thể.
- Không thêm visual chỉ để bài bớt nhiều chữ.
- Mọi hình ảnh cần alt text mô tả nội dung có ý nghĩa với bài.
- Khi bài có Mermaid, bắt buộc đọc và tuân thủ `docs/mermaid.md` trước khi tạo hoặc chỉnh sửa biểu đồ.
- Biểu đồ phải phản ánh đúng luồng nghiệp vụ; không bóp méo logic chỉ để layout đẹp.

## Markdown and Render Hooks

Website dùng Hugo Render Hooks và Goldmark renderer. Ưu tiên cú pháp Markdown chuẩn GFM thay vì shortcode.

### Callouts / Alerts (Render Hook)

Cú pháp chuẩn GFM Alert, hỗ trợ title tùy biến:

```markdown
> [!NOTE]
> Nội dung ghi chú thông tin chung...

> [!TIP] Mẹo kỹ thuật hay
> Nội dung mẹo kỹ thuật, tối ưu hóa...

> [!WARNING] Cảnh báo quan trọng
> Nội dung cảnh báo rủi ro hoặc lưu ý bắt buộc...
```

- Các alert type được hệ thống hỗ trợ render trực tiếp: `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`, `INFO`, `SUCCESS`, `DANGER`, `BUG`, `EXAMPLE`, `TLDR` (hoặc alias tương ứng).
- Chỉ dùng alert khi thật sự cần làm nổi bật thông tin quan trọng. Không dùng nhiều alert liên tiếp hoặc dùng chỉ để trang trí.

### Quote / Trích Dẫn (Render Hook)

Blockquote thông thường (không có tiền tố `[!TYPE]`) sẽ tự động render dưới dạng trích dẫn editorial tinh gọn:

```markdown
> Trích dẫn câu nói hoặc nội dung đáng chú ý ở đây.
```

### Code Blocks và Inline Code

- **Fenced code block:** Luôn khai báo rõ language identifier (`python`, `bash`, `yaml`, `json`, `html`, `sql`, `go`...) trên dòng mở block ` ```<lang> `. Không để code block không tên ngôn ngữ trừ khi là plain text.
- **Inline code:** Dùng cặp backtick `` `variable_name` `` cho tên biến, file path, command ngắn, endpoint URL, package name. Không lạm dụng format cả câu hoặc cụm từ dài.
- Không bóp méo ký tự cú pháp code (như toán tử `&`, `&&`) chỉ vì quy tắc cấm `&` trong prose.

### Links (Render Hook)

Dùng `[Tên hiển thị](url)`. Render hook tự động thêm `target="_blank" rel="noopener noreferrer"` cho external links (bắt đầu bằng `http://` hoặc `https://`).
- Link text phải mang tính mô tả rõ đích đến hoặc ngữ cảnh (ví dụ: `[Tài liệu Docker Compose](https://...)`), tránh dùng từ chung chung như "tại đây", "link này".

### Images (Render Hook)

Cú pháp chuẩn Markdown: `![Alt text](/images/path/to/img.png)` hoặc `![Alt text](/images/path/to/img.png "Chú thích ảnh")`.
- Render hook tự động bọc trong thẻ `<figure>`, lazy loading và hiển thị caption từ Title (hoặc Alt text nếu không có Title).
- Bắt buộc có Alt text có ý nghĩa cho khả năng truy cập (accessibility).

### Lists và Task Lists

- **Unordered list:** Dùng dấu gạch ngang `- ` nhất quán trong toàn bài.
- **Ordered list:** Dùng `1. `, `2. ` khi thứ tự các bước hoặc sequence thực sự quan trọng.
- **Task list:** Dùng `- [ ] ` và `- [x] ` cho checklist hoặc tiến trình công việc.

### Nhấn Mạnh và Định Dạng Chữ (Emphasis)

- Dùng `**chữ đậm**` để nhấn mạnh điểm cốt lõi, từ khóa kỹ thuật lần đầu xuất hiện hoặc nhãn phân mục.
- Dùng `*chữ nghiêng*` cho thuật ngữ ngoại lai, trích đoạn ngắn hoặc ngữ cảnh cần sắc thái nhẹ.
- Tránh lạm dụng bôi đậm liên tục nhiều câu liền kề làm loãng thị giác.

### Prompt Mẫu

Dùng code block với language `text` hoặc `markdown` kèm câu dẫn ngữ cảnh ngắn gọn trước block.

### Shortcodes Cũ

Chỉ dùng khi cần tương thích với content cũ. Không ưu tiên shortcode cho bài mới nếu Markdown chuẩn đã đáp ứng được.

## Frontmatter

Mỗi bài viết mới phải có frontmatter:

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

Chỉ thêm `pinned: true` khi có yêu cầu ghim bài.

## Editing Existing Content

Khi người dùng cung cấp draft hoặc reference note:

1. Xác định luận điểm, insight và evidence thực sự có trong source.
2. Giữ các chi tiết thể hiện trải nghiệm hoặc góc nhìn riêng.
3. Sửa logic, cấu trúc, câu khó hiểu và lỗi kỹ thuật.
4. Cắt repetition, debugging noise và filler.
5. Ưu tiên edit và restructure hơn rewrite toàn bộ.
6. Nếu một đoạn có thể xuất hiện nguyên vẹn trong hàng trăm bài SEO khác, thay nó bằng chi tiết cụ thể có trong source hoặc loại bỏ.
7. Không lấp khoảng trống quan trọng bằng trải nghiệm, result hoặc opinion do AI tự tạo.

## Public-Safety Pass

Trước khi publish, kiểm tra và loại bỏ hoặc làm mờ:

- credential, API key, token và secret;
- identifier hoặc thông tin cá nhân không cần thiết;
- internal hostname, private path, account information hoặc dữ liệu environment không có giá trị với người đọc;
- material được copy từ nguồn khác mà không nên publish nguyên văn.

Không làm mất chi tiết kỹ thuật cần thiết chỉ để sanitize; dùng placeholder có nghĩa khi phù hợp.

## Publishability

Không phải mọi reference note đều cần trở thành bài blog.

Chỉ phát triển thành bài khi material có ít nhất một giá trị chuyển giao rõ, chẳng hạn:

- mental model hữu ích;
- solution có thể tái sử dụng;
- failure mode đáng biết;
- decision hoặc trade-off thú vị;
- experiment hoặc investigation có evidence;
- lesson kỹ thuật cụ thể khó thấy nếu chỉ đọc documentation.

Nếu material chỉ là nhật ký thao tác, state cá nhân hoặc một fact dễ tra cứu mà không có insight bổ sung, giữ nó làm reference note thay vì kéo dài thành bài.

## Working Behavior

- Khi nhận yêu cầu viết bài, xác định article mode và nguồn thông tin hiện có.
- Kiểm tra file hoặc bài liên quan trong repository khi chúng ảnh hưởng trực tiếp đến nội dung.
- Nếu thiếu chi tiết nhỏ không ảnh hưởng claim, chọn phương án hợp lý và tiếp tục.
- Nếu thiếu dữ liệu cho claim quan trọng, giữ uncertainty hoặc yêu cầu dữ liệu thay vì tự bịa.
- Tự review theo guide này trước khi hoàn tất.
- Chạy `hugo --buildDrafts` sau thay đổi khi có quyền truy cập repository.
- Báo cáo ngắn file đã thay đổi, nội dung chính và kết quả build.
