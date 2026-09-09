---
title: "Cấu hình terminal Ubuntu tối giản với Bash"
date: 2026-09-03T11:00:00+07:00
aliases:
  - Ptyxis Bash setup
  - Ubuntu terminal cleanup
tags:
  - ubuntu
  - terminal
  - bash
  - ptyxis
---

> Trạng thái cuối: Ptyxis là terminal ưu tiên cho `Super+Enter`, Bash là shell cần giữ, Kitty đã được gỡ nhưng GNOME Terminal vẫn còn cài làm fallback. Prompt dùng Starship tối giản, chỉ hiển thị thư mục, Git branch và prompt symbol.

## Trạng thái đã xác minh

- `ptyxis` đã cài: `50.1-1ubuntu2`.
- `gnome-terminal` vẫn còn cài: `3.58.0-1ubuntu1`.
- `kitty` không còn cài.
- Custom GNOME binding của `Super+Enter` chạy `xdg-terminal-exec`.
- Terminal list ưu tiên:

  ```text
  org.gnome.Ptyxis.desktop:new-window
  org.gnome.Terminal.desktop
  ```

- `starship` phiên bản `1.25.1` tại `/usr/local/bin/starship`.
- `.bash_profile` source `.profile`.
- `.bashrc` có guard cho fzf/zoxide và khởi tạo Starship ở cuối file.
- Không có alias đè `cat`, `grep`, `ls` hoặc `cd`.

## Cấu hình hiện tại

### Chọn terminal cho GNOME

Các file terminal list có thể được kiểm tra, trong đó Ubuntu ưu tiên file riêng của Ubuntu:

```text
~/.config/ubuntu-xdg-terminals.list
~/.config/xdg-terminals.list
~/.config/gnome-xdg-terminals.list
~/.config/GNOME-xdg-terminals.list
```

Nội dung nên đặt Ptyxis trước GNOME Terminal và giữ GNOME Terminal làm fallback:

```text
org.gnome.Ptyxis.desktop:new-window
org.gnome.Terminal.desktop
```

Binding `Super+Enter` cần gọi:

```text
xdg-terminal-exec
```

Kiểm tra:

```bash
gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/keyboard-first-terminal/ command
sed -n '1,5p' ~/.config/ubuntu-xdg-terminals.list
```

Ubuntu 25.04 trở lên dùng Ptyxis làm terminal mặc định trong Ubuntu Desktop; vì vậy trên Ubuntu 26.04, việc thêm `org.gnome.Ptyxis.desktop:new-window` vào danh sách ưu tiên là phù hợp với cơ chế chính thức. Chỉ có hiệu lực khi package và desktop entry của Ptyxis tồn tại.

### Bash login và tiện ích CLI

`.bash_profile`:

```bash
if [ -f "$HOME/.profile" ]; then
    . "$HOME/.profile"
fi
```

Trong `.bashrc`, chỉ khởi tạo fzf và zoxide khi thành phần tồn tại:

```bash
# fzf: Bash completion and Ctrl-R/Ctrl-T/Alt-C key bindings.
if [ -r /usr/share/doc/fzf/examples/completion.bash ]; then
    . /usr/share/doc/fzf/examples/completion.bash
fi
if [ -r /usr/share/doc/fzf/examples/key-bindings.bash ]; then
    . /usr/share/doc/fzf/examples/key-bindings.bash
fi

# zoxide: smarter directory jumping via `z`.
if command -v zoxide >/dev/null 2>&1; then
    eval "$(zoxide init bash)"
fi
```

Starship được khởi tạo ở cuối `.bashrc` để trở thành prompt cuối cùng:

```bash
# Starship: minimal contextual prompt.
if command -v starship >/dev/null 2>&1; then
    eval "$(starship init bash)"
fi
```

`~/.config/starship.toml` hiện chỉ gồm directory, Git branch, xuống dòng và character:

```toml
add_newline = true

format = """
$directory\
$git_branch\
$line_break\
$character"""

[directory]
truncate_to_repo = false
truncation_length = 3

[git_branch]
format = ' [$branch]($style)'

[character]
success_symbol = '[❯](bold)'
error_symbol = '[❯](bold red)'
```

Không bật `git_status`, runtime version, right prompt, icon hoặc Nerd Font ở baseline này. Chỉ thêm khi có nhu cầu quan sát cụ thể.

## Cài đặt và dọn package

Bộ CLI tối thiểu:

```bash
sudo apt update
sudo apt install fzf zoxide ripgrep bat
```

Nếu muốn máy chỉ còn Ptyxis, có thể gỡ GNOME Terminal sau khi kiểm tra mô phỏng:

```bash
apt-cache rdepends --installed gnome-terminal
apt-get -s remove gnome-terminal
sudo apt remove -y gnome-terminal
sudo apt autoremove
```

Các lệnh `sudo apt-get ...` và `chsh -s /bin/bash` đã từng không chạy được trong phiên sandbox vì `sudo` cần TTY để nhập mật khẩu. Không coi việc đó là đã thay đổi thành công; kiểm tra lại trong terminal desktop thật. Việc gỡ `kitty` và cài Ptyxis đã được phản ánh theo trạng thái cuối đã xác minh.

## Kiểm tra sau khi chỉnh

```bash
bash -n ~/.bashrc
bash -n ~/.bash_profile
bash -n ~/.profile
```

Kiểm tra fzf và zoxide trong Bash interactive:

```bash
bash -ic 'bind -X | grep __fzf_history__; type z'
```

Kết quả đã xác minh trong context này:

```text
"\C-r" "__fzf_history__"
z is a function
```

Kiểm tra không có alias đè command chuẩn:

```bash
bash -lc 'alias ls 2>/dev/null || echo no-ls-alias; alias grep 2>/dev/null || echo no-grep-alias'
```

Kết quả đã xác minh:

```text
no-ls-alias
no-grep-alias
```

Kiểm tra Starship:

```bash
command -v starship
starship --version
starship explain
```

Trong một Git repository, output đã xác minh có dạng:

```text
~/shell  master_noble
❯
```

## Quyết định và trade-off

- Giữ `Ptyxis + Bash + fzf + zoxide + ripgrep + bat` làm stack nền.
- Giữ Starship vì cần Git context, nhưng cấu hình ở mức tối giản; Bash native vẫn là phương án đơn giản hơn nếu Starship không còn tạo giá trị.
- Không dùng shell framework, plugin manager hoặc auto-start `tmux`.
- Không alias đè command chuẩn. Dùng `rg` thay cho tìm kiếm code khi phù hợp, `bat` như command riêng; `eza` nếu cài thì chỉ nên có alias riêng như `ll`.
- `tmux` chỉ nên dùng thủ công cho SSH hoặc session cần detach/reattach.
- Có hai terminal vì Ptyxis và GNOME Terminal là hai package/desktop entry độc lập; danh sách ưu tiên chọn app mở mặc định nhưng không tự gỡ app fallback.

## Caveat

Trong sandbox, `bash -lc` từng báo `Failed to create stream fd: Operation not permitted`. Trace quy về `/etc/profile.d/im-config_wayland.sh` gọi `systemd-cat`, không phải `.bashrc`, fzf, zoxide hoặc Starship. Cần kiểm tra lại trong Ptyxis thật trước khi kết luận đó là lỗi hệ thống.

## Nguồn

- [Ubuntu 26.04 LTS release notes: summary for LTS users](https://documentation.ubuntu.com/release-notes/26.04/summary-for-lts-users/)
- [Ubuntu Desktop: Change the default terminal](https://documentation.ubuntu.com/desktop/en/latest/how-to/change-the-default-terminal/)
