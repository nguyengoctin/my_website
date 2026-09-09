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

> Trên Ubuntu 26.04, lựa chọn hợp lý nếu ưu tiên clean, ổn định và ít bảo trì là **Ptyxis + Bash + fzf + zoxide + ripgrep + bat**. Starship và eza chỉ là QoL tùy chọn; tmux chủ yếu đáng dùng cho SSH/session dài; không cần Kitty hoặc Zsh nếu chưa có nhu cầu cụ thể.

## Stack nên giữ

```text
Ubuntu 26.04
└── Ptyxis
    └── Bash
        ├── fzf
        ├── zoxide
        ├── ripgrep
        └── bat
```

Tùy chọn:

```text
Starship   → prompt đẹp và có context hơn
eza        → listing dễ đọc hơn
tmux       → SSH / session cần detach-reattach
```

### Quyết định

- **Ptyxis:** giữ làm terminal chính.
    
- **Bash:** giữ làm shell mặc định.
    
- **fzf:** cài.
    
- **zoxide:** cài.
    
- **ripgrep (`rg`):** cài.
    
- **bat:** cài.
    
- **Starship:** chỉ thêm nếu muốn prompt có Git/runtime context.
    
- **eza:** chỉ thêm nếu thường xuyên cần listing giàu metadata.
    
- **tmux:** ưu tiên cho server/SSH, không cần mặc định trên desktop.
    
- **Kitty:** có thể bỏ nếu không dùng split/layout/kittens/remote-control hoặc các tính năng đặc thù khác.
    
- **Zsh / Oh My Zsh / plugin manager:** không cần chỉ để có terminal dev tốt.
    

## Cài bộ tối thiểu

```bash
sudo apt update
sudo apt install fzf zoxide ripgrep bat
```

Thêm vào cuối `~/.bashrc`:

```bash
eval "$(fzf --bash)"
eval "$(zoxide init bash)"
```

Reload:

```bash
source ~/.bashrc
```

## Các thao tác đáng học

```text
Ctrl+R        tìm command cũ bằng fzf
z lexi        nhảy tới directory đã dùng trước đó
rg "foo"      tìm text/code trong project
bat file.py   đọc file có syntax highlight
```

Phần lớn lợi ích của stack đến từ vài thao tác này, không phải từ việc cài nhiều tool.

## Nguyên tắc cấu hình

### Không alias đè command Unix chuẩn

Không nên:

```bash
alias cat=bat
alias grep=rg
alias ls=eza
alias cd=z
```

Các tool mới không hoàn toàn tương đương command chuẩn.

Giữ cả hai loại:

```text
cat   → raw/simple output
bat   → đọc file tương tác

grep  → command chuẩn / compatibility
rg    → search project/code

cd    → navigation chuẩn
z     → fast navigation
```

Điều này giúp command dễ portable sang server, container và môi trường khác, đồng thời giảm khả năng script hoặc AI agent gặp hành vi bất ngờ.

### Giữ `.bashrc` nhỏ

Chỉ thêm initialization và alias có giá trị rõ ràng.

Tránh:

- shell framework lớn;
    
- hàng chục plugin;
    
- dotfiles phức tạp;
    
- duplicate initialization;
    
- alias chỉ để thay tên command;
    
- customization chưa giải quyết pain point thực tế.
    

## Ptyxis

Ubuntu 26.04 dùng **Ptyxis** làm terminal mặc định.

Điểm đáng giữ:

- tích hợp GNOME/Ubuntu tốt;
    
- session/directory restoration;
    
- tích hợp container;
    
- ít configuration hơn các terminal power-user như Kitty.
    

Cấu hình thực tế nên giữ đơn giản:

```text
Font: JetBrains Mono 12–13 nếu đã có
Theme: Follow System
Scrollback: khoảng 20,000 dòng
Preserve Working Directory: bật
Audible Bell: tắt
```

Không cần transparency hoặc theme phức tạp nếu mục tiêu chính là đọc code/log.

## Starship

Chỉ cài khi muốn prompt cho biết context như:

- Git branch;
    
- Python;
    
- Node;
    
- command duration;
    
- current directory.
    

Cài:

```bash
sudo apt install starship
```

Bash:

```bash
eval "$(starship init bash)"
```

Giữ prompt tối giản. Không cần Powerline-style prompt chứa quá nhiều icon/runtime/module.

## eza

Nếu cần overview directory giàu thông tin hơn `ls`, có thể cài:

```bash
sudo apt install eza
```

Thay vì override `ls`, tạo command riêng:

```bash
alias ll='eza -lah --git'
```

Như vậy:

```bash
ls
```

vẫn portable, còn:

```bash
ll
```

dùng khi muốn output dễ đọc hơn.

## tmux

Không cần cài chỉ vì đây là tool phổ biến trong dotfiles.

Use case rõ nhất:

```text
Laptop
  ↓ SSH
Server
  ↓
tmux
├── app
├── logs
└── shell
```

Nếu SSH rớt, process/session bên trong tmux vẫn còn và có thể attach lại.

Vì vậy:

- desktop local: chưa cần;
    
- home server / VPS / SSH lâu dài: rất đáng dùng.
    

## Khi nào Kitty đáng giữ

Kitty mạnh hơn Ptyxis nếu thực sự cần:

- split panes;
    
- nhiều terminal layout;
    
- keyboard-driven window management;
    
- kittens;
    
- terminal image protocol;
    
- remote control / scripting;
    
- customization sâu.
    

GPU acceleration một mình không phải lý do đủ mạnh để đổi terminal cho workload dev thông thường.

## Điều đã xác minh

- Ubuntu 26.04 sử dụng **Ptyxis** làm terminal mặc định.
    
- Ptyxis hỗ trợ session/directory restoration và container integration.
    
- `fzf` có Bash integration, gồm fuzzy history qua `Ctrl+R`.
    
- zoxide hỗ trợ Bash và command `z`.
    
- ripgrep được thiết kế cho recursive text/code search.
    
- bat cung cấp syntax highlighting và paging cho việc đọc file.
    
- Starship hỗ trợ Bash và initialization qua `eval "$(starship init bash)"`.
    
- tmux hỗ trợ detach/reattach session.
    

## Điều mang tính quyết định cá nhân

Không có bằng chứng cho thấy một terminal emulator hoặc shell là “tốt nhất” cho mọi developer.

Kết luận **Ptyxis + Bash + bộ CLI nhỏ** dựa trên tiêu chí:

- ít dependency;
    
- ít config;
    
- dễ nhớ;
    
- portable sang server/container;
    
- tránh biến terminal thành một project cần bảo trì riêng.
    

Nếu workflow sau này xuất hiện pain point cụ thể, thêm tool để giải quyết pain point đó thay vì thiết kế trước một stack phức tạp.

## Nguồn

- Ubuntu 26.04 LTS release notes:  
    [https://documentation.ubuntu.com/release-notes/26.04/summary-for-lts-users/](https://documentation.ubuntu.com/release-notes/26.04/summary-for-lts-users/)
    
- Kitty documentation:  
    [https://sw.kovidgoyal.net/kitty/](https://sw.kovidgoyal.net/kitty/)
    
- Starship documentation:  
    [https://starship.rs/](https://starship.rs/)
    
- fzf upstream repository/documentation:  
    [https://github.com/junegunn/fzf](https://github.com/junegunn/fzf)
    
- zoxide upstream repository:  
    [https://github.com/ajeetdsouza/zoxide](https://github.com/ajeetdsouza/zoxide)
    
- bat upstream repository:  
    [https://github.com/sharkdp/bat](https://github.com/sharkdp/bat)
    
- eza upstream repository:  
    [https://github.com/eza-community/eza](https://github.com/eza-community/eza)
    
- tmux documentation/wiki:  
    [https://github.com/tmux/tmux/wiki](https://github.com/tmux/tmux/wiki)