# Hướng Dẫn Thực Tế: Cách Thiết Kế Và Xây Dựng AI Agent


{{< quote >}}
AI Agent không phải là một phép màu công nghệ, mà là một hệ thống phần mềm có kiến trúc, ranh giới và quy luật rõ ràng.
{{< /quote >}}

{{< admonition note "Nguồn tham khảo / Reference" >}}
Bài viết được tổng hợp từ báo cáo kiến trúc kỹ thuật chính thức của **OpenAI**: **"A practical guide to building agents"** (2025).
{{< /admonition >}}

Khi đối mặt với các quy trình nghiệp vụ thay đổi liên tục, nhiều lập trình viên thường sa lầy vào việc bảo trì hàng nghìn dòng lệnh `if-else` lắt léo và dễ sinh lỗi. Cấp độ tiếp theo để giải quyết bài toán này không phải là viết code chặt chẽ hơn, mà là giao quyền cho một **AI Agent** — những thực thể thông minh có khả năng tự động lên kế hoạch, sử dụng công cụ bên ngoài và hoàn thành những chuỗi nhiệm vụ phức tạp mà không cần sự can thiệp liên tục của con người.

---

## 1. Hiểu đúng bản chất của AI Agent

### So sánh: Phần mềm truyền thống vs. Copilot vs. AI Agent

| Loại hệ thống | Quyền điều phối Control Flow | Đặc điểm chính |
| :--- | :--- | :--- |
| **Phần mềm truyền thống** | Cố định Static Workflows | Code định nghĩa sẵn từng bước từ A đến Z; văng Exception nếu sai dữ liệu. |
| **Copilot** | Con người trực tiếp điều phối | Bị động; cần con người ra lệnh từng bước và xử lý kết quả. |
| **AI Agent** | **Tự động hóa hoàn toàn nhờ LLM** | Tự ra quyết định, tự sửa lỗi Self-correction, và linh hoạt gọi Tools. |

---

## 2. Khi nào nên và không nên xây dựng Agent?

{{< admonition warning "Chi phí và Độ trễ" >}}
Xây dựng Agent tốn kém Token Cost, có độ trễ cao và mang tính Non-deterministic (không tất định). Do đó chúng ta cần cân nhắc kỹ ranh giới áp dụng.
{{< /admonition >}}

- **KHÔNG NÊN DÙNG:** Cho các logic If-Else đơn giản có thể hardcode. *(Ví dụ: Nếu khách trên 18 tuổi thì cho đăng ký)*.
- **KHUYÊN DÙNG:**
  1. **Ra quyết định phức tạp cần đánh giá ngữ cảnh:** Phê duyệt hoàn tiền dựa trên lịch sử khách hàng và chính sách linh hoạt.
  2. **Quy trình chứa hàng nghìn luật lệ cồng kềnh SOP:** Thay vì duy trì hàng nghìn dòng code if-else dễ sinh bug, Agent chỉ cần đọc tài liệu chính sách mới để tự căn chỉnh hành vi.
  3. **Xử lý dữ liệu phi cấu trúc:** Đọc hiểu văn bản tự nhiên, trích xuất dữ liệu từ PDF, email, hoặc hồ sơ bồi thường.

---

## 3. Ba thành phần nền tảng của AI Agent

{{< image src="/images/posts/ai-agent-guide/agent-architecture.webp" caption="Kiến trúc nền tảng của một AI Agent: Input → Agent → Output với các lớp Instructions, Tools, Guardrails" alt="Kiến trúc nền tảng AI Agent" >}}

1. **Model - Trí tuệ:** 
   - *Giai đoạn PoC:* Dùng mô hình hàng đầu như GPT-4o hay Claude 3.5 Sonnet để tạo baseline chuẩn.
   - *Tối ưu:* Sau khi có bộ Evals, thay thế bằng các mô hình nhỏ như GPT-4o-mini hay Claude Haiku cho các tác vụ phân loại đơn giản.
2. **Tools - Công cụ:**
   - **Data Tools Read-only:** Truy vấn CRM, đọc PDF, tìm kiếm web.
   - **Action Tools Write Operations:** Gửi email, cập nhật database, chuyển khoản.
   - **Orchestration Tools:** Đóng gói Agent khác thành công cụ để Agent sếp điều phối.
3. **Instructions - Chỉ dẫn:** Định nghĩa kịch bản vận hành bằng cách chuyển đổi SOP doanh nghiệp thành các bước đánh số rõ ràng, bao phủ cả các trường hợp lỗi Edge Cases.

```text
Bạn là một chuyên gia viết chỉ dẫn cho LLM agent. Hãy chuyển đổi tài liệu trợ giúp sau đây thành bộ chỉ dẫn được đánh số rõ ràng, không mơ hồ, hoạt động như mệnh lệnh điều hướng cho agent: {{help_center_doc}}
```

---

## 4. Kiến trúc điều phối (Orchestration)

### 1. Kiến trúc Single-agent
Luôn bắt đầu với Single-agent bằng cách bổ sung dần các Tools. Vòng lặp dừng Exit Conditions khi:
- Một Final-output Tool được kích hoạt.
- Mô hình trả về phản hồi trực tiếp mà không cần gọi thêm Tool.
- Hệ thống chạm ngưỡng tối đa lượt gọi Max Turns hoặc lỗi quá số lần quy định.

### 2. Kiến trúc Multi-agent
Chỉ chuyển sang Multi-agent khi logic quá phức tạp hoặc bị Tool Overload với trên 15 tools trùng lặp chức năng.

{{< admonition tip "Quy tắc thiết kế" >}}
Luôn ưu tiên bắt đầu bằng Single-agent. Chỉ chia nhỏ thành hệ thống Đa tác tử (Multi-agent) khi tập hợp công cụ vượt quá khả năng chọn lọc của mô hình.
{{< /admonition >}}

#### Mô hình Manager
Agent trung tâm Manager nhận yêu cầu và phân phối tác vụ song song cho các Sub-Agents chuyên biệt qua Tool calls.

{{< image src="/images/posts/ai-agent-guide/manager-pattern.webp" caption="Manager Pattern: Manager Agent nhận yêu cầu và phân phối Task song song cho các Sub-Agents" alt="Manager Pattern" >}}

#### Mô hình Handoff Phi Tập Trung
Các Agents hoạt động bình đẳng. Khi yêu cầu vượt quá chuyên môn, Agent hiện tại sẽ Handoff toàn bộ quyền kiểm soát và lịch sử hội thoại cho Agent phù hợp.

{{< image src="/images/posts/ai-agent-guide/decentralized-pattern.webp" caption="Decentralized Pattern: Triage Agent tiếp nhận câu hỏi và Handoff sang Orders Agent" alt="Decentralized Pattern" >}}

---

## 5. Rào chắn bảo mật (Guardrails) và giám sát con người

{{< image src="/images/posts/ai-agent-guide/layered-guardrails.webp" caption="Layered Guardrails: Các lớp bảo vệ độc lập chặn Prompt Injection trước khi Agent xử lý" alt="Layered Guardrails" >}}

### 7 Lớp Guardrails tiêu chuẩn

1. **Relevance Classifier:** Chặn câu hỏi lạc đề.
2. **Safety Classifier:** Phát hiện tấn công Prompt Injection hoặc Jailbreak.
3. **PII Filter:** Lọc bỏ thông tin cá nhân nhạy cảm như Số thẻ, CCCD, Email.
4. **Moderation API:** Tự động chặn nội dung độc hại.
5. **Tool Safeguards:** Phân loại rủi ro Tool theo thang điểm Low, Medium, High. Tool rủi ro cao phải qua phê duyệt.
6. **Rules-based Protections:** Regex chặn SQL Injection, Blocklist, Character Limit.
7. **Output Validation:** Kiểm tra định dạng và tính chính xác của câu trả lời trước khi hiển thị.

### Cơ chế Con người can thiệp Human-in-the-loop

{{< admonition danger "Thao tác rủi ro cao" >}}
Bắt buộc phải có điểm dừng cho con người duyệt (Human Approval) trước khi Agent thực thi các lệnh ghi (Write operations) có tính chất vĩnh viễn hoặc rủi ro tài chính lớn.
{{< /admonition >}}

Chuyển giao quyền điều khiển cho con người khi:
- **Vượt quá ngưỡng thất bại Failure Thresholds:** Agent gọi API lỗi quá 3 lần.
- **Thực hiện High-Risk Actions:** Các thao tác không thể đảo ngược như hoàn tiền lớn hay xóa dữ liệu.

---

## Lời kết

Để chúng ta xây dựng AI Agent thành công trong thực tế:
- Khởi đầu nhỏ với một **Single-agent** được trang bị Tools rõ ràng.
- Chỉ nâng cấp lên **Multi-agent** khi chạm ngưỡng phức tạp về logic hoặc công cụ.
- Bọc hệ thống bằng **Guardrails đa lớp** và giữ con người ở vị trí giám sát **Human-in-the-loop**.

