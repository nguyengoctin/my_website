---
title: "Chuyển Xubuntu sang chế độ headless và bổ sung bộ package Ubuntu Server"
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

> [!TLDR]
> Không cần cài lại chỉ để biến một Xubuntu đang hoạt động thành máy headless. `multi-user.target` có thể bỏ display manager khỏi boot mặc định, còn `ubuntu-server` bổ sung bộ package server. Cách này không biến installation thành một bản Ubuntu Server cài mới theo nghĩa package set và installer history; nó chỉ tạo behavior vận hành phù hợp với server trên installation hiện có.

## Bản chất

Trong installation hiện có, việc có khởi động desktop session hay không được systemd điều khiển bằng default target. Điều này không có nghĩa Xubuntu và Ubuntu Server chỉ khác nhau ở target; hai flavor còn khác package set và default configuration. Với mục tiêu headless, target mới là phần cần thay đổi trực tiếp:

```text
graphical.target   → khởi động display manager, load GNOME/XFCE...
multi-user.target  → khởi động network, SSH, system services — không load GUI
```

Ubuntu Server và Xubuntu đều dùng systemd. Đổi default target thay đổi boot behavior của installation hiện tại mà không reinstall hay xóa dữ liệu người dùng.

`ubuntu-server` là một metapackage của Ubuntu để kéo theo bộ package server. Dependency và recommendation cụ thể phụ thuộc release và APT policy; có thể kiểm tra bằng `apt show ubuntu-server` trước khi cài. Metapackage này không thay filesystem hiện có và cũng không tự gỡ desktop stack.

## Vì sao lựa chọn

**Tại sao không cài Ubuntu Server từ đầu?**

Trong trường hợp này Xubuntu đã được cài trên SSD với SSH, Tailscale và `/data` đều đã cấu hình xong. Cài lại từ đầu có nghĩa là làm lại toàn bộ setup đó — không có lợi ích kỹ thuật rõ ràng.

**Tại sao không chỉ tắt GUI trong settings mà phải đổi systemd target?**

Đặt `multi-user.target` làm default là cách explicit để boot vào multi-user system mà không kéo `graphical.target` làm target mặc định. Đây là thay đổi ở boot policy, không phụ thuộc vào một desktop-session preference.

**Tại sao không gỡ XFCE ngay?**

XFCE là recovery path. Nếu SSH, Wi-Fi, hay một service nào đó có vấn đề sau khi chuyển sang headless, vẫn có thể cắm màn hình và dùng GUI để debug. Gỡ XFCE trước khi chắc chắn remote access và network đã ổn sẽ làm mất một recovery path thuận tiện. Nếu dung lượng chưa phải vấn đề, giữ desktop package trong giai đoạn chuyển đổi giúp rollback dễ hơn.

**Đánh đổi:**

- Giữ XFCE chiếm thêm disk và package maintenance. Khi `multi-user.target` là default và display manager không được khởi động, desktop session không chạy như ở `graphical.target`.

## Cơ chế hoạt động

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

## Hướng dẫn từng bước

### Bước 1 — Đảm bảo SSH hoạt động trước

Đây là điều kiện tiên quyết cho remote administration. Sau khi chuyển sang headless, nếu SSH hoặc network không lên thì remote access sẽ mất và cần local console hoặc một recovery path khác.

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
ssh <user>@<server-hostname>
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

## Bẫy lỗi và Những lần thử thất bại

**Bẫy 1 — Gỡ XFCE trước khi xác minh headless ổn định**

Sau khi gỡ XFCE, nếu SSH có vấn đề (VD: Tailscale chưa lên kịp sau boot, IP đổi...) thì không còn giao diện local để debug. Phải cắm màn hình và thấy màn hình đen hoặc login console — mất thêm thời gian tìm bàn phím, monitor...

**Bẫy 2 — Chạy `apt autoremove --purge` mà không đọc danh sách**

`autoremove` có thể đề xuất gỡ các package không còn được đánh dấu là required nhưng thực ra vẫn cần — VD: một library mà script thủ công đang dùng. Luôn chạy `--dry-run` trước.

**Bẫy 3 — Giả định `multi-user.target` không load bất kỳ GUI nào**

`multi-user.target` chỉ không load display manager. Nếu có service nào đó manually enable mà depends vào X11 hoặc DBUS session, nó vẫn có thể được kéo vào. Cần kiểm tra `systemctl list-units --state=failed` sau reboot.

## Kiểm tra và Xác minh

Sau khi reboot sang `multi-user.target`:

```bash
systemctl get-default
# Kỳ vọng: multi-user.target

ps aux | grep -E 'lightdm|gdm|xfce'
# Không nên thấy display manager hay XFCE process nào đang chạy

systemctl list-units --state=failed
# Kiểm tra có service nào fail không — đặc biệt quan trọng sau lần đổi target đầu tiên

free -h
# So sánh RAM usage trước/sau trên chính máy này nếu cần measurement
```

Xác minh các service cốt lõi vẫn chạy:

```bash
systemctl is-active ssh tailscaled
# Kỳ vọng: active active

findmnt /data
# Kỳ vọng: /data mount đúng HDD
```

## Nguồn tham khảo

- [systemd documentation — systemctl set-default](https://www.freedesktop.org/software/systemd/man/systemctl.html)  
  *(giải thích đầy đủ về targets và symlink default.target)*
- [`ubuntu-server` package trên Ubuntu 26.04](https://packages.ubuntu.com/resolute/ubuntu-server)  
  *(xem dependency và recommendation của metapackage theo release)*
- [Debian/Ubuntu wiki về `multi-user.target` vs `graphical.target`](https://wiki.debian.org/systemd)  
  *(background về systemd targets trên Debian-based distro)*
