---
title: "Connect to Local Server"
description: "A Local Desktop deployment means running the MCP server directly on your own computer instead of a remote cloud or server."
summary: "Triển khai trên máy tính cục bộ có nghĩa là chạy máy chủ MCP trực tiếp trên máy tính của bạn thay vì đám mây."
slug: "connect-to-local-server"
date: 2026-08-01
weight: 94
next: "/ai-engineer/07-model-context-protocol-mcp/connect-to-remote-server/"
prev: "/ai-engineer/07-model-context-protocol-mcp/building-an-mcp-client/"
draft: false


tags:
  - MCP
  - Local Server

toc: true
math: false
mermaid: false
---

**A Local Desktop deployment | means running the | MCP server directly on | your own computer instead | of a remote cloud | or server.**  
*Triển khai trên máy tính cục bộ | có nghĩa là chạy | máy chủ MCP trực tiếp trên | máy tính của riêng bạn thay vì | một đám mây từ xa | hoặc máy chủ.*

**You install the | MCP software, needed runtimes, | and model files onto | your desktop or laptop.**  
*Bạn cài đặt | phần mềm MCP, các runtime cần thiết, | và các tệp mô hình lên | máy tính để bàn hoặc máy tính xách tay của bạn.*

**The server then listens | on a local address | like 127.0.0.1:8000, | accessible only from the | same machine unless you | open ports manually.**  
*Máy chủ sau đó lắng nghe | trên một địa chỉ cục bộ | như 127.0.0.1:8000, | chỉ có thể truy cập từ | cùng một máy trừ khi bạn | mở các cổng theo cách thủ công.*

**This setup is great | for fast tests, personal | demos, or private experiments | since you keep full | control and avoid | cloud costs.**  
*Thiết lập này rất tuyệt | cho các bài kiểm tra nhanh, | demo cá nhân, hoặc các thử nghiệm riêng tư | vì bạn giữ toàn quyền | kiểm soát và tránh | các chi phí đám mây.*

**However, it's limited by | your hardware's speed and | memory, and others cannot | access it without tunneling | tools like ngrok or | local port forwarding.**  
*Tuy nhiên, nó bị giới hạn bởi | tốc độ và bộ nhớ | phần cứng của bạn, và người khác không thể | truy cập nó nếu không có các công cụ | tunneling như ngrok hoặc | chuyển tiếp cổng cục bộ.*

## Resources
- [Connect to local MCP servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers) (official)
- [How to Build and Host Your Own MCP Servers in Easy Steps](ttps://collabnix.com/how-to-build-and-host-your-own-mcp-servers-in-easy-steps/) (article)
- [Local MCP Servers for Cursor (Step by step)](https://www.youtube.com/watch?v=_Qr0WTgR5EM) (video)

## References

- https://roadmap.sh/ai-engineer (Node: Connect to Local Server)

---

[← Building an MCP Client](/ai-engineer/07-model-context-protocol-mcp/building-an-mcp-client/) · [AI Engineer Roadmap](/ai-engineer/) · [Connect to Remote Server →](/ai-engineer/07-model-context-protocol-mcp/connect-to-remote-server/)
