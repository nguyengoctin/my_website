---
title: "Cài Xubuntu lên SSD ngoài để boot Mac mini 2014"
date: 2026-09-09T13:02:00+07:00
aliases:
  - xubuntu external ssd
  - mac mini xubuntu
  - /notes/xubuntu-external-ssd-macmini/
tags:
  - xubuntu
  - mac-mini
  - ssd
  - boot
  - uefi
---

> Mục tiêu là cài Xubuntu lên SSD Kingmax 120 GB qua USB — trên một máy Ubuntu đang chạy — giữ nguyên ổ hệ điều hành hiện tại, rồi mang SSD sang Mac mini 2014 để boot độc lập. Điểm quan trọng nhất: mọi partition cần cho Xubuntu — đặc biệt EFI System Partition và root — phải nằm trên chính SSD ngoài, không phải ổ NVMe của máy cài.

## 1. Bản chất

**UEFI và EFI System Partition (ESP)** là cơ chế boot trên phần cứng hiện đại (kể cả Mac từ 2006 trở đi). Thay vì đọc MBR ở sector đầu ổ đĩa, firmware UEFI tìm EFI System Partition (FAT32, type `EF00`) và load file `.efi` trong đó để khởi động bootloader (GRUB trong trường hợp này).

Để SSD ngoài **self-contained** — có thể cắm vào bất kỳ máy UEFI nào và boot được — EFI phải nằm trên chính SSD đó, không phải trên ổ nội bộ.

**GRUB loopback boot** là cách boot trực tiếp từ ISO file thông qua GRUB, không cần ghi ISO ra USB. GRUB mount ISO như một filesystem ảo và kernel của ISO được load từ đó.

Môi trường đã xác minh:

```text
Laptop hiện tại:  /dev/nvme0n1 → Ubuntu (ổ nội bộ, KHÔNG được đụng vào)
SSD mục tiêu:     /dev/sda     → Kingmax 120 GB qua USB
Mac mini:         Late 2014, hỗ trợ boot từ USB qua Startup Manager
```

## 2. Vì sao lựa chọn

**Tại sao không ghi ISO ra USB thông thường (dd/Balena Etcher)?**

Trong setup này, SSD Kingmax là ổ đích cài Xubuntu — không phải USB installer tạm. Nếu ghi ISO ra SSD thì SSD trở thành live installer, không phải hệ điều hành cài xong. Cần cách boot ISO để chạy installer, chỉ định SSD làm target cài đặt.

**Tại sao GRUB loopback boot thay vì dùng USB khác?**

Máy Ubuntu hiện tại đã có GRUB. Thêm entry vào `40_custom` và boot ISO trực tiếp từ `/boot/iso/` không cần USB thứ hai. Tiết kiệm thiết bị và kiểm soát tốt hơn quá trình boot.

**Tại sao layout đơn giản (EFI + root, không có swap partition)?**

Với SSD 120 GB và mục tiêu home server đơn giản, layout tối giản giảm số bước cài đặt và giảm risk làm nhầm partition. Swapfile có thể cấu hình sau trên root filesystem khi cần — không cần partition riêng.

**Đánh đổi:**

- GRUB loopback boot từ ISO **chưa được xác minh hoạt động** trong context này — đây là procedure dự kiến, cần test thực tế.
- SSD qua USB có thể chậm hơn SSD SATA nội bộ, nhưng trong thực tế thấy hiệu năng cải thiện đáng kể so với HDD SATA cũ của Mac mini.

## 3. Cơ chế hoạt động

```text
GRUB loopback boot flow:

Firmware UEFI
      │ load GRUB từ /boot/efi trên nvme0n1
      ▼
GRUB menu
      │ chọn "Install Xubuntu from ISO"
      ▼
GRUB loopback
      │ mount /boot/iso/xubuntu-26.04.1-desktop-amd64.iso
      │ như filesystem ảo (loop)
      ▼
Load kernel:  (loop)/casper/vmlinuz
Load initrd:  (loop)/casper/initrd
      │
      ▼
Xubuntu Live environment khởi động
      │ (ISO mount tạm trong RAM)
      ▼
Installer Xubuntu chạy
      │ partition và format /dev/sda
      │ cài bootloader/EFI vào /dev/sda
      ▼
Xubuntu cài xong trên /dev/sda (SSD Kingmax)
```

Mac mini Startup Manager flow:

```text
Bật Mac mini + giữ Option/Alt
      │
      ▼
Startup Manager (Apple firmware)
      │ scan các disk có EFI boot entry
      │ tìm thấy "EFI Boot" trên SSD Kingmax
      ▼
Load GRUB từ SSD Kingmax EFI partition
      │
      ▼
GRUB boot Xubuntu trên /dev/sda
```

## 4. Hướng dẫn từng bước

### Bước 1 — Xác minh và wipe SSD

Luôn xác định ổ bằng nhiều thuộc tính, không chỉ tên:

```bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,MOUNTPOINTS
# NAME        → tên device
# SIZE        → dung lượng
# MODEL       → model name của ổ
# TRAN        → transport (usb, sata, nvme)
# FSTYPE      → filesystem type hiện tại
# MOUNTPOINTS → đang mount ở đâu (nếu có)
```

Xác nhận đúng SSD Kingmax (USB, 120 GB). Sau đó unmount nếu có:

```bash
sudo umount /dev/sda1 /dev/sda3 /dev/sda4 2>/dev/null
# 2>/dev/null → suppress lỗi nếu partition không tồn tại hoặc chưa mount
```

Wipe partition table cũ:

```bash
sudo wipefs -a /dev/sda
# -a → xoá tất cả filesystem signature và partition table
# ⚠️ DESTRUCTIVE — chỉ chạy khi chắc chắn đúng device
```

Kiểm tra sau wipe:

```bash
lsblk -f
# SSD phải trống, không còn partition
```

### Bước 2 — Tải và verify ISO

```bash
cd ~/Downloads
wget https://cdimage.ubuntu.com/xubuntu/releases/26.04/release/xubuntu-26.04.1-desktop-amd64.iso
# wget → download với progress bar

wget https://cdimage.ubuntu.com/xubuntu/releases/26.04/release/SHA256SUMS
# Tải file checksum từ cùng thư mục release
```

Verify:

```bash
sha256sum xubuntu-26.04.1-desktop-amd64.iso
# So sánh output với nội dung SHA256SUMS

grep xubuntu-26.04.1-desktop-amd64.iso SHA256SUMS
# Hai hash phải trùng nhau
```

### Bước 3 — Chuẩn bị GRUB loopback boot

Copy ISO vào `/boot/iso`:

```bash
sudo mkdir -p /boot/iso
sudo cp ~/Downloads/xubuntu-26.04.1-desktop-amd64.iso /boot/iso/
# -p → tạo parent directory nếu chưa có
```

Kiểm tra path kernel/initrd trong ISO:

```bash
sudo mkdir -p /mnt/xubuntu-iso
sudo mount -o loop ~/Downloads/xubuntu-26.04.1-desktop-amd64.iso /mnt/xubuntu-iso
# -o loop → mount file như block device

ls -lh /mnt/xubuntu-iso/casper/
# Cần thấy: vmlinuz và initrd

sudo umount /mnt/xubuntu-iso
```

Lấy UUID của root filesystem đang chạy:

```bash
findmnt -no UUID /
# -n → no header
# -o UUID → chỉ in UUID column
```

Ghi lại UUID này — sẽ dùng trong GRUB entry.

Backup và thêm GRUB entry:

```bash
sudo cp /etc/grub.d/40_custom /etc/grub.d/40_custom.bak

sudo nano /etc/grub.d/40_custom
```

Thêm entry (thay UUID bằng giá trị thực tế):

```text
menuentry "Install Xubuntu from ISO" {
    set isofile="/boot/iso/xubuntu-26.04.1-desktop-amd64.iso"
    search --no-floppy --fs-uuid --set=root <UUID-cua-root-filesystem>
    loopback loop ($root)$isofile
    linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=$isofile quiet splash ---
    initrd (loop)/casper/initrd
}
```

Kiểm tra syntax và update GRUB:

```bash
sudo grub-script-check /etc/grub.d/40_custom
# Không có output = không có lỗi syntax

sudo update-grub
# Tạo lại /boot/grub/grub.cfg từ các file trong /etc/grub.d/
```

### Bước 4 — Boot vào Xubuntu Live

Giữ SSD cắm vào laptop:

```bash
sudo reboot
```

Trong GRUB chọn "Install Xubuntu from ISO". Khi Xubuntu Live lên, xác minh lại ổ trước khi cài:

```bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,MOUNTPOINTS
```

Xác định rõ Kingmax SSD (USB, 120 GB) và ổ NVMe laptop. Không dựa hoàn toàn vào tên `/dev/sda` vì có thể thay đổi.

### Bước 5 — Partition và cài Xubuntu

Chọn **manual/custom partitioning** trong installer. Trên SSD Kingmax tạo:

```text
EFI System Partition:
  Size:       1024 MB
  Filesystem: FAT32
  Role:       EFI System Partition
  Mount:      /boot/efi

Root:
  Size:       phần còn lại (~111 GB)
  Filesystem: ext4
  Mount:      /
  Format:     Yes
```

Nếu installer hỏi nơi cài bootloader, target phải là SSD Kingmax, không phải ổ NVMe.

Trước khi bấm Install, đọc kỹ summary. Chỉ các partition thuộc Kingmax SSD được phép tạo/format.

### Bước 6 — Boot trên Mac mini

Sau khi cài xong, shutdown laptop và rút SSD:

```bash
sudo poweroff
```

Cắm SSD + bàn phím USB vào Mac mini. Bật Mac mini và giữ ngay:
- Bàn phím Apple: `Option ⌥`
- Bàn phím PC: `Alt`

Startup Manager xuất hiện, chọn **EFI Boot** (là EFI trên SSD Kingmax).

## 5. Bẫy lỗi và Những lần thử thất bại

**Bẫy 1 — Chọn nhầm disk khi partition**

Nếu chọn nhầm `/dev/nvme0n1` để format, mất khả năng boot laptop. Không thể undo. Luôn xác nhận đúng device bằng SIZE + MODEL + TRAN trước thao tác destructive.

**Bẫy 2 — NTFS dirty flag gây mount fail**

SSD Kingmax ban đầu có partition NTFS bị dirty flag sau khi eject không đúng cách trên Windows. Lỗi khi mount:

```text
ntfs3(sda3): volume is dirty and "force" flag is not set!
```

Vì SSD sẽ được wipe để cài Linux, không cần sửa NTFS — wipefs và cài lại là đủ. Nếu cần giữ dữ liệu, phải dùng Windows `chkdsk` hoặc `ntfsfix` (không phải `ntfsfix -n`).

**Bẫy 3 — Dùng Bluetooth keyboard cho Startup Manager**

Firmware Mac mini 2014 kết nối Bluetooth chậm — Startup Manager có thể xuất hiện và biến mất trước khi keyboard được nhận. Phải dùng bàn phím USB cho lần boot đầu.

**Bẫy 4 — GRUB loopback boot thất bại do path kernel/initrd sai**

Path `/casper/vmlinuz` và `/casper/initrd` phải được verify bằng cách mount ISO thực tế — không hardcode từ hướng dẫn cũ vì có thể thay đổi giữa các release.

**Bẫy 5 — EFI partition nằm trên ổ nội bộ thay vì SSD**

Installer đôi khi tự động chọn EFI partition đang có sẵn (trên NVMe) thay vì tạo mới trên SSD target. Kết quả: Xubuntu boot được khi cắm cả laptop lẫn Mac mini, nhưng không boot được khi chỉ có SSD Kingmax — vì EFI nằm trên NVMe.

## 6. Kiểm tra và Xác minh

Sau khi Xubuntu boot trên Mac mini:

```bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,MOUNTPOINTS
# Xác minh SSD Kingmax là disk đang chứa / và /boot/efi

findmnt /
# SOURCE phải là partition trên Kingmax SSD

findmnt /boot/efi
# SOURCE phải là partition FAT32 trên Kingmax SSD
```

Kỳ vọng:

```text
/          → /dev/sda2 (hoặc tên khác, nhưng thuộc Kingmax)
/boot/efi  → /dev/sda1 (FAT32, thuộc Kingmax)
```

Kiểm tra network:

```bash
nmcli device
ip link
lspci -nn | grep -i network
# Xác minh card network nào được nhận, có cần driver bổ sung không
```

Update hệ thống (nếu có Internet qua Ethernet):

```bash
sudo apt update && sudo apt full-upgrade
sudo reboot
```

## 7. Nguồn tham khảo

- Xubuntu release directory: https://cdimage.ubuntu.com/xubuntu/releases/26.04/release/  
  *(tải ISO và SHA256SUMS từ đây)*
- Ubuntu Community Help Wiki — GRUB2 ISO Boot: https://help.ubuntu.com/community/Grub2/ISOBoot  
  *(giải thích cơ chế loopback và cú pháp GRUB entry)*
- Output thực tế của `lsblk`, `blkid`, `ntfsfix -n`, `dmesg`, `wipefs` trên máy hiện tại  
  *(evidence trực tiếp, không phải chỉ documentation)*
- Ubuntu Community Help Wiki — UEFI boot: https://help.ubuntu.com/community/UEFI  
  *(background về EFI System Partition và UEFI boot process)*
