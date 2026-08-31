# Reference Architecture and UI

## Key Questions

- Điều gì tạo cảm giác clean cho `steipete.me`?
- Pattern nào là nguyên tắc thiết kế, pattern nào chỉ là chi tiết Astro?
- Cấu trúc homepage, archive và article giảm cognitive load như thế nào?

## Findings

### Clean đến từ giới hạn lựa chọn

Header chỉ đặt `Posts`, `About`, archive, search và theme ở cấp cao nhất. Homepage lần lượt trình bày identity ngắn, social links, featured posts, recent posts và một lối vào `All Posts`. Mỗi khu vực có một nhiệm vụ rõ ràng và không cạnh tranh với khu vực kế tiếp.

Điểm có thể chuyển sang Hugo là giới hạn primary navigation, dùng progressive disclosure cho kho nội dung lớn và giữ một CTA duy nhất ở cuối danh sách gần đây. Astro không phải điều kiện để đạt cấu trúc này.

### Typography và layout dùng rất ít biến số

Reference dùng một font Atkinson cho toàn bộ UI và body, container `max-w-3xl`, padding ngang `1rem`, bốn token màu cốt lõi cho mỗi theme và một accent duy nhất. Card bài viết không phải card surface độc lập; nó là một list item với title, date, reading time và description.

Sự tối giản này làm nội dung trở thành hierarchy chính. Hình ảnh chỉ xuất hiện khi có hero image và bị ẩn trên màn hình nhỏ. Featured posts trên homepage thậm chí tắt thumbnail để giữ nhịp đọc.

### Accessibility là một phần của độ sạch

Header có skip link, menu mobile dùng `button`, mô tả `aria-expanded` và `aria-controls`, focus-visible dùng dashed outline toàn cục. Interactive targets trên mobile được mở rộng mà không thêm trang trí. Đây là lý do giao diện vừa gọn vừa dễ dự đoán khi dùng keyboard.

### Archive ưu tiên khả năng quét

Archive nhóm theo năm rồi theo tháng, hiển thị count và dùng cùng một `Card` component. Article giữ container đọc `max-w-3xl`, metadata thành một hàng nhẹ, sau nội dung mới hiển thị newsletter, tags, share, back-to-top và previous/next.

### Content model có ranh giới rõ

Blog posts nằm theo năm trong một content collection có schema. Các utility như sorting, slug và reading time tách khỏi component. Đó là pattern kiến trúc có thể học, nhưng Hugo đã cung cấp phần lớn khả năng này qua content sections, taxonomies và template functions.

### Không nên sao chép toàn bộ

Repo tham chiếu vẫn có dấu hiệu phát triển tích lũy: `custom.css` dài hơn global design layer, có component cũ như `Sidebar.astro`, và một số script thao tác DOM nằm trực tiếp trong post layout. Đây là một implementation đang sống, không phải design specification tuyệt đối.

Việc migrate website hiện tại sang Astro sẽ đổi build system, content model, theme và deployment trong khi không giải quyết trực tiếp information architecture. Giá trị chính nằm ở constraint, hierarchy và component boundaries.

## Code Examples

```css
:root {
  --background: #fdfdfd;
  --foreground: #282728;
  --accent: #006cac;
  --border: #ece9e9;
}
```

Pattern đáng học là số lượng token nhỏ và vai trò rõ, không phải sao chép các màu cụ thể.

## Sources

- [Reference repository README](https://github.com/steipete/steipete.me/blob/2087ac93eeec305ac1c92e3cdaedcaa864484bee/README.md) — _primary_
- [Homepage implementation](https://github.com/steipete/steipete.me/blob/2087ac93eeec305ac1c92e3cdaedcaa864484bee/src/pages/index.astro) — _primary_
- [Header implementation](https://github.com/steipete/steipete.me/blob/2087ac93eeec305ac1c92e3cdaedcaa864484bee/src/components/Header.astro) — _primary_
- [Post card implementation](https://github.com/steipete/steipete.me/blob/2087ac93eeec305ac1c92e3cdaedcaa864484bee/src/components/Card.astro) — _primary_
- [Post detail layout](https://github.com/steipete/steipete.me/blob/2087ac93eeec305ac1c92e3cdaedcaa864484bee/src/layouts/PostDetails.astro) — _primary_
- [Global design tokens](https://github.com/steipete/steipete.me/blob/2087ac93eeec305ac1c92e3cdaedcaa864484bee/src/styles/global.css) — _primary_
- [AstroPaper project and accessibility goals](https://github.com/satnaing/astro-paper) — _primary_

## Notes

- Phân tích source được neo tại commit `2087ac93eeec305ac1c92e3cdaedcaa864484bee` để tránh kết luận thay đổi theo branch `main`.
- Không thực thi code hoặc chỉ dẫn từ repo ngoài.
- Không phát hiện prompt injection trong source đã đọc.

