---
title: "Terminal Ubuntu 26.04 tối giản cho dev"
date: 2026-09-03T14:30:00+07:00
aliases:
  - Ubuntu terminal setup
  - Ptyxis Bash stack
tags:
  - ubuntu
  - terminal
  - bash
  - cli
---

> [!TLDR]
> Trên Ubuntu 26.04, stack terminal tối giản cho dev là **Ptyxis + Bash + fzf + zoxide + ripgrep + bat**. Starship và eza chỉ thêm khi có pain point cụ thể. tmux chủ yếu đáng dùng cho SSH và session server dài hạn. Không cần Zsh hay shell framework nếu chưa có nhu cầu rõ ràng.

## 1. Bản chất

Stack này xây trên nguyên tắc **tối giản có chủ đích** — chỉ cài tool khi có pain point thực tế, không cài vì "người ta hay dùng". Mỗi tool trong stack giải quyết một vấn đề cụ thể:

| Tool | Pain point giải quyết |
|---|---|
| Ptyxis | Terminal mặc định Ubuntu 26.04, tích hợp GNOME, ít config |
| Bash | Shell portable, mặc định trên server/container |
| fzf | Tìm command history nhanh hơn `Ctrl+R` native |
| zoxide | Nhảy đến directory thường dùng không cần gõ full path |
| ripgrep | Tìm text/code trong project nhanh hơn `grep -r` |
| bat | Đọc file có syntax highlight và line number |

Tất cả đều có sẵn qua `apt` — không cần cài từ nguồn hay shell plugin manager.

## 2. Vì sao lựa chọn

**Tại sao không dùng Zsh + Oh My Zsh?**

Zsh có tính năng tốt hơn Bash (globbing, completion, history sharing). Nhưng Oh My Zsh và plugin ecosystem thêm complexity đáng kể: chậm startup, plugin update phải quản lý thêm, behavior khác nhau giữa Bash và Zsh có thể break script. Bash với fzf/zoxide giải quyết 90% pain point mà không cần đổi shell.

**Tại sao không dùng Kitty thay vì Ptyxis?**

Kitty mạnh hơn ở split panes, kittens, image protocol, remote control. Nhưng các tính năng đó có giá trị thực tế khi workflow cần chúng — không phải chỉ vì "Kitty được recommend nhiều". Ptyxis ít phải configure hơn, tích hợp GNOME session restoration, không cần Nerd Font cho baseline setup.

**Tại sao không alias `cat=bat`, `ls=eza`, `grep=rg`?**

Các tool mới không phải replacement hoàn toàn cho command chuẩn. `bat` có thêm pager, decoration, line number — trong script hay pipe, output của `bat` khác `cat`. Script của người khác, AI agent, và môi trường không có tool đó (server, Docker container) kỳ vọng behavior của command chuẩn. Alias đè là nguồn gốc của bug khó debug.

**Đánh đổi khi không dùng shell framework:**

- Không có tab completion tự động cho git subcommand hay custom script — phải viết completion thủ công khi cần.
- Không có plugin ecosystem — mỗi tool phải cài và configure riêng.
- Startup time của Bash thuần thường nhanh hơn Zsh + Oh My Zsh (100–300ms so với 500ms+).

## 3. Cơ chế hoạt động

```text
Mở terminal (Ptyxis)
       │
       ▼
Ptyxis spawn /bin/bash (interactive shell)
       │
       ▼
bash đọc ~/.bashrc
       │
       ├── fzf key bindings → Ctrl+R gọi __fzf_history__ thay vì native reverse-i-search
       ├── zoxide init → tạo function z() và hook vào cd để track directory
       └── starship init → override PS1 với custom prompt

Khi gõ z lexi:
       │
       ├── zoxide query "lexi" trong database ~/.local/share/zoxide/db.zo
       ├── Tìm directory match cao nhất theo frecency (frequency + recency)
       └── cd đến directory đó
```

Frequeny (tần suất) và recency (gần đây) kết hợp thành "frecency" — zoxide ưu tiên directory vừa dùng nhiều vừa dùng gần đây hơn directory chỉ dùng nhiều hoặc chỉ dùng gần đây.

## 4. Hướng dẫn từng bước

### Bước 1 — Cài bộ CLI tối thiểu

```bash
sudo apt update
sudo apt install fzf zoxide ripgrep bat
# fzf     → fuzzy finder
# zoxide  → smart cd
# ripgrep → rg command, recursive search
# bat     → syntax-aware cat
```

### Bước 2 — Thêm initialization vào `.bashrc`

Mở `~/.bashrc` và thêm vào cuối:

```bash
# fzf: history search và fuzzy completion
if [ -r /usr/share/doc/fzf/examples/completion.bash ]; then
    . /usr/share/doc/fzf/examples/completion.bash
fi
if [ -r /usr/share/doc/fzf/examples/key-bindings.bash ]; then
    . /usr/share/doc/fzf/examples/key-bindings.bash
fi
# [ -r file ] → true nếu file tồn tại và có quyền đọc
# Dùng guard để .bashrc portable sang máy không có fzf

# zoxide: smarter directory jumping
if command -v zoxide >/dev/null 2>&1; then
    eval "$(zoxide init bash)"
fi
# command -v → kiểm tra binary trong PATH, không cần which
```

Reload:

```bash
source ~/.bashrc
# hoặc
exec bash
# exec → thay thế shell process hiện tại bằng bash mới — sạch hơn source
```

### Bước 3 — Thêm Starship (tùy chọn)

Chỉ cài nếu muốn prompt hiển thị Git branch, runtime version hoặc exit status:

```bash
sudo apt install starship
```

Thêm vào cuối `.bashrc` (sau tất cả initialization khác):

```bash
if command -v starship >/dev/null 2>&1; then
    eval "$(starship init bash)"
fi
```

Cấu hình tối giản `~/.config/starship.toml`:

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
# truncation_length → hiển thị tối đa 3 cấp directory

[character]
success_symbol = '[❯](bold)'
error_symbol = '[❯](bold red)'
```

### Bước 4 — Thêm eza (tùy chọn)

Nếu cần listing giàu metadata hơn `ls`:

```bash
sudo apt install eza
```

Không override `ls` — thêm alias riêng:

```bash
alias ll='eza -lah --git'
# -l → long format
# -a → hiển thị hidden files
# -h → human-readable size
# --git → hiển thị git status của từng file
```

### Bước 5 — Cài tmux (chỉ khi cần SSH/server)

```bash
sudo apt install tmux
```

Workflow cơ bản:

```bash
tmux new -s main
# new -s → tạo session mới với tên "main"

# Trong session: Ctrl+B D để detach
# Attach lại:
tmux attach -t main
# -t → target session name
```

## 5. Bẫy lỗi và Những lần thử thất bại

**Bẫy 1 — Dùng `eval "$(fzf --bash)"` trên fzf từ APT**

`fzf --bash` là tính năng mới (fzf >= 0.48). Phiên bản fzf trong APT Ubuntu 26.04 có thể cũ hơn và không hỗ trợ flag này. Cách đúng với fzf từ APT là source các file `.bash` trong `/usr/share/doc/fzf/examples/`.

**Bẫy 2 — Đặt Starship init không phải cuối `.bashrc`**

Nếu tool nào đó sau Starship set lại `PS1` (VD: virtualenv, conda...), Starship prompt bị ghi đè. Starship phải là initialization cuối cùng trong file.

**Bẫy 3 — Cài Oh My Zsh "thử" rồi quên gỡ**

Oh My Zsh đổi default shell sang Zsh và thêm nhiều config vào `~/.zshrc`. Nếu sau đó quyết định không dùng Zsh, phải `chsh -s /bin/bash` và dọn các file config Zsh — tốn thêm bước cleanup.

**Bẫy 4 — Auto-start tmux trong `.bashrc`**

Thêm `tmux` hoặc `tmux attach` vào `.bashrc` khiến mọi shell session đều cố attach vào tmux — kể cả shell do script chạy, SSH non-interactive, hay subshell. Gây ra behavior bất ngờ và khó debug. Chỉ dùng tmux thủ công khi cần.

## 6. Kiểm tra và Xác minh

```bash
# Kiểm tra fzf history search
bash -ic 'bind -X | grep __fzf_history__'
# Kỳ vọng: "\C-r" "__fzf_history__"

# Kiểm tra zoxide function z
bash -ic 'type z'
# Kỳ vọng: z is a function

# Kiểm tra không có alias đè command chuẩn
bash -lc 'alias ls 2>/dev/null || echo no-ls-alias'
bash -lc 'alias grep 2>/dev/null || echo no-grep-alias'
bash -lc 'alias cat 2>/dev/null || echo no-cat-alias'
bash -lc 'alias cd 2>/dev/null || echo no-cd-alias'
# Kỳ vọng: tất cả đều in "no-*-alias"

# Kiểm tra Starship (trong Git repo)
cd ~/Projects/my_website && starship explain
# explain → liệt kê modules đang active và giá trị
```

Thao tác thực tế cần test bằng tay:

```text
[ ] Ctrl+R trong terminal → mở fzf history search
[ ] z <tên dir từng dùng> → nhảy đến directory đúng
[ ] rg "từ khóa" → tìm trong project
[ ] bat <file.py> → mở file có syntax highlight
[ ] ll (nếu cài eza) → listing với git status
```

## 7. Nguồn tham khảo

- Ubuntu 26.04 LTS release notes: https://documentation.ubuntu.com/release-notes/26.04/summary-for-lts-users/
- Kitty documentation (để so sánh): https://sw.kovidgoyal.net/kitty/
- Starship documentation: https://starship.rs/
- fzf repository: https://github.com/junegunn/fzf  
  *(xem README về Bash shell integration và phiên bản hỗ trợ `--bash` flag)*
- zoxide repository: https://github.com/ajeetdsouza/zoxide
- bat repository: https://github.com/sharkdp/bat
- eza repository: https://github.com/eza-community/eza
- tmux wiki: https://github.com/tmux/tmux/wiki