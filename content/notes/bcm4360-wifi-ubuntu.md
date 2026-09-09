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

> Trên Mac mini 2014 đã thử nghiệm, Xubuntu nhận Broadcom BCM4360 `14e4:43a0` qua PCI nhưng không tạo WLAN interface. Evidence từ tài liệu Ubuntu và package inventory của Xubuntu 26.04 hướng đến Broadcom STA (`wl`) qua `broadcom-sta-dkms`; cần chú ý DKMS và kernel headers đúng với kernel đang chạy.

## Chẩn đoán trước khi cài driver

```bash
lspci -nnk | grep -A3 -i network
rfkill list
ip link
nmcli device
```

Case đã thử:

```text
Broadcom BCM4360 802.11ac
PCI ID: 14e4:43a0
revision: 03
```

Hardware vẫn xuất hiện trong `lspci`, nhưng WLAN interface không xuất hiện và `rfkill` chỉ thấy Bluetooth. Đây khác với trường hợp interface tồn tại nhưng bị soft-block.

## Driver được chọn

Với PCI ID `14e4:43a0`, hướng được chọn là Broadcom STA:

```text
kernel module: wl
package: broadcom-sta-dkms
```

Không mặc định cài `firmware-b43-installer` chỉ vì thiết bị là Broadcom. PCI ID quan trọng hơn tên vendor chung.

## Khi máy có Internet

Ưu tiên APT:

```bash
sudo apt update
sudo apt install broadcom-sta-dkms
sudo reboot
```

Sau reboot:

```bash
lspci -nnk | grep -A3 -i network
nmcli device
lsmod | grep '^wl'
```

Mục tiêu là `wl` được build/load và WLAN interface xuất hiện.

> Trong setup được ghi lại, việc cài driver trên installed system chưa được xác minh đến bước kết nối Wi-Fi thành công. Vì vậy đây là hướng sửa có evidence tốt, không phải claim “đã fix” của chính máy.

## DKMS là dependency quan trọng

Kiểm tra package dependency trong môi trường đã dùng cho thấy `broadcom-sta-dkms` phụ thuộc `dkms`.

Do đó chỉ copy `broadcom-sta-dkms_*.deb` sang một máy offline có thể chưa đủ.

Kiểm tra:

```bash
dpkg -s dkms
```

## Kernel headers phải khớp kernel đang chạy

```bash
uname -r
ls -ld /lib/modules/$(uname -r)/build
```

Trong case này:

```text
running kernel: 7.0.0-31-generic
```

và build path cho running kernel tồn tại.

Trong khi ISO Xubuntu 26.04 được kiểm tra lại chứa headers `7.0.0-14`. Đây là trap quan trọng:

```text
headers có trong installer ISO ≠ headers của running kernel
```

Không cài headers cũ chỉ vì chúng nằm sẵn trong ISO.

## Nếu buộc phải làm offline

ISO đã kiểm tra có:

```text
broadcom-sta-dkms_6.30.223.271-29ubuntu1_amd64.deb
dkms_3.2.2-1ubuntu1_all.deb
linux-firmware-broadcom-wireless_20260319.git217ca6e4-0ubuntu1_all.deb
```

Trước khi mang package sang:

```bash
uname -r
dpkg -s dkms
ls -ld /lib/modules/$(uname -r)/build
```

Nếu có thể tạo Internet tạm thời thì APT thường đơn giản và ít lỗi dependency hơn chuỗi `.deb` thủ công.

## USB tethering làm bootstrap network

Cắm Android bằng cáp data và bật USB tethering, rồi kiểm tra:

```bash
nmcli device
ping -c 3 google.com
```

Nếu có Internet, quay về:

```bash
sudo apt update
sudo apt install broadcom-sta-dkms
```

Việc điện thoại chia sẻ Wi-Fi hay mobile data phụ thuộc thiết bị/cấu hình, nên kiểm tra thay vì giả định.

## Hardware hay software?

`lspci` vẫn nhận đúng BCM4360 và cùng máy trước đó từng có Wi-Fi hoạt động trên Ubuntu khác. Điều này khiến driver/software trở thành nghi phạm hợp lý hơn hardware failure.

Đây là inference, không phải hardware diagnostic hoàn chỉnh.

## Failure modes đáng nhớ

- Cài `b43` chỉ vì thấy chữ Broadcom.
- Copy mỗi Broadcom `.deb` mà quên DKMS.
- Cài headers từ ISO mà không kiểm tra `uname -r`.
- Chỉ chạy `rfkill unblock` khi WLAN interface còn chưa tồn tại.
- Kết luận card hỏng chỉ vì GUI không có nút Wi-Fi.

## Checklist

```text
[ ] lspci thấy hardware
[ ] Ghi PCI ID
[ ] rfkill/nmcli/ip link kiểm tra interface
[ ] Xác định driver theo PCI ID
[ ] uname -r
[ ] build path cho running kernel tồn tại
[ ] DKMS có sẵn
[ ] Cài driver qua APT nếu có thể
[ ] Reboot
[ ] Kiểm tra wl/module
[ ] WLAN interface xuất hiện
[ ] Test kết nối Wi-Fi thật
```

## Nguồn

- Ubuntu Community Help Wiki — Broadcom wireless: https://help.ubuntu.com/community/WifiDocs/Driver/bcm43xx
- Ubuntu package information — `broadcom-sta-dkms`: https://packages.ubuntu.com/resolute/admin/broadcom-sta-dkms
- Ubuntu bug-report mirror về case Xubuntu 26.04 + BCM4360 `14e4:43a0`: https://www.mail-archive.com/ubuntu-bugs%40lists.ubuntu.com/msg6282293.html

Bug report cuối chỉ là supporting evidence cho môi trường tương tự, không phải guarantee cho mọi máy.
