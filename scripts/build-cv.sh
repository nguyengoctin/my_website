#!/usr/bin/env bash
# ==============================================================================
# Build CV PDF using Typst CLI
# Output: static/cv/Nguyen_Ngoc_Tin-CV.pdf
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_TYP="$ROOT_DIR/cv/resume.typ"
OUT_DIR="$ROOT_DIR/static/cv"
OUT_PDF="$OUT_DIR/Nguyen_Ngoc_Tin-CV.pdf"

mkdir -p "$OUT_DIR"

if command -v typst >/dev/null 2>&1; then
    echo "🔨 Compiling Typst resume: $SRC_TYP -> $OUT_PDF..."
    typst compile "$SRC_TYP" "$OUT_PDF"
    echo "✅ CV PDF successfully generated at: $OUT_PDF"
else
    echo "⚠️ 'typst' CLI not found on local machine."
    echo "👉 You can install typst via 'cargo install --locked typst-cli' or download from https://github.com/typst/typst/releases"
    echo "👉 In CI/CD (GitHub Actions), Typst is automatically installed and compiled before Hugo builds."
fi
