---
title: "Cấu hình GNOME keyboard-first với 4 workspace"
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

> Ubuntu/GNOME hiện được cấu hình theo workflow 4 fixed workspaces: `Super+1..4` để chuyển workspace, `Super+Shift+1..4` để đưa cửa sổ sang workspace tương ứng. Với 2 màn hình xếp dọc, workspace chỉ đổi trên primary display; màn hình phụ giữ cửa sổ tham chiếu khi đổi workspace.

## Kết luận chính

- Dùng 4 fixed workspaces thay vì dynamic workspaces.
- Workspace chỉ thay đổi trên primary display: `org.gnome.mutter workspaces-only-on-primary=true`.
- `Super+Tab` chỉ switch app trong workspace hiện tại.
- `Super+Enter` mở terminal mặc định qua `x-terminal-emulator`, hiện trỏ tới Kitty.
- `Super+E` mở Files/Nautilus.
- `Super+Shift+Up/Down` đưa cửa sổ giữa màn hình trên/dưới theo geometry monitor thực tế.
- Giữ các shortcut điều hướng workspace theo chiều ngang:
  - `Super+PageUp`
  - `Super+PageDown`
  - `Super+Shift+PageUp`
  - `Super+Shift+PageDown`
- Giữ các shortcut window/system quan trọng:
  - `Super+Arrow`
  - `Alt+F4`
  - `Super+L`
  - screenshot bằng `Print`, `Shift+Print`, `Alt+Print`
- Không đổi cấu hình Fcitx5/Lotus.

## Shortcut đang dùng

| Shortcut | Chức năng |
|---|---|
| `Super+1` | Chuyển tới workspace 1 |
| `Super+2` | Chuyển tới workspace 2 |
| `Super+3` | Chuyển tới workspace 3 |
| `Super+4` | Chuyển tới workspace 4 |
| `Super+Shift+1` | Đưa cửa sổ hiện tại tới workspace 1 |
| `Super+Shift+2` | Đưa cửa sổ hiện tại tới workspace 2 |
| `Super+Shift+3` | Đưa cửa sổ hiện tại tới workspace 3 |
| `Super+Shift+4` | Đưa cửa sổ hiện tại tới workspace 4 |
| `Super+PageUp` | Chuyển sang workspace bên trái |
| `Super+PageDown` | Chuyển sang workspace bên phải |
| `Super+Shift+PageUp` | Đưa cửa sổ sang workspace bên trái |
| `Super+Shift+PageDown` | Đưa cửa sổ sang workspace bên phải |
| `Super+Shift+Up` | Đưa cửa sổ lên monitor phía trên |
| `Super+Shift+Down` | Đưa cửa sổ xuống monitor phía dưới |
| `Super+Tab` | Switch app trong workspace hiện tại |
| `Super+Shift+Tab` | Switch app ngược chiều trong workspace hiện tại |
| `Super+Enter` | Mở terminal mặc định |
| `Super+E` | Mở Files/Nautilus |
| `Super+L` | Lock screen |
| `Super+Escape` | Lock screen, binding cũ được giữ lại |

## Môi trường đã xác minh

- Ubuntu 26.04.1 LTS.
- GNOME Shell 50.1.
- Session: Wayland, desktop `ubuntu:GNOME`.
- Ubuntu Dock extension vẫn bật.
- Tiling Assistant extension vẫn bật và đang giữ một phần `Super+Arrow`.
- Monitor layout hiện tại, đọc từ Mutter DisplayConfig:
  - Trên: `eDP-1`, Built-in display, primary, `2560x1440@60.012`, scale `1.6666666269302368`, logical position `(182, 0)`.
  - Dưới: `DP-2`, RTK, secondary, `1920x1080@60.000`, scale `1.0`, logical position `(0, 864)`.
- File manager mặc định: `org.gnome.Nautilus.desktop`.
- Terminal mặc định: `/usr/bin/x-terminal-emulator`, đang trỏ tới `/usr/bin/kitty`.
- Fcitx5 đang dùng Lotus.

## Các cấu hình đã thay đổi

- `org.gnome.mutter dynamic-workspaces=false`.
- `org.gnome.mutter workspaces-only-on-primary=true`.
- `org.gnome.desktop.wm.preferences num-workspaces=4`.
- `org.gnome.desktop.wm.keybindings switch-to-workspace-1..4` được đặt thành `Super+1..4`.
- `org.gnome.desktop.wm.keybindings move-to-workspace-1..4` được đặt thành `Super+Shift+1..4`.
- `org.gnome.desktop.wm.keybindings switch-to-workspace-left/right` được đặt thành `Super+PageUp/PageDown`.
- `org.gnome.desktop.wm.keybindings move-to-monitor-up/down` được đặt thành `Super+Shift+Up/Down`.
- GNOME Shell `switch-to-application-1..4` được bỏ binding để không tranh `Super+1..4`.
- Ubuntu Dock `app-hotkey-1..4` và `app-shift-hotkey-1..4` được bỏ binding.
- Media key `home` được đặt thành `Super+E`.
- Media key `email` được bỏ binding vì trước đó chiếm `Super+E`.
- Custom shortcut mới:
  - name: `Open Default Terminal`
  - command: `x-terminal-emulator`
  - binding: `Super+Enter`
- Lock screen giữ `Super+Escape` và thêm `Super+L`.

## Fcitx5/Lotus

Không thay đổi shortcut của Fcitx5/Lotus vì không xung đột với mục tiêu:

- `Ctrl+Space`: trigger input method.
- `Super+Space`: chuyển input method kế tiếp.
- `Shift+Super+Space`: chuyển input method trước đó.
- `Shift_L`: alternate trigger.

## Kiểm tra

Đã xác minh bằng `gsettings` rằng:

- Có 4 fixed workspaces.
- Workspace chỉ thay đổi trên primary display.
- Binding workspace và move-window đúng với `Super+1..4` và `Super+Shift+1..4`.
- Binding move-to-monitor đúng với `Super+Shift+Up/Down`.
- Ubuntu Dock không còn bắt `Super+1..4` và `Super+Shift+1..4`.
- Tiling Assistant vẫn giữ `Super+Up` cho maximize/tile và `Super+Down` cho restore-window.
- App switcher chỉ xét workspace hiện tại.
- `Super+Enter` trỏ tới custom shortcut mở `x-terminal-emulator`.
- `Super+E` trỏ tới Files/Nautilus.
- Fcitx5 vẫn đang ở input method Lotus.
- Không thấy conflict rõ ràng với các shortcut mục tiêu.

Wayland không cho mô phỏng keyboard end-to-end an toàn trong audit này, nên vẫn cần test thủ công bằng cách bấm thật:

- `Super+1..4`
- `Super+Shift+1..4`
- `Super+Shift+Down`: cửa sổ từ `eDP-1` xuống `DP-2`
- `Super+Shift+Up`: cửa sổ từ `DP-2` lên `eDP-1`
- Đổi workspace bằng `Super+PageUp/PageDown` khi có cửa sổ tham chiếu ở `DP-2`: cửa sổ trên màn hình phụ phải đứng yên
- `Super+Enter`
- `Super+E`
- chuyển/gõ tiếng Việt bằng Fcitx5/Lotus

## Rollback

Rollback script đã được tạo tại:

```sh
~/gnome-keybindings-rollback-20260903.sh
```

Chạy rollback:

```sh
sh ~/gnome-keybindings-rollback-20260903.sh
```

Rollback riêng cho binding move-to-monitor:

```sh
/home/ngoctin/.config/gnome-keyboard-monitor-backup-20260903/rollback-monitor-keybindings.sh
```

Sau rollback nên đăng xuất/đăng nhập lại nếu GNOME Shell chưa nhận đủ thay đổi.

## Đừng làm lại

- Không disable toàn bộ Ubuntu Dock chỉ để lấy lại `Super+1..4`; chỉ cần bỏ các app hotkey liên quan.
- Không reset toàn bộ GNOME/dconf cho một thay đổi phím tắt nhỏ.
- Không đổi shortcut Fcitx5/Lotus nếu không có conflict thực sự.
- Không giả định `Super+1..4` chỉ do Dock giữ; GNOME Shell `switch-to-application-1..4` cũng có thể tranh cùng binding.
- Không dùng `Super+Up/Down` cho chuyển monitor; các phím đó đang thuộc window management/Tiling Assistant.
