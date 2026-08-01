---
title: "Streaming Responses"
description: "Streamed responses is one of the techniques an AI agent can use to send its answer to the user."
summary: "Streamed responses là một trong những kỹ thuật mà một AI agent có thể sử dụng để gửi câu trả lời của nó cho người dùng."
slug: "streaming-responses"
date: 2026-08-01
draft: false

categories:
  - AI Engineer

tags:
  - Prompt Engineering

toc: true
math: false
mermaid: false
---

# Streaming Responses

**Streamed responses is one of the techniques | an AI agent can use | to send its answer to the user.**  
*Streamed responses là một trong những kỹ thuật | một AI agent có thể sử dụng | để gửi câu trả lời của nó cho người dùng.*

**With a streamed response, | the agent starts sending words | as soon as it generates them.**  
*Với một streamed response, | agent bắt đầu gửi các từ | ngay khi nó tạo ra chúng.*

**The user sees the text grow | on the screen in real time. | This feels fast and lets the user**  
*Người dùng thấy văn bản tăng lên | trên màn hình trong thời gian thực. | Điều này tạo cảm giác nhanh và cho phép người dùng*

**stop or change the request early. | It is useful for long answers | and chat-like apps.**  
*dừng hoặc thay đổi yêu cầu sớm. | Nó hữu ích cho các câu trả lời dài | và các ứng dụng kiểu chat.*

**By contrast, an unstreamed response | waits until the whole answer is ready, | then sends it all at once.**  
*Ngược lại, một unstreamed response | đợi cho đến khi toàn bộ câu trả lời sẵn sàng, | sau đó gửi tất cả cùng một lúc.*

**This makes the code on the client side | simpler and is easier to cache | or log, but the user must wait longer,**  
*Điều này làm cho mã ở phía client | đơn giản hơn và dễ dàng cache | hoặc log, nhưng người dùng phải đợi lâu hơn,*

**especially for big outputs.**  
*đặc biệt là đối với các đầu ra lớn.*

## Resources

- [Streaming Responses in AI: How AI Outputs Are Generated in Real Time](https://dev.to/pranshu_kabra_fe98a73547a/streaming-responses-in-ai-how-ai-outputs-are-generated-in-real-time-18kb) (article)
- [Streaming vs Non-Streaming LLM Responses](https://medium.com/@vasanthancomrads/streaming-vs-non-streaming-llm-responses-db297ba5467e) (article)
- [AI for Web Devs: Faster Responses with HTTP Streaming](https://austingil.com/ai-for-web-devs-streaming/) (article)

## References

- https://roadmap.sh/ai-engineer (Node: Streaming Responses)
