# Hugo Codeblock Styling: Community Consensus & Pain Points

## 1. Bối cảnh & Thực trạng
Trong các hệ sinh thái Static Site Generator (SSG) như Hugo, việc hiển thị và tương tác với code block (khối mã nguồn) luôn là tâm điểm tranh luận giữa thẩm mỹ giao diện và tính khả dụng của nhà phát triển (Developer Experience - DX).

## 2. Đồng thuận kỹ thuật từ cộng đồng (Reddit, HN, Hugo Discourse)

### 2.1. Server-side Highlighting (Chroma) vs Client-side Highlighting (Prism/Highlight.js)
- **Đồng thuận tuyệt đối:** 90%+ thảo luận trên Hugo Discourse và Hacker News đều khuyến nghị tận dụng Chroma tích hợp sẵn của Hugo thay vì tải thêm JS runtime (Prism/Highlight.js).
- **Lý do:**
  - Zero JS overhead: Không gây layout shift (CLS), tải trang tức thì.
  - Tích hợp sâu vào build-time: Hugo render HTML tĩnh đã được token hóa sẵn.
- **Ngoại lệ duy nhất:** Chỉ chuyển sang Client-side (hoặc Shiki build step) khi cần tính năng syntax highlighting cực phức tạp (như Twoslash, IDE tooltips, AST parsing chuyên sâu).

### 2.2. CSS-based Chroma vs Inline Styles (`noClasses = false`)
- **Đồng thuận mạnh mẽ:** Bắt buộc đặt `noClasses = false` trong `markup.highlight` và xuất CSS bằng lệnh `hugo gen chromastyles`.
- **Lý do:**
  - Inline style (`noClasses = true`) làm phình kích thước file HTML (bloat DOM) gấp 3-5 lần đối với các bài viết kỹ thuật dài.
  - Sử dụng CSS class giúp dễ dàng switch theme Dark/Light thông qua CSS variables (`pre.chroma`, `.chroma .k`, `.chroma .s`...) mà không cần render lại HTML.

### 2.3. Line Numbers: Table (`lineNumbersInTable = true`) vs Inline (`lineNos = true` / CSS counters)
- **Vấn đề cốt lõi:** Khi người dùng bôi đen (copy thủ công) code block có line numbers:
  - Nếu dùng inline span thô: số dòng bị copy kèm vào clipboard (`1 const a = 1; \n 2 const b = 2;`), gây ức chế tột cùng cho lập trình viên.
  - Giải pháp Table (`lineNumbersInTable = true`): Hugo tách số dòng sang `<td>` cột 1 và code sang `<td>` cột 2 với thuộc tính CSS `user-select: none`. Người dùng bôi đen văn bản tự nhiên không bị dính số dòng.
  - Giải pháp CSS pseudo `::before` (`counter`): Đẹp về DOM phẳng nhưng dễ bị lệch baseline font khi code có dòng dài wrap text.
- **Đồng thuận cộng đồng:** Khuyến nghị chuẩn mực là dùng `lineNumbersInTable = true` kết hợp `user-select: none` trên cột số dòng, hoặc dùng CSS counter có cấu trúc rõ ràng không wrap vỡ layout.

### 2.4. Tranh cãi: Horizontal Scroll (`overflow-x: auto`) vs Word Wrap (`white-space: pre-wrap`)
- **Ý kiến đa số:** Mặc định cho code block là `overflow-x: auto` (cuộn ngang) để giữ nguyên vẹn cấu trúc thụt đầu dòng (indentation) và tính logic của code (nhất là Python, YAML, Bash).
- **Trường hợp cá biệt (Mobile):** Trên màn hình mobile nhỏ (<480px), cuộn ngang trong iframe/block đôi khi gây kẹt cử chỉ vuốt trang (touch trap). Giải pháp: cho phép toggle wrap hoặc chỉ wrap với terminal output/prose code.

### 2.5. Collapsible Code Block (Code gập/mở)
- **Điểm đau lớn từ thực tế:** Nhiều theme (bao gồm LoveIt cũ) mặc định bọc `.code-block` với header gập/mở bằng JS hoặc SCSS `max-height`.
- **Phản ứng cộng đồng:** Người dùng ghét việc click vào codeblock để copy/chọn text lại vô tình kích hoạt sự kiện collapse (thu gọn khối code). Khuyến nghị: Code block nên mở sẵn 100%, chỉ thu gọn khi có tham số chỉ định tường minh (shortcode `collapse=true`) cho các đoạn code quá 100 dòng.
