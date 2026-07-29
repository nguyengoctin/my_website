# Hướng Dẫn Thực Tế: Cách Thiết Kế Và Xây Dựng AI Agent


> *"AI Agent không phải là một phép màu công nghệ, mà là một hệ thống phần mềm có kiến trúc, ranh giới và quy luật rõ ràng."*

{{< admonition note "Nguồn tham khảo / Reference" >}}
Bài viết được tổng hợp từ báo cáo kiến trúc kỹ thuật chính thức của **OpenAI**: **"A practical guide to building agents"** (2025).
{{< /admonition >}}

Cấp độ tiếp theo của phần mềm thông minh là **AI Agent** — những thực thể tự trị có khả năng tự động lên kế hoạch, sử dụng công cụ bên ngoài và hoàn thành những chuỗi nhiệm vụ phức tạp mà không cần sự can thiệp liên tục của con người.

---

## 1. HIỂU ĐÚNG BẢN CHẤT CỦA AI AGENT

### So sánh: Phần mềm truyền thống vs. Copilot vs. AI Agent

| Loại hệ thống | Quyền điều phối Control Flow | Đặc điểm chính |
| :--- | :--- | :--- |
| **Phần mềm truyền thống** | Cố định Static Workflows | Code định nghĩa sẵn từng bước từ A đến Z; văng Exception nếu sai dữ liệu. |
| **Copilot** | Con người trực tiếp điều phối | Bị động; cần con người ra lệnh từng bước và xử lý kết quả. |
| **AI Agent** | **Tự động hóa hoàn toàn nhờ LLM** | Tự ra quyết định, tự sửa lỗi Self-correction, và linh hoạt gọi Tools. |

---

## 2. KHI NÀO NÊN (VÀ KHÔNG NÊN) XÂY DỰNG AGENT?

Xây dựng Agent tốn kém Token Cost, có độ trễ cao và mang tính Non-deterministic. Do đó chúng ta cần cân nhắc kỹ:

- **KHÔNG NÊN DÙNG:** Cho các logic If-Else đơn giản có thể hardcode. *(Ví dụ: Nếu khách trên 18 tuổi thì cho đăng ký)*.
- **KHUYÊN DÙNG:**
  1. **Ra quyết định phức tạp cần đánh giá ngữ cảnh:** Phê duyệt hoàn tiền dựa trên lịch sử khách hàng và chính sách linh hoạt.
  2. **Quy trình chứa hàng nghìn luật lệ cồng kềnh SOP:** Thay vì duy trì hàng nghìn dòng code if-else dễ sinh bug, Agent chỉ cần đọc tài liệu chính sách mới để tự căn chỉnh hành vi.
  3. **Xử lý dữ liệu phi cấu trúc:** Đọc hiểu văn bản tự nhiên, trích xuất dữ liệu từ PDF, email, hoặc hồ sơ bồi thường.

---

## 3. BA THÀNH PHẦN NỀN TẢNG CỦA AI AGENT

{{< image src="/images/posts/ai-agent-guide/agent-architecture.webp" caption="Kiến trúc nền tảng của một AI Agent: Input → Agent → Output với các lớp Instructions, Tools, Guardrails" alt="Kiến trúc nền tảng AI Agent" >}}

1. **Model - Trí tuệ:** 
   - *Giai đoạn PoC:* Dùng mô hình hàng đầu như GPT-4o hay Claude 3.5 Sonnet để tạo baseline chuẩn.
   - *Tối ưu:* Sau khi có bộ Evals, thay thế bằng các mô hình nhỏ như GPT-4o-mini hay Claude Haiku cho các tác vụ phân loại đơn giản.
2. **Tools - Công cụ:**
   - **Data Tools Read-only:** Truy vấn CRM, đọc PDF, tìm kiếm web.
   - **Action Tools Write Operations:** Gửi email, cập nhật database, chuyển khoản.
   - **Orchestration Tools:** Đóng gói Agent khác thành công cụ để Agent sếp điều phối.
3. **Instructions - Chỉ dẫn:** Định nghĩa kịch bản vận hành bằng cách chuyển đổi SOP doanh nghiệp thành các bước đánh số rõ ràng, bao phủ cả các trường hợp lỗi Edge Cases.

{{< prompt title="Prompt Mẫu: Meta-Prompt chuyển đổi SOP thành System Instructions" >}}
Bạn là một chuyên gia viết chỉ dẫn cho LLM agent. Hãy chuyển đổi tài liệu trợ giúp sau đây thành bộ chỉ dẫn được đánh số rõ ràng, không mơ hồ, hoạt động như mệnh lệnh điều hướng cho agent: {{help_center_doc}}
{{< /prompt >}}

---

## 4. KIẾN TRÚC ĐIỀU PHỐI ORCHESTRATION

### 1. Kiến trúc Single-agent
Luôn bắt đầu với Single-agent bằng cách bổ sung dần các Tools. Vòng lặp dừng Exit Conditions khi:
- Một Final-output Tool được kích hoạt.
- Mô hình trả về phản hồi trực tiếp mà không cần gọi thêm Tool.
- Hệ thống chạm ngưỡng tối đa lượt gọi Max Turns hoặc lỗi quá số lần quy định.

### 2. Kiến trúc Multi-agent
Chỉ chuyển sang Multi-agent khi logic quá phức tạp hoặc bị Tool Overload với trên 15 tools trùng lặp chức năng.

#### Mô hình Manager
Agent trung tâm Manager nhận yêu cầu và phân phối tác vụ song song cho các Sub-Agents chuyên biệt qua Tool calls.

{{< image src="/images/posts/ai-agent-guide/manager-pattern.webp" caption="Manager Pattern: Manager Agent nhận yêu cầu và phân phối Task song song cho các Sub-Agents" alt="Manager Pattern" >}}

#### Mô hình Handoff Phi Tập Trung
Các Agents hoạt động bình đẳng. Khi yêu cầu vượt quá chuyên môn, Agent hiện tại sẽ Handoff toàn bộ quyền kiểm soát và lịch sử hội thoại cho Agent phù hợp.

{{< image src="/images/posts/ai-agent-guide/decentralized-pattern.webp" caption="Decentralized Pattern: Triage Agent tiếp nhận câu hỏi và Handoff sang Orders Agent" alt="Decentralized Pattern" >}}

---

## 5. RÀO CHẮN BẢO MẬT GUARDRAILS & CON NGƯỜI GIÁM SÁT

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
Chuyển giao quyền điều khiển cho con người khi:
- **Vượt quá ngưỡng thất bại Failure Thresholds:** Agent gọi API lỗi quá 3 lần.
- **Thực hiện High-Risk Actions:** Các thao tác không thể đảo ngược như hoàn tiền lớn hay xóa dữ liệu.

---

## 6. LỜI KẾT

Để chúng ta xây dựng AI Agent thành công trong thực tế:
- Khởi đầu nhỏ với một **Single-agent** được trang bị Tools rõ ràng.
- Chỉ nâng cấp lên **Multi-agent** khi chạm ngưỡng phức tạp về logic hoặc công cụ.
- Bọc hệ thống bằng **Guardrails đa lớp** và giữ con người ở vị trí giám sát **Human-in-the-loop**.

