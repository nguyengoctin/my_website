# Phase 3: Verify — Build và Kiểm tra

**Plan:** README.md  
**Type:** sequential

## Progress

| Status | Task |
|--------|------|
| ⬜ TODO | Task 1: Chạy `hugo --buildDrafts` kiểm tra build clean |
| ⬜ TODO | Task 2: Kiểm tra không còn vi phạm nào trong tất cả files |

## Tasks

### Task 1: Hugo build check

- **Lệnh:**
  ```bash
  hugo --buildDrafts 2>&1 | tail -20
  ```
- **Expected:** Build thành công, output cuối là `Total in XXX ms` hoặc tương tự, **không có dòng** `ERROR` hay `WARN`.
- **Verify:** Exit code = 0, không có ERROR

### Task 2: Final audit — zero violations

- **Lệnh:**
  ```bash
  python3 scripts/fix_mermaid_violations.py  # DRY_RUN=True (mặc định)
  ```
- **Expected output:**
  ```
  TOTAL FILES FIXED: 0
  TOTAL EMPTY LINES REMOVED: 0
  TOTAL AMPERSANDS FIXED: 0
  ```
- **Verify:** Tất cả counts = 0 (không còn vi phạm nào)

### Rollback

Nếu build fail sau Phase 1-2:
```bash
git diff content/posts/  # Xem thay đổi
git checkout content/posts/  # Khôi phục toàn bộ nếu cần
```
