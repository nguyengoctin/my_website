---
title: "Top-K Sampling"
description: "Top-K sampling is a method used by Large Language Models (LLMs) during text generation to select the next word."
summary: "Top-K sampling là một phương pháp được các mô hình ngôn ngữ lớn (LLMs) sử dụng trong quá trình tạo văn bản để chọn từ tiếp theo."
slug: "top-k"
date: 2026-08-01
weight: 28
next: "/ai-engineer/03-prompt-engineering/top-p/"
prev: "/ai-engineer/03-prompt-engineering/zero-shot/"
draft: false

categories:
  - AI Engineer

tags:
  - prompt engineering
  - sampling

toc: true
math: false
mermaid: false
---

# Top-K Sampling

**Top-K sampling is a method | used by Large Language Models (LLMs) | during text generation | to select the next word.**  
*Top-K sampling là một phương pháp | được các mô hình ngôn ngữ lớn (LLMs) sử dụng | trong quá trình tạo văn bản | để chọn từ tiếp theo.*

**Instead of considering | the entire vocabulary, | it narrows down the choices | to the K most probable words**  
*Thay vì xem xét | toàn bộ từ vựng, | nó thu hẹp các lựa chọn | xuống K từ có xác suất cao nhất*

**predicted by the model. | Low values (1-10) | produce conservative, factual outputs. | Medium values (20-50) | balance creativity and quality.**  
*được dự đoán bởi mô hình. | Các giá trị thấp (1-10) | tạo ra các đầu ra bảo thủ, thực tế. | Các giá trị trung bình (20-50) | cân bằng giữa sự sáng tạo và chất lượng.*

**High values (50+) | enable diverse, creative outputs. | Use low K | for technical tasks, | high K for creative writing.**  
*Các giá trị cao (50+) | cho phép các đầu ra đa dạng, sáng tạo. | Sử dụng K thấp | cho các tác vụ kỹ thuật, | K cao cho viết lách sáng tạo.*

## Resources

- [Top-K Sampling: The Complete Token Selection Guide](https://www.dataannotation.tech/blog/top-k-sampling) (article)
- [What are the LLM’s Top-P + Top-K ?](https://www.youtube.com/watch?v=aDmp2Uim0zQ) (video)

## References

- https://roadmap.sh/ai-engineer (Node: Top-K)

---

[← Zero-Shot](/ai-engineer/03-prompt-engineering/zero-shot/) · [AI Engineer Roadmap](/ai-engineer/) · [Top-P →](/ai-engineer/03-prompt-engineering/top-p/)
