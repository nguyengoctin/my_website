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

> [!TLDR]
> Trên Ubuntu 26.04, stack terminal tối giản là Ptyxis làm terminal mặc định, Bash làm shell, fzf/zoxide/ripgrep/bat làm bộ CLI nhỏ, và Starship làm prompt. Kitty đã được gỡ, GNOME Terminal giữ lại làm fallback. `.bashrc` chỉ chứa initialization guard — không alias đè command Unix chuẩn.

## 1. Bản chất

Stack này giải quyết hai vấn đề:

**Vấn đề 1 — Terminal mặc định không phải Ptyxis sau cài Ubuntu 26.04**

Ubuntu 26.04 đưa Ptyxis làm terminal mặc định, nhưng nếu Kitty đã được cài trước đó, `Super+Enter` hoặc `xdg-terminal-exec` vẫn mở Kitty. Ubuntu dùng danh sách ưu tiên terminal trong `~/.config/ubuntu-xdg-terminals.list` — phải cấu hình file này để ưu tiên Ptyxis.

**Vấn đề 2 — `.bashrc` phình to với initialization không cần thiết**

Thêm fzf, zoxide, Starship vào `.bashrc` mà không có guard kiểm tra sự tồn tại của binary dẫn đến lỗi khi shell chạy trên máy không có các tool đó (server, container, SSH minimal).

Trạng thái đã xác minh:

```text
ptyxis: 50.1-1ubuntu2
gnome-terminal: 3.58.0-1ubuntu1 (giữ làm fallback)
kitty: đã gỡ
starship: 1.25.1 tại /usr/local/bin/starship
```

## 2. Vì sao lựa chọn

**Tại sao Ptyxis thay vì Kitty?**

Kitty mạnh hơn ở split panes, kittens, remote control và image protocol. Nhưng với workflow không cần các tính năng đó, Ptyxis ít config hơn, tích hợp GNOME/Ubuntu tốt hơn, có session restoration và container integration. Không cần GPU-accelerated rendering cho workload dev thông thường.

**Tại sao giữ Bash thay vì Zsh?**

Bash là shell mặc định của Ubuntu và phần lớn server/container. Script viết cho Bash portable hơn Zsh. Zsh, Oh My Zsh và plugin manager thêm complexity mà không giải quyết pain point cụ thể nào trong workflow hiện tại.

**Tại sao không alias đè command Unix chuẩn?**

`bat`, `rg`, `zoxide` không phải là replacement hoàn chỉnh cho `cat`, `grep`, `cd` — chúng có flags và behavior khác. Script, AI agent, và môi trường khác (server, CI) kỳ vọng command chuẩn. Alias đè tạo ra hành vi bất ngờ khi chạy cùng script ở môi trường không có tool đó.

**Đánh đổi:**

- Giữ GNOME Terminal làm fallback tốn thêm ~20MB — chấp nhận được vì đây là recovery option.
- Starship thêm một bước khởi tạo vào mỗi shell session — nếu không cần Git context trong prompt, native Bash PS1 đơn giản hơn.

## 3. Cơ chế hoạt động

```text
Super+Enter được nhấn
      │
      ▼
Custom shortcut GNOME → chạy xdg-terminal-exec
      │
      ▼
xdg-terminal-exec đọc ~/.config/ubuntu-xdg-terminals.list
      │
      ├─ org.gnome.Ptyxis.desktop:new-window  ← ưu tiên 1
      └─ org.gnome.Terminal.desktop            ← fallback
      │
      ▼
Ptyxis mở, spawn bash shell
      │
      ▼
bash đọc ~/.bashrc
      │
      ├─ fzf initialization (nếu file tồn tại)
      ├─ zoxide initialization (nếu binary tồn tại)
      └─ starship init bash (nếu binary tồn tại)
```

Guard pattern trong `.bashrc` đảm bảo initialization chỉ chạy khi tool có sẵn:

```bash
if command -v starship >/dev/null 2>&1; then
    eval "$(starship init bash)"
fi
# command -v → kiểm tra binary có trong PATH không
# >/dev/null 2>&1 → suppress cả stdout và stderr
# Nếu không có starship, block này bị bỏ qua hoàn toàn
```

## 4. Hướng dẫn từng bước

### Bước 1 — Cài Ptyxis và bộ CLI

```bash
sudo apt update
sudo apt install ptyxis fzf zoxide ripgrep bat
# fzf → fuzzy finder, Ctrl+R history search
# zoxide → smart directory jumping với lệnh z
# ripgrep (rg) → recursive text/code search nhanh
# bat → cat với syntax highlighting và line numbers
```

### Bước 2 — Cấu hình terminal ưu tiên

```bash
cat > ~/.config/ubuntu-xdg-terminals.list << 'EOF'
org.gnome.Ptyxis.desktop:new-window
org.gnome.Terminal.desktop
EOF
# << 'EOF' → heredoc, ghi trực tiếp nội dung vào file
# Dòng đầu là terminal ưu tiên nhất, fallback theo thứ tự xuống dưới
```

Kiểm tra:

```bash
cat ~/.config/ubuntu-xdg-terminals.list
```

### Bước 3 — Cập nhật `.bashrc` với guard pattern

Thêm vào cuối `~/.bashrc`:

```bash
# fzf: Bash completion và Ctrl-R/Ctrl-T/Alt-C key bindings
if [ -r /usr/share/doc/fzf/examples/completion.bash ]; then
    . /usr/share/doc/fzf/examples/completion.bash
fi
if [ -r /usr/share/doc/fzf/examples/key-bindings.bash ]; then
    . /usr/share/doc/fzf/examples/key-bindings.bash
fi
# -r → kiểm tra file tồn tại và có thể đọc

# zoxide: smarter directory jumping qua lệnh z
if command -v zoxide >/dev/null 2>&1; then
    eval "$(zoxide init bash)"
fi

# Starship: minimal contextual prompt — phải ở cuối cùng
if command -v starship >/dev/null 2>&1; then
    eval "$(starship init bash)"
fi
```

### Bước 4 — Cấu hình Starship tối giản

```bash
mkdir -p ~/.config
cat > ~/.config/starship.toml << 'EOF'
add_newline = true

format = """
$directory\
$git_branch\
$line_break\
$character"""

[directory]
truncate_to_repo = false
truncation_length = 3
# truncation_length → số directory level hiển thị tối đa

[git_branch]
format = ' [$branch]($style)'

[character]
success_symbol = '[❯](bold)'
error_symbol = '[❯](bold red)'
# error_symbol đổi màu khi exit code != 0
EOF
```

### Bước 5 — Kiểm tra syntax `.bashrc`

```bash
bash -n ~/.bashrc
bash -n ~/.bash_profile
bash -n ~/.profile
# -n → chỉ parse syntax, không thực thi
# Không có output = không có lỗi syntax
```

## 5. Bẫy lỗi và Những lần thử thất bại

**Bẫy 1 — Gỡ Kitty mà quên cập nhật terminal list**

Sau khi gỡ Kitty, `xdg-terminal-exec` báo không tìm thấy terminal nếu `ubuntu-xdg-terminals.list` vẫn còn `kitty.desktop` ở đầu. Phải cập nhật file list trước hoặc ngay sau khi gỡ Kitty.

**Bẫy 2 — Đặt `eval "$(starship init bash)"` không phải ở cuối `.bashrc`**

Nếu có tool nào đó sau Starship cũng cố gắng set `PS1`, Starship prompt bị ghi đè. Starship phải là dòng cuối cùng trong `.bashrc`.

**Bẫy 3 — Lỗi `Failed to create stream fd` khi chạy `bash -lc`**

Trong sandbox, `bash -lc` báo lỗi `Operation not permitted`. Trace cho thấy `/etc/profile.d/im-config_wayland.sh` gọi `systemd-cat` — không phải `.bashrc`, fzf, hay Starship gây ra. Không kết luận vội rằng `.bashrc` lỗi khi thấy lỗi này trong môi trường không phải Ptyxis thật.

**Bẫy 4 — Dùng `eval "$(fzf --bash)"` thay vì source file fzf**

`fzf --bash` là cách mới hơn (fzf >= 0.48). Trên Ubuntu 26.04 với `fzf` từ APT, nên dùng cách source file `completion.bash` và `key-bindings.bash` vì đây là cách được package maintainer hỗ trợ.

## 6. Kiểm tra và Xác minh

Kiểm tra fzf và zoxide trong Bash interactive:

```bash
bash -ic 'bind -X | grep __fzf_history__; type z'
# -i → chạy interactive shell (source .bashrc)
# -c → chạy lệnh sau đó exit
# bind -X → liệt kê key binding đang active
```

Kết quả đã xác minh:

```text
"\C-r" "__fzf_history__"
z is a function
```

Kiểm tra không có alias đè command chuẩn:

```bash
bash -lc 'alias ls 2>/dev/null || echo no-ls-alias; alias grep 2>/dev/null || echo no-grep-alias'
# -l → login shell (source .bash_profile)
```

Kết quả mong đợi:

```text
no-ls-alias
no-grep-alias
```

Kiểm tra Starship:

```bash
command -v starship && starship --version
starship explain
# explain → liệt kê từng module đang active và giá trị hiện tại
```

Trong Git repo, prompt phải có dạng:

```text
~/my_project master
❯
```

Kiểm tra terminal ưu tiên:

```bash
gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/keyboard-first-terminal/ command
# Kỳ vọng: 'xdg-terminal-exec'

cat ~/.config/ubuntu-xdg-terminals.list
# Kỳ vọng: Ptyxis ở dòng đầu
```

## 7. Nguồn tham khảo

- Ubuntu 26.04 LTS release notes — terminal changes: https://documentation.ubuntu.com/release-notes/26.04/summary-for-lts-users/
- Ubuntu Desktop — Change the default terminal: https://documentation.ubuntu.com/desktop/en/latest/how-to/change-the-default-terminal/  
  *(mô tả cơ chế `ubuntu-xdg-terminals.list` chính thức)*
- Starship documentation — Bash integration: https://starship.rs/guide/#step-2-set-up-your-shell-to-use-starship
- fzf — Bash completion/key bindings: https://github.com/junegunn/fzf#setting-up-shell-integration
- zoxide — Bash initialization: https://github.com/ajeetdsouza/zoxide#installation
