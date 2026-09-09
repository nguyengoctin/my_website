---
title: "Mac mini 2014 Home Server: Setup Reference"
date: 2026-09-09T17:00:00+07:00
tags:
  - home-server
  - mac-mini
  - xubuntu
  - tailscale
  - ssh
  - storage
---

## Trạng thái hiện tại

Mac mini Late 2014 đã được chuyển sang mô hình home server chạy Xubuntu:

-   **Mac mini Late 2014**, RAM 8 GB.
-   **Kingmax SSD 120 GB qua USB**: chứa Xubuntu và EFI.
-   **Apple HDD 1 TB SATA bên trong**: đã xóa macOS/APFS, format ext4 và
    mount tại `/data`.
-   Có thể quản trị **headless** từ laptop qua SSH.
-   **Tailscale** đã hoạt động, có thể SSH bằng hostname `macmini`.
-   SSH và Tailscale vẫn hoạt động sau reboot.
-   `/data` tự mount thành công sau reboot.
-   Docker **chưa cài**.

Kiến trúc hiện tại:

``` text
Mac mini Late 2014
│
├── Kingmax SSD 120 GB — USB
│   ├── Xubuntu /
│   └── /boot/efi
│
└── Apple HDD 1 TB — SATA
    └── ext4
        └── /data
```

Mục tiêu tiếp theo:

``` text
SSD 120 GB
├── Xubuntu
├── Docker Engine
└── system/application binaries

HDD 1 TB — /data
├── docker/
├── media/
├── downloads/
└── backups/
```

------------------------------------------------------------------------

## 1. Xubuntu chạy trên SSD ngoài

Hệ điều hành đã được cài lên Kingmax SSD 120 GB kết nối USB.

Layout được xác nhận:

``` text
Kingmax SSD 120 GB
├── ext4  /
└── vfat  /boot/efi
```

Điều này cho phép HDD SATA bên trong được dùng hoàn toàn cho dữ liệu.

Sau khi chuyển từ HDD sang SSD, hiệu năng desktop thực tế cải thiện rất
rõ dù SSD kết nối qua USB.

### Boot

Mac mini có thể boot Linux từ SSD ngoài thông qua Startup Manager:

-   bật máy;
-   giữ `Option` trên bàn phím Apple, hoặc `Alt` trên bàn phím PC;
-   chọn `EFI Boot`.

Sau khi setup server, cần ưu tiên kiểm chứng bằng reboot thực tế thay vì
giả định firmware sẽ boot đúng disk.

------------------------------------------------------------------------

## 2. SSH headless

OpenSSH Server đã được cài và có thể SSH từ laptop.

Cách kết nối ưu tiên:

``` bash
ssh <user>@macmini
```

Không cần màn hình và bàn phím gắn trực tiếp vào Mac mini cho công việc
quản trị thông thường.

Có thể kiểm tra SSH service:

``` bash
systemctl is-enabled ssh
systemctl is-active ssh
```

Trạng thái mong muốn:

``` text
enabled
active
```

### SSH key

Laptop đã tạo Ed25519 key:

``` bash
ssh-keygen -t ed25519
```

Public key được copy sang server:

``` bash
ssh-copy-id <user>@macmini
```

Sau đó:

``` bash
ssh <user>@macmini
```

### Quy tắc bảo mật

File:

``` text
~/.ssh/id_ed25519
```

là **private key** --- không upload, gửi cho người khác hoặc commit vào
Git.

File:

``` text
~/.ssh/id_ed25519.pub
```

là public key và có thể copy sang server.

Chỉ nên tắt password authentication sau khi đã kiểm chứng một phiên SSH
mới bằng key hoạt động ổn định.

------------------------------------------------------------------------

## 3. Tailscale

Tailscale được cài trên:

-   Mac mini;
-   laptop quản trị.

Cả hai đăng nhập cùng tailnet.

SSH qua MagicDNS đã được kiểm chứng:

``` bash
ssh <user>@macmini
```

Điều này có nghĩa không cần nhớ IP LAN hoặc Tailscale IP trong sử dụng
hằng ngày.

### Ý nghĩa

Không cần mở TCP port 22 trên router ra Internet chỉ để SSH vào home
server.

Có thể quản trị Mac mini qua mạng Tailscale thay vì public SSH.

Các thông tin cần bảo vệ vẫn gồm:

-   SSH private key;
-   password;
-   Tailscale auth/API token.

Một địa chỉ private/Tailscale IP tự nó không thay thế credential.

------------------------------------------------------------------------

## 4. Kiểm chứng headless sau reboot

Một home server không nên chỉ được kiểm tra trong phiên hiện tại.

Quy trình:

``` bash
sudo reboot
```

Đợi máy khởi động lại, sau đó từ laptop:

``` bash
ssh <user>@macmini
```

Mac mini đã vượt qua kiểm tra này: sau reboot vẫn có thể SSH vào server.

Điều này xác nhận boot + networking + SSH/Tailscale đủ ổn để tiếp tục
setup server headless.

------------------------------------------------------------------------

## 5. Nhận diện chính xác hai disk

Trước khi xóa HDD, disk được kiểm tra bằng:

``` bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,LABEL,MOUNTPOINTS
```

Kết quả ban đầu cho thấy:

``` text
APPLE HDD HTS541010A9E662
~1 TB
SATA
├── EFI 200 MB
└── APFS ~931 GB

Kingmax SSD 120GB
USB
├── ext4 /
└── vfat /boot/efi
```

Điều quan trọng nhất trước thao tác destructive là nhận diện disk bằng:

-   model;
-   dung lượng;
-   transport;
-   filesystem;
-   mount point.

**Không nên chỉ dựa vào tên `/dev/sda` hay `/dev/sdb`.**

------------------------------------------------------------------------

## 6. HDD Apple 1 TB trước khi xóa

Partition table được kiểm tra bằng:

``` bash
sudo fdisk -l /dev/sda
```

và:

``` bash
sudo blkid /dev/sda1 /dev/sda2
```

Disk sử dụng GPT và còn layout macOS:

``` text
EFI System Partition
Apple APFS
```

Sau khi xác nhận không cần macOS hoặc dữ liệu cũ nữa, toàn bộ HDD được
dành cho Linux.

> Các lệnh trong phần tiếp theo phá hủy dữ liệu. Không copy nguyên lệnh
> sang máy khác mà chưa xác định lại disk.

------------------------------------------------------------------------

## 7. Xóa partition table cũ

Sau khi xác nhận đúng HDD, signature GPT/PMBR cũ được xóa:

``` bash
sudo wipefs -a /dev/sda
```

Sau đó kiểm tra lại:

``` bash
lsblk -o NAME,SIZE,MODEL,FSTYPE,MOUNTPOINTS
```

HDD trở thành disk trống, trong khi SSD chứa `/` vẫn nguyên vẹn.

------------------------------------------------------------------------

## 8. Tạo GPT và partition dữ liệu mới

Tạo GPT:

``` bash
sudo parted /dev/sda --script mklabel gpt
```

Tạo một partition chiếm toàn bộ disk:

``` bash
sudo parted /dev/sda --script mkpart primary ext4 0% 100%
```

Kiểm tra:

``` bash
lsblk -o NAME,SIZE,MODEL,FSTYPE,MOUNTPOINTS
```

Kết quả:

``` text
HDD ~1 TB
└── partition ~931.5 GiB
```

------------------------------------------------------------------------

## 9. Format HDD thành ext4

Partition được format ext4 và đặt label `data`:

``` bash
sudo mkfs.ext4 -L data /dev/sda1
```

Kiểm tra:

``` bash
lsblk -f /dev/sda
```

Filesystem sau khi tạo:

``` text
FSTYPE: ext4
LABEL:  data
```

ext4 phù hợp với trường hợp HDD được dùng chủ yếu bởi Linux/home server.

------------------------------------------------------------------------

## 10. Mount tại `/data`

Tạo mount point:

``` bash
sudo mkdir -p /data
```

Mount thử:

``` bash
sudo mount /dev/sda1 /data
```

Kiểm tra:

``` bash
findmnt /data
df -h /data
```

Sau setup, HDD có khoảng:

``` text
Size: ~916G
Available: ~870G
Filesystem: ext4
Mount: /data
```

Chênh lệch giữa dung lượng quảng cáo 1 TB và dung lượng hiển thị trong
Linux là bình thường, ngoài ra ext4 cũng dành một phần không gian cho
filesystem/reserved blocks.

------------------------------------------------------------------------

## 11. Auto-mount bằng `/etc/fstab`

Đây là một trong những phần quan trọng nhất của setup.

Mở:

``` bash
sudo nano /etc/fstab
```

Thêm entry dạng:

``` fstab
UUID=<UUID-cua-partition-data> /data ext4 defaults,nofail 0 2
```

UUID lấy bằng:

``` bash
lsblk -f
```

hoặc:

``` bash
sudo blkid
```

Sau khi sửa `fstab`:

``` bash
sudo mkdir -p /data
sudo systemctl daemon-reload
sudo mount -a
```

Kiểm tra:

``` bash
findmnt /data
```

`mount -a` nên chạy không lỗi trước khi reboot.

### Vì sao dùng UUID?

Tên `/dev/sdX` **không ổn định**.

Trong quá trình setup, HDD từng xuất hiện dưới tên:

``` text
/dev/sda1
```

nhưng sau reboot nó xuất hiện thành:

``` text
/dev/sdb1
```

Dù vậy:

``` bash
findmnt /data
```

vẫn cho thấy `/data` mount đúng HDD.

Đây chính là lợi ích của:

``` fstab
UUID=... /data ...
```

thay vì:

``` fstab
/dev/sda1 /data ...
```

Linux có thể thay đổi thứ tự nhận diện USB/SATA disk giữa các lần boot.
UUID thuộc filesystem nên ổn định hơn tên device node.

**Kết luận:** dùng UUID trong `fstab`, không hardcode `/dev/sda1`.

------------------------------------------------------------------------

## 12. Lỗi đã gặp khi cấu hình `/data`

Lần đầu chạy:

``` bash
sudo mount -a
```

gặp:

``` text
mount: /data: mount point does not exist
```

Nguyên nhân: thư mục `/data` chưa tồn tại.

Fix:

``` bash
sudo mkdir -p /data
sudo systemctl daemon-reload
sudo mount -a
```

Sau đó:

``` bash
findmnt /data
```

mount thành công.

Bài học: entry trong `fstab` không tự tạo mount-point directory.

------------------------------------------------------------------------

## 13. Quyền truy cập `/data`

Để user quản trị có thể ghi dữ liệu mà không phải dùng `sudo` cho mọi
thao tác:

``` bash
sudo chown <user>:<user> /data
```

Test:

``` bash
touch /data/test.txt
ls -l /data/test.txt
rm /data/test.txt
```

Nếu không báo lỗi, quyền cơ bản hoạt động.

Về sau nếu nhiều service/container cần quyền khác nhau thì nên quản lý
UID/GID và permissions theo từng service thay vì mở quyền quá rộng như
`chmod 777`.

------------------------------------------------------------------------

## 14. Kiểm chứng auto-mount sau reboot

Sau khi hoàn tất `fstab`:

``` bash
sudo reboot
```

SSH lại:

``` bash
ssh <user>@macmini
```

Kiểm tra:

``` bash
findmnt /data
df -h /data
```

Kết quả thực tế sau reboot:

``` text
/data  → ext4
rw,relatime
```

và HDD vẫn được mount đúng dù device node đã đổi.

Đây là kiểm chứng quan trọng cho thấy cấu hình `fstab` hoạt động thực sự
chứ không chỉ mount được trong phiên hiện tại.

------------------------------------------------------------------------

## 15. Layout storage nên dùng tiếp

Một layout đơn giản cho home server:

``` text
/data/
├── docker/
│   ├── compose/
│   └── appdata/
├── media/
├── downloads/
└── backups/
```

Không nhất thiết phải tạo toàn bộ ngay lập tức. Chỉ tạo directory khi
service thực sự cần.

### Vai trò của SSD và HDD

### SSD 120 GB

Nên chứa:

-   Xubuntu;
-   package hệ thống;
-   Docker Engine;
-   executable/application layer;
-   dữ liệu cần I/O nhanh và nhỏ nếu cần.

### HDD 1 TB

Nên chứa:

-   media;
-   downloads;
-   backups;
-   Docker persistent data phù hợp;
-   file lớn;
-   dữ liệu không yêu cầu random I/O cao.

Cần cân nhắc từng database trước khi đặt database workload nặng lên HDD
cơ học.

------------------------------------------------------------------------

## 16. Wi-Fi Broadcom BCM4360

Mac mini sử dụng:

``` text
Broadcom BCM4360
PCI ID: 14e4:43a0
```

Xubuntu ban đầu không tạo WLAN interface.

Hướng xử lý đã xác định là proprietary Broadcom STA driver. Với
Ubuntu/Xubuntu 26.04, package đáng thử khi cần:

``` bash
sudo apt update
sudo apt install broadcom-sta-dkms
sudo reboot
```

Tuy nhiên phần Wi-Fi **chưa được xác nhận hoàn tất** trong setup này.

Vì server hiện đã có networking đủ dùng cho SSH/Tailscale, Wi-Fi không
phải blocker cho phần storage/Docker.

------------------------------------------------------------------------

## 17. Những thứ đã verified

-   Xubuntu boot từ SSD ngoài.
-   Root filesystem nằm trên SSD 120 GB.
-   SSH vào Mac mini hoạt động.
-   Tailscale hoạt động giữa laptop và Mac mini.
-   Có thể SSH bằng hostname `macmini`.
-   Mac mini reboot và quay lại online ở chế độ headless.
-   HDD Apple 1 TB cũ đã được xóa sau khi xác nhận không cần dữ liệu.
-   HDD đã chuyển từ APFS sang ext4.
-   HDD mount tại `/data`.
-   `fstab` bằng UUID hoạt động.
-   `/data` vẫn tự mount sau reboot.
-   Device name có thể đổi qua reboot nhưng UUID mount vẫn hoạt động.

------------------------------------------------------------------------

## 18. Những thứ chưa làm / chưa verified

-   Docker Engine chưa cài.
-   Docker Compose chưa cấu hình.
-   Chưa triển khai service self-host đầu tiên.
-   Chưa xây backup strategy hoàn chỉnh.
-   Wi-Fi BCM4360 chưa xác nhận hoạt động.
-   Chưa thực hiện security hardening sâu hơn cho SSH.
-   Chưa thiết kế quyền UID/GID cho Docker volumes.

------------------------------------------------------------------------

## 19. Nguyên tắc cần nhớ cho các bước sau

### Không tin `/dev/sda` là một disk cố định

Luôn kiểm tra:

``` bash
lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,MOUNTPOINTS
```

trước thao tác destructive.

### Mount persistent bằng UUID

Ưu tiên:

``` fstab
UUID=... /data ext4 ...
```

không dùng:

``` fstab
/dev/sda1 /data ext4 ...
```

### Test trước khi reboot

Sau khi sửa `fstab`:

``` bash
sudo mount -a
```

Nếu có lỗi, sửa trước khi reboot.

### Test sau reboot

Một cấu hình server chưa thực sự hoàn tất cho tới khi reboot và kiểm tra
lại service/storage.

### Không mở SSH port ra Internet nếu không cần

Với mô hình hiện tại, Tailscale đã cung cấp đường quản trị từ xa phù hợp
mà không cần expose TCP/22 trực tiếp trên router.

### Backup vẫn cần thiết

RAID, filesystem hay việc có HDD riêng không tự động trở thành backup.

Nếu `/data` chứa dữ liệu quan trọng, cần có ít nhất một bản sao độc lập
ở nơi khác.

------------------------------------------------------------------------

## Bước tiếp theo

Sau trạng thái hiện tại, thứ tự hợp lý là:

``` text
1. Storage                  ✅
2. Headless SSH/Tailscale   ✅
3. Reboot verification      ✅
4. Docker Engine            ← tiếp theo
5. Docker Compose
6. Test container
7. Reboot + verify Docker
8. Deploy service đầu tiên
9. Backup + monitoring
```

Không cần cài Portainer hay nhiều service cùng lúc. Nên cài Docker
Engine đúng cách trước, chạy một container test, kiểm chứng sau reboot
rồi mới bắt đầu self-host các ứng dụng thật.
