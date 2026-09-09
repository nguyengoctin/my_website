---
title: "Chuyển Xubuntu sang Ubuntu Server mà không cài lại"
date: 2026-09-09T16:15:00+07:00
aliases:
  - xubuntu to ubuntu server
  - ubuntu headless
tags:
  - xubuntu
  - ubuntu-server
  - headless
  - linux
---

> Xubuntu và Ubuntu Server cùng nền Ubuntu, nên không bắt buộc phải cài lại hệ điều hành. Cách an toàn là cài bộ package `ubuntu-server`, chuyển systemd sang boot ở chế độ `multi-user.target`, kiểm tra mọi dịch vụ chạy ổn rồi mới cân nhắc gỡ XFCE.

## Cách nên làm

Cài bộ package dành cho Ubuntu Server:

```bash
sudo apt update
sudo apt install ubuntu-server
```

Đặt máy boot vào chế độ console/headless thay vì giao diện đồ họa:

```bash
sudo systemctl set-default multi-user.target
sudo reboot
```

Sau khi reboot, máy sẽ không tự khởi động desktop. Có thể quản trị qua console hoặc SSH như một server bình thường.

## Quay lại desktop khi cần

Không cần cài lại XFCE nếu trước đó chưa gỡ desktop.

```bash
sudo systemctl set-default graphical.target
sudo reboot
```

Đây là lý do nên **tắt GUI trước, chưa gỡ XFCE ngay**: dễ rollback nếu Wi-Fi, SSH, Docker hoặc dịch vụ nào đó gặp vấn đề.

## Khi nào nên gỡ Xubuntu/XFCE

Chỉ nên dọn desktop sau khi đã dùng headless một thời gian và xác nhận các dịch vụ cần thiết chạy ổn.

Kiểm tra các package Xubuntu đang có:

```bash
dpkg -l | grep xubuntu
```

Có thể bắt đầu bằng việc gỡ các metapackage:

```bash
sudo apt remove xubuntu-desktop xubuntu-desktop-minimal
```

### Cảnh báo với autoremove

Không chạy mù quáng:

```bash
sudo apt autoremove --purge
```

`autoremove` có thể đề xuất xóa nhiều dependency không còn được đánh dấu là cần thiết. Luôn đọc kỹ danh sách package mà APT chuẩn bị xóa trước khi xác nhận.

Nếu mục tiêu chính chỉ là tiết kiệm RAM/CPU và chạy máy như server thì **không nhất thiết phải gỡ XFCE**. Khi `multi-user.target` là default, desktop không tự chạy nên phần lớn tài nguyên của GUI không được sử dụng.

## Quy trình chuyển đổi khuyến nghị

1. Đảm bảo SSH đang hoạt động và có thể đăng nhập từ máy khác.
2. Chạy:

   ```bash
   sudo apt update
   sudo apt install ubuntu-server
   ```

3. Chuyển default target:

   ```bash
   sudo systemctl set-default multi-user.target
   ```

4. Reboot và kiểm tra lại SSH, network, Docker và các service cần thiết.
5. Dùng máy ở chế độ headless một thời gian.
6. Chỉ khi chắc chắn không cần GUI nữa mới gỡ các package Xubuntu/XFCE.

## Những thứ không tự mất khi chuyển sang headless

Việc đổi systemd target không format ổ đĩa và không biến máy thành một installation mới. Vì vậy các thành phần đã cấu hình như:

- mount point và dữ liệu trên `/data`;
- Docker/container;
- SSH;
- Cloudflare Tunnel;
- file cấu hình và dữ liệu người dùng;

không bị xóa chỉ vì đổi từ `graphical.target` sang `multi-user.target`.

Tuy nhiên, việc **gỡ package** sau đó là một thao tác khác và có thể ảnh hưởng dependency, vì vậy cần kiểm tra danh sách package trước khi xác nhận.

## Kết luận

Với một máy Xubuntu đang được chuyển thành home server, lựa chọn ít rủi ro nhất là:

```text
Xubuntu hiện tại
→ cài ubuntu-server
→ multi-user.target
→ kiểm tra server
→ chỉ gỡ XFCE nếu thực sự cần
```

Không cần cài lại Ubuntu Server từ đầu chỉ để có một máy headless.
