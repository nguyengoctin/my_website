# Phase 2: Manual Fix — Diamond Nodes Quá Dài

**Plan:** README.md  
**Type:** sequential

## Progress

| Status | Task |
|--------|------|
| ⬜ TODO | Task 1: Fix diamond nodes trong `bep-di-6-zalo-mini-app-ordering-platform.md` |
| ⬜ TODO | Task 2: Fix diamond nodes trong `toan-tap-coding-friend-ai-engineering.md` |
| ⬜ TODO | Task 3: Fix diamond nodes trong `tu-duy-viet-claudemd-thuc-chien.md` |

## Context

Node hình thoi `{...}` trong Mermaid có góc nhọn 45°. Khi nội dung > 20 ký tự sẽ bị cắt bởi đường viền. Quy tắc: **tối đa 20 ký tự** trong diamond node.

## Tasks

### Task 1: `bep-di-6-zalo-mini-app-ordering-platform.md` — Block 2

- **File:** `content/posts/bep-di-6-zalo-mini-app-ordering-platform.md`
- **Vi phạm:** `AtomicTx{"transaction.atomic()<br/>Bảo toàn dữ liệu"}` — quá dài
- **Sửa:**
  ```
  TRƯỚC: AtomicTx{"transaction.atomic()<br/>Bảo toàn dữ liệu"}
  SAU:   AtomicTx{"transaction.atomic()"}
  ```
  Xóa `<br/>Bảo toàn dữ liệu` để label chỉ còn tên hàm ngắn gọn.
- **Verify:** Mermaid preview không bị cắt góc nhọn

### Task 2: `toan-tap-coding-friend-ai-engineering.md` — Block 3, Block 4

- **File:** `content/posts/toan-tap-coding-friend-ai-engineering.md`
- **Vi phạm Block 3:** `ModeCheck{"Phân loại chế độ?<br/>Quy mô và mức độ kiểm soát"}` — quá dài
- **Vi phạm Block 4:** `CheckTest{"Có cờ --add-tests?<br/>Bật chế độ TDD"}` — quá dài
- **Sửa Block 3:**
  ```
  TRƯỚC: ModeCheck{"Phân loại chế độ?<br/>Quy mô và mức độ kiểm soát"}
  SAU:   ModeCheck{"Phân loại chế độ?"}
  ```
- **Sửa Block 4:**
  ```
  TRƯỚC: CheckTest{"Có cờ --add-tests?<br/>Bật chế độ TDD"}
  SAU:   CheckTest{"Có --add-tests?"}
  ```
- **Verify:** Cả 2 blocks render đúng, không bị cắt

### Task 3: `tu-duy-viet-claudemd-thuc-chien.md` — Block 1, Block 2

- **File:** `content/posts/tu-duy-viet-claudemd-thuc-chien.md`
- **Vi phạm Block 1:** `Check{"Phân loại điểm nghẽn?<br/>Năng lực hay quy trình"}` — quá dài
- **Vi phạm Block 2:** `CheckRule{"Phân loại tính chất?<br/>Cưỡng chế hay Hướng dẫn"}` — quá dài
- **Sửa Block 1:**
  ```
  TRƯỚC: Check{"Phân loại điểm nghẽn?<br/>Năng lực hay quy trình"}
  SAU:   Check{"Điểm nghẽn ở đâu?"}
  ```
- **Sửa Block 2:**
  ```
  TRƯỚC: CheckRule{"Phân loại tính chất?<br/>Cưỡng chế hay Hướng dẫn"}
  SAU:   CheckRule{"Tính chất quy tắc?"}
  ```
- **Verify:** Cả 2 blocks render đúng, diamond node hiển thị gọn
