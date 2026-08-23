#!/usr/bin/env bash
# Upload NotebookLM audio lên Internet Archive (miễn phí, unlimited bandwidth)
# rồi in ra các URL để dán vào data/notebooklm.yml
#
# Setup lần đầu:
#   pip install internetarchive
#   ia configure            # nhập email + password tài khoản archive.org
#
# Cách chạy:
#   ./scripts/upload-notebooklm-audio.sh /home/ngoctin/Downloads/NotebookLM-audio

set -euo pipefail

SRC_DIR="${1:-/home/ngoctin/Downloads/NotebookLM-audio}"
IDENTIFIER="ngoctin-notebooklm"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

command -v ia >/dev/null 2>&1 || { echo "Lỗi: chưa cài 'ia' CLI. Chạy: pip install internetarchive"; exit 1; }

# Đổi tên file sang ASCII không dấu để URL sạch đẹp
declare -A NAME_MAP=(
  ["Biến_AI_thành_gia_sư_lập_trình.m4a"]="bien-ai-thanh-gia-su-lap-trinh.m4a"
  ["Kiến_trúc_bộ_não_tác_nhân_AI.m4a"]="kien-truc-bo-nao-tac-nhan-ai.m4a"
  ["Sức_mạnh_có_sẵn_pin_Django_6.m4a"]="suc-manh-co-san-pin-django-6.m4a"
  ["Sự_thật_về_nghề_kỹ_sư_AI.m4a"]="su-that-ve-nghe-ky-su-ai.m4a"
)

echo "==> Copy + đổi tên file sang ASCII..."
for src in "$SRC_DIR"/*.m4a; do
  base=$(basename "$src")
  dest="${NAME_MAP[$base]:-$base}"
  cp "$src" "$TMP_DIR/$dest"
done

echo "==> Upload lên archive.org item: $IDENTIFIER"
ia upload "$IDENTIFIER" "$TMP_DIR"/*.m4a \
  --metadata title:"NotebookLM Audio Overviews" \
  --metadata collection:opensource_audio \
  --metadata mediatype:audio \
  --metadata creator:"ngoctin" \
  --modify --retries 3

echo ""
echo "==> Hoàn tất! Các URL để dán vào data/notebooklm.yml:"
for remote in "${NAME_MAP[@]}"; do
  echo "https://archive.org/download/$IDENTIFIER/$remote"
done
