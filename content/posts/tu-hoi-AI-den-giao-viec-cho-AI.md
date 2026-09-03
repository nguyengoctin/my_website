---

title: "Từ hỏi AI đến giao việc cho AI"
date: 2026-09-03T11:58:27+07:00
weight: 1
draft: false
author: "Nguyen Ngoc Tin"
description: "Tôi từng nghĩ dùng AI tốt hơn là biết nhiều prompt hơn. Sau một thời gian sưu tầm, tổ chức rồi nghiên cứu lại cách prompting, tôi bắt đầu chuyển từ hỏi AI sang giao cho nó những công việc cụ thể."
tags: ["AI", "Prompt Engineering", "Workflow"]
categories: ["Tech Blog"]
-------------------------

Có một thời gian tôi dùng AI rất đơn giản: nghĩ gì thì hỏi đó. Có lỗi thì paste lỗi vào, không hiểu một khái niệm thì yêu cầu giải thích, cần code thì nhờ viết. Muốn biết công cụ A hay B tốt hơn thì hỏi AI so sánh. Câu trả lời chưa ổn thì tôi đổi cách hỏi rồi thử tiếp.

Cách này vẫn hữu ích. Tôi làm được nhiều việc nhanh hơn trước, nên ban đầu cũng không thấy có gì phải thay đổi. Chỉ là gần như mỗi lần mở AI lên, tôi lại bắt đầu từ đầu: có một vấn đề, nghĩ một câu hỏi cho vấn đề đó, nhận câu trả lời rồi tự xử lý phần còn lại.

Cùng lúc đó, tôi rất dễ FOMO mấy nội dung kiểu “10 câu lệnh ChatGPT giúp bạn...” hay “những prompt bạn nhất định phải biết”. Thấy prompt nào hay là lưu, có framework mới thì thử. Prompt nào dài, chia role, context, task, output nhìn càng bài bản thì càng dễ khiến tôi nghĩ chắc đây là thứ mình đang thiếu.

Tôi từng nghĩ mình dùng AI chưa hiệu quả vì chưa biết đủ nhiều prompt hay, nên prompt cứ nhiều dần. Đến lúc thực sự cần dùng thì lại không biết nên lấy cái nào. Có những prompt gần giống nhau, có prompt của người khác đọc rất hay nhưng đem vào công việc của tôi lại không hợp, cũng có những thứ lúc lưu thấy hữu ích nhưng một thời gian sau nhìn lại chẳng nhớ mình định dùng nó trong trường hợp nào.

Tôi có nhiều prompt hơn, nhưng cách dùng AI không rõ ràng hơn bao nhiêu.

Thế là tôi bắt đầu gom chúng vào [Obsidian](https://obsidian.md/). Ít nhất prompt không còn nằm rải rác trong các conversation và tôi có một chỗ để đặt tên, phân loại, tìm lại. Cách này giải quyết được chuyện lưu trữ, nhưng mỗi lần muốn dùng một prompt, tôi lại phải mở Obsidian, tìm trong một nùi file, copy, quay sang AI, paste rồi mới thêm input.

Sau đó tôi tìm tới [Espanso](https://espanso.org/), một text expander mã nguồn mở. Những prompt dùng thường xuyên có thể được gắn với một trigger ngắn và gọi ra ngay tại nơi tôi đang gõ. Tôi không còn phải mở Obsidian mỗi lần nữa.

Nhanh hơn thật. Nhưng prompt vẫn rối tung.

Đến đây tôi bắt đầu thấy vấn đề không còn nằm ở chuyện lưu prompt ở đâu hay lấy chúng ra nhanh đến mức nào. Nếu bên dưới vẫn là một đống prompt gần giống nhau mà chính tôi cũng không biết lúc nào nên dùng cái nào, thì thêm một công cụ quản lý tốt hơn chỉ làm cho đống đó dễ truy cập hơn.

Tôi cần hiểu lại mình đang dùng prompt để làm gì.

## Từ câu hỏi sang job

Tôi bắt đầu research prompt engineering kỹ hơn. Khi đọc hướng dẫn của [OpenAI](https://platform.openai.com/docs/guides/prompt-engineering), [Google Gemini](https://ai.google.dev/gemini-api/docs/prompting-strategies) và [Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables), tôi gặp một số ý khá giống nhau: task cần đủ rõ, model cần context phù hợp và khi prompt trở nên phức tạp thì việc phân biệt instruction, context, input hay các thành phần khác giúp model biết mình đang được yêu cầu làm gì.

Tôi không lấy một framework nào rồi bê nguyên về. Nhưng khi đặt những gì vừa đọc cạnh vấn đề mình đang gặp, tôi bắt đầu có một cách hình dung khá dễ hiểu: cứ coi AI như một công nhân mà tôi có thể giao việc. Tôi có một job thì giao job đó cho nó. Muốn nó làm đúng, trước hết tôi phải biết công việc là gì, sau đó mới đưa những context cần thiết.

Ví dụ tôi có thể hỏi:

> Espanso có tốt không?

AI hoàn toàn có thể trả lời. Nó có thể kể tính năng, liệt kê ưu nhược điểm và đưa vài lựa chọn thay thế. Nhưng nếu tôi thực sự đang cân nhắc dùng Espanso trên Ubuntu thì đó chưa phải toàn bộ thứ tôi muốn biết.

Tôi muốn xem người dùng thực tế gặp vấn đề gì, lỗi nào xuất hiện lặp lại, có vấn đề nào phụ thuộc môi trường hay phiên bản không, những vấn đề cũ nào đã được sửa, claim nào cần quay về documentation để kiểm tra, những người không dùng Espanso thì chọn gì khác và vì sao. Sau đó tôi mới muốn biết với workflow của mình, nó có đáng dùng hay không.

Câu “Espanso có tốt không?” mới mô tả topic. Công việc phía sau nó lớn hơn một câu hỏi như vậy. Tôi bắt đầu xem đó là một research job.

Cách nhìn này dần lan sang những việc khác tôi thường giao cho AI. Research xem cộng đồng thực sự đang nói gì là một job. So sánh vài lựa chọn để hỗ trợ một quyết định là một job. Audit một prompt đang có là một job. Biến một ý định thành prompt có thể tái sử dụng cũng là một job.

Từ đây tôi ít quan tâm hơn tới việc câu prompt có nghe “xịn” hay không. Tôi muốn biết nó có mô tả đúng công việc cần hoàn thành và có kiểm soát được những chỗ tôi thực sự sợ nó đi sai hay chưa.

Ví dụ khi research cộng đồng, tôi không muốn AI lấy vài comment rồi gọi đó là “đồng thuận”. Tôi muốn nó phân biệt lời kể của một người, một pattern xuất hiện ở nhiều nguồn độc lập và một claim có thể kiểm chứng. Những thứ như tính năng, compatibility, giá, policy hay giới hạn thì ưu tiên quay về nguồn chính thức. Nếu tôi đã nghiêng về một lựa chọn, tôi cũng muốn nó tìm evidence chống lại lựa chọn đó thay vì chỉ tiếp tục gom thêm lý do để đồng ý với tôi.

Những instruction như vậy có lý do để nằm trong prompt vì chúng đang ngăn một failure mode cụ thể. Tôi không cần thêm persona, framework hay checklist chỉ vì một bài hướng dẫn nào đó nói một prompt tốt phải có chúng.

## Pattern và Context

Khi một job bắt đầu xuất hiện nhiều lần, tôi không muốn mỗi lần lại thiết kế prompt từ đầu. Tôi bắt đầu giữ những prompt có tính tái sử dụng và gọi chúng là **Patterns**: research cộng đồng, so sánh lựa chọn, cải thiện prompt, tạo prompt, chắt lọc một cuộc thảo luận thành reference note.

Mỗi Pattern cố gắng phục vụ một job tương đối rõ. Nhưng khi library lớn hơn một chút, tôi lại gặp một chuyện khác: nhiều Pattern bắt đầu lặp lại cùng những thông tin.

Viết cho blog này là một ví dụ. Tôi có những preference gần như không thay đổi giữa các bài: không tự tạo trải nghiệm rồi gán cho tôi, không biến uncertainty thành một kết luận chắc chắn, không sửa một câu hơi vụng thành prose nghe hay hơn nhưng đã xa suy nghĩ ban đầu. NgocTin Note cũng có những constraint riêng về Hugo và Markdown.

Những thứ đó không phải bản thân job viết bài. Nó là context mà AI cần biết khi làm job đó cho tôi.

Từ những gì đã research, tôi bắt đầu tự tổ chức thư viện thành hai phần: **Pattern** mô tả job tôi muốn giao, còn **Context** giữ những thông tin hoặc nguyên tắc có thể tái sử dụng giữa nhiều lần làm việc.

Tôi không tìm thấy một chuẩn prompt engineering nào nói rằng prompt library phải được chia thành đúng `Patterns` và `Contexts`. Phần đó là cách tôi tự áp dụng những gì đã nghiên cứu vào workflow cá nhân, và thực tế tôi vẫn đang thay đổi nó.

Có Pattern tôi bỏ, có thứ tôi gộp lại, có instruction ban đầu nằm trong Pattern nhưng sau đó tôi nhận ra nó thuộc về Context hợp lý hơn. [Obsidian](https://obsidian.md/) vẫn là nơi tôi lưu chúng, còn [Espanso](https://espanso.org/) giúp gọi những Pattern dùng thường xuyên mà không phải mở thư viện lên copy paste.

Phần tôi thấy có ích nhất lại không nằm ở hai công cụ đó. Nó nằm ở câu hỏi tôi có thể tự đặt ra trước khi tạo thêm một prompt: **đây có thực sự là một job mới không?**

Nếu job đã có, có thể thứ đang thay đổi chỉ là context. Nếu cả hai đều không có gì mới, tôi không cần thêm một prompt chỉ vì wording của nó khác.

Tôi chưa nghĩ đây là cách mọi người nên quản lý prompt. Nó đơn giản là cách hiện tại giúp tôi bớt quay lại tình trạng sưu tầm rất nhiều câu lệnh nhưng đến lúc cần thì không biết nên dùng câu nào.

## Research là chỗ tôi thấy rõ nhất

Trước đây tôi có thể hỏi AI một vấn đề rồi đọc kết luận. Cách đó rất nhanh, nhưng càng research nhiều tôi càng để ý rằng một câu trả lời trôi chảy có thể che đi khá nhiều thứ: thông tin đến từ documentation hay một bài blog, một người gặp vấn đề hay nhiều người độc lập cùng gặp, claim đó còn đúng với version hiện tại không, model đang nói fact hay inference.

Nếu tất cả được trộn thành một câu trả lời hoàn chỉnh, tôi rất khó nhìn thấy những khác biệt này. Vì vậy tôi dần giao research job cụ thể hơn: trải nghiệm thực tế thì tìm ở những cộng đồng phù hợp với chủ đề, claim có thể kiểm chứng thì quay về documentation, release note, repository hoặc nguồn sơ cấp phù hợp. Nếu recommendation nghiêng về một phía thì tìm cả counter-evidence. Nếu bản thân tôi chưa hiểu problem space đủ rộng, tôi có thể yêu cầu AI tìm những chiều của vấn đề mà mình chưa biết để hỏi.

Ví dụ nếu tôi muốn self-host một dịch vụ, tôi có thể biết để hỏi cách cài, RAM, Docker hay domain. Nhưng nếu chưa từng vận hành một server đủ lâu, tôi có thể chưa nghĩ ngay tới backup, restore, disk failure, monitoring hay upgrade strategy. AI có thể giúp tôi nhìn thấy những thứ đó sớm hơn. Sau đó tôi vẫn phải xem cái nào thực sự liên quan tới trường hợp của mình, cái nào cần kiểm chứng và cái nào đủ quan trọng để ảnh hưởng tới quyết định.

Tôi không cần output đầu tiên của AI luôn đúng. Tôi cần một cách làm việc mà cái sai có cơ hội bị phát hiện trước khi nó trở thành quyết định của tôi.

Càng dùng AI nhiều, tôi càng thấy đây mới là phần cần để ý. AI có thể research, viết code, phân tích một vấn đề, tìm lựa chọn thay thế, phản biện recommendation và tổng hợp một lượng thông tin mà tôi khó xử lý với cùng tốc độ. Tôi muốn tận dụng những khả năng đó, nhưng tôi vẫn muốn giữ cho mình việc xác định vấn đề đang được giải quyết, tiêu chí nào thật sự quan trọng, evidence nào đủ để tin và output cuối cùng có đang trả lời đúng job hay chỉ nghe rất hợp lý.

Nếu tôi dùng một kết luận để hành động và nó sai, người chịu hậu quả vẫn là tôi.

Tôi cũng không nghĩ Prompt Library hiện tại sẽ tồn tại mãi. Có thể agent tốt hơn khiến Espanso không còn cần thiết. Có thể cách quản lý context sau này khác hoàn toàn. Có thể một số workflow tôi đang tự xây hôm nay rồi sẽ trở thành tính năng mặc định của những công cụ AI.

Tôi chưa biết. Thứ tôi muốn giữ lại không phải một bộ prompt hay một bộ công cụ cố định, mà là cách bắt đầu từ công việc mình thực sự cần làm: xác định job, đưa context cần thiết, kiểm tra những phần đáng nghi và tự quyết định output cuối cùng có đáng dùng hay không.

Prompt với tôi bây giờ ít giống một thứ để sưu tầm hơn. Nó chỉ là cách tôi giao việc.
