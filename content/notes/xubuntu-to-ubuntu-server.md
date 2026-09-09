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

> Xubuntu và Ubuntu Server cùng nền Ubuntu — không bắt buộc phải cài lại để có một máy headless. Cách an toàn là cài bộ package `ubuntu-server`, đổi systemd default target sang `multi-user.target`, kiểm tra mọi dịch vụ chạy ổn sau reboot, rồi mới cân nhắc gỡ XFCE. Thứ tự này cho phép rollback nhanh nếu có vấn đề.

## 1. Bản chất

Trên Linux, "server mode" và "desktop mode" không phải hai hệ điều hành khác nhau — chúng chỉ khác nhau ở **systemd default target**:

```text
graphical.target   → khởi động display manager, load GNOME/XFCE...
multi-user.target  → khởi động network, SSH, system services — không load GUI
```

Ubuntu Server và Xubuntu đều dùng systemd. Chuyển default target là cách chuyển đổi giữa hai chế độ mà không cần reinstall, không mất dữ liệu người dùng, không xoá config đã có.

Gói `ubuntu-server` là một metapackage kéo theo các công cụ và service phổ biến cho server (như `landscape-common`, `open-vm-tools`, `unattended-upgrades`...) — nó không thay thế kernel hay filesystem.

## 2. Vì sao lựa chọn

**Tại sao không cài Ubuntu Server từ đầu?**

Trong trường hợp này Xubuntu đã được cài trên SSD với SSH, Tailscale và `/data` đều đã cấu hình xong. Cài lại từ đầu có nghĩa là làm lại toàn bộ setup đó — không có lợi ích kỹ thuật rõ ràng.

**Tại sao không chỉ tắt GUI trong settings mà phải đổi systemd target?**

Tắt GUI trong Xubuntu settings chỉ ảnh hưởng đến session hiện tại. Muốn máy không load GNOME/XFCE sau mỗi lần reboot, phải đổi default target ở tầng systemd.

**Tại sao không gỡ XFCE ngay?**

XFCE là recovery path. Nếu SSH, Wi-Fi, hay một service nào đó có vấn đề sau khi chuyển sang headless, vẫn có thể cắm màn hình và dùng GUI để debug. Gỡ XFCE trước khi chắc chắn mọi thứ chạy ổn là đánh đổi recovery ability lấy vài trăm MB disk — không đáng.

**Đánh đổi:**

- Giữ XFCE tốn thêm ~300–500 MB disk nhưng hầu như không tốn RAM/CPU khi ở `multi-user.target` vì display manager không khởi động.

## 3. Cơ chế hoạt động

```text
systemd boot sequence với graphical.target:
  multi-user.target
        │
        ▼
  display-manager.service (LightDM/GDM)
        │
        ▼
  XFCE/GNOME session load

systemd boot sequence với multi-user.target:
  multi-user.target
        │
        ├── networking.service
        ├── sshd.service
        ├── tailscaled.service
        └── ... (các service thông thường)
        ↑
  (display-manager.service không được kéo vào)
```

`systemctl set-default` chỉ thay đổi symlink `/etc/systemd/system/default.target`:

```bash
ls -l /etc/systemd/system/default.target
# graphical.target → /lib/systemd/system/graphical.target
# sau set-default multi-user.target:
# multi-user.target → /lib/systemd/system/multi-user.target
```

## 4. Hướng dẫn từng bước

### Bước 1 — Đảm bảo SSH hoạt động trước

Đây là điều kiện tiên quyết. Sau khi chuyển sang headless, nếu SSH không lên thì không còn cách truy cập máy từ xa.

```bash
systemctl is-enabled ssh
systemctl is-active ssh
# Cả hai phải trả về: enabled / active
```

Nếu chưa cài:

```bash
sudo apt install openssh-server
sudo systemctl enable --now ssh
# enable --now → bật service ngay và đặt tự chạy khi boot
```

### Bước 2 — Cài ubuntu-server metapackage

```bash
sudo apt update
sudo apt install ubuntu-server
# ubuntu-server là metapackage, không thay thế kernel
# nó kéo theo các package tiện ích phổ biến cho server
```

### Bước 3 — Đổi default target

```bash
sudo systemctl set-default multi-user.target
# set-default → ghi đè symlink /etc/systemd/system/default.target
```

Kiểm tra:

```bash
systemctl get-default
# Kỳ vọng: multi-user.target
```

### Bước 4 — Reboot và xác minh

```bash
sudo reboot
```

Sau khi máy lên, từ laptop SSH vào:

```bash
ssh <user>@macmini
```

Nếu vào được, headless thành công. Kiểm tra các service cần thiết:

```bash
systemctl is-active ssh
systemctl is-active tailscaled
findmnt /data
```

### Rollback về desktop khi cần

```bash
sudo systemctl set-default graphical.target
sudo reboot
# Nếu XFCE chưa bị gỡ, desktop sẽ load bình thường
```

### Bước 5 — Gỡ XFCE (chỉ khi đã chắc chắn)

Chỉ làm sau khi dùng headless ổn định ít nhất vài ngày:

```bash
dpkg -l | grep xubuntu
# Liệt kê các package xubuntu đang có
```

Gỡ metapackage:

```bash
sudo apt remove xubuntu-desktop xubuntu-desktop-minimal
```

Trước khi chạy autoremove, đọc kỹ danh sách sẽ bị xoá:

```bash
apt-get --dry-run autoremove
# --dry-run (hoặc -s) → chỉ mô phỏng, không thực sự xoá
# Đọc kỹ list trước khi xác nhận
```

Nếu danh sách chấp nhận được:

```bash
sudo apt autoremove --purge
# --purge → xoá cả config file của package, không chỉ binary
```

## 5. Bẫy lỗi và Những lần thử thất bại

**Bẫy 1 — Gỡ XFCE trước khi xác minh headless ổn định**

Sau khi gỡ XFCE, nếu SSH có vấn đề (VD: Tailscale chưa lên kịp sau boot, IP đổi...) thì không còn giao diện local để debug. Phải cắm màn hình và thấy màn hình đen hoặc login console — mất thêm thời gian tìm bàn phím, monitor...

**Bẫy 2 — Chạy `apt autoremove --purge` mà không đọc danh sách**

`autoremove` có thể đề xuất gỡ các package không còn được đánh dấu là required nhưng thực ra vẫn cần — VD: một library mà script thủ công đang dùng. Luôn chạy `--dry-run` trước.

**Bẫy 3 — Giả định `multi-user.target` không load bất kỳ GUI nào**

`multi-user.target` chỉ không load display manager. Nếu có service nào đó manually enable mà depends vào X11 hoặc DBUS session, nó vẫn có thể được kéo vào. Cần kiểm tra `systemctl list-units --state=failed` sau reboot.

## 6. Kiểm tra và Xác minh

Sau khi reboot sang `multi-user.target`:

```bash
systemctl get-default
# Kỳ vọng: multi-user.target

ps aux | grep -E 'lightdm|gdm|xfce'
# Không nên thấy display manager hay XFCE process nào đang chạy

systemctl list-units --state=failed
# Kiểm tra có service nào fail không — đặc biệt quan trọng sau lần đổi target đầu tiên

free -h
# So sánh RAM usage trước/sau — headless thường tiết kiệm 200-400MB
```

Xác minh các service cốt lõi vẫn chạy:

```bash
systemctl is-active ssh tailscaled
# Kỳ vọng: active active

findmnt /data
# Kỳ vọng: /data mount đúng HDD
```

## 7. Nguồn tham khảo

- systemd documentation — systemctl set-default: https://www.freedesktop.org/software/systemd/man/systemctl.html  
  *(giải thích đầy đủ về targets và symlink default.target)*
- Ubuntu manpage — `ubuntu-server` package: `apt show ubuntu-server`  
  *(xem dependencies thực tế của metapackage)*
- Debian/Ubuntu wiki về `multi-user.target` vs `graphical.target`: https://wiki.debian.org/systemd  
  *(background về systemd targets trên Debian-based distro)*
