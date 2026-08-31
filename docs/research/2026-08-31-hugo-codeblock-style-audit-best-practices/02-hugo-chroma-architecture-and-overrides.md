# Hugo Chroma Architecture & Override Strategy

## 1. Audit kiến trúc Codeblock trong Project hiện tại

### 1.1. Cấu hình hiện tại (`hugo.toml`):
```toml
[markup.highlight]
  codeFences = true
  guessSyntax = false
  lineNos = true
  lineNumbersInTable = true
  noClasses = false
```

### 1.2. Mâu thuẫn giữa Config Hugo & Theme LoveIt:
1. **Xung đột Line Numbers (Table vs Counter):**
   - Hugo sinh cấu trúc HTML dạng `<table><tbody><tr><td class="lntd">...</td><td class="lntd">...</td></tr></tbody></table>`.
   - Theme LoveIt trong `_code.scss` lại cố gắng style `.code-line-numbers span.line::before` với CSS counter. Kết quả: khi bật `lineNumbersInTable = true`, số dòng render từ table HTML và CSS counter bị lệch hoặc vỡ khung nếu theme CSS chưa chuẩn hóa `table.lntable`.
2. **Xung đột Collapsible Header:**
   - LoveIt thiết kế header `.code-header` có click listener để toggle `.open` (gập mở block).
   - `.highlight` mặc định bị giới hạn `max-height: 0` khi chưa `.open`, và `max-height: 20000px` khi `.open` kèm CSS animation. Điều này làm người đọc cảm thấy giật lag khi cuộn trang hoặc khó copy nếu trạng thái khởi tạo JS bị chậm.
3. **Typography & Wrapping Issue:**
   - Trong `_code.scss`, thẻ `code` toàn cục bị gán `@include line-break(anywhere);` và `@include overflow-wrap(break-word);`.
   - Tác dụng phụ: Biến các token code dài hoặc URL trong code block bị bẻ gãy từ vô tội vạ, làm sai lệch ngữ nghĩa câu lệnh khi người đọc copy paste vào terminal/IDE.
4. **Dark/Light Mode Theme Override:**
   - Theme LoveIt dùng map `$code-highlight-color-map` trong SCSS tĩnh. Khi người dùng muốn đổi syntax theme theo chuẩn hiện đại (như Catppuccin, One Dark, Github Dark), việc ghi đè (override) phải sửa SCSS thay vì chỉ thay file CSS Chroma.

## 2. Best Practice kiến trúc chuẩn cho Hugo Codeblocks

1. **Chuẩn hóa Line Numbers Table:**
   ```scss
   .highlight {
     table.lntable {
       width: 100%;
       display: block;
       overflow-x: auto;
       border-spacing: 0;
       border-collapse: collapse;
     }
     .lntd:first-child {
       user-select: none;
       text-align: right;
       padding-right: 1rem;
       color: var(--code-linenumber-color);
       border-right: 1px solid var(--code-border-color);
     }
     .lntd:last-child {
       padding-left: 1rem;
       width: 100%;
     }
   }
   ```
2. **Loại bỏ cưỡng chế ngắt dòng trên Codeblock (`pre code`):**
   - Chỉ áp dụng `break-word` cho inline code (`:not(pre) > code`).
   - Khối `pre code` bắt buộc phải là `white-space: pre` và `overflow-x: auto` để giữ nguyên format.
3. **Cơ chế Copy Button độc lập:**
   - Button copy định vị `absolute` ở góc trên bên phải header hoặc block.
   - Khi bấm, chỉ đọc `innerText` của `code` cell (bỏ qua line numbers cell).
