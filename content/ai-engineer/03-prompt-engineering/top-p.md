---
title: "Top-P Sampling"
description: "Top-P sampling, also known as nucleus sampling, is a technique used in language models to generate text."
summary: "Top-P sampling, còn được gọi là nucleus sampling, là một kỹ thuật được sử dụng trong các mô hình ngôn ngữ để tạo văn bản."
slug: "top-p"
date: 2026-08-01
weight: 29
next: "/ai-engineer/03-prompt-engineering/few-shot/"
prev: "/ai-engineer/03-prompt-engineering/top-k/"
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

# Top-P Sampling

**Top-P sampling, also known as | nucleus sampling, is a technique | used in language models | to generate text.**  
*Top-P sampling, còn được gọi là | nucleus sampling, là một kỹ thuật | được sử dụng trong các mô hình ngôn ngữ | để tạo văn bản.*

**Instead of considering | all possible next words, | it focuses on the smallest set | of words whose cumulative probability**  
*Thay vì xem xét | tất cả các từ tiếp theo có thể, | nó tập trung vào tập hợp nhỏ nhất | các từ có xác suất tích lũy*

**exceeds a threshold 'P'. | Unlike Top-K's fixed number, | Top-P dynamically adjusts | based on the probability distribution.**  
*vượt quá một ngưỡng 'P'. | Không giống như số cố định của Top-K, | Top-P điều chỉnh linh hoạt | dựa trên phân phối xác suất.*

**Low values (0.1-0.5) | produce focused outputs, | medium (0.6-0.9) | balance creativity and coherence, | and high (0.9-0.99) | enable creative diversity.**  
*Các giá trị thấp (0.1-0.5) | tạo ra các đầu ra tập trung, | trung bình (0.6-0.9) | cân bằng giữa sự sáng tạo và tính mạch lạc, | và cao (0.9-0.99) | cho phép sự đa dạng sáng tạo.*

## Resources

- [What are the LLM’s Top-P + Top-K ?](https://www.youtube.com/watch?v=aDmp2Uim0zQ) (video)

## References

- https://roadmap.sh/ai-engineer (Node: Top-P)

---

[← Top-K](/ai-engineer/03-prompt-engineering/top-k/) · [AI Engineer Roadmap](/ai-engineer/) · [Few-Shot →](/ai-engineer/03-prompt-engineering/few-shot/)
