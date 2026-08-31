---
title: "Bếp Dì 6: Order Snapshotting and Idempotency Architecture"
category: "features"
tags: [bep-di-6, django, postgresql, redis, idempotency, snapshotting]
created: 2026-08-31
updated: 2026-08-31
---

# Bếp Dì 6: Order Snapshotting and Idempotency Architecture

## Overview

Tài liệu ghi nhận quyết định kiến trúc và luồng xử lý giao dịch đơn hàng trong dự án Bếp Dì 6 (Zalo Mini App and Django REST Framework).

## Key Architecture Decisions

1. **Immutable Snapshotting:**
   - Khi tạo đơn hàng, bảng `OrderItem` sao chép cứng `product_name_snapshot`, `unit_price_snapshot` và `toppings_snapshot`.
   - Ngăn ngừa sai lệch dữ liệu kế toán và lịch sử tài chính khi thực đơn thay đổi giá bán.

2. **Distributed Idempotency Key:**
   - Frontend sinh UUIDv4 `Idempotency-Key` gửi kèm header.
   - Backend sử dụng Redis Distributed Lock (`SET NX EX 60`) kết hợp `transaction.atomic()` tại database.
   - Triệt tiêu lỗi tạo trùng đơn hàng khi mạng lag hoặc người dùng nhấn nút nhiều lần.
