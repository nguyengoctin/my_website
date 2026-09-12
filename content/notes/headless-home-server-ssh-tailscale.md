---
title: "Biến Mac mini thành home server headless với SSH và Tailscale"
date: 2026-09-09T15:20:00+07:00
aliases:
  - Headless home server
  - SSH Tailscale
tags:
  - mac-mini
  - home-server
  - ssh
  - tailscale
  - headless
---

> [!TLDR]
> Mô hình home server cá nhân đơn giản nhất là SSH để quản trị, Tailscale để kết nối từ Internet mà không public port 22, và SSH key để xác thực. Server chỉ thực sự "headless-ready" khi sau reboot — không cắm màn hình, không cắm bàn phím — vẫn SSH vào được từ xa.

## 1. Bản chất

**SSH (Secure Shell)** là giao thức cho phép điều khiển từ xa một máy Linux qua terminal có mã hoá. Với home server, SSH là giao diện quản trị chính — không cần màn hình hay bàn phím cắm trực tiếp.

**Tailscale** là VPN mesh dựa trên WireGuard, tạo một private overlay network (tailnet) giữa các thiết bị. Thay vì public port 22 ra Internet, SSH đi qua tunnel Tailscale — thiết bị ngoài tailnet không thể kết nối.

**SSH key authentication** thay thế password bằng cặp public/private key. Private key giữ trên client, public key đặt trên server. Server chỉ cho phép kết nối từ client có private key khớp với public key đã đăng ký.

Kiến trúc:

```text
Laptop (client)
    │ SSH qua Tailscale private network
    ▼
Mac mini / Linux home server
    │ sshd chạy trên port 22 (không public)
    │ tailscaled kết nối vào tailnet
    ▼
Tailscale relay / DERP (nếu cần)
```

## 2. Vì sao lựa chọn

**Tại sao Tailscale thay vì port-forward TCP/22 trên router?**

Public SSH trên port 22 nghĩa là toàn bộ Internet có thể thử kết nối — bot scan liên tục, brute-force password, khai thác zero-day SSH. Dù có SSH key và disabled password auth, attack surface vẫn rộng hơn cần thiết. Tailscale thu nhỏ attack surface xuống chỉ còn thiết bị trong tailnet.

Port-forward cũng đòi hỏi biết public IP nhà (thay đổi nếu ISP dùng dynamic IP) và không hoạt động khi laptop đang cùng mạng LAN với server (NAT loopback không phải router nào cũng hỗ trợ).

**Tại sao SSH key thay vì password?**

Password có thể bị brute-force. SSH key với Ed25519 về lý thuyết không thể brute-force trong thời gian thực tế. Với passphrase trên private key, kể cả ai đó có file key cũng không dùng được nếu không biết passphrase.

**Đánh đổi:**

- Tailscale free tier giới hạn số device và tính năng (ACL phức tạp, subnet router...). Với home server cá nhân thông thường, free tier đủ dùng.
- Tailscale là centralized control plane — nếu Tailscale service có sự cố, không thể kết nối thiết bị dù đã trong cùng LAN. Giải pháp: giữ LAN SSH làm fallback.

## 3. Cơ chế hoạt động

```text
Kết nối SSH qua Tailscale:

Laptop                          Mac mini
  │                               │
  │── tailscaled ──────── tailscaled
  │   (trong tailnet)     (trong tailnet)
  │                               │
  │ ssh user@macmini              │
  │ ─────────────────────────────►│
  │ (Tailscale MagicDNS           │
  │  resolve "macmini"            │
  │  thành Tailscale IP)          │
  │                               │
  │◄─────────────────────────────►│
  │        SSH tunnel             │
```

Xác thực SSH key:

```text
Client có private key           Server có public key
        │                               │
        │── SSH handshake ─────────────►│
        │                               │ Server tạo challenge
        │◄─── challenge ────────────────│
        │                               │
        │ Client ký challenge bằng private key
        │── signature ─────────────────►│
        │                               │ Server verify bằng public key
        │◄─── access granted ───────────│
```

Khác biệt giữa host key và user key:

```text
SSH host key:  client dùng để xác minh danh tính server
               → tránh bị MITM, fingerprint xuất hiện khi lần đầu kết nối

SSH user key:  server dùng để xác minh danh tính người dùng
               → thay thế password authentication
```

Hai fingerprint này độc lập nhau và không cần trùng nhau.

## 4. Hướng dẫn từng bước

### Bước 1 — Cài và bật OpenSSH Server trên server (Mac mini)

```bash
sudo apt update
sudo apt install openssh-server
sudo systemctl enable --now ssh
# enable     → đặt service tự khởi động khi boot
# --now      → khởi động service ngay lập tức (không cần reboot)
```

Kiểm tra:

```bash
systemctl is-enabled ssh
systemctl is-active ssh
# Kỳ vọng: enabled / active
```

Xem LAN IP:

```bash
hostname -I
# In tất cả IP của máy, lấy IP dạng 192.168.x.x hoặc 10.x.x.x
```

Test từ laptop qua LAN:

```bash
ssh <user>@<server-lan-ip>
```

### Bước 2 — Cài Tailscale trên server

```bash
# Cài curl nếu chưa có
sudo apt install curl

# Cài Tailscale qua installer chính thức
curl -fsSL https://tailscale.com/install.sh | sh
# -f → fail silently on server errors (không tạo file rỗng)
# -s → silent mode
# -S → hiện lỗi khi -s được dùng
# -L → follow redirect
```

Đăng nhập vào tailnet:

```bash
sudo tailscale up
# Mở URL hiện ra trong browser để authenticate
```

Kiểm tra:

```bash
tailscale status
# Liệt kê các device đang online trong tailnet

tailscale ip -4
# -4 → lấy IPv4 Tailscale của thiết bị này
```

### Bước 3 — Cài Tailscale trên laptop (client)

Tải và cài theo OS tại https://tailscale.com/download, đăng nhập cùng tài khoản tailnet với server.

Test SSH qua Tailscale:

```bash
ssh <user>@<tailscale-ip>
# hoặc với MagicDNS (nếu bật):
ssh <user>@macmini
```

### Bước 4 — Tạo SSH key trên laptop

```bash
ssh-keygen -t ed25519 -C "<tên-máy-client>"
# -t ed25519  → thuật toán Ed25519 (elliptic curve, key nhỏ hơn và nhanh hơn RSA-4096)
# -C          → comment gắn vào public key, giúp identify nguồn gốc key
```

Với laptop mang ra ngoài, nên đặt passphrase khi được hỏi.

Mặc định tạo:

```text
~/.ssh/id_ed25519      → private key (giữ bí mật)
~/.ssh/id_ed25519.pub  → public key (được phép copy sang server)
```

### Bước 5 — Copy public key sang server

```bash
ssh-copy-id <user>@macmini
# Tự động append public key vào ~/.ssh/authorized_keys trên server
```

Hoặc qua Tailscale IP:

```bash
ssh-copy-id <user>@<tailscale-ip>
```

Test key authentication trong session mới (không đóng session cũ):

```bash
ssh <user>@macmini
```

Chỉ sau khi key login thực sự hoạt động mới cân nhắc tắt password authentication.

### Bước 6 — Đảm bảo headless sau reboot

Kiểm tra cả hai service đều enabled:

```bash
systemctl is-enabled ssh tailscaled
# Kỳ vọng: enabled / enabled
```

Reboot từ xa:

```bash
sudo reboot
```

Đợi máy boot xong, SSH lại:

```bash
ssh <user>@macmini
```

Nếu vào được, chuỗi headless đã hoạt động:

```text
Power on → Linux boot → Network → tailscaled → sshd → Remote SSH
```

## 5. Bẫy lỗi và Những lần thử thất bại

**Bẫy 1 — Hardening SSH trước khi có recovery path**

Tắt password authentication (`PasswordAuthentication no`) trước khi xác minh key login hoạt động trong session mới. Nếu key có vấn đề, mất khả năng SSH hoàn toàn và phải cắm màn hình để fix.

Thứ tự an toàn:
1. Giữ session hiện tại mở
2. Copy public key
3. Mở session mới — test key login
4. Reboot
5. Test key login lại sau reboot
6. Chỉ sau đó mới đổi `sshd_config`

**Bẫy 2 — Dùng Bluetooth keyboard cho lần boot đầu**

Firmware Mac mini có thể chưa kết nối Bluetooth đủ sớm trong quá trình boot để nhận phím `Option/Alt`. Kết quả: Startup Manager không hiện, Mac boot thẳng vào hệ điều hành mặc định. Phải mượn bàn phím USB cho lần đầu.

**Bẫy 3 — Nhầm SSH host key và SSH user key**

Lần đầu kết nối SSH, terminal hỏi xác nhận host fingerprint — đây là **host key**, dùng để xác minh server. Không nhầm với user key (private/public key dùng để authenticate user). Hai fingerprint không liên quan nhau.

**Bẫy 4 — Test SSH chỉ trong LAN, không test từ mạng ngoài**

SSH qua LAN hoạt động không đảm bảo SSH qua Tailscale từ mạng ngoài cũng hoạt động. Phải test đúng scenario: laptop chuyển sang hotspot điện thoại, SSH vào server.

## 6. Kiểm tra và Xác minh

```bash
# Trên server — kiểm tra service status
systemctl is-enabled ssh tailscaled
systemctl is-active ssh tailscaled
# Kỳ vọng: tất cả enabled và active

# Kiểm tra Tailscale connectivity
tailscale status
# Server và client phải thấy nhau trong danh sách

# Sau reboot — từ laptop
ssh <user>@macmini
# Kỳ vọng: vào được không cần màn hình gắn vào server

# Test ngoài LAN (laptop dùng hotspot điện thoại)
ssh <user>@macmini
# Kỳ vọng: vào được qua Tailscale
```

Checklist headless verification:

```text
[ ] ssh enabled + active trên server
[ ] tailscaled enabled + active trên server
[ ] SSH qua LAN thành công
[ ] Tailscale status thấy cả server và client
[ ] SSH qua Tailscale IP thành công
[ ] SSH key đã setup, key login hoạt động
[ ] Reboot server headless
[ ] SSH lại được sau reboot
[ ] Test từ mạng ngoài LAN
```

## 7. Nguồn tham khảo

- Tailscale Linux installation: https://tailscale.com/download/linux  
  *(script cài chính thức, luôn dùng từ đây thay vì copy script cũ từ blog)*
- OpenSSH project: https://www.openssh.com/  
  *(tài liệu chính thức về ssh, ssh-keygen, sshd_config)*
- Tailscale MagicDNS documentation: https://tailscale.com/kb/1081/magicdns  
  *(giải thích cơ chế resolve hostname trong tailnet)*
- OpenSSH man pages: `man ssh`, `man ssh-keygen`, `man sshd_config`
