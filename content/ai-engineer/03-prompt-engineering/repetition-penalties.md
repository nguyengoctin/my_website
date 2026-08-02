---
title: "Repetition Penalties"
description: "Repetition penalties discourage LLMs from repeating words or phrases by reducing the probability of selecting previously used tokens."
summary: "Repetition penalties ngăn cản các LLM lặp lại các từ hoặc cụm từ bằng cách giảm xác suất chọn các token đã được sử dụng trước đó."
slug: "repetition-penalties"
date: 2026-08-01
weight: 35
next: "/ai-engineer/03-prompt-engineering/sampling-parameters/"
prev: "/ai-engineer/03-prompt-engineering/streaming-responses/"
draft: false


tags:
  - Prompt Engineering

toc: true
math: false
mermaid: false
---

**Repetition penalties discourage LLMs | from repeating words or phrases | by reducing the probability**  
*Repetition penalties ngăn cản các LLM | lặp lại các từ hoặc cụm từ | bằng cách giảm xác suất*

**of selecting previously used tokens. | This includes frequency penalty (scales with usage count) | and presence penalty (applies equally to any used token).**  
*chọn các token đã được sử dụng trước đó. | Điều này bao gồm frequency penalty (tỷ lệ với số lần sử dụng) | và presence penalty (áp dụng như nhau cho bất kỳ token nào đã sử dụng).*

**These parameters improve output quality | by promoting vocabulary diversity | and preventing redundant phrasing.**  
*Các tham số này cải thiện chất lượng đầu ra | bằng cách thúc đẩy sự đa dạng từ vựng | và ngăn chặn cách diễn đạt dư thừa.*

## Resources

- [Stop the LLM From Rambling: Using Penalties to Control Repetition](https://dev.to/superorange0707/stop-the-llm-from-rambling-using-penalties-to-control-repetition-5h8) (article)
- [What are LLM Presence and Frequency Penalties?](https://www.youtube.com/watch?v=J66CRz6s734) (video)

## References

- https://roadmap.sh/ai-engineer (Node: Repetition Penalties)

---

[← Streaming Responses](/ai-engineer/03-prompt-engineering/streaming-responses/) · [AI Engineer Roadmap](/ai-engineer/) · [Sampling Parameters →](/ai-engineer/03-prompt-engineering/sampling-parameters/)
