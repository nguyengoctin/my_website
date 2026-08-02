---
title: "Circuit Breaker"
description: "Circuit breaker pattern protects systems from failures by temporarily stopping operations when overloaded."
summary: "Mẫu Circuit breaker bảo vệ các hệ thống khỏi lỗi bằng cách tạm thời dừng các hoạt động khi bị quá tải."
slug: "circuit-breaker"
date: 2026-08-01
weight: 155
prev: "/backend/23-building-for-scale/scylladb/"
draft: false

categories:
  - Backend

tags:
  - Backend

toc: true
math: false
mermaid: false
---

**Circuit breaker pattern | protects systems from failures | by temporarily stopping operations | when overloaded.**  
*Mẫu Circuit breaker | bảo vệ các hệ thống khỏi lỗi | bằng cách tạm thời dừng các hoạt động | khi bị quá tải.*

**Has three states: | closed (normal), | open (stopped operations), | and half-open (testing recovery).**  
*Có ba trạng thái: | đóng (bình thường), | mở (đã dừng hoạt động), | và nửa mở (đang kiểm tra phục hồi).*

**Prevents cascading failures | in distributed systems.**  
*Ngăn chặn các lỗi dây chuyền | trong các hệ thống phân tán.*

## Resources

- [Circuit Breaker - Azure Architecture Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) (official)
- [Resilience4j - Circuit Breaker Library for Java](https://github.com/resilience4j/resilience4j) (opensource)
- [The Circuit Breaker Pattern](https://aerospike.com/blog/circuit-breaker-pattern/) (article)
- [What is the Circuit Breaker Pattern?](https://www.youtube.com/watch?v=ADHcBxEXvFA) (video)

## References

- https://roadmap.sh/backend (Node: Circuit Breaker)

---

[← ScyllaDB](/backend/23-building-for-scale/scylladb/) · [Backend Roadmap](/backend/)
