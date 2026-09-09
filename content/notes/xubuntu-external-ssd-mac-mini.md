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

> Mục tiêu là cài Xubuntu lên SSD Kingmax 120 GB qua USB trên một máy Ubuntu khác, giữ nguyên ổ hệ điều hành hiện tại, rồi tháo SSD và cắm sang Mac mini 2014 để boot độc lập. Điểm quan trọng nhất là mọi partition cần cho Xubuntu — đặc biệt EFI và `/` — phải nằm trên chính SSD ngoài.

## Kết luận cần nhớ

Trong môi trường đã kiểm tra:

```text
/dev/nvme0n1 = ổ Ubuntu hiện tại của laptop
/dev/sda     = Kingmax SSD 120 GB qua USB
```

Quy tắc an toàn:

```text
/dev/sda     = ổ mục tiêu, được phép partition/format
/dev/nvme0n1 = ổ hệ điều hành hiện tại, tuyệt đối không format
```

Không nên dựa duy nhất vào tên `/dev/sda`, vì tên block device có thể thay đổi sau reboot hoặc khi sang máy khác. Trước thao tác destructive luôn kiểm tra thêm `SIZE`, `MODEL`, `TRAN`:

```bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,MOUNTPOINTS
```

Flow tổng thể:

```text
Laptop Ubuntu hiện tại
        ↓
Chuẩn bị SSD ngoài
        ↓
Boot Xubuntu installer
        ↓
Cài Xubuntu vào SSD ngoài
        ↓
Shutdown laptop
        ↓
Rút SSD
        ↓
Cắm SSD + bàn phím USB vào Mac mini 2014
        ↓
Giữ Option/Alt khi bật Mac
        ↓
Chọn EFI Boot
        ↓
Xubuntu chạy trên Mac mini
```

---

## 1. Sự cố NTFS ban đầu và cách xác định nguyên nhân

SSD Kingmax ban đầu có nhiều partition:

```text
sda
├─sda1  vfat
├─sda2
├─sda3  ntfs
└─sda4  ntfs
```

Ubuntu nhìn thấy `/dev/sda3` nhưng không mount được và hiện lỗi dạng:

```text
wrong fs type, bad option, bad superblock ...
```

### Xác định filesystem

```bash
lsblk -f
```

và:

```bash
sudo blkid /dev/sda3
```

Kết quả đã xác minh:

```text
TYPE="ntfs"
PARTLABEL="Basic data partition"
```

### Kiểm tra NTFS không sửa dữ liệu

```bash
sudo ntfsfix -n /dev/sda3
```

Kết quả thực tế:

```text
Mounting volume... OK
Processing of $MFT and $MFTMirr completed successfully.
Checking the alternate boot sector... OK
NTFS volume version is 3.1.
NTFS partition /dev/sda3 was processed successfully.
```

Điều này cho thấy cấu trúc NTFS cơ bản không có lỗi rõ ràng.

### Xem nguyên nhân mount fail từ kernel

Ngay sau khi mount thất bại:

```bash
sudo dmesg | tail -n 50
```

Kernel đã báo:

```text
ntfs3(sda3): volume is dirty and "force" flag is not set!
ntfs3(sda3): It is recommended to use chkdsk.
```

Kết luận: lỗi mount lúc đó là **NTFS dirty flag**, không có bằng chứng cho thấy SSD vật lý hỏng.

Nếu cần giữ dữ liệu, hướng phù hợp là dùng Windows `chkdsk` hoặc cân nhắc `ntfsfix`. Nhưng trong trường hợp SSD sẽ được xóa để cài Linux, sửa filesystem NTFS cũ không còn cần thiết.

---

## 2. Xóa sạch SSD cũ

Chỉ làm khi chắc chắn không cần dữ liệu trên SSD.

Unmount các partition nếu đang mount:

```bash
sudo umount /dev/sda1 2>/dev/null
sudo umount /dev/sda3 2>/dev/null
sudo umount /dev/sda4 2>/dev/null
```

Xóa filesystem signatures và partition table:

```bash
sudo wipefs -a /dev/sda
```

Output thực tế xác nhận GPT và protective MBR đã bị xóa:

```text
/dev/sda: 8 bytes were erased ... (gpt)
/dev/sda: 8 bytes were erased ... (gpt)
/dev/sda: 2 bytes were erased ... (PMBR)
/dev/sda: calling ioctl to re-read partition table: Success
```

Kiểm tra:

```bash
lsblk -f
```

Sau khi wipe thành công, kết quả đã thấy:

```text
sda

nvme0n1
├─nvme0n1p1 vfat  /boot/efi
└─nvme0n1p2 ext4  /
```

Tức SSD ngoài đã sạch, không còn partition cũ.

### Caveat

`wipefs -a /dev/sda` là thao tác destructive. Nếu chọn nhầm `/dev/nvme0n1`, có thể làm mất khả năng boot hoặc dữ liệu của hệ điều hành hiện tại.

Trước mỗi thao tác dạng này nên chạy:

```bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,MOUNTPOINTS
```

và xác nhận SSD bằng model/size, không chỉ bằng tên device.

---

## 3. Layout nên dùng cho SSD Xubuntu

Với SSD khoảng 120 GB và mục tiêu vừa desktop vừa home server, layout đơn giản là hợp lý:

```text
SSD ngoài
├─ EFI System Partition   ~1 GiB   FAT32
└─ root                   còn lại  ext4
```

Trong installer có thể thành:

```text
/dev/sda1   FAT32   /boot/efi
/dev/sda2   ext4    /
```

Không cần tạo ngay:

- swap partition riêng;
- `/home` riêng;
- LVM;
- full-disk encryption.

Lý do: ưu tiên boot đơn giản, portable, dễ cứu và dễ debug. Swapfile có thể cấu hình sau nếu cần.

---

## 4. Chuẩn bị ISO Xubuntu trên máy Ubuntu hiện tại

Mục tiêu là cài lên SSD ngoài mà không cần USB installer.

ISO dự kiến sử dụng trong context này:

```text
xubuntu-26.04.1-desktop-amd64.iso
```

Kiểm tra file đã tải:

```bash
ls -lh ~/Downloads/xubuntu*.iso
```

Nếu tải bằng terminal:

```bash
cd ~/Downloads
wget https://cdimage.ubuntu.com/xubuntu/releases/26.04/release/xubuntu-26.04.1-desktop-amd64.iso
```

### Verify checksum

Nên tải `SHA256SUMS` từ cùng thư mục release:

```bash
cd ~/Downloads
wget https://cdimage.ubuntu.com/xubuntu/releases/26.04/release/SHA256SUMS
```

Tính checksum:

```bash
sha256sum xubuntu-26.04.1-desktop-amd64.iso
```

So với:

```bash
grep xubuntu-26.04.1-desktop-amd64.iso SHA256SUMS
```

Hai SHA256 phải trùng nhau trước khi dùng ISO.

> Trong context hiện tại chưa có kết quả checksum thực tế, nên bước verify này vẫn cần thực hiện.

---

## 5. Boot ISO trực tiếp từ GRUB, không cần USB

Đây là kế hoạch được chọn vì máy hiện tại đã chạy Ubuntu và SSD ngoài cần được dùng làm target cài đặt.

### Copy ISO vào `/boot/iso`

```bash
sudo mkdir -p /boot/iso
sudo cp ~/Downloads/xubuntu-26.04.1-desktop-amd64.iso /boot/iso/
```

Kiểm tra:

```bash
ls -lh /boot/iso/
```

### Kiểm tra kernel/initrd trong ISO

Không nên đoán path nếu release thay đổi. Có thể mount ISO để kiểm tra:

```bash
sudo mkdir -p /mnt/xubuntu-iso

sudo mount -o loop   ~/Downloads/xubuntu-26.04.1-desktop-amd64.iso   /mnt/xubuntu-iso
```

Kiểm tra:

```bash
ls -lh /mnt/xubuntu-iso/casper/
```

Cần thấy các file tương ứng:

```text
vmlinuz
initrd
```

Unmount:

```bash
sudo umount /mnt/xubuntu-iso
```

### Lấy UUID của root filesystem hiện tại

```bash
findmnt -no UUID /
```

Trong lần kiểm tra trước, UUID root là:

```text
98932dcd-2480-4f44-a832-f3c0d39e4635
```

Không nên hardcode từ note nếu môi trường đã thay đổi; chạy lại lệnh trước khi cấu hình GRUB.

### Backup GRUB custom entry

```bash
sudo cp /etc/grub.d/40_custom /etc/grub.d/40_custom.bak
```

Mở:

```bash
sudo nano /etc/grub.d/40_custom
```

Entry đã được đề xuất:

```text
menuentry "Install Xubuntu from ISO" {
    set isofile="/boot/iso/xubuntu-26.04.1-desktop-amd64.iso"
    search --no-floppy --fs-uuid --set=root 98932dcd-2480-4f44-a832-f3c0d39e4635
    loopback loop ($root)$isofile
    linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=$isofile quiet splash ---
    initrd (loop)/casper/initrd
}
```

Thay UUID bằng giá trị thực tế nếu khác.

Kiểm tra syntax:

```bash
sudo grub-script-check /etc/grub.d/40_custom
```

Nếu không có lỗi:

```bash
sudo update-grub
```

### Trạng thái xác minh

Phần boot ISO qua GRUB **chưa được thực thi thành công trong context hiện tại**. Đây là procedure dự kiến, cần kiểm chứng khi làm thực tế.

---

## 6. Boot vào Xubuntu Live

Giữ SSD Kingmax cắm vào laptop rồi:

```bash
sudo reboot
```

Trong GRUB chọn:

```text
Install Xubuntu from ISO
```

Nếu menu GRUB bị ẩn, thử `Esc` trong lúc khởi động.

Khi Xubuntu Live lên, ưu tiên vào live environment trước thay vì cài ngay.

Kiểm tra lại ổ:

```bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,MOUNTPOINTS
```

Phải xác định rõ đâu là:

```text
ổ hệ điều hành laptop
Kingmax SSD 120 GB qua USB
```

Không dựa hoàn toàn vào việc Kingmax chắc chắn vẫn là `/dev/sda`.

---

## 7. Partition SSD trong installer

Chọn manual partitioning / custom partitioning nếu installer cung cấp.

Trên **SSD Kingmax**, tạo:

### EFI System Partition

Khoảng:

```text
1024 MB
```

Thiết lập:

```text
Filesystem: FAT32
Role/type:  EFI System Partition
Mount:      /boot/efi
```

### Root

Dùng phần dung lượng còn lại:

```text
Filesystem: ext4
Mount:      /
Format:     Yes
```

Kết quả mong muốn:

```text
Kingmax SSD
├─ FAT32 EFI ~1 GiB → /boot/efi
└─ ext4 còn lại     → /
```

### Bootloader

Nếu installer hỏi nơi cài bootloader, target phải là **SSD Kingmax**, không phải ổ NVMe của laptop.

Mục tiêu là SSD phải self-contained: EFI và root đều nằm trên SSD đó.

---

## 8. Checkpoint quan trọng trước khi bấm Install

Trước xác nhận ghi partition, đọc kỹ summary.

Chỉ các partition thuộc Kingmax SSD mới được:

- tạo;
- xóa;
- format;
- dùng làm EFI/root.

Không được thấy ổ hệ thống hiện tại như:

```text
/dev/nvme0n1p1
/dev/nvme0n1p2
```

bị format.

Nếu summary không đủ rõ để chắc chắn, dừng lại và kiểm tra bằng `lsblk` hoặc chụp màn hình trước khi tiếp tục.

### Rủi ro thực tế

Việc cài Xubuntu lên SSD ngoài **không tự làm hỏng ổ hiện tại**. Rủi ro xuất hiện khi:

- chọn nhầm disk để erase/format;
- dùng nhầm EFI partition trên ổ hiện tại;
- installer ghi bootloader/EFI vào ổ nội bộ thay vì SSD ngoài.

---

## 9. Cài xong: khi nào tháo SSD

Đây là bước dễ quên nhưng quan trọng.

Sau khi installer hoàn tất:

1. Không rút SSD khi máy còn chạy.
2. Shutdown laptop hoàn toàn:

```bash
sudo poweroff
```

3. Đợi máy tắt hẳn.
4. Rút box SSD Kingmax khỏi laptop.
5. Mang SSD sang Mac mini 2014.

Flow:

```text
Installer hoàn tất
      ↓
Power off laptop
      ↓
Rút Kingmax SSD
      ↓
Cắm vào Mac mini
```

---

## 10. Boot SSD trên Mac mini 2014

Chuẩn bị:

- Kingmax SSD + box USB;
- màn hình;
- bàn phím USB cho lần boot đầu tiên.

Bàn phím Apple:

```text
Option ⌥
```

Bàn phím Windows/PC:

```text
Alt ≈ Option
```

### Procedure

1. Cắm SSD vào Mac mini.
2. Cắm bàn phím USB.
3. Giữ `Option` hoặc `Alt`.
4. Bật Mac mini.
5. Tiếp tục giữ phím cho đến khi Startup Manager xuất hiện.
6. Chọn:

```text
EFI Boot
```

Nếu EFI trên SSD được tạo đúng, Mac mini có thể boot GRUB/Xubuntu từ đó.

### Không có bàn phím thì sao?

Lần boot đầu không nên phụ thuộc vào Bluetooth keyboard vì firmware có thể chưa kết nối Bluetooth đủ sớm.

Giải pháp đơn giản và đáng tin cậy nhất là mượn một bàn phím USB trong vài phút.

Sau khi Xubuntu đã boot ổn và máy được cấu hình làm server/headless, bàn phím không còn cần thường xuyên.

> Việc Mac mini cụ thể nhận `EFI Boot` và boot thành công từ SSD vẫn cần kiểm chứng trên phần cứng thật.

---

## 11. Xác nhận Xubuntu thật sự chạy độc lập từ SSD

Sau khi boot trên Mac mini:

```bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,MOUNTPOINTS
```

Kiểm tra root:

```bash
findmnt /
```

Kiểm tra EFI:

```bash
findmnt /boot/efi
```

Mục tiêu:

```text
/          → partition ext4 trên Kingmax SSD
/boot/efi  → partition FAT32 EFI trên Kingmax SSD
```

Ví dụ:

```text
/dev/sda2  /
/dev/sda1  /boot/efi
```

Nhưng tên device có thể đổi thành `/dev/sdb` hoặc tên khác. Điều quan trọng là cả hai partition thuộc đúng SSD Kingmax.

Nếu `/boot/efi` trỏ sang ổ khác, installation chưa hoàn toàn self-contained.

---

## 12. Kiểm tra hardware trên Mac mini trước khi biến thành server

Sau khi boot được, kiểm tra trước:

```bash
nmcli device
```

```bash
ip link
```

```bash
uname -a
```

Có thể xem PCI hardware:

```bash
lspci -nn
```

Sau đó update:

```bash
sudo apt update
sudo apt full-upgrade
```

Reboot:

```bash
sudo reboot
```

Với Mac mini 2014, Wi‑Fi có thể cần xử lý riêng tùy chipset/driver thực tế. Không nên giả định trước khi xem hardware thật.

---

## 13. Chỉ sau khi OS ổn mới dựng home server

Thứ tự nên dùng:

```text
Xubuntu boot ổn trên Mac mini
        ↓
Ethernet/Wi-Fi hoạt động
        ↓
Update hệ thống
        ↓
SSH
        ↓
Docker
        ↓
VPN/Tailscale hoặc Cloudflare Tunnel
        ↓
Các service self-hosted
```

Không cần cài Docker hay toàn bộ server stack trên laptop trước khi xác nhận hệ điều hành chạy ổn trên Mac mini.

---

## 14. Những điều đã xác minh và chưa xác minh

### Đã xác minh trên máy hiện tại

- Kingmax SSD được nhận qua USB.
- SSD có dung lượng danh nghĩa 120 GB.
- Kernel nhận bridge USB Realtek RTL9201.
- NTFS `/dev/sda3` từng bị dirty flag.
- `ntfsfix -n` cho thấy MFT/MFTMirr và alternate boot sector OK.
- `wipefs -a /dev/sda` đã xóa GPT/PMBR thành công.
- `lsblk -f` sau đó cho thấy SSD không còn partition.
- Ubuntu hiện tại vẫn chạy trên `nvme0n1`.

### Chưa được kiểm chứng thực tế trong context này

- SHA256 của ISO Xubuntu.
- GRUB entry boot ISO có boot thành công hay không.
- Installer có tạo EFI hoàn toàn trên SSD ngoài hay không.
- SSD có xuất hiện dưới `EFI Boot` trên Mac mini 2014 hay không.
- Wi‑Fi/Ethernet và các driver cụ thể trên Mac mini.
- Xubuntu boot ổn định lâu dài từ box USB hiện tại.

Những mục này nên được kiểm tra tuần tự thay vì coi là đã hoàn thành.

---

## 15. Checklist ngắn khi làm lại

```text
[ ] Xác định SSD bằng NAME + SIZE + MODEL + TRAN
[ ] Xác nhận không cần dữ liệu cũ
[ ] SSD đã wipe sạch
[ ] Tải đúng Xubuntu ISO
[ ] Verify SHA256
[ ] Boot ISO
[ ] Trong Live: xác định lại Kingmax SSD
[ ] Tạo EFI FAT32 ~1 GiB trên SSD
[ ] Tạo ext4 / trên phần còn lại
[ ] Không format ổ hệ điều hành hiện tại
[ ] Bootloader/EFI thuộc SSD ngoài
[ ] Cài hoàn tất
[ ] Power off laptop
[ ] Rút SSD
[ ] Cắm SSD + bàn phím USB vào Mac mini
[ ] Giữ Option/Alt khi bật máy
[ ] Chọn EFI Boot
[ ] Kiểm tra findmnt / và /boot/efi
[ ] Kiểm tra network/hardware
[ ] Update hệ thống
[ ] Sau đó mới cấu hình home server
```

## Nguồn/đầu mối đã dùng trong quá trình xử lý

- Xubuntu official release directory: `cdimage.ubuntu.com/xubuntu/releases/26.04/release/`
- Ubuntu Community Help Wiki về boot ISO bằng GRUB 2 (`Grub2/ISOBoot`).
- Output thực tế của `lsblk`, `blkid`, `ntfsfix`, `dmesg` và `wipefs` trên máy hiện tại.
