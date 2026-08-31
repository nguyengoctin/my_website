# Kiến Trúc Dữ Liệu Nguồn Cho CV: Markdown và YAML trong Hugo

## Key Questions

- Lưu trữ nội dung CV trong `data/cv.yaml` (dữ liệu có cấu trúc) hay `content/cv.md` (Markdown thuần) tối ưu hơn cho bảo trì dài hạn?
- Làm thế nào để duy trì nguyên lý "Single Source of Truth" khi cần xuất ra nhiều định dạng khác nhau (Web HTML, Print PDF, Typst)?
- Giới hạn và ưu nhược điểm của schema chuẩn hóa JSON Resume so với Custom YAML Schema trong hệ sinh thái Hugo là gì?

## Findings

### So sánh mô hình lưu trữ: Markdown thuần so với Structured Data (YAML)

Khi tích hợp CV vào static site generator như Hugo, cộng đồng kỹ thuật phân hóa thành hai trường phái rõ rệt:

1. **Trường phái Content-first (Markdown thuần trong `content/cv.md`):**
   - *Cơ chế:* Nội dung CV được viết bằng các đề mục Markdown (`#`, `##`), danh sách gạch đầu dòng (`-`) và định dạng in đậm.
   - *Ưu điểm:* Viết rất nhanh, trực quan khi chỉnh sửa văn bản, render tự nhiên thông qua pipeline Markdown mặc định của Hugo (Goldmark).
   - *Nhược điểm:* Khó bóc tách dữ liệu để tái sử dụng ở nơi khác (ví dụ: tạo file JSON, đẩy qua template Typst hoặc render các UI component tùy biến). Việc can thiệp vào cấu trúc hiển thị phụ thuộc hoàn toàn vào CSS hoặc Custom Render Hooks.

2. **Trường phái Data-first (Structured Data trong `data/cv.yaml` hoặc `data/cv.json`):**
   - *Cơ chế:* Tách hoàn toàn dữ liệu thô (thông tin cá nhân, danh sách công việc, kỹ năng, học vấn, dự án) thành các trường key-value rõ ràng.
   - *Ưu điểm:* Dữ liệu độc lập hoàn toàn với giao diện. Hugo có thể đọc qua biến `.Site.Data.cv` và lặp qua các mảng để render HTML với layout chuẩn. Dữ liệu này cũng có thể chia sẻ trực tiếp sang các script chuyển đổi (như RenderCV hoặc Typst compile script).
   - *Nhược điểm:* Cú pháp YAML khắt khe về thụt đầu dòng (indentation). Việc viết các đoạn văn dài có chứa liên kết hoặc formatting yêu cầu cú pháp multiline string của YAML (`|` hoặc `>`).

### Vấn đề của JSON Resume Schema trong môi trường Hugo

JSON Resume (`resume.json`) cung cấp một tiêu chuẩn mở cho CV. Tuy nhiên, trong thực tế triển khai trên website cá nhân:
- Schema của JSON Resume khá cứng nhắc ở một số trường thực tế của lập trình viên (ví dụ: mục Technical Highlights, Architecture Decisions, hoặc các chứng chỉ phi truyền thống).
- Khi nhúng vào Hugo, `cv.yaml` với cấu trúc tùy biến (custom schema) mang lại tính linh hoạt cao hơn nhiều, cho phép định nghĩa các trường bổ sung như `featured: true`, `tech_stack: [...]`, hoặc `highlight_metrics: [...]` mà không vi phạm schema validator.

### Mô hình Hybrid tối ưu cho Hugo

Mô hình được cộng đồng khuyến nghị cao nhất cho Hugo là **Hybrid Structured Data**:
- Lưu dữ liệu chính trong `data/cv.yaml`.
- Các mô tả chi tiết của từng vị trí công việc hỗ trợ cú pháp Markdown inline (dùng hàm `markdownify` của Hugo khi render).
- Tạo một trang `content/cv/_index.md` hoặc `content/cv.md` làm điểm kích hoạt URL `/cv`, trong đó layout tương ứng sẽ nạp dữ liệu từ `data/cv.yaml`.

## Code Examples

### Cấu trúc file dữ liệu `data/cv.yaml`

```yaml
basics:
  name: "Nguyen Ngoc Tin"
  label: "Software Engineer and Solutions Architect"
  email: "tin@example.com"
  phone: "+84 900 000 000"
  website: "https://ngoctin.dev"
  location: "Ho Chi Minh City, Vietnam"
  summary: >
    Kỹ sư phần mềm tập trung vào hệ thống phân tán, kiến trúc hiệu năng cao
    và tối ưu hóa hạ tầng web.

skills:
  - category: "Languages"
    items: ["Go", "TypeScript", "Python", "Rust", "SQL"]
  - category: "Frameworks and Tools"
    items: ["Hugo", "Docker", "Kubernetes", "PostgreSQL", "TailwindCSS"]

experience:
  - company: "Tech Solutions Corp"
    position: "Senior Backend Engineer"
    location: "Ho Chi Minh City"
    start_date: "2023-01"
    end_date: "Present"
    highlights:
      - "Thiết kế và tối ưu pipeline xử lý dữ liệu giảm **40%** latency hệ thống."
      - "Xây dựng hạ tầng CI/CD tự động hóa toàn bộ quy trình kiểm thử và deploy."
      - "Chủ trì kiến trúc microservices phục vụ hơn 500k active users hàng ngày."

education:
  - institution: "University of Technology"
    area: "Computer Science"
    study_type: "Bachelor of Engineering"
    start_date: "2018"
    end_date: "2022"
```

### Template render trong Hugo (`layouts/cv/single.html` hoặc `layouts/page/cv.html`)

```html
{{ define "main" }}
{{ $cv := .Site.Data.cv }}
<article class="resume-container">
  <header class="resume-header">
    <h1 class="resume-name">{{ $cv.basics.name }}</h1>
    <p class="resume-title">{{ $cv.basics.label }}</p>
    <div class="resume-contact">
      <span>{{ $cv.basics.email }}</span>
      <span>•</span>
      <span>{{ $cv.basics.location }}</span>
      <span>•</span>
      <a href="{{ $cv.basics.website }}">{{ $cv.basics.website }}</a>
    </div>
  </header>

  <section class="resume-section">
    <h2>Experience</h2>
    {{ range $cv.experience }}
    <div class="resume-item">
      <div class="resume-item-header">
        <h3 class="company">{{ .company }} — <span class="position">{{ .position }}</span></h3>
        <span class="date">{{ .start_date }} - {{ .end_date }}</span>
      </div>
      <ul class="resume-highlights">
        {{ range .highlights }}
        <li>{{ . | markdownify }}</li>
        {{ end }}
      </ul>
    </div>
    {{ end }}
  </section>
</article>
{{ end }}
```

## Sources

- [Hugo Data Templates Documentation](https://gohugo.io/templates/data-templates/) — _primary_
- [JSON Resume Standard Specification](https://jsonresume.org/schema/) — _primary_
- [RenderCV: A Python-based Resume Engine (YAML to PDF/HTML)](https://github.com/rendercv/rendercv) — _primary_
- [Hacker News discussion: Managing your resume with text and code](https://news.ycombinator.com/item?id=38198754) — _secondary / background_

## Notes

- Sử dụng `markdownify` trong Hugo layout cho phép định dạng bold, code inline hoặc liên kết ngay trong danh sách highlights của YAML mà không làm mất cấu trúc dữ liệu.
- Định dạng ngày tháng (`YYYY-MM`) trong YAML nên giữ dạng ISO để tiện cho việc format qua các helper date của Hugo (`time.Format`).
