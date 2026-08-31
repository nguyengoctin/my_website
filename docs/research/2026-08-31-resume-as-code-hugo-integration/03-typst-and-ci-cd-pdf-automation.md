# Tự Động Hóa Xuất PDF: Typst và CI/CD Pipeline

## Key Questions

- So sánh giữa Typst, Headless Chromium (Playwright/Chrome CLI) và LaTeX trong bài toán biên dịch CV tự động: Đâu là lựa chọn tối ưu về tốc độ, kích thước và độ tin cậy?
- Làm thế nào để thiết lập GitHub Actions tự động biên dịch mã nguồn CV thành file `static/cv.pdf` mỗi khi có commit mới?
- Cách tổ chức source code Typst hoặc script headless browser trong cùng repository với website Hugo?

## Findings

### Ma Trận So Sánh Các Giải Pháp Biên Dịch PDF Tự Động

| Tiêu chí | Typst Pipeline | Headless Chromium (Playwright / Chrome CLI) | LaTeX (TeX Live / XeLaTeX) |
| :--- | :--- | :--- | :--- |
| **Tốc độ build** | **Cực nhanh (~20 - 50ms)** | Trung bình (~5 - 15 giây khởi động browser) | Chậm (~30 - 60 giây) |
| **Kích thước dependency CI** | **Rất nhẹ (~30MB binary)** | Nặng (~300MB - 500MB Node.js + browser) | Rất nặng (~2GB - 4GB TeX packages) |
| **Độ chính xác Typographic** | **Hoàn hảo (chuẩn ấn bản)** | Tương đối (phụ thuộc engine CSS print) | Hoàn hảo (chuẩn học thuật) |
| **Trải nghiệm viết code** | Cú pháp hiện đại, rõ ràng, dễ học | Viết HTML/CSS quen thuộc | Cú pháp macro phức tạp, khó debug |
| **Bảo trì dài hạn** | Rất cao (single binary, độc lập) | Trung bình (dễ lệch nếu Chromium update) | Cao nhưng cồng kềnh |

### Xu hướng dịch chuyển sang Typst

Trong giai đoạn 2024 - 2026, cộng đồng mã nguồn mở (đặc biệt trên Hacker News và GitHub) có xu hướng dịch chuyển ồ ạt từ LaTeX sang **Typst** cho các tài liệu cá nhân và CV vì:
1. **Tính độc lập:** Typst phân phối dưới dạng 1 file binary duy nhất được viết bằng Rust, không cần cài đặt hàng nghìn package phụ thuộc.
2. **Khả năng script hóa:** Typst hỗ trợ cấu trúc dữ liệu, vòng lặp, hàm và biến ngay trong cú pháp mà không cần dùng đến các macro rắc rối như TeX.
3. **Chất lượng PDF xuất ra:** File PDF do Typst sinh ra tuân thủ nghiêm ngặt tiêu chuẩn PDF/A, font chữ được nhúng đầy đủ (embedded subsets), đảm bảo 100% khả năng highlight, copy và tương thích tuyệt đối với các bộ máy OCR/ATS.

### Chiến lược tích hợp vào Hugo

Chúng ta có hai chiến lược tự động hóa:
*   **Phương án A (Typst-first):** Lưu file `resume.typ` trong thư mục `assets/cv/` hoặc `cv/`. Trong workflow CI/CD của GitHub Actions, chạy lệnh `typst compile resume.typ static/cv.pdf` ngay trước bước `hugo --minify`. Khi Hugo build, file `cv.pdf` sẽ tự động nằm ở thư mục gốc của trang web (`https://domain/cv.pdf`).
*   **Phương án B (HTML-first + Headless Chrome):** Hugo build ra trang `/cv/index.html`, sau đó dùng Chrome CLI trong CI/CD để in trang đó ra `static/cv.pdf`.

## Code Examples

### 1. File mẫu Typst tinh gọn (`cv/resume.typ`)

```typst
#set page(
  paper: "a4",
  margin: (x: 1.5cm, y: 1.5cm),
)

#set text(
  font: "Liberation Sans",
  size: 10pt,
  lang: "en",
)

#let section(title) = {
  v(8pt)
  text(weight: "bold", size: 12pt, upper(title))
  v(-3pt)
  line(length: 100%, stroke: 0.5pt + gray)
  v(2pt)
}

#let item(title, subtitle, date, location, details) = {
  grid(
    columns: (1fr, auto),
    text(weight: "bold", title) + if subtitle != "" [ --- #text(style: "italic", subtitle)] else [],
    text(style: "italic", fill: luma(100), date),
  )
  if location != "" {
    v(-4pt)
    text(size: 8.5pt, fill: luma(120), location)
  }
  v(2pt)
  list(..details)
  v(4pt)
}

// Header
#align(center)[
  #text(size: 20pt, weight: "bold")[Nguyen Ngoc Tin] \
  #v(2pt)
  #text(size: 10.5pt)[Software Engineer and Solutions Architect] \
  #v(4pt)
  #text(size: 9pt)[
    tin\@example.com #h(4pt) • #h(4pt)
    +84 900 000 000 #h(4pt) • #h(4pt)
    #link("https://ngoctin.dev")[ngoctin.dev] #h(4pt) • #h(4pt)
    Ho Chi Minh City, Vietnam
  ]
]

// Sections
#section("Experience")

#item(
  "Tech Solutions Corp",
  "Senior Backend Engineer",
  "2023 - Present",
  "Ho Chi Minh City, Vietnam",
  (
    [Thiết kế và tối ưu pipeline xử lý dữ liệu giảm *40%* latency hệ thống.],
    [Xây dựng hạ tầng CI/CD tự động hóa toàn bộ quy trình kiểm thử và deploy.],
    [Chủ trì kiến trúc microservices phục vụ hơn 500k active users hàng ngày.],
  )
)

#section("Technical Skills")
- *Languages:* Go, TypeScript, Python, Rust, SQL
- *Frameworks and Tools:* Hugo, Docker, Kubernetes, PostgreSQL, TailwindCSS
```

### 2. GitHub Actions Workflow Tích Hợp Build Typst và Hugo

```yaml
name: Deploy Hugo Website with Automated CV Build

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      # 1. Cài đặt Typst và biên dịch PDF
      - name: Setup Typst
        uses: enter-at/setup-typst@v0.3
        with:
          typst-version: "latest"

      - name: Compile CV to PDF
        run: |
          mkdir -p static
          typst compile cv/resume.typ static/cv.pdf

      # 2. Cài đặt Hugo và build toàn bộ website
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: "latest"
          extended: true

      - name: Build Hugo Site
        run: hugo --gc --minify

      # 3. Deploy
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

## Sources

- [Typst Official Documentation and CLI Reference](https://typst.app/docs/) — _primary_
- [setup-typst GitHub Action](https://github.com/enter-at/setup-typst) — _primary_
- [RenderCV: Open Source CLI for Resume as Code](https://github.com/rendercv/rendercv) — _primary_
- [Hacker News: Typst: A new markup-based typesetting system](https://news.ycombinator.com/item?id=35243144) — _secondary / background_

## Notes

- Font chữ mặc định của Typst trong môi trường GitHub Actions Ubuntu runner có sẵn các font phổ biến như `Liberation Sans`, `DejaVu Sans`. Nếu cần font tùy biến (ví dụ `Inter` hoặc `Roboto`), chỉ cần đặt file font `.ttf`/`.otf` trong thư mục `fonts/` và truyền cờ `--font-path fonts/` khi gọi lệnh `typst compile`.
- Không cần cài đặt bất kỳ runtime nặng nề nào khác; toàn bộ bước build Typst chỉ tốn chưa tới 2 giây trong GitHub Actions.
