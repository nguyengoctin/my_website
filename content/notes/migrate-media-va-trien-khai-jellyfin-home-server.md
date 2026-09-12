---
title: "Migrate thư viện TV sang home server và triển khai Jellyfin bằng Docker"
date: 2026-09-10T14:22:00+07:00
aliases:
  - jellyfin-home-server
  - media-server-mac-mini
tags:
  - jellyfin
  - docker
  - home-server
  - tailscale
  - rsync
---

> [!TLDR]
> Với một home server đơn giản chỉ có một HDD dữ liệu, cách triển khai hiệu quả là giữ media thành thư viện chuẩn trên `/data/media/tv`, mount read-only vào Jellyfin container, dùng `Shows` làm loại library cho TV series, và truy cập từ xa qua Tailscale thay vì public port trực tiếp.

## Trạng thái cuối cùng

Jellyfin đã chạy trên Mac mini Ubuntu bằng Docker Compose và đọc được thư viện TV từ HDD.

Data flow thực tế:

```text
Laptop
  │
  │ rsync qua SSH/Tailscale
  ▼
Mac mini
  │
  ├── /data/media/tv              # media trên HDD
  │
  └── Docker
       └── Jellyfin
            └── /media/tv:ro      # bind mount read-only
```

Library được tổ chức theo series và season:

```text
/data/media/tv/
├── Friends (1994)/
│   ├── Season 01/
│   ├── Season 02/
│   └── ...
├── Silicon Valley (2014)/
│   ├── Season 01/
│   └── ...
└── The Office (US) (2005)/
    ├── Season 01/
    └── ...
```

Jellyfin phải tạo library với:

```text
Content type: Shows
Folder: /media/tv
```

Không dùng `Movies` cho cấu trúc này. Khi từng episode bị hiện thành hàng trăm movie riêng lẻ, nguyên nhân trong lần setup này là library đã được tạo nhầm với `Content type = Movies`.

---

## Environment đã xác minh

Server:

```text
Hardware: Apple Mac mini Late 2014 (Macmini7,1)
OS: Ubuntu 26.04.1 LTS
Kernel: Linux 7.0.0-31-generic
User: ngoctin
UID: 1000
GID: 1000
```

Storage:

```text
/dev/sda1 -> /        # Kingmax SSD 120GB
/dev/sdb1 -> /data    # Apple HDD 1TB 5400 rpm, ext4
```

Media cuối cùng:

```text
/data/media/tv
```

Quyền thư mục đã xác minh:

```text
drwxr-xr-x ngoctin ngoctin /data/media/tv
```

User `ngoctin` thuộc group `docker`, nên có thể chạy Docker CLI không cần `sudo`.

Tailscale đã được cài và server có thể được truy cập qua tailnet. SSH đã được cấu hình key-only từ trước.

---

## Quyết định kiến trúc

### Media nằm trên HDD

Media là workload chủ yếu đọc tuần tự và dung lượng lớn, nên đặt trên HDD 1TB:

```text
/data/media/tv
```

Với vài stream cá nhân, HDD 5400 rpm phù hợp hơn việc tiêu tốn SSD chỉ để chứa video.

Không triển khai RAID, ZFS, mergerfs hay SSD cache cho media trong setup hiện tại vì chỉ có một HDD dữ liệu và workload chưa cần các lớp phức tạp đó.

### Jellyfin chỉ được đọc media

Bind mount media bằng `:ro`:

```yaml
- /data/media/tv:/media/tv:ro
```

Điều này tách quyền quản lý ứng dụng khỏi dữ liệu gốc. Jellyfin có thể scan và stream nhưng không được sửa/xóa file media qua mount này.

### Truy cập từ xa bằng Tailscale

Không mở trực tiếp port Jellyfin ra Internet qua router.

Mô hình hiện tại:

```text
Client ngoài nhà
   │
   │ Tailscale
   ▼
Mac mini
   │
   └── Jellyfin :8096
```

Port `8096` là cổng HTTP mặc định mà Jellyfin lắng nghe trong setup này.

Với người khác, nên share riêng node `macmini` bằng Tailscale Machine Sharing thay vì cho họ tham gia toàn bộ tailnet. Người xem vẫn nên có một Jellyfin user riêng.

---

## Chuẩn hóa thư viện trước khi đưa vào Jellyfin

Source ban đầu trên laptop có cấu trúc riêng cho video và VTT:

```text
data/
├── videos/
│   ├── friends/
│   ├── silicon_valley/
│   └── the_office/
└── subtitles/bilingual/VTT/
    ├── friends/
    ├── silicon_valley/
    └── the_office/
```

Jellyfin dễ nhận diện TV series hơn khi video và external subtitle của cùng episode nằm cạnh nhau dưới series/season tương ứng.

Đích cuối:

```text
Series/
└── Season 01/
    ├── Series_S01E01.mp4
    ├── Series_S01E01.vtt
    ├── Series_S01E02.mp4
    └── Series_S01E02.vtt
```

Tên series/year như `Friends (1994)` và `Silicon Valley (2014)` giúp metadata matcher phân biệt title tốt hơn. Đây là convention hữu ích, không phải điều kiện tuyệt đối để Jellyfin chạy.

---

## Migrate dữ liệu bằng rsync

### Kiểm tra dung lượng trước khi copy

Trên laptop:

```bash
du -sh .
du -sh videos
du -sh subtitles
du -sh videos/*
```

Trên server:

```bash
ssh macmini
df -h /data
```

### Tạo staging trên server

```bash
mkdir -p /data/media/tv-import/videos
mkdir -p /data/media/tv-import/subtitles
mkdir -p /data/media/tv
```

### Copy video và subtitle

Chạy từ laptop tại thư mục chứa `videos/` và `subtitles/`:

```bash
rsync -avh --info=progress2 --partial \
  videos/ \
  macmini:/data/media/tv-import/videos/

rsync -avh --info=progress2 --partial \
  subtitles/bilingual/VTT/ \
  macmini:/data/media/tv-import/subtitles/
```

Các option đáng nhớ:

- `-a`: archive mode, giữ cấu trúc và metadata file phù hợp.
- `-v`: verbose.
- `-h`: kích thước dễ đọc.
- `--info=progress2`: hiển thị tiến độ toàn bộ transfer.
- `--partial`: giữ partial file khi transfer bị ngắt để lần sau có thể tiếp tục hiệu quả hơn.

`rsync` được chọn thay cho `scp -r` vì migration media lớn có thể bị ngắt và cần resume/re-run.

Không dùng `--checksum` trong mỗi lần copy thông thường vì nó buộc rsync hash toàn bộ source và destination để quyết định file nào thay đổi. Có thể dùng checksum ở bước verification cuối khi muốn kiểm tra mạnh hơn.

---

## Verification sau transfer

So sánh dung lượng và file count ở hai phía trước khi xóa source trên laptop.

Laptop:

```bash
du -sh videos
du -sh subtitles/bilingual/VTT
find videos -type f | wc -l
find subtitles/bilingual/VTT -type f | wc -l
```

Server:

```bash
du -sh /data/media/tv-import/videos
du -sh /data/media/tv-import/subtitles
find /data/media/tv-import/videos -type f | wc -l
find /data/media/tv-import/subtitles -type f | wc -l
```

Có thể chạy dry-run checksum comparison từ laptop:

```bash
rsync -avhnc videos/ macmini:/data/media/tv-import/videos/
rsync -avhnc subtitles/bilingual/VTT/ macmini:/data/media/tv-import/subtitles/
```

Trong đó:

- `-n`: dry run, không sửa gì.
- `-c`: so sánh bằng checksum.

Nếu không còn changed-file cần transfer thì source/destination khớp theo phép so sánh của rsync.

Không xóa bản laptop trước khi:
- transfer đã verify;
- Jellyfin nhìn thấy library;
- đã phát thử một số episode;
- cấu trúc series/season đã đúng.

---

## Merge staging vào layout Jellyfin

Một lỗi thực tế trong lần migrate này là dùng:

```bash
seq -w 1 5
```

với giả định output sẽ là:

```text
01 02 03 04 05
```

Nhưng khi số lớn nhất chỉ có một digit, output thực tế là:

```text
1 2 3 4 5
```

Hậu quả: script tìm `season_1` thay vì `season_01`, tạo destination `Season 1` thay vì `Season 01`, và không move được video.

Cách ổn định hơn là format explicit:

```bash
for i in $(seq 1 5); do
    n=$(printf "%02d" "$i")
    ...
done
```

### Friends

Destination:

```text
/data/media/tv/Friends (1994)/Season XX
```

### Silicon Valley

Destination:

```text
/data/media/tv/Silicon Valley (2014)/Season XX
```

Script sửa sau lỗi `seq -w`:

```bash
for i in $(seq 1 5); do
    n=$(printf "%02d" "$i")

    correct="/data/media/tv/Silicon Valley (2014)/Season $n"
    wrong="/data/media/tv/Silicon Valley (2014)/Season $i"

    mkdir -p "$correct"

    if [ -d "$wrong" ] && [ "$wrong" != "$correct" ]; then
        find "$wrong" -maxdepth 1 -type f -exec mv -t "$correct" -- {} +
        rmdir "$wrong" 2>/dev/null || true
    fi

    video_dir="/data/media/tv-import/videos/silicon_valley/season_$n"

    if [ -d "$video_dir" ]; then
        find "$video_dir" -maxdepth 1 -type f -exec mv -t "$correct" -- {} +
    fi
done
```

### The Office

Destination:

```text
/data/media/tv/The Office (US) (2005)/Season XX
```

Pattern đã dùng:

```bash
for i in $(seq 1 9); do
    n=$(printf "%02d" "$i")
    dest="/data/media/tv/The Office (US) (2005)/Season $n"

    mkdir -p "$dest"

    video_dir="/data/media/tv-import/videos/the_office/season_$n"
    if [ -d "$video_dir" ]; then
        find "$video_dir" -maxdepth 1 -type f -exec mv -t "$dest" -- {} +
    fi

    sub_dir=$(find /data/media/tv-import/subtitles/the_office \
        -maxdepth 1 -type d -name "*${n}" -print -quit)

    if [ -n "$sub_dir" ]; then
        find "$sub_dir" -maxdepth 1 -type f -exec mv -t "$dest" -- {} +
    fi
done
```

`find ... -exec mv` được dùng thay cho:

```bash
mv "$dir/"*
```

vì cách dùng glob có thể báo `cannot stat ... *` khi directory rỗng và xử lý kém hơn với một số edge case.

---

## Caveat về tên có `\_`

Trong staging xuất hiện directory được `ls` hiển thị như:

```text
season\_01
season\_02
...
```

Điều này làm script hard-code `season_01` không match ở nhánh subtitle.

Cách tránh phụ thuộc chính xác vào phần prefix trong trường hợp đó:

```bash
sub_dir=$(find /data/media/tv-import/subtitles/<series> \
    -maxdepth 1 -type d -name "*${n}" -print -quit)
```

Trước khi kết luận tên file thực sự chứa backslash, nên kiểm tra bằng shell-safe representation:

```bash
printf '%q\n' /data/media/tv-import/subtitles/friends/*
```

`ls` có thể escape ký tự trong output, nên output hiển thị không phải lúc nào cũng phản ánh literal filename theo cách dễ đọc bằng mắt.

---

## Audit media sau khi merge

### Episode có video nhưng thiếu VTT

```bash
find /data/media/tv -type f -name '*.mp4' -print0 |
while IFS= read -r -d '' video; do
    base="${video%.mp4}"
    if [ ! -f "${base}.vtt" ]; then
        echo "Missing subtitle: $video"
    fi
done
```

Kết quả thực tế:

```text
Missing subtitle: /data/media/tv/Silicon Valley (2014)/Season 02/SiliconValley_S02E07.mp4
Missing subtitle: /data/media/tv/The Office (US) (2005)/Season 03/TheOffice_S03E05.mp4
```

### VTT không có video tương ứng

```bash
find /data/media/tv -type f -name '*.vtt' -print0 |
while IFS= read -r -d '' sub; do
    base="${sub%.vtt}"
    if [ ! -f "${base}.mp4" ]; then
        echo "Missing video: $sub"
    fi
done
```

Kết quả thực tế:

```text
Missing video: /data/media/tv/Silicon Valley (2014)/Season 03/SiliconValley_S03E02.vtt
```

Tổng tại thời điểm audit:

```text
465 MP4
464 VTT
150G /data/media/tv
```

Ba mismatch trên không ngăn Jellyfin scan và phát phần còn lại của library.

---

## Permission của media

User chạy container là:

```text
uid=1000(ngoctin)
gid=1000(ngoctin)
```

Permission được chuẩn hóa bằng:

```bash
sudo chown -R ngoctin:ngoctin /data/media/tv
find /data/media/tv -type d -exec chmod 755 {} \;
find /data/media/tv -type f -exec chmod 644 {} \;
```

Không dùng:

```bash
chmod -R 777
```

Jellyfin chỉ cần khả năng traverse directory và đọc file media.

---

## Docker Compose của Jellyfin

Compose directory:

```bash
mkdir -p /data/docker/compose/jellyfin
cd /data/docker/compose/jellyfin
```

Appdata đang dùng trong triển khai thực tế:

```bash
mkdir -p /data/docker/appdata/jellyfin/config
mkdir -p /data/docker/appdata/jellyfin/cache
```

Lưu ý: `/data` nằm trên HDD trong server hiện tại, nên config/cache của Jellyfin cũng đang ở HDD. Trước đó có cân nhắc đặt config/cache trên SSD để workload small-file nhanh hơn, nhưng chưa thực hiện migration đó. Không nên mô tả setup hiện tại như thể appdata đã nằm trên SSD.

`compose.yaml`:

```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: jellyfin

    user: "1000:1000"

    ports:
      - "8096:8096"

    volumes:
      - /data/docker/appdata/jellyfin/config:/config
      - /data/docker/appdata/jellyfin/cache:/cache
      - /data/media/tv:/media/tv:ro

    restart: unless-stopped
```

Ý nghĩa quan trọng:

```text
Host path                 Container path
/data/media/tv       ->   /media/tv
```

Do đó trong Jellyfin UI phải add:

```text
/media/tv
```

Không phải:

```text
/data/media/tv
```

Container không tự nhìn thấy filesystem của host; nó chỉ thấy những path được bind mount vào namespace của nó.

### Validate và start

```bash
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail=50 jellyfin
```

### Xác minh container nhìn thấy media

```bash
docker exec jellyfin ls /media/tv
```

Kỳ vọng có:

```text
Friends (1994)
Silicon Valley (2014)
The Office (US) (2005)
```

Kiểm tra sâu hơn:

```bash
docker exec jellyfin ls "/media/tv/Friends (1994)/Season 01" | head
```

Nếu thấy `.mp4` và `.vtt`, bind mount đã hoạt động.

---

## Lỗi library bị nhận thành Movies

Failure mode thực tế:

```text
Movies
1-100 of 465
```

Mỗi episode bị hiển thị như một movie riêng.

Root cause đã xác định: `/media/tv` được add dưới library type `Movies`.

Fix:

1. Remove library entry sai trong Jellyfin.
2. Add Media Library lại.
3. Chọn:

```text
Content type: Shows
Folder: /media/tv
```

Vì media mount `:ro`, việc remove library khỏi Jellyfin không xóa file gốc trong `/data/media/tv`.

Sau khi scan đúng, Jellyfin có thể group theo:

```text
Series
└── Season
    └── Episode
```

thay vì hiển thị 465 file rời.

---

## Truy cập Jellyfin trong LAN và qua Tailscale

Lấy địa chỉ server:

```bash
hostname -I
```

Lấy riêng Tailscale IPv4:

```bash
tailscale ip -4
```

Truy cập:

```text
http://<SERVER-IP>:8096
```

Nếu MagicDNS hoạt động, có thể thử:

```text
http://macmini:8096
```

Không cần port-forward router để sử dụng qua Tailscale.

### Share cho người khác

Đối với một người xem bên ngoài mạng nhà, mô hình ưu tiên là:

```text
Tailscale Admin Console
→ Machines
→ macmini
→ Share
```

Share riêng node `macmini` thay vì cấp quyền vào toàn bộ tailnet.

Người nhận:
1. cài Tailscale trên điện thoại/laptop;
2. đăng nhập và accept share;
3. kết nối tới Jellyfin bằng IP Tailscale mà họ nhìn thấy cho node được share;
4. đăng nhập bằng Jellyfin user riêng.

Tailscale account và Jellyfin account là hai lớp độc lập:

```text
Tailscale
  └── ai được phép kết nối tới server?

Jellyfin
  └── ai được phép đăng nhập và xem library?
```

Không chia sẻ Jellyfin admin account cho người xem thông thường.

---

## Hardware transcoding: chưa bật

Không bật hardware acceleration ngay trong bước cài ban đầu.

Thứ tự tốt hơn:

```text
Direct Play hoạt động
→ xác định có thật sự cần transcoding không
→ kiểm tra GPU/device
→ mới cấu hình HWA
```

Kiểm tra Linux render device:

```bash
ls -l /dev/dri
```

Mac mini 2014 thuộc thế hệ Intel cũ; tài liệu Jellyfin nêu QSV trên Linux được ưu tiên cho phần cứng mainstream được hỗ trợ, nhưng pre-Broadwell cần xem xét VA-API để tương thích. Cần xác minh GPU cụ thể của máy trước khi áp dụng HWA; chưa có cấu hình VA-API nào được triển khai trong lần setup này.

---

## Những điều không nên làm trong setup này

Không cần:
- RAID chỉ để chạy một HDD media;
- ZFS/mergerfs khi chưa có nhu cầu pooling nhiều disk;
- SSD cache cho media chỉ để “tăng tốc” streaming;
- public-forward trực tiếp `8096` ra Internet;
- `chmod -R 777`;
- xóa source trên laptop trước verification;
- bật HWA trước khi biết transcoding có phải bottleneck hay không.

Các quyết định này cần xem xét lại nếu sau này:
- thêm nhiều HDD;
- cần redundancy hoặc snapshot;
- có nhiều concurrent remote stream;
- phải transcode 4K/HEVC thường xuyên;
- muốn public service cho người không dùng Tailscale;
- appdata/cache trên HDD trở thành bottleneck.

---

## Checklist dùng lại

Sau một migration hoặc rebuild, có thể kiểm tra theo thứ tự:

```bash
df -h /data

find /data/media/tv -type f -name '*.mp4' | wc -l
find /data/media/tv -type f -name '*.vtt' | wc -l
du -sh /data/media/tv

docker compose config
docker compose ps
docker compose logs --tail=50 jellyfin

docker exec jellyfin ls /media/tv
```

Trong Jellyfin:

```text
Library type = Shows
Folder = /media/tv
```

Sau cùng:
- mở một series;
- kiểm tra season grouping;
- phát thử vài episode;
- kiểm tra remote access qua Tailscale;
- chỉ xóa bản media cũ khi đã chắc chắn migration ổn.

---

## References

Nguồn chính thức đã được dùng trong quá trình quyết định và kiểm chứng:

- Jellyfin — Container installation: https://jellyfin.org/docs/general/installation/container/
- Jellyfin — TV Shows: https://jellyfin.org/docs/general/server/media/shows/
- Jellyfin — Movies: https://jellyfin.org/docs/general/server/media/movies/
- Jellyfin — Networking: https://jellyfin.org/docs/general/post-install/networking/
- Jellyfin — Tailscale: https://jellyfin.org/docs/general/post-install/networking/tailscale/
- Jellyfin — Hardware acceleration: https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/
- Jellyfin — Intel hardware acceleration: https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/intel/
- Jellyfin — Backup and Restore: https://jellyfin.org/docs/general/administration/backup-and-restore/
- Jellyfin — Configuration: https://jellyfin.org/docs/general/administration/configuration/

Community discussions đã được dùng để đối chiếu practice thực tế:

- r/jellyfin — Docker access to external HDD: https://www.reddit.com/r/jellyfin/comments/1souohd/how_to_give_jellyfin_in_docker_access_to_my/
- r/selfhosted — SSD/HDD setup for media server: https://www.reddit.com/r/selfhosted/comments/1v82xq0/best_ssd_hdd_setup_for_media_server/
- r/selfhosted — SSD cache and HDD spindown discussion: https://www.reddit.com/r/selfhosted/comments/1uxh1tf/ssd_cache_to_keep_hdd_powered_down/
