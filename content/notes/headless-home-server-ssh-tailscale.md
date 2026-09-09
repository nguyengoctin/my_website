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

> Mô hình đơn giản cho home server cá nhân là dùng SSH để quản trị Linux, Tailscale để kết nối qua Internet mà không public port 22, và SSH key để xác thực. Khi server reboot không màn hình mà vẫn tự lên mạng, Tailscale và SSH rồi truy cập lại được, nó mới thực sự headless-ready.

## Kiến trúc

```text
Laptop
   │ SSH
   ▼
Tailscale private network
   │
   ▼
Mac mini / Linux home server
```

Trong LAN có thể SSH bằng private IP. Khi ra ngoài nhà, dùng Tailscale. Nếu MagicDNS hoạt động:

```bash
ssh <user>@macmini
```

## Trình tự setup

```text
1. Linux boot ổn định
2. OpenSSH server
3. Test SSH trong LAN
4. Tailscale trên server
5. Tailscale trên client
6. Test SSH qua Tailscale
7. SSH key trên client
8. Copy public key sang server
9. Test key authentication
10. Reboot headless
11. Test SSH lại
12. Test từ mạng Internet khác
13. Sau đó mới harden thêm
```

## OpenSSH server

```bash
sudo apt update
sudo apt install openssh-server
sudo systemctl enable --now ssh
```

Kiểm tra:

```bash
systemctl is-enabled ssh
systemctl is-active ssh
```

Mong muốn:

```text
enabled
active
```

Xem LAN IP:

```bash
hostname -I
```

Test từ client:

```bash
ssh <user>@<server-lan-ip>
```

## Vì sao LAN IP không đủ

`192.168.x.x`, `10.x.x.x` và dải private tương tự không tự route từ Internet. Setup này chọn Tailscale thay vì port-forward TCP/22 ra public Internet.

## Tailscale

Nếu thiếu curl:

```bash
sudo apt update
sudo apt install curl
```

Cài theo installer chính thức:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

Khởi tạo:

```bash
sudo tailscale up
```

Đăng nhập server và client vào cùng tailnet.

Kiểm tra:

```bash
tailscale status
tailscale ip -4
```

Có thể SSH bằng:

```bash
ssh <user>@<tailscale-ip>
```

hoặc với MagicDNS:

```bash
ssh <user>@macmini
```

SSH bằng hostname qua Tailscale đã hoạt động trong setup thực tế.

## SSH host key

Lần đầu kết nối, SSH có thể yêu cầu xác nhận ED25519 host fingerprint. Trong môi trường quan trọng, không nên nhấn `yes` một cách máy móc.

Nếu cùng server từng được truy cập qua địa chỉ khác, fingerprint nhất quán là một tín hiệu hữu ích để xác nhận cùng SSH host.

Bản public không cần chứa fingerprint thật của server nếu không có use case phân phối fingerprint.

## SSH key trên client

Tạo trên laptop/client:

```bash
ssh-keygen -t ed25519 -C "<client-name>"
```

Mặc định:

```text
~/.ssh/id_ed25519      → private key
~/.ssh/id_ed25519.pub  → public key
```

Private key phải giữ bí mật. Public key được phép copy sang server.

Với laptop thường mang ra ngoài, đặt passphrase cho private key là lựa chọn hợp lý.

## Copy public key sang server

```bash
ssh-copy-id <user>@macmini
```

hoặc:

```bash
ssh-copy-id <user>@<tailscale-ip>
```

Sau đó mở connection mới:

```bash
ssh <user>@macmini
```

Chỉ sau khi key login thực sự hoạt động mới cân nhắc thay đổi password authentication.

## Host key và user key khác nhau

```text
SSH host key:
client dùng để xác minh server

SSH user authentication key:
server dùng để xác minh client/user
```

Hai fingerprint không cần giống nhau.

## Headless verification

```bash
systemctl is-enabled ssh
systemctl is-active ssh
systemctl is-enabled tailscaled
systemctl is-active tailscaled
```

Mong muốn cả hai service đều `enabled` và `active`.

Reboot từ xa:

```bash
sudo reboot
```

Sau khi máy boot lại, không cần cắm màn hình/bàn phím chỉ để hỗ trợ boot. Từ client:

```bash
ssh <user>@macmini
```

Nếu vào được, chuỗi quan trọng đã được kiểm chứng:

```text
Power on
→ Linux boot
→ Network
→ tailscaled
→ sshd
→ Remote SSH
```

## Test từ ngoài LAN

Để test đúng use case:

```text
Server: giữ ở mạng nhà
Laptop: chuyển sang hotspot điện thoại hoặc mạng khác
```

Rồi:

```bash
ssh <user>@macmini
```

SSH qua Tailscale đã được xác minh trong setup; external-network test nên được xem là verification riêng nếu chưa thực hiện.

## Không cần public port 22

Kiến trúc:

```text
SSH → Tailscale → private overlay network
```

thay cho:

```text
Internet → router TCP/22 → sshd
```

Với server chỉ dành cho user/device trong tailnet, không cần port-forward SSH chỉ để remote administration.

## Thứ nào là secret?

Thường không phải credential:

```text
private LAN IP
Tailscale device IP
hostname
SSH public key
```

Phải bảo vệ:

```text
SSH private key
password
Tailscale auth key
Tailscale API/access token
recovery credentials
```

Khi publish, nên sanitize username thật, IP cụ thể, SSH fingerprint, filesystem UUID và home-directory path nếu chúng không giúp người đọc.

## Commands vận hành

```bash
ssh <user>@macmini
tailscale status
uptime
free -h
df -h
hostname -I
sudo reboot
sudo poweroff
```

Thoát SSH:

```bash
exit
```

## Hardening: đừng làm quá sớm

Thứ tự an toàn:

```text
1. Giữ session hiện tại mở
2. Copy public key
3. Mở session mới
4. Xác minh key login
5. Reboot
6. Xác minh key login lại
7. Đảm bảo recovery path
8. Sau đó mới cân nhắc hardening sshd
```

Không tự khóa mình khỏi server chỉ để đạt một checklist security.

## Bước tiếp theo

Sau khi remote/headless ổn định:

```text
1. Inspect HDD trong máy
2. Backup dữ liệu cần giữ
3. Quyết định filesystem/mount
4. Mount HDD thành /data
5. Cài Docker
6. Deploy từng service
7. Backup
8. Theo dõi resource/storage
9. Review security theo services thực sự expose
```

## Checklist

```text
[ ] Linux boot ổn định
[ ] ssh enabled + active
[ ] SSH qua LAN
[ ] Tailscale trên server/client
[ ] Cùng tailnet
[ ] SSH qua Tailscale
[ ] SSH key trên client
[ ] Public key trên server
[ ] Key login trong session mới
[ ] tailscaled enabled + active
[ ] Reboot headless
[ ] SSH trở lại sau reboot
[ ] Test external network
[ ] Chỉ harden sau khi có recovery path
```

## Nguồn

- Tailscale Linux installation: https://tailscale.com/download/linux
- OpenSSH: https://www.openssh.com/
