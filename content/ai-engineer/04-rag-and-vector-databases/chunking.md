---
title: "Chunking"
description: "The chunking step in Retrieval-Augmented Generation (RAG) involves breaking down large documents or data sources into smaller, manageable chunks."
summary: "Bước chunking trong Retrieval-Augmented Generation (RAG) bao gồm việc chia nhỏ các tài liệu hoặc nguồn dữ liệu lớn thành các phần nhỏ hơn, dễ quản lý."
slug: "chunking"
date: 2026-08-01
weight: 67
next: "/ai-engineer/04-rag-and-vector-databases/embedding/"
prev: "/ai-engineer/04-rag-and-vector-databases/rag-vs-fine-tuning/"
draft: false

categories:
  - AI Engineer

tags:
  - RAG
  - Chunking
  - Data Processing

toc: true
math: false
mermaid: false
---

**The chunking step | in Retrieval-Augmented Generation | (RAG) involves breaking down**  
*Bước chunking | trong Retrieval-Augmented Generation | (RAG) bao gồm việc chia nhỏ*

**large documents or | data sources into | smaller, manageable chunks. | This**  
*các tài liệu lớn hoặc | các nguồn dữ liệu thành | các phần nhỏ, dễ quản lý. | Điều này*

**is done to | ensure that the | retriever can efficiently search**  
*được thực hiện để | đảm bảo rằng | bộ truy xuất có thể tìm kiếm hiệu quả*

**through large volumes | of data while | staying within the token**  
*thông qua các khối lượng | dữ liệu lớn trong khi | vẫn nằm trong giới hạn token*

**or input limits | of the model. | Each chunk, typically | a paragraph or section,**  
*hoặc giới hạn đầu vào | của mô hình. | Mỗi phần, thường là | một đoạn văn hoặc phần,*

**is converted into | an embedding, and | these embeddings are stored**  
*được chuyển đổi thành | một embedding, và | các embedding này được lưu trữ*

**in a vector | database. | When a | query is made, the**  
*trong một cơ sở | dữ liệu vector. | Khi một | truy vấn được thực hiện, bộ*

**retriever searches for | the most relevant | chunks rather than the**  
*truy xuất tìm kiếm | các phần liên quan nhất | thay vì toàn bộ*

**entire document, enabling | faster and more | accurate retrieval. |**  
*tài liệu, cho phép | việc truy xuất nhanh hơn | và chính xác hơn. |*

## Resources

- [Understanding LangChain's RecursiveCharacterTextSplitter](https://dev.to/eteimz/understanding-langchains-recursivecharactertextsplitter-2846) (article)
- [Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/) (article)
- [A Guide to Chunking Strategies for Retrieval Augmented Generation](https://zilliz.com/learn/guide-to-chunking-strategies-for-rag) (article)

## References

- https://roadmap.sh/ai-engineer (Node: Chunking)

---

[← RAG vs Fine-tuning](/ai-engineer/04-rag-and-vector-databases/rag-vs-fine-tuning/) · [AI Engineer Roadmap](/ai-engineer/) · [Embedding →](/ai-engineer/04-rag-and-vector-databases/embedding/)
