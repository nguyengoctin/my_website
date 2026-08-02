---
title: "Function Calling"
description: "LLM native “function calling” lets a large language model decide when to run a piece of code and which inputs to pass to it."
summary: "Tính năng “function calling” gốc của LLM cho phép một mô hình ngôn ngữ lớn quyết định khi nào cần chạy một đoạn code và những đầu vào nào cần truyền cho nó."
slug: "function-calling"
date: 2026-08-01
weight: 94
next: "/backend/13-integration-patterns/integration-patterns/"
prev: "/backend/12-ai-assisted-coding/anthropic/"
draft: false

categories:
  - {'card': 'Backend', 'page': 'Backend Developer', '_id': '6986094d45613096ac8d34a0'}

tags:
  - backend

toc: true
math: false
mermaid: false
---

**LLM native “function calling” | lets a large language | model decide when to**  
*Tính năng “function calling” gốc của LLM | cho phép một mô hình | ngôn ngữ lớn quyết định khi nào*

**run a piece of | code and which inputs | to pass to it.**  
*cần chạy một đoạn | code và những đầu vào nào | cần truyền cho nó.*

**You first tell the | model what functions are | available. For each one,**  
*Bạn trước tiên cho mô hình | biết những hàm nào | khả dụng. Đối với mỗi hàm,*

**you give a short | name, a short description, | and a list of arguments**  
*bạn cung cấp một cái tên | ngắn gọn, một mô tả ngắn, | và một danh sách các đối số*

**with their types. During | a chat, the model | can answer in JSON**  
*với các kiểu dữ liệu của chúng. | Trong một cuộc trò chuyện, | mô hình có thể trả lời bằng JSON*

**that matches this schema | instead of plain text. | Your wrapper program reads**  
*khớp với schema này | thay vì văn bản thuần túy. | Chương trình bao bọc của bạn đọc*

**the JSON, calls the | real function, and then | feeds the result back**  
*JSON, gọi hàm | thực tế, và sau đó | truyền kết quả ngược lại*

**to the model so | it can keep going. | This loop helps an**  
*cho mô hình để | nó có thể tiếp tục. | Vòng lặp này giúp một*

**agent search the web, | look up data, send | an email, or do any**  
*agent tìm kiếm trên web, | tra cứu dữ liệu, gửi | một email, hoặc thực hiện bất kỳ*

**other task you expose. | Because the output is | structured, you get fewer**  
*tác vụ nào khác mà bạn cung cấp. | Vì đầu ra được | cấu trúc, bạn nhận được ít*

**mistakes than when the | model tries to write | raw code or natural-language**  
*sai lầm hơn so với khi | mô hình cố gắng viết | code thô hoặc các lệnh*

**commands.**  
*ngôn ngữ tự nhiên.*

## Resources

- [A Comprehensive Guide to Function Calling in LLMs](https://thenewstack.io/a-comprehensive-guide-to-function-calling-in-llms/) (article)
- [Function Calling with LLMs | Prompt Engineering Guide](https://www.promptingguide.ai/applications/function_calling) (article)
- [Function Calling with Open-Source LLMs](https://medium.com/@rushing_andrei/function-calling-with-open-source-llms-594aa5b3a304) (article)
- [LLM Function Calling - AI Tools Deep Dive](https://www.youtube.com/watch?v=gMeTK6zzaO4) (video)

---

[← Anthropic](/backend/12-ai-assisted-coding/anthropic/) · [Backend Roadmap](/backend/) · [Integration Patterns →](/backend/13-integration-patterns/integration-patterns/)
