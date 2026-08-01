---
title: "Indexing Embeddings"
description: "Embeddings are stored in a vector database by first converting data, such as text, images, or audio, into high-dimensional vectors using machine learning models."
summary: "Các embedding được lưu trữ trong cơ sở dữ liệu vector bằng cách trước tiên chuyển đổi dữ liệu, chẳng hạn như văn bản, hình ảnh hoặc âm thanh, thành các vector đa chiều bằng cách sử dụng các mô hình học máy."
slug: "indexing-embeddings"
date: 2026-08-01
weight: 62
next: "/ai-engineer/04-rag-and-vector-databases/performing-similarity-search/"
prev: "/ai-engineer/04-rag-and-vector-databases/mongodb-atlas/"
draft: false

categories:
  - AI Engineer

tags:
  - Embeddings
  - Indexing
  - Vector Database

toc: true
math: false
mermaid: false
---

**Embeddings are stored | in a vector database | by first converting data,**  
*Các embedding được lưu trữ | trong cơ sở dữ liệu vector | bằng cách trước tiên chuyển đổi dữ liệu,*

**such as text, | images, or audio, | into high-dimensional vectors using**  
*chẳng hạn như văn bản, | hình ảnh hoặc âm thanh, | thành các vector đa chiều bằng cách sử dụng*

**machine learning models. | These vectors, also | called embeddings, capture the**  
*các mô hình học máy. | Các vector này, còn | được gọi là embedding, nắm bắt các*

**semantic relationships and | patterns within the | data. | Once generated, each**  
*mối quan hệ ngữ nghĩa và | các mẫu hình bên trong | dữ liệu. | Sau khi được tạo, mỗi*

**embedding is indexed | in the vector | database along with its**  
*embedding được lập chỉ mục | trong cơ sở dữ liệu | vector cùng với các*

**associated metadata, such | as the original | data (e.g., text or**  
*siêu dữ liệu liên quan, chẳng hạn | như dữ liệu gốc | (ví dụ: văn bản hoặc*

**image) or an | identifier. | The vector database | then organizes these embeddings**  
*hình ảnh) hoặc một | định danh. | Cơ sở dữ liệu vector | sau đó tổ chức các embedding này*

**to support efficient | similarity searches, typically | using techniques like approximate**  
*để hỗ trợ các tìm kiếm | tương đồng hiệu quả, thường | sử dụng các kỹ thuật như láng giềng*

**nearest neighbor (ANN) | search. |**  
*gần đúng (ANN) | tìm kiếm. |*

## Resources

- [Indexing & Embeddings](https://developers.llamaindex.ai/python/framework/understanding/rag/indexing/) (article)
- [Vector Databases Simply Explained! (Embeddings & Indexes)](https://www.youtube.com/watch?v=dN0lsF2cvm4) (video)

## References

- https://roadmap.sh/ai-engineer (Node: Indexing Embeddings)

---

[← MongoDB Atlas](/ai-engineer/04-rag-and-vector-databases/mongodb-atlas/) · [AI Engineer Roadmap](/ai-engineer/) · [Performing Similarity Search →](/ai-engineer/04-rag-and-vector-databases/performing-similarity-search/)
