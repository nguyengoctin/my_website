---
title: "CAP Theorem"
description: "CAP Theorem states distributed systems can only guarantee two of three properties: Consistency (same data across nodes), Availability (system responds to requests), and Partition tolerance (operates despite network failures)."
summary: "Định lý CAP phát biểu rằng các hệ thống phân tán chỉ có thể đảm bảo hai trong ba thuộc tính: Tính nhất quán (dữ liệu giống nhau trên các nút), Tính sẵn sàng (hệ thống phản hồi các yêu cầu), và Khả năng chịu phân vùng (hoạt động bất chấp lỗi mạng)."
slug: "cap-theorem"
date: 2026-08-01
weight: 129
next: "/backend/21-scaling-databases/scaling-databases/"
prev: "/backend/20-real-time-data/sharding-strategies/"
draft: false


tags:
  - Backend

toc: true
math: false
mermaid: false
---

**CAP Theorem states | distributed systems can only guarantee | two of three properties:**  
*Định lý CAP phát biểu rằng | các hệ thống phân tán chỉ có thể đảm bảo | hai trong ba thuộc tính:*

**Consistency (same data across nodes), | Availability (system responds to requests), | and Partition tolerance**  
*Tính nhất quán (dữ liệu giống nhau trên các nút), | Tính sẵn sàng (hệ thống phản hồi các yêu cầu), | và Khả năng chịu phân vùng*

**(operates despite network failures). | Guides distributed system design decisions | and database selection.**  
*(hoạt động bất chấp lỗi mạng). | Hướng dẫn các quyết định thiết kế hệ thống phân tán | và lựa chọn cơ sở dữ liệu.*

## Resources

- [What is CAP Theorem?](https://www.bmc.com/blogs/cap-theorem/) (article)
- [An Illustrated Proof of the CAP Theorem](https://mwhittaker.github.io/blog/an_illustrated_proof_of_the_cap_theorem/) (article)
- [CAP Theorem and its applications in NoSQL Databases](https://www.ibm.com/uk-en/cloud/learn/cap-theorem) (article)
- [What is CAP Theorem?](https://www.youtube.com/watch?v=_RbsFXWRZ10) (video)

## References

- https://roadmap.sh/backend (Node: CAP Theorem)

---

[← Sharding Strategies](/backend/20-real-time-data/sharding-strategies/) · [Backend Roadmap](/backend/) · [Scaling Databases →](/backend/21-scaling-databases/scaling-databases/)
