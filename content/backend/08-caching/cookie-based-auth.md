---
title: "Cookie-Based Authentication"
description: "Cookie-based authentication maintains user sessions by storing session IDs in browser cookies."
summary: "Xác thực dựa trên cookie duy trì các phiên người dùng bằng cách lưu trữ ID phiên trong cookie của trình duyệt."
slug: "cookie-based-auth"
date: 2026-08-01
weight: 53
next: "/backend/08-caching/memcached/"
prev: "/backend/08-caching/ms-iis/"
draft: false

categories:
  - Backend

tags:
  - Backend

toc: true
math: false
mermaid: false
---

**Cookie-based authentication maintains | user sessions by storing | session IDs in browser cookies.**  
*Xác thực dựa trên cookie duy trì | các phiên người dùng bằng cách lưu trữ | ID phiên trong cookie của trình duyệt.*

**Server stores session data | and uses cookies | as keys.**  
*Máy chủ lưu trữ dữ liệu phiên | và sử dụng cookie | làm khóa.*

**Simple to implement | and browser-native, | but vulnerable to CSRF attacks**  
*Đơn giản để triển khai | và là tính năng gốc của trình duyệt, | nhưng dễ bị tấn công CSRF*

**and challenging for | cross-origin requests.**  
*và đầy thách thức đối với | các yêu cầu cross-origin.*

## Resources
- [HTTP Cookies - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies) (official)
- [Session vs Token Authentication](https://www.section.io/engineering-education/token-based-vs-session-based-authentication/) (article)
- [Session vs Token Authentication in 100 Seconds](https://www.youtube.com/watch?v=UBUNrFtufWo) (video)
- [How do cookies work?](https://www.youtube.com/watch?v=rdVPflECed8) (video)

## References
- https://roadmap.sh/backend (Node: [label])

---

[← MS IIS](/backend/08-caching/ms-iis/) · [Backend Roadmap](/backend/) · [Memcached →](/backend/08-caching/memcached/)
