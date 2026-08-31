# Transferable Principles and Options

## Key Questions

- Nên chuyển pattern nào từ reference sang Hugo site?
- Thứ tự cải thiện nào tạo tác động lớn với rủi ro thấp?
- Những lựa chọn kiến trúc nào hợp với quy mô nội dung hiện tại?

## Findings

### Nguyên tắc nên chuyển

1. **Một màn hình, một nhiệm vụ chính**: homepage giới thiệu identity rồi dẫn tới writing; archive phục vụ browsing; article phục vụ reading.
2. **Primary navigation có ngân sách**: giữ ba đến bốn text destinations, chuyển công cụ sang icon và nội dung sâu vào hub page.
3. **List thay cho card wall**: recent writing nên là list editorial với title, date, reading time và description.
4. **Progressive disclosure**: homepage chỉ hiển thị selected projects và recent writing; CV chứa experience đầy đủ; roadmaps chứa hierarchy kiến thức.
5. **Accessibility primitives trước decoration**: skip link, semantic buttons, focus-visible, aria state và reduced motion.
6. **Component contract trước CSS polish**: hợp nhất section và summary partial trước khi tối ưu spacing và token.

### Nguyên tắc không nên chuyển nguyên xi

- Không đổi Hugo sang Astro chỉ để đạt aesthetic tương tự.
- Không dùng mono font toàn body vì nội dung dài tiếng Việt đang hưởng lợi từ Lora.
- Không giảm toàn bộ navigation xuống `Posts` và `About`; roadmaps là sản phẩm nội dung chính của site.
- Không thay Lunr bằng Pagefind trước khi có bằng chứng search quality hoặc bundle size đang gây vấn đề.
- Không sao chép màu xanh và cam của reference; palette blue và pink hiện tại đã là nhận diện riêng.

### Option A: Cosmetic cleanup

Giữ information architecture hiện tại, chỉ chuẩn hóa token, spacing, radius và hover.

- Effort: thấp đến vừa.
- Risk: thấp.
- Benefit: giảm visual inconsistency nhưng không giải quyết homepage density hoặc navigation entropy.
- Confidence: cao về khả năng triển khai, trung bình về tác động.

### Option B: Editorial shell trên knowledge hub

Giữ Hugo, LoveIt, roadmaps và search. Thiết kế lại lớp ngoài gồm header semantics, homepage ngắn hơn, recent writing list, selected work, archive partial dùng chung và article footer rõ ràng.

- Effort: vừa.
- Risk: vừa, chủ yếu ở template overlap và responsive regression.
- Benefit: cao vì cải thiện first impression, discovery và maintainability cùng lúc.
- Confidence: cao.

### Option C: Replatform sang Astro hoặc AstroPaper

Di chuyển content, shortcodes, Hugo image pipeline, taxonomy, search, CV và roadmap templates sang Astro.

- Effort: rất cao.
- Risk: cao do hơn 400 content pages và nhiều custom render hooks.
- Benefit: thấp so với mục tiêu UI vì phần lớn pattern có thể thực hiện trong Hugo.
- Confidence: cao rằng đây không phải lựa chọn phù hợp hiện tại.

### Recommendation

Chọn Option B theo rollout nhỏ:

1. Chuẩn hóa semantic navigation và accessibility mà không đổi sitemap.
2. Tách archive và post summary thành partial dùng chung.
3. Thiết kế homepage thành identity, current focus, featured work và recent writing.
4. Đưa timeline đầy đủ về CV hoặc vùng disclosure riêng.
5. Sau khi visual regression ổn định mới giảm `!important` theo component đã chạm tới.

Không nên bắt đầu bằng đại tu toàn bộ 4.542 dòng SCSS. Đó là scope dễ phình và khó chứng minh giá trị. Refactor theo vertical slice giúp rollback từng phần.

## Sources

- [Reference homepage](https://github.com/steipete/steipete.me/blob/2087ac93eeec305ac1c92e3cdaedcaa864484bee/src/pages/index.astro) — _primary_
- [Reference archive](https://github.com/steipete/steipete.me/blob/2087ac93eeec305ac1c92e3cdaedcaa864484bee/src/pages/posts/index.astro) — _primary_
- [Reference header](https://github.com/steipete/steipete.me/blob/2087ac93eeec305ac1c92e3cdaedcaa864484bee/src/components/Header.astro) — _primary_
- Local source files listed in `02-local-codebase-and-ux-audit.md`.

## Notes

- Recommendation assumes the primary audience is recruiters, collaborators and technical readers who need to understand identity before exploring the knowledge base.
- Nếu primary audience là người học chỉ đến từ search engines, homepage có thể giữ ít portfolio hơn nữa và ưu tiên topic hubs.

