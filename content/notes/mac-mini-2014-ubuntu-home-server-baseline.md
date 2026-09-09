---
title: "Chuẩn hóa Mac mini 2014 thành home server Ubuntu với Docker, Tailscale và UFW"
date: 2026-09-09T22:44:00+07:00
aliases:
  - "Mac mini 2014 home server"
  - "Ubuntu home server baseline"
tags:
  - home-server
  - ubuntu
  - docker
  - tailscale
  - ufw
---

> Home server này được chuẩn hóa theo hướng đơn giản và dễ vận hành: Ubuntu làm host, Tailscale làm đường quản trị private, UFW chặn incoming mặc định, Docker chạy application layer, còn dữ liệu bền vững được tách sang `/data`. Trước khi thêm nhiều service, cần ưu tiên boot persistence, disk health, SSH, firewall, logging và backup.

## Trạng thái đã xác minh

Environment thực tế tại thời điểm setup:

```text
Hardware:        Apple Macmini7,1
OS:              Ubuntu 26.04.1 LTS
Kernel:          Linux 7.0.0-31-generic
Architecture:    x86-64
Timezone:        Asia/Ho_Chi_Minh
RAM:             7.6 GiB
Swap:            4 GiB
OS disk:         Kingmax SSD 120GB
Data disk:       APPLE HDD HTS541010A9E662 1TB, 5400 rpm
Docker Engine:   29.8.0
Docker Compose:  5.5.1
```

Clock đã đồng bộ NTP:

```text
System clock synchronized: yes
NTP service: active
RTC in local TZ: no
```

`systemctl --failed` trả về:

```text
0 loaded units listed.
```

Tại thời điểm kiểm tra, RAM idle chỉ dùng khoảng `628 MiB`, còn khoảng `7.0 GiB available`, swap chưa được dùng.

## Storage layout và boot persistence

Ổ hệ điều hành:

```text
/dev/sdb1  ext4   /
/dev/sdb2  vfat   /boot/efi
```

Ổ data:

```text
/dev/sda1  ext4   /data
```

`/data` được mount bằng UUID trong `/etc/fstab`:

```fstab
UUID=45f76020-9e21-4e50-a9c4-24af82c1c8bd /data ext4 defaults,nofail 0 2
```

Ý nghĩa thực tế của decision này:

- dùng UUID thay vì `/dev/sda1` để tránh phụ thuộc tên device có thể đổi;
- `nofail` cho phép hệ thống tiếp tục boot nếu data disk vắng hoặc mount lỗi;
- pass `2` cho phép filesystem data được `fsck` sau root filesystem.

Root filesystem và EFI trong `fstab`:

```fstab
/dev/disk/by-uuid/a5dd75c0-e19d-4973-a2d9-76135202f03f / ext4 defaults 0 1
/dev/disk/by-uuid/1F6C-FC99 /boot/efi vfat defaults 0 1
/swap.img none swap sw 0 0
```

## Cấu trúc `/data`

Để tránh Docker data, media, backup và source code nằm lẫn lộn, cấu trúc đã được tạo:

```text
/data
├── backups
├── docker
│   ├── appdata
│   └── compose
├── lost+found
├── media
│   ├── movies
│   ├── music
│   └── tv
├── projects
└── sync
```

Ownership:

```text
/data                ngoctin:ngoctin
/data/backups        ngoctin:ngoctin
/data/docker         ngoctin:ngoctin
/data/media          ngoctin:ngoctin
/data/projects       ngoctin:ngoctin
/data/sync           ngoctin:ngoctin
/data/lost+found     root:root
```

`lost+found` thuộc root và không cần chỉnh permission. Đây là thư mục ext4 dành cho filesystem recovery.

Decision quan trọng: chưa chuyển Docker data root mặc định khỏi `/var/lib/docker`. OS disk là SSD và còn nhiều dung lượng trống, nên image/layer/runtime của Docker để trên SSD; persistent app data lớn mới bind mount sang `/data`.

## SMART và sức khỏe ổ đĩa

### HDD 1 TB `/dev/sda`

Do HDD đi qua bridge nên `smartctl --scan` ban đầu nhận dạng là SCSI:

```text
/dev/sda -d scsi
```

Với `-d scsi`, SMART bị báo unavailable. Tuy nhiên bridge vẫn hỗ trợ ATA passthrough, nên dùng:

```bash
sudo smartctl -a -d sat /dev/sda
```

đã đọc được SMART đầy đủ.

Thông tin chính:

```text
Device Model:               APPLE HDD HTS541010A9E662
Capacity:                   1.00 TB
Rotation Rate:              5400 rpm
SMART overall-health:       PASSED
Power_On_Hours:             8623
Temperature:                35°C
Reallocated_Sector_Ct:      3
Reallocated_Event_Count:    3
Current_Pending_Sector:     0
Offline_Uncorrectable:      0
UDMA_CRC_Error_Count:       0
SMART Error Log:            No Errors Logged
```

Kết luận: HDD vẫn dùng được cho data, nhưng đã có `3` reallocated sectors nên cần theo dõi theo thời gian.

Điều quan trọng không phải chỉ là giá trị `3`, mà là xu hướng:

```text
3 -> 3 -> 3
```

ổn hơn nhiều so với:

```text
3 -> 8 -> 20 -> 50
```

Nếu `Current_Pending_Sector` hoặc `Offline_Uncorrectable` tăng trên `0`, hoặc số reallocated sector tăng dần, cần xem đó là tín hiệu ổ đang xuống cấp.

Model này không nằm trong smartctl database hiện tại:

```text
Device is: Not in smartctl database 7.5/5706
```

Do đó không nên diễn giải cứng các vendor-specific raw attribute bất thường như:

```text
Power-Off_Retract_Count = 60129542272
```

SMART short test:

```bash
sudo smartctl -t short -d sat /dev/sda
sudo smartctl -l selftest -d sat /dev/sda
```

SMART extended test:

```bash
sudo smartctl -t long -d sat /dev/sda
sudo smartctl -l selftest -d sat /dev/sda
```

Ổ báo extended test khoảng `258` phút.

### SSD 120 GB `/dev/sdb`

Command:

```bash
sudo smartctl -a -d sat /dev/sdb
```

Thông tin chính:

```text
Device Model:               Kingmax SSD 120GB
Capacity:                   120 GB
SMART overall-health:       PASSED
Power_On_Hours:             8830
Temperature:                33°C
Raw_Read_Error_Rate:        0
SMART Error Log:            No Errors Logged
Extended offline test:      Completed without error
TRIM Command:               Available
```

SSD cũng không nằm trong smartctl database hiện tại:

```text
Device is: Not in smartctl database 7.5/5706
```

Vì vậy các field như `Unknown_Attribute`, `Unknown_SSD_Attribute` hoặc raw value của `Total_LBAs_Written` không nên tự suy diễn thành phần trăm health nếu chưa có mapping chính xác của controller.

Một số short self-test cũ có trạng thái:

```text
Aborted by host
```

Điều này không đủ để kết luận SSD lỗi. Extended self-test trước đó đã hoàn thành mà không có error.

## Thermal baseline

`sensors` đọc được `coretemp` và `applesmc`.

Các giá trị đáng tin và đã quan sát:

```text
CPU Package:  47°C
Core 0:       45°C
Core 1:       47°C
Fan:          1805 RPM
Fan min:      1800 RPM
Fan max:      4800 RPM
```

Đây là baseline idle/light-load hợp lý cho máy.

`applesmc` expose nhiều Apple SMC key có giá trị vô lý, ví dụ:

```text
TC0G:   +93.0°C
TCPG:   +98.0°C
TH0A:  -127.0°C
TCXr:   -55.8°C
```

Không nên coi các giá trị này là nhiệt độ phần cứng thực tế khi chúng mâu thuẫn rõ với `coretemp` và fan speed. Với máy này, ưu tiên quan sát `Package id 0`, từng CPU core và fan RPM.

Theo dõi realtime:

```bash
watch -n 2 sensors
```

hoặc dùng:

```bash
btop
```

## SSH hardening

SSH service đã active và enabled. Login thực tế đã được xác minh bằng ED25519 public key qua Tailscale.

Trước hardening:

```text
permitrootlogin prohibit-password
pubkeyauthentication yes
passwordauthentication yes
```

Một drop-in riêng đã được dùng thay vì sửa toàn bộ file chính:

```text
/etc/ssh/sshd_config.d/99-hardening.conf
```

Nội dung:

```text
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
```

Procedure an toàn:

```bash
sudo sshd -t
sudo systemctl reload ssh
```

`sshd -t` phải không trả lỗi trước khi reload.

Sau thay đổi, verification:

```bash
sudo sshd -T | grep -E 'passwordauthentication|permitrootlogin|pubkeyauthentication'
```

Kết quả đã xác minh:

```text
permitrootlogin no
pubkeyauthentication yes
passwordauthentication no
```

Không nên đóng SSH session hiện tại trước khi mở một terminal thứ hai và xác minh login bằng key vẫn hoạt động.

## Tailscale và mô hình truy cập private

Tailscale service:

```text
tailscaled.service active (running)
```

Tailscale IP của Mac mini tại thời điểm setup:

```text
100.124.234.108
```

SSH client đã kết nối từ Tailnet IP:

```text
100.113.175.1
```

Mental model được chọn:

```text
Client
  │
  │ Tailscale
  ▼
tailscale0
  │
  ▼
Mac mini
```

Home server không cần expose SSH ra Internet công khai. Tailscale là đường quản trị private chính.

## UFW

UFW được chọn làm host firewall với policy:

```text
Default incoming: deny
Default outgoing: allow
```

Traffic từ Tailscale được allow:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow in on tailscale0
sudo ufw enable
```

Verification:

```bash
sudo ufw status verbose
```

Trạng thái đã xác minh:

```text
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), deny (routed)

Anywhere on tailscale0       ALLOW IN    Anywhere
Anywhere (v6) on tailscale0  ALLOW IN    Anywhere (v6)
```

Sau khi enable UFW, phải giữ SSH session cũ mở và test một SSH session mới qua Tailscale. Nếu bị lockout, rollback từ session cũ:

```bash
sudo ufw disable
```

## Kernel và Wi‑Fi caveat

`journalctl -p 3 -b` gần như sạch, chỉ có:

```text
wpa_supplicant: bgscan simple: Failed to enable signal strength monitoring
```

Wi‑Fi vẫn hoạt động, nên chưa có bằng chứng lỗi chức năng cần sửa.

`dmesg` có warning đáng chú ý liên quan Broadcom proprietary driver:

```text
wl: loading out-of-tree module taints kernel.
wl: module license 'MIXED/Proprietary' taints kernel.
Unpatched return thunk in use. This should not happen!
```

Call trace đi qua module `wl`.

Hardware được nhận:

```text
Broadcom BCM43a0 802.11 Hybrid Wireless Controller
```

Kernel taint ở đây không đồng nghĩa kernel bị malware hoặc hỏng; nó cho biết proprietary/out-of-tree module đang được load.

Các warning khác đã thấy nhưng chưa có bằng chứng gây lỗi thực tế:

```text
[Firmware Bug]: Corrupted DMI table
hpet_acpi_add: no address or irqs in _CRS
usb ... device-initiated U1 failed
thunderbolt ... device link creation ... failed
applesmc ... hwmon_device_register() is deprecated
```

Không sửa các warning này chỉ để làm log sạch. Chỉ điều tra tiếp nếu có symptom tương ứng.

Server hiện dùng Wi‑Fi:

```text
wlp2s0   UP
enp3s0f0 DOWN
```

Ethernet vẫn là lựa chọn tốt hơn về độ ổn định và throughput nếu sau này chạy workload như Jellyfin, file sync hoặc backup lớn, nhưng Wi‑Fi hiện tại vẫn đủ để tiếp tục setup.

## Docker Engine và Compose

Docker được cài từ repository chính thức của Docker cho Ubuntu `resolute`.

Repository:

```text
/etc/apt/sources.list.d/docker.sources
```

Nội dung:

```text
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: resolute
Components: stable
Architectures: amd64
Signed-By: /etc/apt/keyrings/docker.asc
```

Packages đã cài:

```text
docker-ce
docker-ce-cli
containerd.io
docker-buildx-plugin
docker-compose-plugin
docker-ce-rootless-extras
```

Version đã xác minh:

```text
Docker Engine: 29.8.0
Docker Compose: v5.5.1
```

Docker service:

```text
docker.service active (running)
enabled
```

Verification đầu tiên:

```bash
sudo docker run hello-world
sudo docker compose version
```

`hello-world` đã trả:

```text
Hello from Docker!
```

### Docker permissions

User `ngoctin` đã được thêm vào group `docker`:

```bash
sudo usermod -aG docker ngoctin
newgrp docker
```

Verification:

```bash
docker ps
docker run --rm hello-world
```

đã chạy không cần `sudo`.

Caveat: membership trong group `docker` có quyền rất mạnh trên host và về thực tế có thể dẫn tới quyền tương đương root thông qua Docker daemon. Không nên xem đây là một permission group bình thường.

## Docker runtime baseline

`docker info`:

```text
Server Version: 29.8.0
Storage Driver: overlayfs
Logging Driver: json-file
Cgroup Driver: systemd
Cgroup Version: 2
```

Docker bridge:

```text
docker0
172.17.0.1/16
```

Khi chưa có container chạy, `docker0` có thể hiện:

```text
NO-CARRIER
state DOWN
```

Đây không phải lỗi nếu Docker daemon và container networking vẫn hoạt động bình thường.

Docker đã tạo các nftables/iptables-nft chain như:

```text
DOCKER
DOCKER-USER
DOCKER-FORWARD
DOCKER-BRIDGE
DOCKER-CT
DOCKER-INTERNAL
```

## Docker và UFW: caveat quan trọng

Host có UFW `deny incoming`, nhưng không nên suy ra mọi published Docker port sẽ tự động bị UFW chặn theo cùng cách như host service thông thường.

Docker tự quản lý firewall/NAT rules để publish container ports.

Vì vậy với service chỉ dành cho bản thân qua Tailnet, convention được chọn là bind port trực tiếp vào Tailscale IP thay vì `0.0.0.0`.

Ví dụ:

```yaml
ports:
  - "100.124.234.108:8080:80"
```

thay vì:

```yaml
ports:
  - "8080:80"
```

Mental model:

```text
100.124.234.108:8080
        │
        ▼
container:80
```

Điều này giúp service private chỉ listen trên host Tailscale address thay vì mọi interface.

Cần xem lại strategy này nếu Tailscale IP thay đổi, nếu chuyển sang MagicDNS/reverse proxy, nếu muốn expose trên LAN, hoặc nếu service được publish ra Internet qua Cloudflare Tunnel/reverse proxy.

## Docker logging

Docker hiện dùng:

```text
Logging Driver: json-file
```

Với server chạy lâu dài, container log không nên để tăng vô hạn.

Config được đề xuất cho `/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Validation:

```bash
python3 -m json.tool /etc/docker/daemon.json
```

Sau đó:

```bash
sudo systemctl restart docker
docker info | grep 'Logging Driver'
systemctl is-active docker
```

Trong context hiện tại chưa có output xác minh rằng config log rotation này đã được áp dụng, nên cần kiểm tra lại trước khi coi là hoàn tất.

## Compose test với Nginx

Project test:

```text
/data/docker/compose/hello-web
```

Compose:

```yaml
services:
  web:
    image: nginx:alpine
    container_name: hello-web
    restart: unless-stopped
    ports:
      - "100.124.234.108:8080:80"
```

Validation:

```bash
docker compose config
```

Lifecycle đã được test:

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose stop
docker compose start
docker compose restart
docker compose down
```

Browser từ client Tailscale đã truy cập thành công:

```text
http://100.124.234.108:8080
```

Nginx log xác nhận:

```text
100.113.175.1 ... "GET / HTTP/1.1" 200
```

`favicon.ico` trả `404` chỉ vì default nginx page không có favicon, không phải lỗi service.

`docker compose down` đã xóa:

```text
Container hello-web
Network hello-web_default
```

Bài test này xác minh end-to-end:

```text
Docker Hub image
      ↓
container
      ↓
container port 80
      ↓
host Tailscale IP :8080
      ↓
browser trên Tailnet
```

## Uptime Kuma

Uptime Kuma được chọn làm service thật đầu tiên vì nhẹ và hữu ích để monitor các service sau này.

Directories:

```text
/data/docker/compose/uptime-kuma
/data/docker/appdata/uptime-kuma
```

Compose:

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:2
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - "100.124.234.108:3001:3001"
    volumes:
      - /data/docker/appdata/uptime-kuma:/app/data
```

Persistent data của container `/app/data` được bind sang:

```text
/data/docker/appdata/uptime-kuma
```

Database được chọn trong setup UI:

```text
SQLite
```

Lý do: một instance home server nhỏ chưa cần thêm PostgreSQL/MariaDB chỉ để vận hành monitoring.

Truy cập private:

```text
http://100.124.234.108:3001
```

Một monitor HTTP có thể dùng để tự kiểm tra Uptime Kuma:

```text
URL: http://100.124.234.108:3001
Heartbeat Interval: 60s
```

Caveat quan trọng: Uptime Kuma nằm trên cùng Mac mini nên không thể báo khi cả server mất điện hoặc mất mạng hoàn toàn. Muốn monitor host từ bên ngoài cần một external monitor độc lập.

## n8n

n8n đã được triển khai sau Uptime Kuma.

Directories:

```text
/data/docker/compose/n8n
/data/docker/appdata/n8n
```

Compose đã dùng:

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "100.124.234.108:5678:5678"
    environment:
      - TZ=Asia/Ho_Chi_Minh
      - GENERIC_TIMEZONE=Asia/Ho_Chi_Minh
      - N8N_SECURE_COOKIE=false
    volumes:
      - /data/docker/appdata/n8n:/home/node/.n8n
```

Truy cập private:

```text
http://100.124.234.108:5678
```

`N8N_SECURE_COOKIE=false` chỉ được dùng vì n8n hiện đang truy cập qua HTTP trên Tailnet.

Decision này phải được xem lại nếu n8n chuyển sang HTTPS, reverse proxy hoặc Cloudflare Tunnel. Khi có HTTPS, không nên tiếp tục giữ secure cookie bị tắt chỉ vì config cũ.

n8n hiện đang dùng SQLite mặc định trong persistent state directory. Chưa có lý do thực tế trong context hiện tại để thêm PostgreSQL chỉ để làm setup phức tạp hơn.

## Mental model vận hành

Kiến trúc hiện tại:

```text
Mac mini 2014
│
├── Ubuntu 26.04.1 LTS
│
├── systemd
│
├── SSD 120 GB
│   ├── /
│   └── Docker runtime / images / layers
│
├── HDD 1 TB
│   └── /data
│       ├── docker/appdata
│       ├── docker/compose
│       ├── media
│       ├── backups
│       ├── sync
│       └── projects
│
├── Network
│   ├── Wi-Fi
│   └── Tailscale
│
├── Security
│   ├── SSH key only
│   ├── root SSH disabled
│   └── UFW deny incoming
│
└── Docker
    ├── Uptime Kuma
    └── n8n
```

Application lifecycle nên được nghĩ theo ba lớp:

```text
compose.yml
    ↓
container
    ↓
persistent data trên /data
```

`docker compose down` xóa container/network của project nhưng persistent bind-mounted data trong `/data/docker/appdata/...` vẫn tồn tại.

## Verification checklist sau reboot

Một home server chỉ thật sự ổn khi reboot xong tự phục hồi được.

Sau reboot, kiểm tra:

```bash
findmnt /data
systemctl is-active ssh
systemctl is-active tailscaled
sudo ufw status
systemctl is-active docker
docker ps
```

Mục tiêu:

```text
/data mounted          yes
SSH                    active
Tailscale              active
UFW                    active
Docker                 active
Uptime Kuma            running
n8n                    running
```

Do các container dùng:

```yaml
restart: unless-stopped
```

chúng phải tự trở lại sau khi Docker daemon khởi động, trừ khi trước đó container đã bị stop chủ động.

## Những việc chưa nên coi là hoàn tất

### Backup

`/data/backups` nằm trên cùng HDD với `/data/docker/appdata`.

Do đó:

```text
/data/docker/appdata
/data/backups
```

không tạo thành backup độc lập nếu `/dev/sda` chết.

Trước khi lưu ảnh, tài liệu quan trọng, database hoặc workflow khó tái tạo, cần thêm ít nhất một bản copy nằm ngoài HDD này.

### Docker log rotation

Config log rotation đã được đề xuất nhưng chưa có output xác minh đã apply.

### SMART automation

SMART đã được đọc thủ công nhưng chưa có procedure định kỳ hoặc alert nếu các counter xấu tăng.

Đặc biệt cần theo dõi:

```text
Reallocated_Sector_Ct
Current_Pending_Sector
Offline_Uncorrectable
```

trên HDD `/dev/sda`.

### Wi-Fi

Server hiện vẫn phụ thuộc Broadcom `wl` proprietary driver. Không cần thay đổi nếu ổn định, nhưng Ethernet nên được cân nhắc khi server bắt đầu làm file server, streaming hoặc backup thường xuyên.

## Tooling hữu ích

Các package đã được khuyến nghị cho server terminal:

```bash
sudo apt install \
  curl wget git \
  vim nano \
  htop btop \
  tree jq \
  unzip rsync \
  ncdu fzf \
  lm-sensors \
  smartmontools
```

Các command có giá trị vận hành thực tế:

```bash
btop
df -h
free -h
ncdu /data
ss -tulpn
systemctl --failed
journalctl
sensors
smartctl
docker ps
docker compose ps
docker compose logs
```

Starship và zoxide là tiện ích UX, không phải server baseline. Cài khi cần, nhưng không nên ưu tiên hơn health, firewall, backup và observability.

## References

- Docker Engine on Ubuntu: https://docs.docker.com/engine/install/ubuntu/
- Docker Linux post-installation steps: https://docs.docker.com/engine/install/linux-postinstall/
- Docker Compose on Linux: https://docs.docker.com/compose/install/linux/
- Tailscale Linux install: https://tailscale.com/docs/install/linux
- Tailscale Ubuntu/UFW guidance: https://tailscale.com/docs/how-to/secure-ubuntu-server-with-ufw
- Tailscale firewall integration: https://tailscale.com/docs/integrations/firewalls
- Ubuntu `sshd_config` manual: https://manpages.ubuntu.com/manpages/noble/man5/sshd_config.5.html
- Ubuntu `systemd.mount` manual: https://manpages.ubuntu.com/manpages/resolute/man5/systemd.mount.5.html
- Ubuntu `smartctl` manual: https://manpages.ubuntu.com/manpages/resolute/man8/smartctl.8.html
- Uptime Kuma repository: https://github.com/louislam/uptime-kuma
- n8n Docker installation: https://docs.n8n.io/hosting/installation/docker/
