---
title: "Tracing & Logging"
description: "Tracing records the full lifecycle of a request through your AI system, from the initial user input through any intermediate LLM calls, tool uses, or retrieval steps, all the way to the final response."
summary: "Tracing ghi lại toàn bộ vòng đời của một yêu cầu thông qua hệ thống AI của bạn, từ đầu vào ban đầu của người dùng qua bất kỳ cuộc gọi LLM trung gian, việc sử dụng công cụ hoặc các bước truy xuất, cho đến phản hồi cuối cùng."
slug: "tracing-logging"
date: 2026-08-01
weight: 150
next: "/ai-engineer/11-evaluation-safety-and-ethics/costlatency-monitoring/"
prev: "/ai-engineer/11-evaluation-safety-and-ethics/llm-evaluations/"
draft: false

categories:
  - AI Engineer

tags:
  - Tracing
  - Logging
  - Debugging

toc: true
math: false
mermaid: false
---

**Tracing records the full lifecycle | of a request through your AI system, | from the initial user input | through any intermediate LLM calls, | tool uses, or retrieval steps, | all the way to the final response.**  
*Tracing ghi lại toàn bộ vòng đời | của một yêu cầu thông qua hệ thống AI của bạn, | từ đầu vào ban đầu của người dùng | qua bất kỳ cuộc gọi LLM trung gian, | việc sử dụng công cụ hoặc các bước truy xuất, | cho đến phản hồi cuối cùng.*

**Logging captures individual events | like errors, latency spikes, | or unexpected outputs.**  
*Logging ghi lại các sự kiện riêng lẻ | như lỗi, đột biến độ trễ, | hoặc các đầu ra không mong đợi.*

**Together, they let you | reconstruct exactly what happened | during any given interaction, | which is essential | for debugging agents | and multi-step pipelines.**  
*Cùng với nhau, chúng cho phép bạn | tái tạo chính xác những gì đã xảy ra | trong bất kỳ tương tác nào, | điều này rất cần thiết | để gỡ lỗi các agents | và các đường ống đa bước.*

## Resources

- [A guide to LLM debugging, tracing, and monitoring](https://wandb.ai/onlineinference/genai-research/reports/A-guide-to-LLM-debugging-tracing-and-monitoring--VmlldzoxMzk1MjAyOQ) (article)

## References

- https://roadmap.sh/ai-engineer (Node: Tracing & logging)

---

[← LLM Evaluations](/ai-engineer/11-evaluation-safety-and-ethics/llm-evaluations/) · [AI Engineer Roadmap](/ai-engineer/) · [Cost/latency monitoring →](/ai-engineer/11-evaluation-safety-and-ethics/costlatency-monitoring/)
