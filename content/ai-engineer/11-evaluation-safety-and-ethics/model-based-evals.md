---
title: "Model-Based Evals"
description: "Model-based evals use a separate AI model to automatically score or assess the outputs of your LLM application."
summary: "Các đánh giá dựa trên mô hình sử dụng một mô hình AI riêng biệt để tự động chấm điểm hoặc đánh giá đầu ra của ứng dụng LLM của bạn."
slug: "model-based-evals"
date: 2026-08-01
weight: 158
next: "/ai-engineer/11-evaluation-safety-and-ethics/human-evals/"
prev: "/ai-engineer/11-evaluation-safety-and-ethics/deterministic-evals/"
draft: false

categories:
  - AI Engineer

tags:
  - Evaluation
  - LLM-as-a-Judge
  - Automation

toc: true
math: false
mermaid: false
---

**Model-based evals use | a separate AI model | to automatically score | or assess the outputs**  
*Các đánh giá dựa trên mô hình sử dụng | một mô hình AI riêng biệt | để tự động chấm điểm | hoặc đánh giá đầu ra*

**of your LLM application. | Instead of writing | manual rules or relying | on human reviewers,**  
*của ứng dụng LLM của bạn. | Thay vì viết | các quy tắc thủ công hoặc dựa vào | những người đánh giá là con người,*

**you delegate the judgment | to another model, | a technique commonly known | as LLM-as-a-Judge.**  
*bạn ủy quyền việc đánh giá | cho một mô hình khác, | một kỹ thuật thường được gọi | là LLM-as-a-Judge.*

**You write a prompt | describing the evaluation criteria, | and the judge model | rates the response.**  
*Bạn viết một prompt | mô tả các tiêu chí đánh giá, | và mô hình giám khảo | xếp hạng phản hồi.*

**This approach handles | subjective, open-ended quality dimensions | that rules cannot capture, | while scaling far more**  
*Cách tiếp cận này xử lý | các khía cạnh chất lượng chủ quan, mở | mà các quy tắc không thể nắm bắt, | trong khi mở rộng quy mô hơn nhiều*

**cheaply than human review, | though it requires | careful prompt design | to avoid bias**  
*với chi phí rẻ hơn so với đánh giá của con người, | mặc dù nó đòi hỏi | thiết kế prompt cẩn thận | để tránh thiên kiến*

**and inconsistency in | the judges themselves.**  
*và sự không nhất quán | ở chính các giám khảo.*

## Resources

- [A pragmatic guide to LLM evals for devs](https://newsletter.pragmaticengineer.com/p/evals) (article)
- [LLM-as-a-judge: a complete guide to using LLMs for evaluations](https://www.evidentlyai.com/llm-guide/llm-as-a-judge) (article)
- [LLM as a Judge: Scaling AI Evaluation Strategies](https://www.youtube.com/watch?v=trfUBIDeI1Y) (video)

## References

- https://roadmap.sh/ai-engineer (Node: Model-Based Evals)

---

[← Deterministic Evals](/ai-engineer/11-evaluation-safety-and-ethics/deterministic-evals/) · [AI Engineer Roadmap](/ai-engineer/) · [Human Evals →](/ai-engineer/11-evaluation-safety-and-ethics/human-evals/)
