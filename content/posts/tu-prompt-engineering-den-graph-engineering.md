---
title: "Từ Prompt Engineering Đến Graph Engineering: Sự Trỗi Dậy Của Hệ Thống AI Đa Tác Vụ"
date: 2026-07-29T16:15:00+07:00
draft: false
author: "Nguyen Ngoc Tin"
description: "Phân tích sự dịch chuyển kiến trúc AI từ mô hình đơn tác tử sang Graph Engineering: Giải mã hiện tượng Context Bloat, bộ nhớ Shared State và kỷ nguyên của Hệ thống Đa tác vụ Multi-Agent Systems."
tags: ["AI Agents", "Graph Engineering", "System Architecture", "LangGraph", "Multi-Agent Systems", "Software Engineering"]
categories: ["Tech Blog"]
---

{{< quote author="Andrew Ng" >}}
Architecture matters more than the model.
{{< /quote >}}

Nhiều lập trình viên hiện nay đang mắc kẹt khi ứng dụng AI của họ thỉnh thoảng lại rơi vào vòng lặp vô hạn, hoặc gọi API bừa bãi đến mức treo cả hệ thống. Để giải quyết triệt để cơn ác mộng này, phương thức chúng ta thiết kế các hệ thống AI đã buộc phải trải qua 4 bước dịch chuyển kiến trúc cốt lõi:
1. **Prompt Engineering:** Biến hóa ngôn ngữ tự nhiên để vắt kiệt khả năng suy luận của mô hình.
2. **Context Engineering:** Cung cấp đúng dữ liệu doanh nghiệp làm ngữ cảnh cho mô hình thông qua RAG.
3. **Loop Engineering:** Cho phép tác tử tự suy nghĩ, gọi công cụ và tự sửa sai trong một vòng lặp kín.
4. **Graph Engineering:** Cấu trúc hóa quy trình thành cỗ máy trạng thái State Machine gồm các Nút, Cạnh và Bộ nhớ chia sẻ Shared State.

---

23: ## 1. Cơn ác mộng Loop Engineering và sự sụp đổ của tác tử đơn độc
24: 
25: Mô hình đơn tác tử Monolithic Single Agent bắt một LLM duy nhất gánh mọi vai trò từ Business Analyst, Coder đến QA và Architect:
26: 
27: ```text
28: Nhận Mục Tiêu → Suy Luận → Gọi Công Cụ → Đánh Giá Kết Quả → Lặp Lại
29: ```
30: 
31: {{< admonition danger "3 Mẫu thất bại chí mạng (Failure Patterns)" >}}
32: 1. **Retrieval Thrash:** Rơi vào vòng xoáy tìm kiếm thông tin không bao giờ chốt kết quả do thiếu tiêu chuẩn dừng Termination Criteria.
33: 2. **Tool Storms:** Bão công cụ quá tải gọi API liên tục để sắp xếp hoặc di chuyển tệp hàng nghìn lần, treo hệ thống.
34: 3. **Recursive Verification:** Xác minh đệ quy tự viết mã, sửa lỗi nhỏ, xóa đi viết lại từ đầu vô hạn vì thiếu cơ chế theo dõi tiến trình Progress Detection.
35: {{< /admonition >}}
36: 
37: ---
38: 
39: ## 2. Giải mã Context Bloat: Cửa sổ ngữ cảnh không phải là ổ cứng
40: 
41: Context Window hoạt động tương đương với bộ nhớ ngẫu nhiên RAM, chứ không phải ổ cứng lưu trữ cố định.
42: 
43: ```mermaid
44: flowchart LR
45:     A["System Prompt"] --> B["MCP Tools"]
46:     B --> C["History"]
47:     C --> D["Context Rot"]
48: ```
49: 
50: - **Tool Definition Bloat:** Nạp 50-60 công cụ qua chuẩn MCP tiêu tốn tới **55.000 token** ngay từ lượt tương tác đầu tiên — chiếm 25% cửa sổ 200K token trước khi người dùng gõ từ nào.
51: - **Attention Dilution - Suy thoái chú ý:** Do độ phức tạp tính toán `O(n²)`, hiện tượng *Lost in the Middle* làm suy giảm khả năng tuân thủ quy tắc từ **73% ở lượt 5 xuống chỉ còn 33% ở lượt 16**.
52: 
53: ---
54: 
55: ## 3. Graph Engineering: Xây dựng tổ chức AI phân tán
56: 
57: ```mermaid
58: flowchart TD
59:     Supervisor["Supervisor"] --> NodeA["Research Agent"]
60:     Supervisor --> NodeB["Coder Agent"]
61:     NodeA --> SharedState["Shared State"]
62:     NodeB --> SharedState
63:     SharedState --> Checkpoint["Checkpoint"]
64: ```
65: 
66: - **Nút Nodes:** Đơn vị thực thi chuyên biệt như Code Python, API Call, hoặc Sub-agent.
67: - **Cạnh Edges:** Định tuyến dữ liệu tất định `A → B` hoặc có điều kiện như Test lỗi → quay lại Coder.
68: - **Shared State:** Bộ nhớ trạng thái chung hoạt động như Google Docs chung của nhóm. Mỗi Nút chỉ nạp đúng phần dữ liệu nó cần, xử lý xong và ghi kết quả trở lại Docs.
69: 
70: {{< quote author="Anthropic Engineering" >}}
71: Agent có thể quên, nhưng hệ thống Đồ thị thì không bao giờ quên.
72: {{< /quote >}}
73: 
74: ---
75: 
76: ## 4. Bốn mẫu kiến trúc phối hợp đa tác vụ
77: 
78: 1. **Routing - Định tuyến:** Chuyển câu hỏi đơn giản tới Haiku hoặc GPT-4o-mini; đẩy bài toán phức tạp cho Sonnet hoặc GPT-4o.
79: 2. **Parallelization và Map-Reduce:** Nhân bản 100 nút song song phân tích 100 báo cáo tài chính cùng lúc rồi đẩy về nút tổng hợp.
80: 3. **Orchestrator-Workers:** Agent Trưởng nhóm phân tích bài toán, giao nhiệm vụ con cho các Worker Agents và nghiệm thu.
81: 4. **Evaluator-Optimizer:** Nút **Generator** viết nội dung, nút **Evaluator** độc lập phản biện và yêu cầu Generator tinh chỉnh.
82: 
83: ---
84: 
85: ## 5. Động lực học thời điểm suy luận (Inference-time Compute)
86: 
87: ```text
88: Hiệu Năng Hệ Thống = Năng Lực Mô Hình × Độ Tinh Xảo Của Kiến Trúc Đồ Thị
89: ```

- **SWE-Search:** Kết hợp thuật toán tìm kiếm cây MCTS với 3 tác tử SWE-Agent, Value Agent và Discriminator Agent, tăng **23% hiệu suất** sửa lỗi phần mềm trên bảng xếp hạng SWE-bench.
- **AWorld:** Áp dụng Lý thuyết Điều khiển tự động hóa. Một **Guard Agent** liên tục giám sát **Execution Agent**, đo lường dấu vân tay lỗi và điều chỉnh quỹ đạo kịp thời.

---

## Lời kết

Chúng ta không còn chỉ đóng vai trò là những người ra lệnh thụ động cho cỗ máy. Chúng ta đang cùng nhau trở thành những **Kiến trúc sư hệ thần kinh**, sử dụng các khối logic, cỗ máy trạng thái và cơ chế cô lập ngữ cảnh để kiến tạo nên những tổ chức AI tự vận hành mạnh mẽ.
