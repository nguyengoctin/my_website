---
slug: 2026-08-26-fix-mermaid-violations
auto: false
status: done
---

# Plan: Fix Mermaid Best Practice Violations

**Mode:** normal  
**Created:** 2026-08-26  
**Status:** DONE

## Overview

Dựa trên research `2026-08-26-hugo-mermaid-bestpractice`, toàn bộ 13 file Markdown có Mermaid vi phạm đã được chuẩn hóa hoàn toàn:
- Loại bỏ toàn bộ các dòng trống không hợp lệ.
- Thay thế ký tự `&` thành chữ "và" trong nhãn node.
- Rút gọn 5 diamond nodes `{}` quá dài để chống tràn góc.

## Progress

| Status | Phase | File | Tasks |
|--------|-------|------|-------|
| ✅ DONE | Phase 1: Auto Fix | phase-1-auto-fix.md | 2 tasks |
| ✅ DONE | Phase 2: Manual Fix | phase-2-manual-fix.md | 3 tasks |
| ✅ DONE | Phase 3: Verify | phase-3-verify.md | 2 tasks |

## Assumptions

- Script `scripts/fix_mermaid_violations.py` đã chạy dry run thành công: 13 files, 28 empty lines, 3 ampersands
- Hugo dev server đang chạy tại `localhost:1313`
- `hugo --buildDrafts` là lệnh kiểm tra cuối cùng

## Risks

- Script thay thế `&` bằng "và" có thể miss trường hợp nếu & không có space quanh (e.g. `A&B`): đã kiểm tra, không có trường hợp này trong codebase
- Một số editor tự thêm lại empty line khi lưu file — cần kiểm tra sau khi sửa

## Next Steps

Sau implementation: `hugo --buildDrafts` -> `/cf-review` -> `/cf-commit`
