---
title: "Long Polling"
description: "Long polling technique where server holds client requests instead of sending empty responses."
summary: "Kỹ thuật Long polling nơi máy chủ giữ các yêu cầu của máy khách thay vì gửi các phản hồi trống."
slug: "long-short-polling"
date: 2026-08-01
weight: 127
next: "/backend/20-real-time-data/sharding-strategies/"
prev: "/backend/20-real-time-data/data-replication/"
draft: false


tags:
  - Backend

toc: true
math: false
mermaid: false
---

**Long polling technique | where server holds | client requests**  
*Kỹ thuật Long polling | nơi máy chủ giữ | các yêu cầu của máy khách*

**instead of sending | empty responses. | Server waits for specified period**  
*thay vì gửi | các phản hồi trống. | Máy chủ chờ trong một khoảng thời gian xác định*

**for new data, | responding immediately when available | or after timeout.**  
*cho dữ liệu mới, | phản hồi ngay lập tức khi có sẵn | hoặc sau khi hết thời gian chờ.*

**Client then immediately re-requests, | creating continuous | request-response cycles.**  
*Máy khách sau đó yêu cầu lại ngay lập tức, | tạo ra các chu kỳ | request-response liên tục.*

## Resources

- [Long Polling](https://javascript.info/long-polling) (article)
- [What is Long Polling?](https://www.youtube.com/watch?v=LD0_-uIsnOE) (video)

## References

- https://roadmap.sh/backend (Node: Long / Short Polling)

---

[← Data Replication](/backend/20-real-time-data/data-replication/) · [Backend Roadmap](/backend/) · [Sharding Strategies →](/backend/20-real-time-data/sharding-strategies/)
