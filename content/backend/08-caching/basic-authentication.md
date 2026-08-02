---
title: "Basic authentication"
description: "Basic Authentication sends base64-encoded username:password in HTTP headers."
summary: "Basic Authentication gửi username:password được mã hóa base64 trong các HTTP header."
slug: "basic-authentication"
date: 2026-08-01
weight: 46
next: "/backend/08-caching/nginx/"
prev: "/backend/08-caching/caching/"
draft: false


tags:
  - Backend

toc: true
math: false
mermaid: false
---

**Basic Authentication sends | base64-encoded username:password | in HTTP headers.**  
*Basic Authentication gửi | username:password được mã hóa base64 | trong các HTTP header.*

**Simple to implement | but insecure since | base64 is easily decoded.**  
*Đơn giản để triển khai | nhưng không an toàn vì | base64 rất dễ bị giải mã.*

**Should only be used | over HTTPS | for credential protection.**  
*Chỉ nên được sử dụng | qua HTTPS | để bảo vệ thông tin đăng nhập.*

**Best for low-risk scenarios | or fallback mechanisms.**  
*Tốt nhất cho các kịch bản rủi ro thấp | hoặc các cơ chế dự phòng.*

## Resources
- [HTTP Basic Authentication](https://roadmap.sh/guides/http-basic-authentication) (article)
- [Basic Authentication in 5 minutes](https://www.youtube.com/watch?v=rhi1eIjSbvk) (video)
- [Illustrated HTTP Basic Authentication](https://www.youtube.com/watch?v=mwccHwUn7Gc) (video)

## References
- https://roadmap.sh/backend (Node: [label])

---

[← Caching](/backend/08-caching/caching/) · [Backend Roadmap](/backend/) · [Nginx →](/backend/08-caching/nginx/)
