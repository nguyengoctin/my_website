---
title: "Mac mini 2014 Home Server: Tham chiếu Setup"
date: 2026-09-09T17:00:00+07:00
aliases:
  - Mac mini home server setup
  - macmini server reference
tags:
  - home-server
  - mac-mini
  - xubuntu
  - tailscale
  - ssh
  - storage
---

> Mac mini Late 2014 đã được chuyển thành home server chạy Xubuntu. Trạng thái hiện tại: boot từ SSD Kingmax 120 GB qua USB, HDD Apple 1 TB bên trong đã format ext4 và mount tại `/data`, SSH và Tailscale hoạt động ổn định sau reboot headless. Docker chưa cài.

## 1. Bản chất

Đây là note tham chiếu trạng thái thực tế của hệ thống — không phải tutorial từ đầu. Mục đích là ghi lại những gì đã làm, lý do quyết định từng bước, và trạng thái hiện tại để tiếp tục setup.

Kiến trúc hiện tại:

```text
Mac mini Late 2014 — RAM 8 GB
│
├── Kingmax SSD 120 GB — USB
│   ├── ext4  /          (Xubuntu + system)
│   └── vfat  /boot/efi  (UEFI boot entry)
│
└── Apple HDD 1 TB — SATA nội bộ
    └── ext4  /data       (dữ liệu, Docker volumes)
```

Mục tiêu storage tiếp theo:

```text
SSD 120 GB → Xubuntu, Docker Engine, application binaries
HDD 1 TB   → /data (media, downloads, backups, Docker persistent data)
```

## 2. Vì sao lựa chọn

**Tại sao boot từ SSD ngoài (USB) thay vì dùng HDD nội bộ?**

Mac mini 2014 dùng HDD SATA 1 TB — I/O chậm cho system workload. SSD dù qua USB vẫn cải thiện hiệu năng desktop đáng kể và cho phép dùng toàn bộ HDD 1 TB làm storage dữ liệu mà không phải partition HDD theo kiểu phức tạp.

**Tại sao giữ ext4 cho HDD thay vì ZFS hay btrfs?**

Mục tiêu đơn giản: một partition ext4 duy nhất chiếm toàn bộ 1 TB, mount tại `/data`. ext4 ổn định, được Ubuntu hỗ trợ tốt, không cần RAID hay snapshot ở giai đoạn này. ZFS hoặc btrfs sẽ có giá trị hơn khi có nhiều disk và cần RAID/snapshot.

**Tại sao dùng UUID trong `/etc/fstab` thay vì `/dev/sda1`?**

Thứ tự nhận disk có thể thay đổi giữa các lần boot — đặc biệt khi có cả USB và SATA. Trong setup này, HDD từng xuất hiện là `/dev/sda1` sau đó chuyển thành `/dev/sdb1` sau reboot. UUID thuộc filesystem, không thay đổi dù device name đổi. `fstab` với UUID đảm bảo `/data` luôn mount đúng HDD bất kể thứ tự boot.

**Đánh đổi:**

- SSD qua USB có overhead hơn SSD nội bộ, nhưng với workload server thông thường (SSH, Docker, file serving) không đáng kể.
- Chỉ một disk lưu dữ liệu — không có redundancy. Nếu HDD hỏng, mất dữ liệu. Backup strategy là phần cần làm tiếp theo.

## 3. Cơ chế hoạt động

```text
Boot flow Mac mini:

Power on
    │ Giữ Option/Alt
    ▼
Apple Startup Manager
    │ Scan USB và SATA cho EFI boot entries
    ▼
Chọn "EFI Boot" (từ Kingmax SSD)
    │
    ▼
GRUB load từ /boot/efi trên SSD
    │
    ▼
Xubuntu boot từ ext4 / trên SSD
    │
    ├── tailscaled.service start
    ├── ssh.service start
    └── /data auto-mount từ fstab (UUID → HDD 1 TB)
```

```text
fstab UUID mount mechanism:

Kernel boot
    │ đọc /etc/fstab
    │ thấy entry: UUID=<xyz> /data ext4 defaults,nofail 0 2
    ▼
Kernel gọi udev để tìm device có filesystem UUID=<xyz>
    │ scan tất cả block devices
    ▼
Tìm thấy UUID trên /dev/sdb1 (hoặc /dev/sda1 tuỳ thứ tự boot)
    │
    ▼
Mount /dev/sdb1 tại /data
```

`nofail` trong fstab options đảm bảo boot không bị block nếu HDD không được nhận — server vẫn lên và SSH được, chỉ là `/data` không có.

## 4. Hướng dẫn từng bước

### Thiết lập đã hoàn thành — SSH và Tailscale

Chi tiết trong note [`headless-home-server-ssh-tailscale`](/notes/headless-home-server-ssh-tailscale/). Trạng thái hiện tại: SSH và Tailscale đã hoạt động sau reboot.

### Thiết lập đã hoàn thành — Format và mount HDD

**Xác định disk trước mọi thao tác destructive:**

```bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,LABEL,MOUNTPOINTS
# Phân biệt rõ SSD Kingmax (USB, 120 GB) và HDD Apple (SATA, ~1 TB)
# Không dựa chỉ vào tên /dev/sda hay /dev/sdb
```

**Xóa partition table cũ của HDD (macOS APFS layout):**

```bash
sudo wipefs -a /dev/sda
# Thay /dev/sda bằng device name thực tế của HDD Apple
# ⚠️ DESTRUCTIVE — chỉ chạy khi chắc chắn đúng device
```

**Tạo GPT và partition mới:**

```bash
sudo parted /dev/sda --script mklabel gpt
# mklabel gpt → tạo GPT partition table
# --script    → non-interactive, không hỏi confirm

sudo parted /dev/sda --script mkpart primary ext4 0% 100%
# mkpart primary → tạo primary partition
# 0% 100%        → chiếm toàn bộ dung lượng disk
```

**Format ext4:**

```bash
sudo mkfs.ext4 -L data /dev/sda1
# -L data → đặt label "data" cho filesystem
# Label giúp nhận diện thêm ngoài UUID
```

**Tạo mount point và mount thử:**

```bash
sudo mkdir -p /data
sudo mount /dev/sda1 /data
# Kiểm tra trước khi cấu hình fstab

findmnt /data
df -h /data
# Kỳ vọng: ~870 GB available (1 TB - filesystem overhead)
```

**Cấu hình auto-mount trong fstab:**

```bash
# Lấy UUID của partition data
sudo blkid /dev/sda1
# hoặc:
lsblk -f | grep sda1
```

```bash
sudo nano /etc/fstab
```

Thêm dòng (dùng UUID thực tế):

```text
UUID=<UUID-cua-partition-data> /data ext4 defaults,nofail 0 2
```

Giải thích các field:

```text
UUID=...    → identifier của filesystem
/data       → mount point
ext4        → filesystem type
defaults    → standard mount options (rw, relatime, errors=remount-ro...)
nofail      → boot không fail nếu device không tìm thấy
0           → dump (0 = không backup bằng dump)
2           → fsck order (2 = check sau root filesystem)
```

```bash
sudo systemctl daemon-reload
# Reload systemd để nhận fstab changes

sudo mount -a
# -a → mount tất cả entry trong fstab chưa được mount
# Nếu có lỗi, sửa trước khi reboot

findmnt /data
# Phải thấy /data đang mount
```

**Cấp quyền write cho user:**

```bash
sudo chown <user>:<user> /data
# Cho phép user thông thường write vào /data mà không cần sudo
```

Test:

```bash
touch /data/test.txt && rm /data/test.txt
# Không có lỗi = quyền cơ bản OK
```

### Xác minh auto-mount sau reboot

```bash
sudo reboot
```

SSH lại:

```bash
ssh <user>@macmini
```

```bash
findmnt /data
df -h /data
# Phải thấy /data mount với HDD Apple
# Device name có thể đổi (sda1 → sdb1) nhưng mount vẫn đúng nhờ UUID
```

### Bước tiếp theo — Cài Docker Engine

```bash
# Cài Docker theo script chính thức (chỉ sau khi storage đã xác minh)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker <user>
# usermod -aG → thêm user vào group docker
# Cần logout và login lại để group change có hiệu lực
```

Test Docker:

```bash
docker run --rm hello-world
# --rm → xoá container sau khi chạy xong
```

Xác minh Docker sau reboot:

```bash
sudo reboot
# SSH lại và kiểm tra:
systemctl is-active docker
docker ps
```

## 5. Bẫy lỗi và Những lần thử thất bại

**Bẫy 1 — mount -a báo "mount point does not exist"**

Lần đầu thêm `/data` vào fstab và chạy `mount -a`, gặp lỗi `mount: /data: mount point does not exist`. Nguyên nhân: chưa tạo thư mục `/data`. fstab không tự tạo mount point directory — phải `mkdir -p /data` trước.

**Bẫy 2 — Device name thay đổi sau reboot**

HDD Apple xuất hiện là `/dev/sda1` khi setup, sau reboot chuyển thành `/dev/sdb1` (vì Kingmax SSD USB được nhận trước). Nếu fstab dùng `/dev/sda1`, `/data` sẽ mount vào Kingmax SSD thay vì HDD — hoặc fail hoàn toàn. UUID giải quyết vấn đề này.

**Bẫy 3 — Kết luận hardware hỏng khi `wipefs` thành công nhưng `lsblk` vẫn thấy partition**

Sau `wipefs -a`, chạy `lsblk` ngay lập tức đôi khi vẫn thấy partition cũ vì kernel cache chưa refresh. Chạy `sudo partprobe /dev/sda` hoặc reboot để kernel re-read partition table.

**Bẫy 4 — `chmod 777 /data` vì "tiện"**

Mở quyền 777 cho `/data` nghĩa là mọi process, mọi user trên máy đều có thể đọc/ghi/xoá. Khi Docker container chạy dưới UID khác, có thể overwrite data không có ý định. Nên dùng `chown` với user cụ thể và quản lý permission theo service.

**Bẫy 5 — Cài nhiều service Docker cùng lúc trước khi verify từng bước**

Cài Portainer, Jellyfin, qBittorrent, Nextcloud cùng lúc mà không verify từng service sau reboot — khi có sự cố không biết service nào gây ra. Thứ tự đúng: cài Docker → test container → verify sau reboot → cài service đầu tiên → verify → tiếp tục.

## 6. Kiểm tra và Xác minh

Checklist trạng thái hiện tại:

```bash
# Boot và SSH
systemctl is-enabled ssh tailscaled
systemctl is-active ssh tailscaled
# Kỳ vọng: enabled/enabled, active/active

# Storage
findmnt /data
df -h /data
# Kỳ vọng: /data mount, ~870 GB available

# Headless verification
sudo reboot
# SSH lại và chạy lại các lệnh trên
```

Checklist những gì chưa làm:

```text
[ ] Docker Engine
[ ] Docker Compose
[ ] Service self-host đầu tiên
[ ] Backup strategy cho /data
[ ] Wi-Fi BCM4360 (xem note bcm4360-wifi-ubuntu)
[ ] SSH hardening (PasswordAuthentication no)
[ ] UID/GID management cho Docker volumes
```

## 7. Nguồn tham khảo

- fstab man page: `man fstab`  
  *(giải thích đầy đủ các field và mount options)*
- systemd fstab integration: https://www.freedesktop.org/software/systemd/man/systemd.mount.html  
  *(giải thích `nofail`, `x-systemd.automount` và các option nâng cao)*
- Docker Engine installation — Linux: https://docs.docker.com/engine/install/ubuntu/  
  *(script chính thức, tránh dùng `docker.io` từ APT vì thường là version cũ)*
- parted documentation: https://www.gnu.org/software/parted/manual/  
  *(reference cho GPT partitioning và mkpart syntax)*
- Các note liên quan trong cùng project:
  - [`headless-home-server-ssh-tailscale`](/notes/headless-home-server-ssh-tailscale/) — SSH và Tailscale setup chi tiết
  - [`bcm4360-wifi-ubuntu`](/notes/bcm4360-wifi-ubuntu/) — Wi-Fi driver cho Mac mini
  - [`xubuntu-external-ssd-mac-mini`](/notes/xubuntu-external-ssd-mac-mini/) — Cài Xubuntu lên SSD ngoài
