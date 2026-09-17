---
title: "Thiết kế và xây dựng AI Agent trong thực tế"
date: 2026-07-26T21:38:18+07:00
draft: false
author: "Nguyen Ngoc Tin"
description: "Phân tích kiến trúc thiết kế AI Agent theo tài liệu OpenAI: từ Single-agent, Multi-agent, quản lý Tools, thiết lập Guardrails đa tầng đến cơ chế Human-in-the-loop."
tags: ["AI Agent", "System Architecture", "LLM", "Software Engineering", "OpenAI"]
categories: ["Tech Blog"]
---

> [!TLDR]
> AI Agent không phải là một chiếc hộp đen thần kỳ mà là một hệ thống phần mềm có ranh giới kiểm soát và công cụ rõ ràng. Bài viết tổng hợp các nguyên lý kiến trúc cốt lõi từ tài liệu kỹ thuật của OpenAI: phân biệt Agent với phần mềm truyền thống, tiêu chí đánh đổi khi xây dựng, kiến trúc điều phối Single/Multi-agent và 7 lớp Guardrails bảo vệ.

Khi đối mặt với các quy trình nghiệp vụ thay đổi liên tục, việc bảo trì hàng nghìn dòng lệnh `if-else` lắt léo rất dễ sinh lỗi. Giải pháp là giao quyền cho **AI Agent** — hệ thống có khả năng tự động lên kế hoạch, sử dụng công cụ bên ngoài và hoàn thành những chuỗi nhiệm vụ phức tạp theo mục tiêu được giao.

---

## Bản chất của AI Agent

So sánh quyền điều phối Control Flow giữa ba mô hình hệ thống:

- **Phần mềm truyền thống (Static Workflows):** Quyền điều phối hoàn toàn cố định trong mã nguồn. Logic được định nghĩa sẵn từng bước từ đầu đến cuối; phát sinh ngoại lệ nếu gặp dữ liệu bất thường.
- **Copilot (Human-driven):** Con người trực tiếp giữ quyền điều phối. Hệ thống đóng vai trò hỗ trợ bị động, cần người dùng ra lệnh từng bước và tự xử lý kết quả.
- **AI Agent (LLM-driven):** Quyền điều phối được tự động hóa dựa trên mô hình ngôn ngữ lớn. Hệ thống tự lập luận, tự chọn công cụ phù hợp và có khả năng tự sửa lỗi (Self-correction) dựa trên phản hồi của môi trường.

---

## Ranh giới khi quyết định xây dựng Agent

> [!WARNING]
> Xây dựng Agent tốn chi phí token, có độ trễ cao và mang tính không tất định (Non-deterministic). Cần xác định rõ ranh giới bài toán trước khi triển khai.

- **Trường hợp không nên dùng:** Các logic nghiệp vụ đơn giản có thể hardcode bằng câu lệnh điều kiện. Ví dụ: kiểm tra người dùng trên 18 tuổi để mở quyền đăng ký.
- **Trường hợp nên dùng:**
  - **Quyết định phức tạp cần đánh giá ngữ cảnh:** Phê duyệt hoàn tiền dựa trên lịch sử khách hàng và chính sách linh hoạt.
  - **Quy trình chứa nhiều luật lệ nghiệp vụ thay đổi thường xuyên:** Thay vì liên tục sửa code `if-else`, Agent có thể đọc tài liệu chính sách mới để tự căn chỉnh hành vi.
  - **Xử lý dữ liệu phi cấu trúc:** Đọc hiểu văn bản tự nhiên, trích xuất dữ liệu từ PDF, email hoặc hồ sơ bồi thường.

---

## Ba thành phần nền tảng của AI Agent

{{< image src="/images/posts/ai-agent-guide/agent-architecture.webp" caption="Kiến trúc nền tảng của một AI Agent: Input → Agent → Output với các lớp Instructions, Tools, Guardrails" alt="Kiến trúc nền tảng AI Agent" >}}

1. **Model (Trí tuệ):**
   - *Giai đoạn PoC:* Dùng mô hình mạnh như GPT-4o hoặc Claude Sonnet để thiết lập baseline chuẩn về năng lực lập luận.
   - *Giai đoạn tối ưu:* Sau khi xây dựng bộ đánh giá (Evals), thay thế bằng các mô hình nhỏ như GPT-4o-mini hoặc Claude Haiku cho các tác vụ phân loại đơn giản để giảm chi phí và độ trễ.
2. **Tools (Công cụ):**
   - *Data Tools (Read-only):* Truy vấn CRM, đọc tài liệu PDF, tìm kiếm web.
   - *Action Tools (Write operations):* Gửi email, cập nhật cơ sở dữ liệu, kích hoạt giao dịch.
   - *Orchestration Tools:* Đóng gói Agent khác thành công cụ để Agent điều phối gọi thực thi.
3. **Instructions (Chỉ dẫn):** Định nghĩa kịch bản vận hành bằng cách chuyển đổi quy trình chuẩn (SOP) thành các bước rõ ràng, xử lý trước các trường hợp biên (Edge cases).

```text
Bạn là một chuyên gia viết chỉ dẫn cho LLM agent. Hãy chuyển đổi tài liệu trợ giúp sau đây thành bộ chỉ dẫn được đánh số rõ ràng, không mơ hồ, hoạt động như mệnh lệnh điều hướng cho agent: {{help_center_doc}}
```

---

## Kiến trúc điều phối (Orchestration)

### Kiến trúc Single-agent
Luôn bắt đầu với Single-agent bằng cách bổ sung dần các Tools. Vòng lặp dừng khi thỏa mãn một trong các điều kiện:
- Một Final-output Tool được kích hoạt.
- Mô hình trả về phản hồi trực tiếp mà không cần gọi thêm Tool.
- Hệ thống chạm ngưỡng tối đa số lượt gọi (Max Turns) hoặc gặp lỗi quá số lần quy định.

### Kiến trúc Multi-agent
Chỉ chuyển sang Multi-agent khi logic quá phức tạp hoặc số lượng công cụ vượt quá 15 tools gây nhiễu lựa chọn của mô hình.

> [!TIP]
> Luôn ưu tiên bắt đầu bằng Single-agent. Chỉ chia nhỏ thành hệ thống đa tác tử khi tập hợp công cụ vượt quá khả năng chọn lọc chính xác của mô hình.

#### Mô hình Manager
Agent trung tâm đóng vai trò Manager nhận yêu cầu và phân phối tác vụ song song cho các Sub-Agents chuyên biệt qua Tool calls.

{{< image src="/images/posts/ai-agent-guide/manager-pattern.webp" caption="Manager Pattern: Manager Agent nhận yêu cầu và phân phối tác vụ cho các Sub-Agents" alt="Manager Pattern" >}}

#### Mô hình Handoff phi tập trung
Các Agent hoạt động ngang hàng. Khi yêu cầu vượt quá phạm vi chuyên trách, Agent hiện tại sẽ Handoff toàn bộ quyền kiểm soát và ngữ cảnh hội thoại cho Agent phù hợp tiếp quản.

{{< image src="/images/posts/ai-agent-guide/decentralized-pattern.webp" caption="Decentralized Pattern: Triage Agent tiếp nhận yêu cầu và chuyển giao sang Orders Agent" alt="Decentralized Pattern" >}}

---

## Rào chắn bảo mật và giám sát con người

{{< image src="/images/posts/ai-agent-guide/layered-guardrails.webp" caption="Layered Guardrails: Các lớp bảo vệ độc lập chặn Prompt Injection trước khi Agent xử lý" alt="Layered Guardrails" >}}

### Bảy lớp Guardrails tiêu chuẩn

1. **Relevance Classifier:** Chặn câu hỏi nằm ngoài phạm vi nghiệp vụ.
2. **Safety Classifier:** Phát hiện tấn công Prompt Injection hoặc Jailbreak.
3. **PII Filter:** Lọc bỏ thông tin cá nhân nhạy cảm như số thẻ, số định danh, mật khẩu.
4. **Moderation API:** Tự động chặn nội dung vi phạm tiêu chuẩn an toàn.
5. **Tool Safeguards:** Phân loại mức độ rủi ro của từng công cụ (Low, Medium, High). Công cụ có rủi ro cao bắt buộc phải có bước phê duyệt.
6. **Rules-based Protections:** Biểu thức chính quy chặn SQL Injection, blocklist từ khóa và giới hạn độ dài ký tự.
7. **Output Validation:** Kiểm tra định dạng cấu trúc và độ chính xác của câu trả lời trước khi gửi về client.

### Cơ chế con người can thiệp (Human-in-the-loop)

> [!CAUTION]
> Bắt buộc phải có điểm dừng phê duyệt (Human Approval) trước khi Agent thực thi các lệnh ghi (Write operations) có tính chất vĩnh viễn hoặc rủi ro tài chính cao.

Chuyển giao quyền điều khiển cho con người trong các tình huống:
- **Vượt ngưỡng thất bại (Failure Thresholds):** Agent gọi công cụ thất bại liên tiếp quá số lần cho phép (ví dụ quá 3 lần).
- **Hành động có rủi ro cao:** Các thao tác không thể hoàn tác như hoàn tiền lớn, thay đổi quyền hạn hoặc xóa dữ liệu.

---

## Tóm lược nguyên tắc triển khai

- Khởi đầu với **Single-agent** đi kèm danh sách công cụ nhỏ gọn, tường minh.
- Chỉ mở rộng sang **Multi-agent** khi gặp bài toán phức tạp vượt quá khả năng chọn tool của một mô hình đơn lẻ.
- Xây dựng **Guardrails đa tầng** để chặn rủi ro dữ liệu đầu vào và đầu ra.
- Giữ con người ở vị trí giám sát **Human-in-the-loop** đối với mọi thao tác thay đổi trạng thái quan trọng.

