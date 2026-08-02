---
title: "RAG & Implementation"
description: "Retrieval-Augmented Generation (RAG) combines information retrieval with language generation to produce more accurate, context-aware responses."
summary: "Retrieval-Augmented Generation (RAG) kết hợp việc truy xuất thông tin với tạo ngôn ngữ để tạo ra các phản hồi chính xác hơn và nhận biết ngữ cảnh."
slug: "what-are-rags"
date: 2026-08-01
weight: 64
next: "/ai-engineer/04-rag-and-vector-databases/rag-usecases/"
prev: "/ai-engineer/04-rag-and-vector-databases/performing-similarity-search/"
draft: false


tags:
  - RAG
  - LLM
  - Retrieval

toc: true
math: false
mermaid: false
---

**Retrieval-Augmented Generation (RAG) | combines information retrieval | with language generation to**  
*Retrieval-Augmented Generation (RAG) | kết hợp việc truy xuất thông tin | với tạo ngôn ngữ để*

**produce more accurate, | context-aware responses. | It uses two components:**  
*tạo ra các phản hồi | chính xác hơn và nhận biết ngữ cảnh. | Nó sử dụng hai thành phần:*

**a retriever, which | searches a database | to find relevant information,**  
*một bộ truy xuất, cái mà | tìm kiếm trong cơ sở dữ liệu | để tìm thông tin liên quan,*

**and a generator, | which crafts a | response based on the**  
*và một bộ tạo, | cái mà tạo ra một | phản hồi dựa trên*

**retrieved data. | Implementing | RAG involves using a**  
*dữ liệu đã truy xuất. | Việc triển khai | RAG bao gồm việc sử dụng một*

**retrieval model (e.g., | embeddings and vector | search) alongside a generative**  
*mô hình truy xuất (ví dụ: | embedding và tìm kiếm | vector) cùng với một mô hình tạo*

**language model (like | GPT). | The process | starts by converting a**  
*ngôn ngữ (như | GPT). | Quy trình | bắt đầu bằng việc chuyển đổi một*

**query into embeddings, | retrieving relevant documents | from a vector database,**  
*truy vấn thành các embedding, | truy xuất các tài liệu liên quan | từ một cơ sở dữ liệu vector,*

**and feeding them | to the language | model, which then generates**  
*và cung cấp chúng | cho mô hình | ngôn ngữ, cái mà sau đó tạo ra*

**a coherent, informed | response. | This approach | grounds outputs in real-world**  
*một phản hồi mạch lạc, | có cơ sở. | Cách tiếp cận này | đặt các đầu ra dựa trên dữ liệu*

**data, resulting in | more reliable and | detailed answers. |**  
*thực tế, dẫn đến | các câu trả lời chi tiết | và đáng tin cậy hơn. |*

## Resources

- [What is RAG?](https://aws.amazon.com/what-is/retrieval-augmented-generation/) (article)
- [RAG Explained: Understanding Embeddings, Similarity, and Retrieval](https://towardsdatascience.com/rag-explained-understanding-embeddings-similarity-and-retrieval/?utm_source=roadmap&utm_medium=Referral&utm_campaign=TDS+roadmap+integration) (article)
- [What is Retrieval-Augmented Generation? IBM](https://www.youtube.com/watch?v=T-D1OfcDW1M) (video)

## References

- https://roadmap.sh/ai-engineer (Node: What are RAGs?)

---

[← Performing Similarity Search](/ai-engineer/04-rag-and-vector-databases/performing-similarity-search/) · [AI Engineer Roadmap](/ai-engineer/) · [RAG Usecases →](/ai-engineer/04-rag-and-vector-databases/rag-usecases/)
