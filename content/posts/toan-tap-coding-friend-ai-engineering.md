---
pinned: true
title: "Kỷ Luật Kỹ Thuật Cùng Coding Friend: Tối Ưu Năng Suất Khi Lập Trình Với AI Agent"
date: 2026-09-30T19:50:00+07:00
draft: false
author: "Nguyen Ngoc Tin"
description: "Khám phá cách Coding Friend giúp chúng ta thiết lập quy trình kỹ thuật kỷ luật với AI agent: từ khảo sát, lập kế hoạch, viết code có kiểm thử, phản biện mã nguồn đa tầng đến hệ thống bộ nhớ bền vững."
tags: ["AI Coding", "Coding Friend", "Claude Code", "Productivity", "Workflow", "TDD"]
categories: ["Tech Blog"]
---

Khi bắt đầu làm việc với các AI agent như Claude Code, Codex CLI hay Google Antigravity, cảm giác ban đầu của tôi thực sự rất ấn tượng. Tốc độ sinh mã của mô hình ngôn ngữ lớn diễn ra trong chớp mắt. Nhưng sau một thời gian áp dụng vào các dự án phần mềm thực tế, tôi nhận ra một nghịch lý: **viết code nhanh hơn không đồng nghĩa với hoàn thành dự án nhanh hơn**.

Nếu không có sự kiểm soát chặt chẽ, AI agent sẽ rất nhanh chóng đẩy dự án vào tình trạng mất kiểm soát:
- Tự ý thay đổi nhiều file nằm ngoài phạm vi yêu cầu ban đầu.
- Bỏ qua khâu viết kiểm thử hoặc tự nhận là đã sửa xong dù lệnh build vẫn còn lỗi tiềm ẩn.
- Mất sạch ngữ cảnh sau mỗi phiên làm việc: mỗi sáng mở terminal lên, tôi lại phải kiên nhẫn giải thích lại kiến trúc dự án, thư viện sử dụng và quy ước đặt tên, vừa tốn thời gian vừa tiêu tốn hàng nghìn token vô ích.
- Thời gian đi dọn dẹp hậu quả và sửa lỗi hồi quy có khi còn lâu hơn cả việc tự gõ code từ đầu.

AI agent không hề thiếu năng lực lập trình; thứ agent thiếu chính là **kỷ luật kỹ thuật** của một kỹ sư giàu kinh nghiệm.

Dự án **Coding Friend** của tác giả Đinh Anh Thi ([cf.dinhanhthi.com](https://cf.dinhanhthi.com/)) được tạo ra để giải quyết chính xác bài toán này: biến AI agent bạn đang dùng thành một cộng sự làm việc có phương pháp, có kiểm tra và có bộ nhớ tích lũy.

---

## Coding Friend là gì và cơ chế vận hành cốt lõi

Coding Friend không phải là một mô hình AI mới, cũng không phải một giao diện web cồng kềnh. Đây là một bộ công cụ tinh gọn và có chính kiến được cài đặt trực tiếp vào môi trường agent mà bạn đang dùng: Claude Code, Codex CLI, Google Antigravity hoặc oh-my-pi.

Thay vì để agent tự do thao tác theo trực giác ngẫu hứng, Coding Friend bổ sung vào hệ thống 4 thành phần nền tảng:

1. **Skills (`/cf-*`)**: Các kỹ năng chuyên trách có thể gọi chủ động bằng lệnh gạch chéo hoặc được hệ thống tự động kích hoạt khi xuất hiện tình huống tương ứng trong luồng trò chuyện.
2. **Sub-agents chuyên biệt**: Các tác tử con chạy trên những không gian ngữ cảnh độc lập để thực hiện tác vụ nặng mà không làm ô nhiễm bộ nhớ của phiên chính.
3. **Lifecycle Hooks**: Các điểm chặn an toàn nhằm kiểm soát quyền hạn, phê duyệt lệnh tự động và bảo vệ dự án trước nguy cơ prompt injection.
4. **CF Memory**: Bộ nhớ dự án bền vững qua giao thức Model Context Protocol, giúp agent đọc và ghi chép tri thức vào thư mục `docs/`.

{{< diagram src="/diagrams/coding-friend-architecture.svg" dark="/diagrams/coding-friend-architecture-dark.svg" alt="Kiến trúc tổng quan của Coding Friend" caption="Kiến trúc Coding Friend: Phối hợp giữa Skills, Sub-agents, Hooks và Bộ nhớ dự án" >}}

Khi bạn đưa ra một yêu cầu, lệnh tương ứng sẽ điều phối các sub-agent chuyên biệt. `cf-explorer` đi đọc hiểu codebase, `cf-planner` thiết kế các phương án, `cf-implementer` bắt tay viết mã, còn `cf-reviewer` chịu trách nhiệm soi xét từng dòng diff. Mọi tri thức rút ra trong quá trình làm việc được ghi nhận có hệ thống vào thư mục `docs/` để tái sử dụng lâu dài.

---

## Vòng lặp phát triển 5 bước nâng cao năng suất mỗi ngày

Điểm mấu chốt giúp Coding Friend gia tăng năng suất thực chiến cho lập trình viên là **quy trình làm việc 5 bước có kỷ luật**. Toàn bộ chu trình từ lúc nảy sinh ý tưởng đến khi tạo Pull Request được xâu chuỗi mạch lạc:

{{< diagram src="/diagrams/coding-friend-workflow.svg" dark="/diagrams/coding-friend-workflow-dark.svg" alt="Quy trình làm việc hàng ngày với Coding Friend" caption="Vòng lặp phát triển 5 bước: Khảo sát, Lập kế hoạch, Viết mã kiểm thử, Đánh giá và Phát hành" >}}

### 1. Lập kế hoạch trước khi chạm vào mã với `/cf-plan`

Một thói quen nguy hiểm khi làm việc với AI là đưa ra yêu cầu rồi để agent lập tức sửa file. Với các tính năng mở rộng qua nhiều tầng kiến trúc, cách làm này gần như chắc chắn dẫn đến đứt gãy hệ thống.

Lệnh `/cf-plan` buộc agent phải dừng lại tư duy trước khi hành động:
- Sub-agent `cf-explorer` quét nhanh các module liên quan trong kho mã nguồn.
- Sub-agent `cf-planner` so sánh 2 đến 3 phương án kiến trúc khả dĩ, chỉ ra ưu nhược điểm và rủi ro của từng cách tiếp cận.
- Bản kế hoạch được chia thành các phase nhỏ. Mỗi phase bị giới hạn nghiêm ngặt **không quá 15 file**.

> [!TIP]
> Giới hạn 15 file cho mỗi phase là một quy chuẩn thiết kế thông minh: nó vừa đảm bảo agent không bị quá tải ngữ cảnh dẫn đến ảo giác, vừa giữ cho quá trình code review sau đó diễn ra nhanh, rẻ và chuẩn xác.

Các cờ tùy chọn hữu ích trong thực tế:
- `--fast`: Bỏ qua bước khảo sát chuyên sâu, lập kế hoạch nhanh gọn trực tiếp trong khung chat và không lưu thành file.
- `--auto`: Bật chế độ autopilot tự hành. Sau khi bạn duyệt kế hoạch tổng quan, agent sẽ tự động chạy qua từng phase, tự gọi review, tự sửa lỗi và commit mà không cần bạn phải bấm xác nhận thủ công nhiều lần.
- `--add-tests`: Tự động kích hoạt cơ chế TDD cho các sub-agent thực thi trong từng phase.

```bash
# Lập kế hoạch tính năng xác thực người dùng
/cf-plan Xây dựng hệ thống xác thực hai lớp với JWT

# Lập kế hoạch nhanh cho tác vụ nhỏ
/cf-plan --fast Tối ưu truy vấn danh sách bài viết gần đây
```

Nếu một kế hoạch đang thực thi dở dang mà bạn cần chuyển phiên làm việc, lệnh `/cf-plan-resume` sẽ tải lại ngữ cảnh, bỏ qua các đầu việc đã xong và tiếp tục triển khai các tác vụ còn lại.

### 2. Viết mã có kiểm soát với cổng kiểm thử `cf-tdd`

Trước khi bất kỳ dòng mã production nào được ghi vào file, `cf-tdd` sẽ tự động đóng vai trò người gác cổng.

Kỹ năng này hoạt động ở hai chế độ rõ ràng:
- **Chế độ trực tiếp mặc định (Direct Mode)**: Dành cho các chỉnh sửa đơn giản hoặc các tác vụ không yêu cầu bổ sung test mới.
- **Chế độ TDD dẫn hướng kiểm thử**: Được kích hoạt khi truyền cờ `--add-tests` (hoặc `--tdd`), hay khi bật cấu hình `tdd: true` trong file cấu hình dự án. Agent sẽ tuân thủ nghiêm ngặt chu trình Đỏ → Xanh → Tái cấu trúc:
  1. Viết một bài kiểm thử thất bại (RED) mô tả đúng hành vi mong đợi.
  2. Viết lượng mã vừa đủ để bài test vượt qua thành công (GREEN).
  3. Dọn dẹp và tối ưu mã nguồn mà không làm gãy bài test (REFACTOR).

Nhờ cổng gác này, chúng ta loại bỏ được thói quen xấu của AI là viết mã xong xuôi rồi mới tạo ra những bài test hình thức chạy qua loa để đối phó.

### 3. Sửa lỗi có phương pháp với `/cf-fix` và `cf-sys-debug`

Khi gặp lỗi hỏng hóc hoặc regression trong mã nguồn, phản xạ thông thường của AI là thử sai ngẫu nhiên: sửa một chỗ, chạy lại thấy lỗi khác, lại sửa tiếp cho đến khi toàn bộ logic rối loạn.

Coding Friend định hình việc gỡ lỗi thành một quy trình khoa học:

1. **`/cf-fix`**: Tiếp nhận hiện tượng lỗi, tự động tra cứu hồ sơ các lỗi tương tự từng được ghi nhận trong `docs/memory/bugs/`, khoanh vùng nguyên nhân gốc rễ, sửa đổi mã và viết test hồi quy để chứng minh lỗi đã biến mất hoàn toàn.
2. **`cf-sys-debug`**: Tự động kích hoạt khi lỗi tái diễn nhiều lần hoặc khó tái hiện. Kỹ năng này bắt buộc agent phải tuân thủ 4 bước chặt chẽ:
   - Nêu rõ giả thuyết lỗi kèm vị trí `file:line` cụ thể trước khi được phép chỉnh sửa mã nguồn.
   - Thiết kế bài thử nghiệm cô lập để chứng minh hoặc bác bỏ giả thuyết.
   - Áp dụng bản vá có kiểm thử bảo vệ hồi quy.
   - Ghi lại tài liệu phân tích lỗi chi tiết vào bộ nhớ dự án để phòng tránh tái phạm.

```text
> ✨ CODING FRIEND → /cf-fix activated
Root cause:   Thiếu xử lý null check khi payload token rỗng, auth/jwt.go:42
Fix:          Bổ sung kiểm tra độ dài buffer trước khi decode, auth/jwt.go:42
Confirmed:    Chạy test TestDecodeEmptyToken thành công
Tests:        12 passed, 0 failed
Status: DONE
```

### 4. Đánh giá mã nguồn đa tầng với `/cf-review`

Sau khi code đã được viết xong, Coding Friend không vội vàng chấp nhận kết quả mà đưa diff vào quy trình đánh giá 5 tầng độc lập thông qua `cf-reviewer`:

- **Quy chuẩn dự án**: Đối chiếu với file `AGENTS.md` để đảm bảo không vi phạm các điều cấm kỵ của kho mã nguồn.
- **Bám sát kế hoạch**: Kiểm tra xem code có đi chệch khỏi kế hoạch ban đầu hoặc sửa đổi các file ngoài phạm vi hay không.
- **Chất lượng kỹ thuật**: Rà soát cách đặt tên, độ phức tạp thuật toán, việc xử lý ngoại lệ và loại bỏ các đoạn mã thừa thãi do AI tự sinh.
- **Bảo mật**: Phân tích các lỗ hổng rò rỉ secret, injection và kiểm tra xác thực dữ liệu đầu vào.
- **Kiểm thử**: Đánh giá độ bao phủ kiểm thử của các nhánh mã nguồn mới.

Điểm đặc biệt là Coding Friend hỗ trợ **phản biện chéo cross-agent giữa nhiều mô hình**. Bạn có thể huy động đồng thời OpenAI Codex (`--codex`), Google Gemini (`--gemini`) hay Anthropic Claude (`--claude`) cùng tham gia review song song. Các kết quả sau đó được tổng hợp về một báo cáo duy nhất với cấu trúc phân cấp trực quan:

```text
🚨 Critical
- None.

⚠️ Important
- auth/jwt.go:58: Cần thu hồi refresh token cũ ngay sau khi cấp phát cặp key mới để ngăn chặn tấn công replay.

💡 Suggestions
- config/auth.go:12: Có thể chuyển thời gian hết hạn token sang biến môi trường để dễ cấu hình trên môi trường staging.

📋 Summary
Phát hiện 1 điểm cần hoàn thiện trước khi merge.
Review status: COMPLETE
```

Nếu truyền thêm cờ `--fix`, agent sẽ tự động sửa các lỗi thuộc nhóm Critical và Important, sau đó chạy lại vòng review cho đến khi toàn bộ diff đạt trạng thái sạch sẽ.

### 5. Đóng gói và phát hành với `/cf-commit` và `/cf-ship`

Trước khi cho phép kết thúc công việc, cổng xác minh `cf-verification` sẽ tự động chạy các lệnh test, build và lint thực tế trên máy bạn. Agent bị chặn hoàn toàn, không thể tự ý tuyên bố "đã xong" nếu không đưa ra được bằng chứng xác thực từ kết quả thực thi lệnh.

Khi mọi thứ đã sẵn sàng:
- `/cf-commit`: Phân tích diff, quét kiểm tra secret lần cuối và tạo commit theo chuẩn Conventional Commits, tập trung giải thích lý do tại sao thay đổi mã nguồn thay vì chỉ mô tả lại cú pháp.
- `/cf-ship`: Thực hiện chuỗi xác minh cuối cùng, commit mã, đẩy lên remote và mở Pull Request trên GitHub hoặc GitLab hoàn toàn tự động.

---

## Hệ thống bộ nhớ 3 tầng: Không bao giờ lặp lại bánh xe lịch sử

Một trong những hạn chế lớn nhất khi lập trình cùng AI agent nguyên bản là tính chất vô cảm với quá khứ: mỗi phiên làm việc mới đều như một trang giấy trắng. Bạn phải liên tục nhắc lại các quyết định thiết kế đã thống nhất từ tuần trước.

Coding Friend giải quyết triệt để vấn đề này bằng hệ thống **CF Memory** chạy nền qua giao thức MCP, lấy thư mục `docs/memory/` trong dự án làm nguồn chân lý duy nhất.

{{< diagram src="/diagrams/coding-friend-memory-tiers.svg" dark="/diagrams/coding-friend-memory-tiers-dark.svg" alt="Hệ thống bộ nhớ 3 tầng trong Coding Friend" caption="Cơ chế tìm kiếm 3 tầng của CF Memory: Tự động suy thoái linh hoạt từ SQLite FTS5 sang MiniSearch và grep markdown" >}}

Hệ thống tra cứu được thiết kế với cơ chế suy thoái linh hoạt (graceful degradation):
1. **Tầng 1 (Tối ưu)**: Sử dụng SQLite kết hợp tìm kiếm toàn văn FTS5 và vector embeddings để tìm kiếm ngữ nghĩa chính xác cao.
2. **Tầng 2 (Dự phòng nhanh)**: Nếu môi trường thiếu thư viện native của SQLite, hệ thống tự động chuyển sang MiniSearch chạy thuần trên bộ nhớ Node.js.
3. **Tầng 3 (Dự phòng cơ bản)**: Nếu không có cả hai tầng trên, hệ thống vẫn tra cứu mượt mà bằng lệnh grep trực tiếp trên các file markdown thô.

Đặc biệt, Coding Friend phân định rất rạch ròi giữa hai luồng tri thức:

- **Bộ nhớ dự án (`docs/memory/`)**: Được cập nhật qua lệnh `/cf-remember` hoặc tự động ghi nhận khi kết thúc phiên. Nơi đây lưu trữ các quyết định kiến trúc (`decisions/`), quy ước viết code (`conventions/`), phân tích lỗi (`bugs/`) và luồng tính năng (`features/`). Nhờ vậy, agent trong các phiên sau có thể tự tìm kiếm thông tin và không lãng phí token để hỏi lại bạn.
- **Sổ tay học tập cá nhân (`~/.coding-friend/learn/`)**: Được cập nhật qua lệnh `/cf-learn`. Thay vì để tri thức trôi tuột sau khi giải quyết xong một bài toán hóc búa, kỹ năng này tổng hợp các bài học kỹ thuật thành những ghi chú súc tích dành riêng cho bạn.

> [!NOTE]
> Bạn có thể chạy lệnh `cf learn host` ngay trên máy tính để biến toàn bộ kho ghi chú học tập trong `~/.coding-friend/learn/` thành một website tra cứu cá nhân trực quan và hiện đại.

---

## Tự động hóa an toàn và lá chắn phòng vệ Prompt Injection

Khi ứng dụng AI agent vào công việc thực tế, hai rào cản lớn nhất đối với trải nghiệm lập trình viên là: sự mệt mỏi khi phải liên tục phê duyệt lệnh và mối lo ngại về an ninh bảo mật. Coding Friend giải quyết cả hai vấn đề này bằng các cơ chế tự động hóa có kiểm soát.

### Cơ chế phê duyệt thông minh Auto-approve

Nếu cứ mỗi lệnh `ls`, `cat` hay `npm test` mà agent đều dừng lại chờ người dùng gõ Enter xác nhận, nhịp làm việc sẽ bị đứt quãng liên tục. Cơ chế Auto-approve của Coding Friend tạo ra một hành lang an toàn:

{{< diagram src="/diagrams/coding-friend-auto-approve.svg" dark="/diagrams/coding-friend-auto-approve-dark.svg" alt="Cơ chế phê duyệt tự động Auto-approve" caption="Cơ chế phê duyệt tự động: Lọc lệnh an toàn, cho phép sửa file dự án và hỗ trợ bộ phân loại LLM" >}}

- **Rule-Based Gate**: Tự động phê duyệt ngay lập tức các lệnh đọc dữ liệu an toàn. Chặn đứng các lệnh có nguy cơ phá hủy hệ thống hoặc can thiệp sâu vào lịch sử Git.
- **Working-Dir Edits**: Tự động cho phép tạo và sửa đổi các file nằm trong phạm vi thư mục của dự án hiện tại.
- **Test Runners Whitelist**: Tự động thông qua các lệnh chạy kiểm thử quen thuộc như `npm test`, `pytest`, `go test`, `cargo test` cùng các đường ống lệnh đi kèm.
- **LLM Classifier**: Đối với các lệnh phức tạp chưa rõ phạm vi, bạn có thể tùy chọn kích hoạt bộ phân loại bằng mô hình ngôn ngữ lớn để đánh giá mức độ rủi ro trước khi xin ý kiến người dùng.

### Lá chắn 3 lớp phòng vệ Prompt Injection

Khi làm việc với các kho mã nguồn mở hoặc khi yêu cầu agent tìm kiếm tài liệu trên web, agent có thể vô tình đọc phải các đoạn văn bản chứa mã độc prompt injection nhằm điều khiển hành vi của mô hình.

Coding Friend thiết lập nguyên tắc cốt lõi: **Toàn bộ dữ liệu từ bên ngoài (kết quả web search, output từ tool MCP hay file lạ) đều là dữ liệu không đáng tin cậy**.

{{< diagram src="/diagrams/coding-friend-security-pipeline.svg" dark="/diagrams/coding-friend-security-pipeline-dark.svg" alt="Quy trình bảo mật phòng vệ Prompt Injection" caption="Lá chắn bảo mật 3 tầng: Cô lập dữ liệu, Trích xuất thông tin thuần túy và Cảnh báo mối nguy hại" >}}

Hệ thống bảo vệ vận hành qua 3 giai đoạn chặt chẽ:
1. **Cô lập dữ liệu**: Gắn nhãn dữ liệu ngoại lai là dữ liệu thô, cấm tuyệt đối việc thực thi chúng như các chỉ thị điều khiển.
2. **Trích xuất thông tin**: Chỉ bóc tách thông tin và dữ kiện kỹ thuật, chủ động loại bỏ các câu lệnh ngầm được cài cắm.
3. **Cảnh báo nguy cơ**: Ngay lập tức cảnh báo tới người dùng nếu phát hiện các mẫu nội dung có dấu hiệu tấn công hoặc tìm cách đánh cắp biến môi trường và khóa bí mật.

---

## Cài đặt nhanh và đưa vào dự án trong 5 phút

Việc đưa Coding Friend vào dự án diễn ra rất nhanh chóng. Bạn chỉ cần môi trường Node.js 20 trở lên và công cụ AI agent mà bạn đang sử dụng.

### Cách 1: Cài đặt tự động bằng một dòng Prompt khuyên dùng

Bạn chỉ cần sao chép đoạn chỉ dẫn sau và dán trực tiếp vào cửa sổ chat của AI agent:

```text
Install Coding Friend from https://cf.dinhanhthi.com on my system. First read the installation documentation to understand what Coding Friend is and how to install it properly. Check if I have Node.js 20+, install coding-friend-cli globally, then install the plugin for my current AI agent (auto-detect: Claude Code, Codex, oh-my-pi, Antigravity, etc.). After installation, initialize the project with cf init. Guide me through the entire process and verify everything works correctly.
```

Agent sẽ tự động đọc tài liệu chính thức từ trang chủ, nhận diện môi trường làm việc của bạn và cấu hình toàn bộ hệ thống từ đầu đến cuối.

### Cách 2: Cài đặt thủ công qua dòng lệnh CLI

Nếu muốn tự tay kiểm soát các bước, bạn có thể mở terminal và chạy chuỗi lệnh sau:

```bash
# Bước 1: Cài đặt công cụ dòng lệnh toàn cục
npm i -g coding-friend-cli

# Bước 2: Cài đặt plugin tương ứng với agent đang dùng
cf install               # Mặc định cho Claude Code
cf install --agent agy   # Dành cho Google Antigravity
cf install --agent codex # Dành cho OpenAI Codex
cf install --agent omp   # Dành cho oh-my-pi

# Bước 3: Khởi tạo cấu hình và thư mục docs cho dự án hiện tại
cf init

# Bước 4: Kiểm tra trạng thái hoạt động của hệ thống
cf status
```

> [!NOTE]
> Nếu tên lệnh `cf` trên máy bạn bị trùng với công cụ khác (chẳng hạn Cloudflare CLI), bạn có thể dùng lệnh thay thế `cdf` với đầy đủ tính năng tương đương: `cdf install`, `cdf init`, `cdf status`.

Sau khi khởi tạo với `cf init`, dự án của bạn sẽ xuất hiện thư mục `docs/` để lưu trữ kế hoạch và bộ nhớ, cùng file cấu hình `.coding-friend/config.json`. Bạn có thể tùy biến ngôn ngữ, chế độ TDD hay quy tắc review thông qua lệnh:

```bash
cf config
```

### Mở rộng kỹ năng linh hoạt với Custom Guides

Một điểm sáng tạo khác trong kiến trúc của Coding Friend là tính năng **Custom Guides**. Bạn có thể tùy biến hành vi của bất kỳ skill nào mà không cần phải can thiệp hay sửa đổi mã nguồn của plugin gốc.

Chỉ cần chạy lệnh tạo hướng dẫn riêng:

```bash
cf guide create cf-commit
```

Lệnh này sẽ tạo ra file `.coding-friend/skills/cf-commit-custom/SKILL.md` ngay trong dự án của bạn. Bạn có thể chèn các quy tắc kiểm tra nhánh Git hoặc định dạng mã vé công việc vào các phần:

```markdown
## Before
- Kiểm tra tên nhánh hiện tại phải tuân thủ định dạng `feat/*` hoặc `fix/*`.

## Rules
- Tiêu đề commit bắt buộc phải chứa mã vé công việc tương ứng lấy từ tên nhánh.

## After
- Chạy lệnh kiểm tra tính hợp lệ của commit message trước khi hoàn tất.
```

Ở các lần chạy tiếp theo, mỗi khi bạn gõ `/cf-commit`, Coding Friend sẽ tự động nạp các quy tắc bổ sung này vào quy trình mà không cần phải khởi động lại phiên làm việc.

---

## Năng suất thực sự đến từ sự chuẩn mực

Lập trình cùng AI agent đang thay đổi diện mạo của ngành công nghiệp phần mềm mỗi ngày. Nhưng việc gõ phím nhanh hơn chỉ thực sự mang lại giá trị khi sản phẩm đầu ra có chất lượng cao, có thể bảo trì và kiểm thử được.

Thay vì tiếp tục "vibe coding" một cách may rủi và dành phần lớn thời gian để khắc phục các lỗi do AI sinh ra thiếu kiểm soát, **Coding Friend** mang đến cho chúng ta một khuôn khổ làm việc chuẩn mực:
- **Khảo sát kỹ lưỡng và lập kế hoạch trước khi viết code** (`/cf-plan`).
- **Gác cổng kiểm thử chặt chẽ trong từng dòng thay đổi** (`cf-tdd`).
- **Sửa lỗi có phương pháp và chặn đứng hồi quy** (`/cf-fix`, `cf-sys-debug`).
- **Phản biện mã nguồn khách quan đa tầng** (`/cf-review`).
- **Tích lũy tri thức bền vững cho cả AI và con người** (`/cf-remember`, `/cf-learn`).

Khi kỷ luật kỹ thuật được tự động hóa vào ngay chính công cụ bạn dùng hàng ngày, bạn sẽ thấy tốc độ sinh mã của AI kết hợp cùng tư duy kiến trúc của lập trình viên tạo nên một năng suất làm việc vượt trội và đáng tin cậy.
