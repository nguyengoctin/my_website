---
title: "Cấu hình GNOME keyboard-first với 4 workspace cố định"
date: 2026-09-03T09:30:00+07:00
aliases:
  - GNOME workspace shortcuts
  - Ubuntu keyboard-first workflow
  - GNOME multi-monitor keyboard
tags:
  - ubuntu
  - gnome
  - keyboard
  - workspace
---

> [!TLDR]
> Ubuntu/GNOME được cấu hình theo workflow 4 fixed workspaces: `Super+1..4` để chuyển workspace, `Super+Shift+1..4` để đưa cửa sổ sang workspace tương ứng. Với 2 màn hình xếp dọc, workspace chỉ đổi trên primary display — màn hình phụ giữ nguyên cửa sổ tham chiếu khi đổi workspace.

## 1. Bản chất

GNOME mặc định dùng **dynamic workspaces** — workspace tự tạo khi có cửa sổ mới và tự xoá khi trống. Với keyboard-first workflow nhiều màn hình, điều này bất tiện vì vị trí workspace liên tục thay đổi.

Giải pháp là chuyển sang **fixed workspaces** với số lượng cố định (4), gán phím tắt số cho từng workspace, và cấu hình workspace chỉ áp dụng cho primary display — màn hình phụ giữ cửa sổ tham chiếu cố định trong khi làm việc.

Môi trường đã xác minh:

```text
Ubuntu 26.04.1 LTS
GNOME Shell 50.1
Session: Wayland, ubuntu:GNOME
Primary:   eDP-1 — 2560x1440@60 — scale 1.667 — vị trí (182, 0)
Secondary: DP-2  — 1920x1080@60 — scale 1.0   — vị trí (0, 864)
Terminal mặc định: x-terminal-emulator → kitty (sau đó chuyển sang Ptyxis)
```

## 2. Vì sao lựa chọn

**Tại sao fixed workspaces thay vì dynamic?**

Dynamic workspace phù hợp với workflow single-monitor và ít cửa sổ. Khi dùng nhiều workspace cùng lúc với nhiều màn hình, vị trí workspace dynamic thay đổi sau mỗi thao tác đóng/mở cửa sổ — shortcut `Super+1` hôm nay trỏ vào workspace khác với hôm qua.

Fixed workspaces loại bỏ hoàn toàn vấn đề này: `Super+1` luôn là workspace 1.

**Tại sao `workspaces-only-on-primary=true`?**

Không bật option này, cả hai màn hình đổi workspace cùng lúc — màn hình phụ không thể dùng làm nền tham chiếu cố định (tài liệu, terminal log, chat...). Với `workspaces-only-on-primary=true`, màn hình phụ trở thành không gian bền vững trong khi primary display chứa workspace context đang làm việc.

**Đánh đổi:**

- Không thể chuyển workspace độc lập trên từng màn hình — nếu cần multi-context trên cả hai màn hình, workflow này không phù hợp.
- GNOME Shell và Ubuntu Dock đều có binding riêng cho `Super+1..4` — phải bỏ cả hai trước khi gán workspace shortcut.

## 3. Cơ chế hoạt động

```text
Phím Super+1 được nhấn
       │
       ▼
GNOME Shell nhận keybinding
       │
       ├─ switch-to-application-1 (GNOME Shell) → đã bỏ
       ├─ app-hotkey-1 (Ubuntu Dock)            → đã bỏ
       └─ switch-to-workspace-1 (WM) → ACTIVE
              │
              ▼
       Mutter chuyển primary display sang workspace 1
              │
              ▼
       Secondary display (DP-2) không thay đổi
       vì workspaces-only-on-primary=true
```

Ba lớp binding có thể xung đột với cùng một phím:

| Lớp | gsettings schema | Binding mặc định |
|---|---|---|
| GNOME Shell | `org.gnome.shell.keybindings` | `switch-to-application-1..4` = Super+1..4 |
| Ubuntu Dock | `org.gnome.shell.extensions.dash-to-dock` | `app-hotkey-1..4` = Super+1..4 |
| Window Manager | `org.gnome.desktop.wm.keybindings` | `switch-to-workspace-*` = chưa có |

Phải dọn cả hai lớp trên trước khi lớp WM có thể nhận Super+1..4.

## 4. Hướng dẫn từng bước

### Bước 1 — Chuyển sang fixed workspaces

```bash
gsettings set org.gnome.mutter dynamic-workspaces false
# dynamic-workspaces false → tắt chế độ tự tạo/xoá workspace

gsettings set org.gnome.desktop.wm.preferences num-workspaces 4
# num-workspaces → số lượng workspace cố định

gsettings set org.gnome.mutter workspaces-only-on-primary true
# workspaces-only-on-primary → workspace chỉ thay đổi trên primary display
```

### Bước 2 — Bỏ binding xung đột của GNOME Shell

```bash
gsettings set org.gnome.shell.keybindings switch-to-application-1 "[]"
gsettings set org.gnome.shell.keybindings switch-to-application-2 "[]"
gsettings set org.gnome.shell.keybindings switch-to-application-3 "[]"
gsettings set org.gnome.shell.keybindings switch-to-application-4 "[]"
# "[]" → mảng rỗng, tức bỏ hoàn toàn binding đó
```

### Bước 3 — Bỏ binding xung đột của Ubuntu Dock

```bash
gsettings set org.gnome.shell.extensions.dash-to-dock app-hotkey-1 "[]"
gsettings set org.gnome.shell.extensions.dash-to-dock app-hotkey-2 "[]"
gsettings set org.gnome.shell.extensions.dash-to-dock app-hotkey-3 "[]"
gsettings set org.gnome.shell.extensions.dash-to-dock app-hotkey-4 "[]"
gsettings set org.gnome.shell.extensions.dash-to-dock app-shift-hotkey-1 "[]"
gsettings set org.gnome.shell.extensions.dash-to-dock app-shift-hotkey-2 "[]"
gsettings set org.gnome.shell.extensions.dash-to-dock app-shift-hotkey-3 "[]"
gsettings set org.gnome.shell.extensions.dash-to-dock app-shift-hotkey-4 "[]"
```

### Bước 4 — Gán workspace shortcut

```bash
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-1 "['<Super>1']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-2 "['<Super>2']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-3 "['<Super>3']"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-4 "['<Super>4']"

gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-1 "['<Super><Shift>1']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-2 "['<Super><Shift>2']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-3 "['<Super><Shift>3']"
gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-4 "['<Super><Shift>4']"
# move-to-workspace → đưa cửa sổ hiện tại sang workspace tương ứng
```

### Bước 5 — Phím tắt chuyển monitor

```bash
gsettings set org.gnome.desktop.wm.keybindings move-to-monitor-up "['<Super><Shift>Up']"
gsettings set org.gnome.desktop.wm.keybindings move-to-monitor-down "['<Super><Shift>Down']"
# move-to-monitor → đưa cửa sổ sang màn hình vật lý khác (theo chiều dọc)
```

### Bước 6 — Terminal và Files shortcut

Bỏ binding cũ chiếm `Super+E`:

```bash
gsettings set org.gnome.settings-daemon.plugins.media-keys email "[]"
# email media key mặc định là Super+E — phải bỏ trước
```

Gán `Super+E` cho Files/Nautilus:

```bash
gsettings set org.gnome.settings-daemon.plugins.media-keys home "['<Super>e']"
# home media key → mở file manager mặc định
```

Tạo custom shortcut `Super+Enter` mở terminal:

Vào Settings → Keyboard → View and Customize Shortcuts → Custom Shortcuts, thêm:

```text
Name:    Open Default Terminal
Command: xdg-terminal-exec
Binding: Super+Enter
```

### Bước 7 — Lock screen

```bash
gsettings set org.gnome.settings-daemon.plugins.media-keys screensaver "['<Super>l', '<Super>Escape']"
# screensaver → lock screen, giữ cả Super+L (chuẩn) lẫn Super+Escape (binding cũ)
```

## 5. Bẫy lỗi và Những lần thử thất bại

**Bẫy 1 — Chỉ bỏ GNOME Shell binding mà quên Ubuntu Dock**

Sau khi bỏ `switch-to-application-1..4` ở GNOME Shell, Super+1 vẫn không chuyển workspace. Nguyên nhân: Ubuntu Dock có binding riêng `app-hotkey-1..4` cũng chiếm Super+1..4. Phải bỏ cả hai lớp.

**Bẫy 2 — Dùng `Super+Up/Down` cho chuyển monitor**

`Super+Up` thuộc Tiling Assistant (maximize/tile) và `Super+Down` thuộc window management (restore). Dùng chúng cho chuyển monitor sẽ conflict — phải dùng `Super+Shift+Up/Down`.

**Bẫy 3 — Disable toàn bộ Ubuntu Dock chỉ để lấy lại Super+1..4**

Không cần. Chỉ cần bỏ `app-hotkey-1..4` và `app-shift-hotkey-1..4` trong dash-to-dock extension settings là đủ. Dock vẫn hoạt động bình thường.

**Bẫy 4 — Reset toàn bộ dconf cho một thay đổi nhỏ**

`dconf reset -f /` xoá mọi setting GNOME kể cả theme, font, accessibility — không cần làm vậy chỉ để sửa một nhóm keybinding.

**Bẫy 5 — Đổi shortcut Fcitx5 không cần thiết**

Fcitx5/Lotus dùng `Ctrl+Space`, `Super+Space`, `Shift+Super+Space`, `Shift_L` — không xung đột với workflow trên. Không cần đụng vào.

## 6. Kiểm tra và Xác minh

Xác minh bằng `gsettings` sau khi cấu hình:

```bash
gsettings get org.gnome.mutter dynamic-workspaces
# Kỳ vọng: false

gsettings get org.gnome.desktop.wm.preferences num-workspaces
# Kỳ vọng: 4

gsettings get org.gnome.mutter workspaces-only-on-primary
# Kỳ vọng: true

gsettings get org.gnome.desktop.wm.keybindings switch-to-workspace-1
# Kỳ vọng: ['<Super>1']

gsettings get org.gnome.shell.keybindings switch-to-application-1
# Kỳ vọng: @as [] (mảng rỗng)

gsettings get org.gnome.shell.extensions.dash-to-dock app-hotkey-1
# Kỳ vọng: @as []
```

Wayland không cho mô phỏng keyboard tự động — cần test thủ công:

```text
[ ] Super+1..4 → chuyển workspace
[ ] Super+Shift+1..4 → đưa cửa sổ sang workspace
[ ] Super+Shift+Down → cửa sổ từ eDP-1 xuống DP-2
[ ] Super+Shift+Up  → cửa sổ từ DP-2 lên eDP-1
[ ] Đổi workspace bằng Super+PageUp/Down: cửa sổ trên DP-2 đứng yên
[ ] Super+Enter mở terminal
[ ] Super+E mở Files/Nautilus
[ ] Fcitx5/Lotus vẫn hoạt động
```

### Rollback

```bash
sh ~/gnome-keybindings-rollback-20260903.sh
# Script rollback toàn bộ keybinding đã thay đổi

sh /home/ngoctin/.config/gnome-keyboard-monitor-backup-20260903/rollback-monitor-keybindings.sh
# Rollback riêng phần move-to-monitor
```

Sau rollback nên đăng xuất và đăng nhập lại nếu GNOME Shell chưa nhận đủ thay đổi.

## 7. Nguồn tham khảo

- GNOME Shell keybindings — gsettings schema: `org.gnome.shell.keybindings`  
  *(dùng `gsettings list-keys org.gnome.shell.keybindings` để xem toàn bộ)*
- Mutter keybindings: `org.gnome.mutter`, `org.gnome.desktop.wm.keybindings`
- Ubuntu Dock / Dash-to-Dock: `org.gnome.shell.extensions.dash-to-dock`  
  *(dùng `gsettings list-keys ...` để kiểm tra key đúng cho version hiện tại)*
- GNOME Settings Daemon media keys: `org.gnome.settings-daemon.plugins.media-keys`
