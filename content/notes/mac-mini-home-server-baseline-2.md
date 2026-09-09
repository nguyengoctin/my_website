---
title: Baseline vận hành home server Mac mini 2014 với Ubuntu, Tailscale, Docker và SMART phần 2
date: 2026-09-09T23:21:00+07:00
aliases:
  - mac-mini-home-server-baseline
tags:
  - homelab
  - ubuntu
  - docker
  - tailscale
  - smartmontools
---

> Baseline quan trọng nhất: giữ service private qua Tailscale, để Docker chỉ khởi động sau khi Tailscale thật sự online, giới hạn log để tránh đầy SSD, dùng `smartd` để theo dõi disk và gửi cảnh báo ra Telegram. Những phần chưa cần thiết như backup automation hay auto-update container nên để sau khi có dữ liệu và workload thực sự đáng bảo vệ.

## Trạng thái hệ thống đã xác minh

Environment tại thời điểm hoàn tất baseline:

```text
Hardware: Apple Macmini7,1
OS: Ubuntu 26.04.1 LTS
Kernel: Linux 7.0.0-31-generic
RAM: 7.6 GiB
Swap: 4 GiB
Timezone: Asia/Ho_Chi_Minh
Network chính: Wi-Fi
User: ngoctin
Tailscale IP: 100.124.234.108
```

Storage hiện tại:

```text
/dev/sda1 -> /
/dev/sdb1 -> /data
```

Lưu ý: tên `/dev/sda` và `/dev/sdb` đã đổi sau reboot so với một số kiểm tra trước đó. Không nên dùng device letter như một định danh cố định cho disk trong script dài hạn.

Mount persistent của `/data` trong `/etc/fstab`:

```fstab
UUID=45f76020-9e21-4e50-a9c4-24af82c1c8bd /data ext4 defaults,nofail 0 2
```

Cấu trúc dữ liệu:

```text
/data
├── backups
├── docker
│   ├── appdata
│   └── compose
├── media
│   ├── movies
│   ├── music
│   └── tv
├── projects
└── sync
```

Các thư mục trên thuộc `ngoctin:ngoctin`.

## Convention triển khai Docker

Docker baseline:

```text
Docker Engine: 29.8.0
Docker Compose: v5.5.1
Storage driver: overlayfs
Cgroup: systemd, v2
Logging driver: json-file
```

`ngoctin` đã thuộc group `docker`, nên:

```bash
docker ps
```

chạy không cần `sudo`.

Convention đang dùng:

```text
Docker image/layer/runtime     -> SSD hệ điều hành
Persistent app data           -> /data/docker/appdata
Compose files                 -> /data/docker/compose
Published private service     -> bind trực tiếp vào Tailscale IP
```

Ví dụ:

```yaml
services:
  web:
    image: nginx:alpine
    container_name: hello-web
    restart: unless-stopped
    ports:
      - "100.124.234.108:8080:80"
```

Đã xác minh từ một máy khác trong Tailnet rằng:

```text
http://100.124.234.108:8080
```

trả HTTP 200.

Quyết định hiện tại là không bind service vào `0.0.0.0` nếu không cần thiết. Mặc định giữ private qua Tailscale.

## Service đang chạy

Uptime Kuma:

```text
Compose:
  /data/docker/compose/uptime-kuma

Persistent data:
  /data/docker/appdata/uptime-kuma

Port:
  100.124.234.108:3001
```

n8n:

```text
Compose:
  /data/docker/compose/n8n

Persistent data:
  /data/docker/appdata/n8n

Port:
  100.124.234.108:5678
```

n8n hiện dùng HTTP bên trong Tailnet nên cấu hình:

```text
N8N_SECURE_COOKIE=false
```

Cấu hình này chỉ phù hợp với trạng thái hiện tại. Nếu n8n chuyển sang HTTPS thì phải xem lại và không mặc định giữ `N8N_SECURE_COOKIE=false`.

## Docker log rotation

Docker dùng `json-file`, nhưng đã có rotation ở daemon level:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

File:

```text
/etc/docker/daemon.json
```

Ý nghĩa vận hành:

- mỗi log file tối đa khoảng 10 MB;
- giữ tối đa 3 file cho mỗi container;
- tránh trường hợp container ghi log nhiều làm đầy SSD hệ điều hành.

Không cần thay đổi thêm khi chưa có bằng chứng cấu hình hiện tại gây vấn đề.

## Race condition khi reboot: Docker lên trước Tailscale

### Triệu chứng

Reboot verification đầu tiên cho thấy:

```text
Docker: active
Tailscale IP: đã xuất hiện sau boot
Containers: không chạy
```

Docker log có lỗi:

```text
failed to bind host port 100.124.234.108:3001/tcp:
cannot assign requested address
```

### Root cause đã xác minh

Service được bind trực tiếp vào:

```text
100.124.234.108
```

nhưng Docker khởi động trước khi Tailscale hoàn tất việc đưa IP này lên interface `tailscale0`.

Docker mặc định có:

```ini
After=network-online.target ...
Wants=network-online.target ...
```

nhưng `network-online.target` không đảm bảo Tailscale IP riêng đã sẵn sàng.

Ubuntu/Tailscale trên máy đã có:

```text
tailscale-online.target
tailscale-wait-online.service
```

`tailscale-online.target`:

```ini
[Unit]
Description=Tailscale is online
Requires=tailscale-wait-online.service
After=tailscale-wait-online.service
```

### Fix

Không sửa trực tiếp unit file package ở:

```text
/usr/lib/systemd/system/docker.service
```

Thay vào đó tạo systemd drop-in:

```text
/etc/systemd/system/docker.service.d/override.conf
```

Nội dung:

```ini
[Unit]
Wants=tailscale-online.target
After=tailscale-online.target
```

Tạo bằng:

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d

printf '%s\n' \
'[Unit]' \
'Wants=tailscale-online.target' \
'After=tailscale-online.target' \
| sudo tee /etc/systemd/system/docker.service.d/override.conf >/dev/null

sudo systemctl daemon-reload
```

Verification:

```bash
systemctl show docker.service -p Wants -p After
```

Đã xác minh thấy:

```text
Wants=tailscale-online.target network-online.target containerd.service
```

và `After=` có `tailscale-online.target`.

### Vì sao cần cả `Wants=` và `After=`

`After=` chỉ tạo ordering nếu unit liên quan thật sự được đưa vào transaction.

`Wants=tailscale-online.target` kéo target này vào dependency graph.

`After=tailscale-online.target` đảm bảo Docker chỉ chạy sau target đó.

Mental model:

```text
Boot
  ↓
tailscaled
  ↓
tailscale-wait-online.service
  ↓
tailscale-online.target
  ↓
docker.service
  ↓
containers bind vào 100.124.234.108
```

Không dùng `sleep 10` hoặc delay cứng vì dependency systemd đã giải quyết đúng bản chất race condition.

### Verification sau fix

Sau reboot lần hai:

- `/data` mount thành công;
- `tailscale0` có `100.124.234.108`;
- SSH qua Tailscale hoạt động;
- Docker active;
- Uptime Kuma và n8n tự chạy lại;
- không có failed unit đáng kể;
- không còn lỗi `cannot assign requested address`.

Đây là verification quan trọng nhất của baseline 24/7.

## SSH và firewall

SSH đã harden:

```text
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
```

Login bằng ED25519 public key qua Tailscale đã hoạt động.

UFW:

```text
Default incoming: deny
Default outgoing: allow
```

Rule quản trị private:

```text
ALLOW IN on tailscale0
```

Caveat quan trọng: Docker tự quản lý firewall/NAT rules cho published ports. Không được suy luận rằng `ufw deny incoming` tự động bảo vệ mọi port do Docker publish.

Vì vậy convention bind trực tiếp vào Tailscale IP vẫn là một lớp kiểm soát đáng giữ.

## SMART monitoring

`smartctl`:

```text
smartctl 7.5
```

`smartmontools.service` đã:

```text
enabled
active (running)
```

smartd tự phát hiện và monitor cả hai disk.

Config active trong:

```text
/etc/smartd.conf
```

là:

```text
DEVICESCAN -d removable -n standby -m root -M exec /usr/share/smartmontools/smartd-runner
```

`smartd-runner`:

```sh
#!/bin/sh -e

run-parts --report --lsbsysinit -- /etc/smartmontools/run.d
```

Nghĩa là alert handler có thể được mở rộng bằng cách thêm executable script vào:

```text
/etc/smartmontools/run.d/
```

### HDD baseline

HDD 1 TB:

```text
APPLE HDD HTS541010A9E662
```

SMART đã xác minh:

```text
Reallocated_Sector_Ct    = 3
Current_Pending_Sector   = 0
Offline_Uncorrectable    = 0
UDMA_CRC_Error_Count     = 0
```

Interpretation cần giữ: số `3` không tự nó chứng minh disk sắp chết; điều cần theo dõi là xu hướng theo thời gian, đặc biệt nếu `Reallocated_Sector_Ct` tăng hoặc xuất hiện pending/uncorrectable sectors.

Cả SSD và HDD đều từng báo SMART overall health PASSED.

Không tự diễn giải các vendor-specific attribute lạ vì model không nằm trong smartctl database.

### Device letter không ổn định

Sau reboot, mapping đã thay đổi so với baseline trước đó.

Tại thời điểm kiểm tra sau reboot:

```text
/dev/sda = Kingmax SSD 120 GB
/dev/sdb = APPLE HDD 1 TB
```

Không viết monitoring script dài hạn dựa vào giả định:

```text
/dev/sda luôn là HDD
```

Nếu sau này cần script riêng, ưu tiên nhận diện qua model/serial hoặc `/dev/disk/by-id/`.

## SMART alert qua Telegram

Handler mặc định:

```text
/etc/smartmontools/run.d/10mail
```

yêu cầu:

```text
/usr/bin/mail
```

nhưng hệ thống không có `mail`, `mailx` hoặc `sendmail`.

Do đó mail path mặc định không tạo ra notification hữu ích trên server headless.

Quyết định: không cài cả mail stack chỉ để phục vụ SMART alert. Thay vào đó, thêm Telegram notification handler chạy trực tiếp từ smartd.

Secret:

```text
/etc/smartmontools/telegram.env
```

Quyền:

```text
root:root
0600
```

Nội dung dạng:

```text
BOT_TOKEN=<secret>
CHAT_ID=<telegram-chat-id>
```

Token không nên lưu trong shell history hoặc log.

Handler:

```text
/etc/smartmontools/run.d/20telegram
```

Script:

```sh
#!/bin/sh

set -u

. /etc/smartmontools/telegram.env

MESSAGE="⚠️ SMART warning on $(hostname)

${SMARTD_SUBJECT:-SMART alert}

Device: ${SMARTD_DEVICE:-unknown}
Failure: ${SMARTD_FAILTYPE:-unknown}

${SMARTD_FULLMESSAGE:-${SMARTD_MESSAGE:-No details}}"

curl --fail --silent --show-error \
  --max-time 15 \
  --data-urlencode "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" \
  "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  >/dev/null
```

Quyền executable:

```bash
sudo chmod 700 /etc/smartmontools/run.d/20telegram
```

Mail handler cũ được giữ lại nhưng bỏ executable vì hiện không có mail command:

```bash
sudo chmod -x /etc/smartmontools/run.d/10mail
```

### Test handler riêng

Đã test bằng environment giả:

```bash
sudo env \
  SMARTD_SUBJECT="SMART test notification" \
  SMARTD_DEVICE="/dev/test" \
  SMARTD_FAILTYPE="TEST" \
  SMARTD_FULLMESSAGE="This is a test notification from Mac mini home server." \
  /etc/smartmontools/run.d/20telegram
```

Telegram nhận thành công.

### Test end-to-end qua smartd

Đã tạm thêm:

```text
-M test
```

vào dòng `DEVICESCAN`, restart smartmontools và xác minh Telegram nhận alert qua toàn bộ chain:

```text
smartd
  ↓
smartd-runner
  ↓
run-parts
  ↓
20telegram
  ↓
Telegram
```

Sau test, `-M test` đã được bỏ lại để tránh gửi notification mỗi lần daemon start.

Trạng thái cuối: SMART monitoring + alert hoạt động.

## Update strategy

`unattended-upgrades.service`:

```text
enabled
active (running)
```

APT periodic:

```text
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

Allowed origins có Ubuntu release/security và các security origin tương ứng.

Hai timer:

```text
apt-daily.timer
apt-daily-upgrade.timer
```

đều đang tồn tại.

Tại thời điểm kiểm tra:

```text
No reboot currently required
```

Không có cấu hình active bật auto reboot. Các dòng `Automatic-Reboot` thấy trong `50unattended-upgrades` đều đang là comment.

Policy đã chọn:

```text
Ubuntu security update   -> tự động
Auto reboot              -> không
Docker image auto-update -> không
Reboot                   -> thủ công, có kiểm soát
```

Không bật auto-update container như Watchtower ở baseline hiện tại. Lý do: server ưu tiên ổn định và khả năng debug hơn việc tự kéo image mới không kiểm soát.

Khi thấy:

```text
/var/run/reboot-required
```

thì xem đó là tín hiệu lên lịch reboot, không phải lý do reboot ngay lập tức.

## Backup strategy

Tại thời điểm kiểm tra, dữ liệu persistent còn rất nhỏ:

```text
/data/docker/appdata   5.8M
/data/docker/compose   28K
/data/projects         4.0K
/data/sync             4.0K
/data/media            16K
```

Quyết định hiện tại: chưa dựng backup automation vì server mới, chưa có dữ liệu đáng kể.

Dữ liệu đáng ưu tiên backup khi bắt đầu sử dụng thật:

```text
/data/docker/appdata
/data/docker/compose
/data/projects
/data/sync
```

Media nên có strategy riêng khi dung lượng tăng.

Không cần backup Docker images/layers vì có thể pull hoặc build lại.

### Caveat quan trọng

```text
/data/backups
```

nằm trên cùng HDD với `/data`.

Do đó nó không bảo vệ khỏi failure vật lý của HDD.

Một disaster backup đúng nghĩa phải đi sang thiết bị/storage độc lập, ví dụ ThinkPad, external drive hoặc cloud.

ThinkPad hiện là một candidate backup target trong tương lai.

## Disk health và nhiệt độ baseline

SSD:

```text
Kingmax SSD 120 GB
SMART overall health: PASSED
Temperature từng đo: 33°C
Extended self-test từng completed without error
```

HDD:

```text
APPLE HDD HTS541010A9E662
1 TB
5400 rpm
SMART overall health: PASSED
Temperature từng đo: 35°C
```

Thermal baseline của Mac mini:

```text
CPU Package ~47°C
Core 0 ~45°C
Core 1 ~47°C
Fan ~1805 RPM
```

Đây là baseline để so sánh về sau, không phải threshold cảnh báo.

## Wi-Fi và workload

Network chính hiện vẫn là Wi-Fi.

Broadcom proprietary driver `wl` có kernel warning/taint, nhưng chưa quan sát thấy lỗi chức năng liên quan.

Không thay đổi driver chỉ để làm sạch warning khi hệ thống đang ổn.

Nếu sau này chạy workload có traffic lớn hoặc kéo dài như:

```text
Jellyfin
large file transfer
backup
sync
```

thì Ethernet đáng cân nhắc vì ổn định hơn cho server 24/7.

## Những việc chưa hoàn tất

Không nên chất thêm homelab app trước khi có nhu cầu thực tế.

Các bước hợp lý tiếp theo:

```text
1. Cấu hình Uptime Kuma chỉ cho các monitor thực sự hữu ích.
2. Nối Uptime Kuma vào Telegram hoặc notification channel độc lập.
3. Tạo workflow n8n đầu tiên có giá trị thực tế.
4. Khi bắt đầu có dữ liệu quan trọng, triển khai backup sang thiết bị độc lập.
5. Theo dõi Reallocated_Sector_Ct của HDD xem có tăng khỏi baseline 3 không.
6. Cân nhắc Ethernet khi workload network nặng xuất hiện.
```

Không cần:

```text
- đổi config chỉ để "best practice hóa";
- expose service ra Internet;
- auto-update container không kiểm soát;
- dựng backup system phức tạp khi chưa có dữ liệu;
- cài thêm app chỉ để làm đầy homelab dashboard.
```

## Checklist phục hồi sau reboot

Nếu server có vấn đề sau một lần reboot, kiểm tra theo thứ tự:

```bash
uptime
```

```bash
findmnt /data
df -h / /data
```

```bash
tailscale status
ip addr show tailscale0 | grep 'inet '
```

```bash
systemctl status tailscale-online.target --no-pager
systemctl status tailscale-wait-online.service --no-pager
```

```bash
systemctl status docker --no-pager
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

```bash
systemctl --failed --no-pager
```

Nếu container bind vào Tailscale IP fail với:

```text
cannot assign requested address
```

thì kiểm tra drop-in:

```bash
systemctl cat docker.service
```

và:

```bash
systemctl show docker.service -p Wants -p After
```

Docker phải có dependency vào:

```text
tailscale-online.target
```

## References

Nguồn chính thức đã được dùng trong quá trình xác minh behavior của Tailscale/systemd:

- Tailscale CLI reference, phần liên quan `tailscale wait` và cơ chế chờ Tailscale online: https://tailscale.com/docs/reference/tailscale-cli
