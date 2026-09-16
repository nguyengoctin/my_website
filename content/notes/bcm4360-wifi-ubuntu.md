---
title: "Sửa Wi-Fi Broadcom BCM4360 trên Ubuntu/Xubuntu"
date: 2026-09-09T14:15:00+07:00
aliases:
  - BCM4360 Ubuntu
  - Broadcom Wi-Fi Linux
tags:
  - ubuntu
  - xubuntu
  - wifi
  - broadcom
  - mac-mini
---

> [!NOTE]
> **Tóm tắt:** Trên Mac mini 2014, Xubuntu nhận Broadcom BCM4360 `14e4:43a0` qua PCI nhưng không tạo WLAN interface. Nguyên nhân là kernel không load đúng driver — không phải hardware lỗi. Giải pháp là cài `broadcom-sta-dkms` (module `wl`) đúng PCI ID, đảm bảo DKMS biên dịch module khớp kernel đang chạy.

## Bản chất

Broadcom BCM4360 là chip Wi-Fi 802.11ac xuất hiện trên một số máy Mac đời này. Với PCI ID `14e4:43a0` trong setup này, driver `b43` không hỗ trợ thiết bị theo bảng support của Linux Wireless; driver Broadcom STA `wl` từ `broadcom-sta-dkms` là path đã được dùng và xác minh hoạt động trên máy.

DKMS (Dynamic Kernel Module Support) là hệ thống tự động biên dịch lại kernel module mỗi khi kernel được cập nhật. Không có DKMS, module chỉ chạy được trên đúng kernel đã build lần đầu.

Ba driver family thường xuất hiện khi xử lý Broadcom trên Linux, nhưng support phải kiểm tra theo **PCI ID**, không theo tên “Broadcom” chung:

- `wl` từ `broadcom-sta-dkms`: driver Broadcom STA proprietary; đây là driver đã được dùng và xác minh với `14e4:43a0` trong setup này.
- `b43`: driver open-source cho một tập thiết bị Broadcom khác; bảng support upstream đánh dấu `14e4:43a0` là không hỗ trợ.
- `brcmfmac`: driver in-tree cho các Broadcom FullMAC device; material này không có evidence rằng nó hỗ trợ PCI ID `14e4:43a0`.

## Vì sao lựa chọn

**Tại sao dùng `broadcom-sta-dkms` thay vì `b43` hay `brcmfmac`?**

PCI ID `14e4:43a0` tra trong [Ubuntu Broadcom Wiki](https://help.ubuntu.com/community/WifiDocs/Driver/bcm43xx) chỉ thẳng đến `broadcom-sta-dkms`. Hai driver còn lại không hỗ trợ chip này:

- Bảng support của `b43` đánh dấu PCI ID `14e4:43a0` (BCM4360) là không hỗ trợ và ghi `wl` là alternative.
- `brcmfmac` không phải driver đã được xác minh cho PCI ID này trong material của setup, nên không dùng nó làm phương án thay thế chỉ dựa vào tên Broadcom.

**Đánh đổi khi dùng `broadcom-sta-dkms`:**

- Driver độc quyền — không audit được source, phụ thuộc Broadcom release
- Mỗi lần kernel update, DKMS phải biên dịch lại (tự động nếu kernel headers đúng)
- Không hỗ trợ monitor mode hay packet injection

Trong setup đã ghi nhận, `broadcom-sta-dkms` là phương án đã được xác minh hoạt động cho `14e4:43a0`. Không mở rộng observation này thành claim rằng mọi kernel, distro hoặc packaging khác đều chỉ có một lựa chọn.

## Cơ chế hoạt động

Luồng từ phần cứng đến WLAN interface:

```text
Hardware BCM4360 (PCIe)
    │
    ▼
Kernel phát hiện qua lspci / udev
    │
    ▼
Kernel tìm module phù hợp (wl.ko)
    │  ← DKMS build wl.ko từ source Broadcom
    │    khớp với kernel version đang chạy
    ▼
modprobe wl load module
    │
    ▼
Driver tạo WLAN interface (wlan0 / wlp...)
    │
    ▼
NetworkManager nhận interface
    │
    ▼
Kết nối Wi-Fi
```

Tại sao interface không xuất hiện dù `lspci` thấy hardware: kernel biết có chip BCM4360 nhưng không có module `wl.ko` nào được build cho kernel đang chạy — hoặc module bị conflict với `b43` hay `bcma`.

## Hướng dẫn từng bước

### Bước 1 — Chẩn đoán phần cứng

```bash
lspci -nnk | grep -A3 -i network
```

- `-nn` — in cả tên thiết bị lẫn PCI ID dạng `[vendor:device]`
- `-k` — hiện kernel module đang dùng và có thể dùng cho device đó
- `-A3` — in thêm 3 dòng sau mỗi match (để thấy đủ thông tin chip)
- `-i network` — lọc chỉ thiết bị network

Kết quả mong đợi:

```text
02:00.0 Network controller [0280]: Broadcom BCM4360 802.11ac [14e4:43a0] (rev 03)
    Subsystem: Apple Inc. BCM4360 802.11ac [106b:0117]
    Kernel driver in use: (none)
    Kernel modules: wl, bcma
```

Nếu thấy `Kernel driver in use: (none)` — xác nhận thiếu driver.

```bash
rfkill list
```

- Kiểm tra Wi-Fi có bị soft-block (software) hay hard-block (nút vật lý) không

```bash
ip link
```

- Liệt kê tất cả network interface — xác nhận không có interface `wlan0` hay `wlp`

### Bước 2 — Xác minh kernel và headers

```bash
uname -r
```

- In kernel version đang chạy — phải khớp với headers sẽ cài

```bash
ls -ld /lib/modules/$(uname -r)/build
```

- Kiểm tra build symlink cho running kernel có tồn tại không
- DKMS cần đường dẫn này để biết nơi chứa kernel headers

### Bước 3 — Cài driver (có Internet)

```bash
sudo apt update
sudo apt install broadcom-sta-dkms
```

`apt install broadcom-sta-dkms` sẽ tự động:
1. Pull `dkms` nếu chưa có
2. Kéo kernel headers khớp running kernel
3. Chạy `dkms build` và `dkms install` để build `wl.ko`

```bash
sudo reboot
```

Reboot để kernel load module sạch, tránh conflict với module cũ còn trong memory.

### Bước 4 — Xác minh sau reboot

```bash
lsmod | grep '^wl'
```

- `lsmod` — liệt kê kernel modules đang loaded
- `grep '^wl'` — lọc module tên bắt đầu bằng `wl`

```bash
lspci -nnk | grep -A3 -i network
```

Lần này mong đợi `Kernel driver in use: wl`.

```bash
nmcli device
```

- Kiểm tra NetworkManager đã nhận WLAN interface chưa

### Nếu không có Internet — làm offline

Kiểm tra dependencies trước khi mang file sang:

```bash
dpkg -s dkms
# Kiểm tra DKMS đã cài chưa

uname -r
# Ghi lại kernel version

ls -ld /lib/modules/$(uname -r)/build
# Xác minh build path cho running kernel
```

Các file cần mang theo từ ISO Xubuntu 26.04:

```text
broadcom-sta-dkms_6.30.223.271-29ubuntu1_amd64.deb
dkms_3.2.2-1ubuntu1_all.deb
linux-firmware-broadcom-wireless_20260319.git217ca6e4-0ubuntu1_all.deb
```

Cài:

```bash
sudo dpkg -i dkms_*.deb broadcom-sta-dkms_*.deb
```

- `dpkg -i` — cài trực tiếp từ file `.deb`, không qua APT

### Bootstrap Internet tạm bằng USB tethering

Cắm Android bằng cáp data, bật USB tethering trong Settings, rồi kiểm tra:

```bash
nmcli device
# Tìm interface usb0 hoặc enp... kiểu ethernet

ping -c 3 8.8.8.8
# -c 3 — gửi đúng 3 gói rồi dừng
```

Nếu ping được, quay lại Bước 3 và dùng APT bình thường.

## Bẫy lỗi và Những lần thử thất bại

**Bẫy 1 — Cài `b43` chỉ vì thấy "Broadcom"**

Nhiều hướng dẫn cũ trên Internet gợi ý `firmware-b43-installer` cho mọi chip Broadcom. `b43` không hỗ trợ BCM4360. Kết quả: cài xong không có gì thay đổi, tốn thời gian debug.

**Bẫy 2 — Mang `broadcom-sta-dkms.deb` mà quên `dkms.deb`**

DKMS là hard dependency. Nếu `dkms` chưa có trên máy offline, `dpkg -i broadcom-sta-dkms.deb` báo lỗi dependency và không cài được. Phải mang đủ cả hai gói.

**Bẫy 3 — Dùng kernel headers từ ISO thay vì headers khớp running kernel**

ISO Xubuntu 26.04 chứa `linux-headers-7.0.0-14`, nhưng kernel đang chạy sau cài đặt và update là `7.0.0-31`. DKMS build `wl.ko` cho `7.0.0-14` — module này không load được trên `7.0.0-31`. Không cài headers từ ISO nếu không kiểm tra `uname -r` trước.

**Bẫy 4 — Chạy `rfkill unblock all` khi interface chưa tồn tại**

`rfkill` chỉ unblock interface đã được tạo ra. Nếu module `wl` chưa load, không có interface nào để unblock. Phải fix driver trước, rfkill sau.

**Bẫy 5 — Kết luận hardware hỏng quá sớm**

`lspci` thấy hardware nhưng interface không có → không đồng nghĩa card hỏng. Card hỏng thật thì `lspci` cũng không thấy. Đây là symptom thiếu driver, không phải hardware failure.

## Kiểm tra và Xác minh

Sau khi cài xong và reboot, chạy theo thứ tự:

```bash
lsmod | grep '^wl'
```

Phải thấy module `wl` đang loaded. Nếu không có gì — DKMS chưa build được, kiểm tra `dkms status`.

```bash
dkms status
```

Phải thấy `broadcom-sta/6.30.223.271, <kernel-version>: installed`. Nếu thấy `built` nhưng không `installed`, chạy `sudo dkms install broadcom-sta/6.30.223.271`.

```bash
lspci -nnk | grep -A3 -i network
```

`Kernel driver in use:` phải là `wl`.

```bash
nmcli device
```

Phải thấy một device type `wifi` với interface `wlan0` hoặc `wlp*`. Nếu status là `unavailable` — module loaded nhưng có vấn đề khác (thử `sudo modprobe -r wl && sudo modprobe wl`).

Kết nối thử một Wi-Fi network và `ping -c 3 8.8.8.8` để xác minh end-to-end.

## Nguồn tham khảo

- [Ubuntu Community Help Wiki — Broadcom wireless drivers](https://help.ubuntu.com/community/WifiDocs/Driver/bcm43xx)  
  *(bảng PCI ID → driver mapping chính xác nhất, là nguồn đầu tiên nên tra)*
- [Ubuntu package tracker — `broadcom-sta-dkms`](https://packages.ubuntu.com/resolute/broadcom-sta-dkms)  
  *(xem dependencies chính xác, changelog, supported architectures)*
- DKMS man page: `man dkms`  
  *(giải thích `dkms build`, `dkms install`, `dkms status` và cơ chế hoạt động)*
- [Bug report thực tế — Xubuntu 26.04 + BCM4360 `14e4:43a0`](https://www.mail-archive.com/ubuntu-bugs%40lists.ubuntu.com/msg6282293.html)  
  *(supporting evidence cho môi trường tương tự, không phải guarantee)*
- [Linux Wireless: b43 support table](https://wireless.docs.kernel.org/en/latest/en/users/drivers/b43.html)
- [Ubuntu package: broadcom-sta-dkms](https://packages.ubuntu.com/resolute/broadcom-sta-dkms)
