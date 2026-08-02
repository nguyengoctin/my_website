---
title: "Hướng Dẫn Cấu Hình Và Sử Dụng Giao Diện LoveIt Cơ Bản"
author: "Dillon"
date: 2020-03-06
draft: false
description: "Khám phá giao diện Hugo - LoveIt và các khái niệm cốt lõi đằng sau nó."
tags: ["documentation", "installation", "configuration"]
categories: ["Tech Blog"]
---

Khám phá giao diện **Hugo - LoveIt** và các khái niệm cốt lõi đằng sau nó.

<!--more-->

---

## 1 Yêu cầu

Nhờ sự đơn giản của Hugo, Hugo là phụ thuộc (dependency) duy nhất của giao diện này.

Chỉ cần cài đặt phiên bản Hugo mới nhất cho hệ điều hành của bạn (Windows, Linux, macOS).

> [!NOTE]
> **Khi nào bạn cần sử dụng Hugo phiên bản Extended (Hugo extended edition)?**
> 
> Khi bạn muốn tùy chỉnh kiểu dáng (style customization), bạn cần sử dụng phiên bản Hugo extended để hiển thị/chuyển đổi SCSS sang CSS một cách chính xác.

---

## 2 Cài đặt

Các bước dưới đây sẽ giúp bạn khởi tạo trang web mới của mình. Nếu bạn chưa biết gì về Hugo, chúng tôi khuyên bạn nên tìm hiểu thêm thông qua tài liệu tuyệt vời dành cho người bắt đầu của Hugo.

### 2.1 Tạo Dự án của Bạn

Hugo cung cấp một lệnh mới để tạo một trang web mới:

```bash
hugo new site my_website
cd my_website
```

### 2.2 Cài đặt Giao diện (Theme)

Kho lưu trữ (repository) của giao diện LoveIt là: [https://github.com/dillonzq/LoveIt](https://github.com/dillonzq/LoveIt).

Bạn có thể tải xuống tệp nén `.zip` bản phát hành của giao diện và giải nén nó vào thư mục `themes`.

Hoặc, clone kho lưu trữ này vào thư mục `themes`:

```bash
git clone https://github.com/dillonzq/LoveIt.git themes/LoveIt
```

Hoặc, tạo một kho lưu trữ git rỗng và biến kho lưu trữ theme này thành một submodule trong thư mục trang web của bạn:

```bash
git init
git submodule add https://github.com/dillonzq/LoveIt.git themes/LoveIt
```

#### Độ tương thích của giao diện LoveIt

| Nhánh hoặc phiên bản LoveIt | Phiên bản Hugo được hỗ trợ |
| :--- | :--- |
| **master** (Unstable) | $\ge$ 0.128.0 |
| **0.3.X** (Khuyên dùng) | 0.128.0 - 0.145.0 |
| **0.2.X** (Cũ/Outdated) | 0.68.0 - 0.127.0 |

---

### 2.3 Cấu hình Cơ bản

Dưới đây là cấu hình cơ bản cho giao diện LoveIt:

```toml
baseURL = "http://example.org/"

# Thay đổi giao diện mặc định được sử dụng khi build trang web với Hugo
theme = "LoveIt"

# Tiêu đề trang web
title = "Trang Hugo Mới Của Tôi"

# Mã ngôn ngữ ["en", "zh-CN", "fr", "pl", ...]
languageCode = "en"
# Tên ngôn ngữ ["English", "简体中文", "Français", "Polski", ...]
languageName = "English"

# Cấu hình Menu
[menu]
  [[menu.main]]
    weight = 1
    identifier = "posts"
    # Bạn có thể thêm thông tin phụ trước tên (hỗ trợ định dạng HTML), ví dụ như icon
    pre = ""
    # Bạn có thể thêm thông tin phụ sau tên (hỗ trợ định dạng HTML), ví dụ như icon
    post = ""
    name = "Bài viết"
    url = "/posts/"
    # Tiêu đề sẽ hiển thị khi bạn rê chuột vào liên kết menu này
    title = ""
  [[menu.main]]
    weight = 2
    identifier = "tags"
    pre = ""
    post = ""
    name = "Thẻ"
    url = "/tags/"
    title = ""
  [[menu.main]]
    weight = 3
    identifier = "categories"
    pre = ""
    post = ""
    name = "Danh mục"
    url = "/categories/"
    title = ""

# Cấu hình liên quan đến Markup trong Hugo
[markup]
  # Tô màu cú pháp (Syntax Highlighting)
  [markup.highlight]
    # false là cấu hình bắt buộc
    noClasses = false
```

> [!NOTE]
> Khi build trang web, bạn có thể thiết lập giao diện bằng tùy chọn `--theme`. Tuy nhiên, chúng tôi khuyên bạn nên chỉnh sửa tệp cấu hình (`hugo.toml`) và đặt giao diện làm mặc định.

---

### 2.4 Tạo Bài viết Đầu tiên

Dưới đây là cách tạo bài viết đầu tiên của bạn:

```bash
hugo new posts/first_post.md
```

Hãy thoải mái chỉnh sửa tệp bài viết bằng cách thêm một số nội dung mẫu và thay đổi giá trị `title` ở phần đầu của tệp.

> [!NOTE]
> Theo mặc định, tất cả các bài viết và trang đều được tạo dưới dạng bản nháp (`draft`). Nếu bạn muốn hiển thị các trang này, hãy xóa thuộc tính `draft: true` khỏi phần metadata, đặt thuộc tính `draft: false` hoặc thêm tham số `-D`/`--buildDrafts` vào lệnh `hugo`.

---

### 2.5 Khởi chạy Trang web ở Local

Khởi chạy bằng lệnh sau:

```bash
hugo serve
```

Truy cập vào [http://localhost:1313](http://localhost:1313).

> [!TIP]
> Khi bạn chạy `hugo serve`, mỗi khi nội dung của các tệp thay đổi, trang web sẽ tự động làm mới với các thay đổi đó.

> [!NOTE]
> Vì giao diện sử dụng `.Scratch` trong Hugo để thực hiện một số tính năng, chúng tôi rất khuyên bạn nên thêm tham số `--disableFastRender` vào lệnh `hugo serve` để xem trước trực tiếp trang bạn đang chỉnh sửa:
> ```bash
> hugo serve --disableFastRender
> ```

---

### 2.6 Build Trang web

Khi trang web của bạn sẵn sàng để triển khai, hãy chạy lệnh sau:

```bash
hugo
```

Thư mục `public` sẽ được tạo ra, chứa tất cả nội dung tĩnh và tài nguyên cho trang web của bạn. Giờ đây, nó có thể được triển khai trên bất kỳ máy chủ web nào.

> [!TIP]
> Trang web có thể được tự động xuất bản và lưu trữ với Netlify. Hoặc bạn có thể sử dụng AWS Amplify, GitHub Pages, Render và nhiều dịch vụ khác…

---

## 3 Cấu hình

### 3.1 Cấu hình Trang web (Site Configuration)

Ngoài cấu hình toàn cục của Hugo và cấu hình menu, LoveIt cho phép bạn định nghĩa các tham số sau trong cấu hình trang web của bạn (dưới đây là tệp `hugo.toml` với các giá trị mặc định).

```toml
baseURL = "http://example.org/"

# Thay đổi giao diện mặc định được sử dụng khi build trang web với Hugo
theme = "LoveIt"

# Tiêu đề trang web
title = "Trang Hugo Mới Của Tôi"

# Mã ngôn ngữ ["en", "zh-CN", "fr", "pl", ...]
languageCode = "en"
# Tên ngôn ngữ ["English", "简体中文", "Français", "Polski", ...]
languageName = "English"
# Có bao gồm ngôn ngữ Trung/Nhật/Hàn hay không
hasCJKLanguage = false

# Mô tả bản quyền chỉ được sử dụng cho cấu hình SEO schema
copyright = ""

# Có sử dụng robots.txt hay không
enableRobotsTXT = true
# Có sử dụng nhật ký git commit hay không
enableGitInfo = true
# Có sử dụng mã emoji hay không
enableEmoji = true

# Bỏ qua một số lỗi build
ignoreErrors = ["error-remote-getjson", "error-missing-instagram-accesstoken"]

# Cấu hình phân trang (Pagination)
[pagination]
  disableAliases = false
  pagerSize = 10
  path = "page"

# Cấu hình Menu
[menu]
  [[menu.main]]
    weight = 1
    identifier = "posts"
    pre = ""
    post = ""
    name = "Bài viết"
    url = "/posts/"
    title = ""
  [[menu.main]]
    weight = 2
    identifier = "tags"
    pre = ""
    post = ""
    name = "Thẻ"
    url = "/tags/"
    title = ""
  [[menu.main]]
    weight = 3
    identifier = "categories"
    pre = ""
    post = ""
    name = "Danh mục"
    url = "/categories/"
    title = ""

[params]
  # Giao diện mặc định của trang web ["auto", "light", "dark"]
  defaultTheme = "auto"
  # URL kho lưu trữ git công khai chỉ khi enableGitInfo là true
  gitRepo = ""
  # Hàm băm được sử dụng cho SRI, khi để trống sẽ không sử dụng SRI
  # ["sha256", "sha384", "sha512", "md5"]
  fingerprint = ""
  # Định dạng ngày tháng
  dateFormat = "2006-01-02"
  # Tiêu đề trang web cho Open Graph và Twitter Cards
  title = "Trang web xịn của tôi"
  # Mô tả trang web cho RSS, SEO, Open Graph và Twitter Cards
  description = "Đây là trang web xịn của tôi"
  # Hình ảnh trang web cho Open Graph và Twitter Cards
  images = ["/logo.png"]

# Cấu hình Tác giả (Author)
  [params.author]
    name = "xxxx"
    email = ""
    link = ""

  # Cấu hình Header
  [params.header]
    # Chế độ header trên máy tính ["fixed", "normal", "auto"]
    desktopMode = "fixed"
    # Chế độ header trên di động ["fixed", "normal", "auto"]
    mobileMode = "auto"
    # Cấu hình tiêu đề Header
    [params.header.title]
      # URL của LOGO
      logo = ""
      # Tên tiêu đề
      name = ""
      # Bạn có thể thêm thông tin phụ trước tên (hỗ trợ HTML)
      pre = ""
      # Bạn có thể thêm thông tin phụ sau tên (hỗ trợ HTML)
      post = ""
      # Có sử dụng hiệu ứng gõ chữ typeit cho tiêu đề hay không
      typeit = false

  # Cấu hình Footer
  [params.footer]
    enable = true
    # Nội dung tùy chỉnh (hỗ trợ HTML)
    custom = ''
    # Có hiển thị thông tin Hugo và giao diện hay không
    hugo = true
    # Có hiển thị thông tin bản quyền hay không
    copyright = true
    # Có hiển thị tác giả hay không
    author = true
    # Thời gian tạo trang web
    since = 2019
    # Thông tin ICP chỉ ở Trung Quốc (hỗ trợ HTML)
    icp = ""
    # Thông tin giấy phép (hỗ trợ HTML)
    license = '<a rel="license external nofollow noopener noreffer" href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank">CC BY-NC 4.0</a>'

  # Cấu hình trang Section (tất cả bài viết)
  [params.section]
    paginate = 20
    dateFormat = "01-02"
    rss = 10

  # Cấu hình trang Danh sách (List - danh mục hoặc thẻ)
  [params.list]
    paginate = 20
    dateFormat = "01-02"
    rss = 10

  # Cấu hình App icon
  [params.app]
    title = "Trang web xịn của tôi"
    noFavicon = false
    svgFavicon = ""
    themeColor = "#ffffff"
    iconColor = "#5bbad5"
    tileColor = "#da532c"

  # Cấu hình Tìm kiếm (Search)
  [params.search]
    enable = true
    # Loại công cụ tìm kiếm ["lunr", "algolia"]
    type = "lunr"
    contentLength = 4000
    placeholder = ""
    maxResultLength = 10
    snippetLength = 30
    highlightTag = "em"
    absoluteURL = false
    [params.search.algolia]
      index = ""
      appID = ""
      searchKey = ""

  # Cấu hình Trang chủ (Home page)
  [params.home]
    rss = 10
    # Hồ sơ trang chủ
    [params.home.profile]
      enable = true
      gravatarEmail = ""
      avatarURL = "/images/avatar.webp"
      title = ""
      subtitle = "Đây là Trang Hugo Mới Của Tôi"
      typeit = true
      social = true
      disclaimer = ""
    # Bài viết trang chủ
    [params.home.posts]
      enable = true
      paginate = 6

  # Cấu hình Mạng xã hội của tác giả
  [params.social]
    GitHub = "xxxx"
    Linkedin = ""
    X = "xxxx"
    Twitter = ""
    Instagram = "xxxx"
    Facebook = "xxxx"
    Telegram = "xxxx"
    Medium = ""
    Email = "xxxx@xxxx.com"
    RSS = true

  # Cấu hình Toàn cục Trang (Page global config)
  [params.page]
    hiddenFromHomePage = false
    hiddenFromSearch = false
    twemoji = false
    lightgallery = false
    ruby = true
    fraction = true
    fontawesome = true
    linkToMarkdown = true
    rssFullText = false

    # Mục lục (Table of contents)
    [params.page.toc]
      enable = true
      keepStatic = false
      auto = true

    # Công thức toán học KaTeX
    [params.page.math]
      enable = true
      inlineLeftDelimiter = ""
      inlineRightDelimiter = ""
      blockLeftDelimiter = ""
      blockRightDelimiter = ""
      copyTex = true
      mhchem = true

    # Cấu hình Mã nguồn (Code)
    [params.page.code]
      copy = true
      maxShownLines = 50

    # Cấu hình Chia sẻ mạng xã hội
    [params.page.share]
      enable = true
      X = true
      Facebook = true
      Telegram = true
      Linkedin = false
      Whatsapp = false

    # Cấu hình Bình luận (Comment)
    [params.page.comment]
      enable = false
      [params.page.comment.disqus]
        enable = false
        shortname = ""
      [params.page.comment.giscus]
        enable = false

  # Cấu hình Thư viện bên thứ ba
  [params.page.library]
    [params.page.library.css]
    [params.page.library.js]

  # Cấu hình SEO trang
  [params.page.seo]
    images = []
    [params.page.seo.publisher]
      name = ""
      logoUrl = ""

  # Cấu hình TypeIt
  [params.typeit]
    speed = 100
    cursorSpeed = 1000
    cursorChar = "|"
    duration = -1

  # Cấu hình SEO trang web
  [params.seo]
    image = ""
    thumbnailUrl = ""

  # Cấu hình Phân tích (Analytics)
  [params.analytics]
    enable = true
    [params.analytics.google]
      id = ""
      respectDoNotTrack = false

  # Cấu hình Chấp nhận Cookie
  [params.cookieconsent]
    enable = true
    [params.cookieconsent.content]
      message = ""
      dismiss = ""
      link = ""

  # Cấu hình CDN
  [params.cdn]
    data = ""

  # Cấu hình Độ tương thích
  [params.compatibility]
    polyfill = false
    objectFit = false

# Cấu hình Markup trong Hugo
[markup]
  [markup.highlight]
    codeFences = true
    guessSyntax = true
    lineNos = true
    lineNumbersInTable = true
    noClasses = false
  [markup.goldmark]
    [markup.goldmark.extensions]
      definitionList = true
      footnote = true
      linkify = true
      strikethrough = true
      table = true
      taskList = true
      typographer = true
    [markup.goldmark.renderer]
      unsafe = true
  [markup.tableOfContents]
    startLevel = 2
    endLevel = 6

[sitemap]
  changefreq = "weekly"
  filename = "sitemap.xml"
  priority = 0.5

[Permalinks]
  posts = ":filename"

[mediaTypes]
  [mediaTypes."text/plain"]
    suffixes = ["md"]

[outputFormats.MarkDown]
  mediaType = "text/plain"
  isPlainText = true
  isHTML = false

[outputs]
  home = ["HTML", "RSS", "JSON"]
  page = ["HTML", "MarkDown"]
  section = ["HTML", "RSS"]
  taxonomy = ["HTML", "RSS"]
```

> [!NOTE]
> Môi trường mặc định là `development` khi dùng `hugo serve` và `production` khi dùng `hugo`.
> Do các hạn chế trong môi trường phát triển cục bộ, hệ thống bình luận, CDN và fingerprint sẽ không được bật. Bạn có thể bật các tính năng này bằng lệnh: `hugo serve -e production`.

---

### 3.2 Favicons, Browserconfig, Manifest

Khuyên bạn nên đặt các biểu tượng favicon riêng của mình:
- `apple-touch-icon.png` (180x180)
- `favicon-32x32.png` (32x32)
- `favicon-16x16.png` (16x16)
- `mstile-150x150.png` (150x150)
- `android-chrome-192x192.png` (192x192)
- `android-chrome-512x512.png` (512x512)

Vào thư mục `/static`. Chúng dễ dàng được tạo thông qua [https://realfavicongenerator.net/](https://realfavicongenerator.net/).

Chỉnh sửa `browserconfig.xml` và `site.webmanifest` để đặt `theme-color` và `background-color`.

---

### 3.3 Tùy chỉnh Kiểu dáng (Style Customization)

> [!IMPORTANT]
> **Yêu cầu phiên bản Hugo Extended**
> Vì Hugo cần xử lý SCSS sang CSS, phiên bản Hugo extended là bắt buộc để tùy chỉnh kiểu dáng.

Giao diện LoveIt được thiết kế để có thể cấu hình linh hoạt bằng cách định nghĩa các tệp kiểu dáng `.scss` tùy chỉnh.

Thư mục chứa các tệp kiểu dáng `.scss` tùy chỉnh là `assets/css` tương đối so với thư mục gốc dự án của bạn.

Trong `assets/css/_override.scss`, bạn có thể ghi đè các biến trong `themes/LoveIt/assets/css/_variables.scss` để tùy chỉnh giao diện. Ví dụ:

```scss
@import url('https://fonts.googleapis.com/css?family=Fira+Mono:400,700&display=swap&subset=latin-ext');
$code-font-family: Fira Mono, Source Code Pro, Menlo, Consolas, Monaco, monospace;
```

Trong `assets/css/_custom.scss`, bạn có thể thêm mã CSS tùy chỉnh để điều chỉnh kiểu dáng.

---

## 4 Đa ngôn ngữ và i18n

Giao diện LoveIt hoàn toàn tương thích với chế độ đa ngôn ngữ của Hugo, cung cấp khả năng chuyển đổi ngôn ngữ ngay trong trình duyệt.

### 4.1 Độ tương thích

| Ngôn ngữ | Mã Hugo | Thuộc tính lang HTML | Hỗ trợ Lunr.js |
| :--- | :--- | :--- | :--- |
| **Tiếng Anh (English)** | `en` | `en` | $\checkmark$ |
| **Tiếng Trung Giản thể** | `zh-cn` | `zh-CN` | $\checkmark$ |
| **Tiếng Trung Phồn thể** | `zh-tw` | `zh-TW` | $\checkmark$ |
| **Tiếng Pháp (French)** | `fr` | `fr` | $\checkmark$ |
| **Tiếng Ba Lan (Polish)** | `pl` | `pl` | $\checkmark$ |
| **Tiếng Bồ Đào Nha (Brazil)** | `pt-br` | `pt-BR` | $\checkmark$ |
| **Tiếng Ý (Italian)** | `it` | `it` | $\checkmark$ |
| **Tiếng Tây Ban Nha** | `es` | `es` | $\checkmark$ |
| **Tiếng Đức (German)** | `de` | `de` | $\checkmark$ |
| **Tiếng Nga (Russian)** | `ru` | `ru` | $\checkmark$ |
| **Tiếng Việt (Vietnamese)** | `vi` | `vi` | $\checkmark$ |
| **Tiếng Nhật (Japanese)** | `ja` | `ja` | $\checkmark$ |
| **Tiếng Hàn (Korean)** | `ko` | `ko` | $\checkmark$ |

### 4.2 Cấu hình Cơ bản

Xác định ngôn ngữ của bạn trong cấu hình trang web. Ví dụ với trang web tiếng Anh, tiếng Trung và tiếng Pháp:

```toml
# Xác định ngôn ngữ nội dung mặc định ["en", "zh-cn", "fr", "pl", ...]
defaultContentLanguage = "en"

[languages]
  [languages.en]
    weight = 1
    title = "Trang Hugo Mới Của Tôi"
    languageCode = "en"
    languageName = "English"

  [languages.zh-cn]
    weight = 2
    title = "我的全新 Hugo 网站"
    languageCode = "zh-CN"
    languageName = "简体中文"
    hasCJKLanguage = true

  [languages.fr]
    weight = 3
    title = "Mon nouveau site Hugo"
    languageCode = "fr"
    languageName = "Français"
```

Sau đó, đối với mỗi trang mới, hãy thêm mã ngôn ngữ vào tên tệp.
Tệp đơn `my-page.md` được tách thành ba tệp:
- Tiếng Anh: `my-page.en.md`
- Tiếng Trung: `my-page.zh-cn.md`
- Tiếng Pháp: `my-page.fr.md`

---

## 5 Tìm kiếm (Search)

Dựa trên **Lunr.js** hoặc **Algolia**, tính năng tìm kiếm được hỗ trợ trong giao diện LoveIt.

### 5.1 Cấu hình Đầu ra

Để tạo `index.json` cho việc tìm kiếm, thêm loại tệp đầu ra `JSON` vào phần `home` của cấu hình `outputs`:

```toml
[outputs]
  home = ["HTML", "RSS", "JSON"]
```

### 5.2 Cấu hình Tìm kiếm

Dựa trên tệp `index.json` được tạo bởi Hugo, bạn có thể kích hoạt tính năng tìm kiếm:

```toml
[params.search]
  enable = true
  # Loại công cụ tìm kiếm ["lunr", "algolia"]
  type = "lunr"
  contentLength = 4000
  placeholder = ""
  maxResultLength = 10
  snippetLength = 30
  highlightTag = "em"
  absoluteURL = false
```

#### So sánh công cụ tìm kiếm:
- **lunr**: Đơn giản, không cần đồng bộ `index.json`, không giới hạn `contentLength`, nhưng tốn băng thông hơn và hiệu năng thấp hơn.
- **algolia**: Hiệu năng cao và tiết kiệm băng thông, nhưng cần đồng bộ `index.json` và có giới hạn đối với `contentLength`.
