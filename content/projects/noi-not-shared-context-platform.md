---
title: "Nối Nốt: Nền tảng Context Chung Cho Hệ Sinh Thái Ứng Dụng Đa Miền"
date: 2026-09-30T10:00:00+07:00
draft: false
author: "Nguyen Ngoc Tin"
description: "Thiết kế kiến trúc Shared Context Platform 3 tầng giúp liên kết dữ liệu giữa các ứng dụng chuyên biệt mà không ép buộc dùng chung schema."
tags: ["Architecture", "System Design", "Shared Context", "Open Source", "Platform"]
categories: ["Projects", "System Architecture"]
---

> [!TLDR]
> Nối Nốt là nền tảng cho phép nhiều ứng dụng và công cụ phục vụ các khía cạnh khác nhau của đời sống cùng vận hành trên một context chung. Thay vì cố gắng gom tất cả tính năng vào một siêu ứng dụng cồng kềnh hay ép buộc mọi miền dữ liệu dùng chung một schema cứng nhắc, Nối Nốt duy trì mạng lưới liên kết thực thể, sự kiện và hành động ở tầng nền tảng.
>
> **Vai trò:** Định hình kiến trúc tổng thể, xây dựng tài liệu đặc tả sản phẩm, thiết kế mô hình dữ liệu tầng context chung và phát triển các thành phần cốt lõi của nền tảng.

## Bối cảnh và bài toán thực tế

Trong đời sống số hàng ngày, dữ liệu của một cá nhân thường bị phân mảnh nghiêm trọng trên hàng chục ứng dụng độc lập:

- **Contacts:** lưu thông tin liên lạc của một người.
- **Calendar:** ghi nhận cuộc hẹn gặp người đó.
- **Tasks:** chứa việc cần làm phát sinh từ cuộc hẹn.
- **Finance:** ghi nhận khoản chi tiêu cho buổi gặp mặt.
- **Documents:** lưu trữ ghi chú hoặc tài liệu bàn thảo liên quan.

Mỗi ứng dụng chuyên biệt thường giải quyết rất xuất sắc bài toán nghiệp vụ trong phạm vi hẹp của nó. Tuy nhiên, vấn đề phát sinh khi một sự kiện thực tế trong cuộc sống luôn giao thoa qua nhiều miền thông tin khác nhau. Một sự kiện có thể liên quan đồng thời tới con người, tổ chức, địa điểm, tài liệu, công việc, lịch trình và giao dịch tài chính.

Hiện nay, các ứng dụng gần như chỉ biết phần dữ liệu thuộc quyền sở hữu nội bộ. Người dùng buộc phải dùng trí nhớ cá nhân để tự chắp nối các mảnh ghép rời rạc này.

---

## Triết lý thiết kế cốt lõi

Nối Nốt tiếp cận bài toán kết nối dữ liệu với các nguyên tắc kiến trúc rõ ràng:

1. **Tôn trọng tính chuyên biệt của từng ứng dụng:** Mỗi ứng dụng có thể sở hữu giao diện, cấu trúc dữ liệu và workflow tối ưu riêng cho domain của nó. Một ứng dụng tài chính cần bảng kê giao dịch chuyên sâu, trong khi ứng dụng ghi chú cần trải nghiệm soạn thảo mượt mà.
2. **Không áp đặt schema đồng nhất:** Nối Nốt không đòi hỏi mọi ứng dụng phải dùng chung một cơ sở dữ liệu hay một schema nguyên khối.
3. **Liên kết ở tầng nền tảng:** Điểm hội tụ nằm ở phía dưới. Những đối tượng, sự kiện và hành động có liên quan được duy trì liên kết trong một lớp context chung thay vì trở thành những ốc đảo dữ liệu cô lập.

---

## Kiến trúc 3 tầng của Nối Nốt

Mô hình sản phẩm của Nối Nốt được cấu trúc thành ba tầng logic mạch lạc:

{{< diagram src="/diagrams/noi-not-shared-context-platform-1.svg" dark="/diagrams/noi-not-shared-context-platform-1-dark.svg" alt="Sơ đồ kiến trúc 3 tầng của nền tảng Nối Nốt" caption="Kiến trúc 3 tầng và lớp Shared Context của Nối Nốt" >}}

### 1. Core Apps (Ứng dụng nền tảng)
Các chức năng có ý nghĩa xuyên suốt mọi miền nghiệp vụ và tồn tại trực tiếp ở cấp độ platform:
- **Inbox:** Điểm tiếp nhận và lưu trữ nhanh thông tin thô khi chưa kịp phân loại hay gắn context.
- **Today:** Góc nhìn tập trung vào những đầu việc, lịch trình và sự kiện cần sự chú ý trong ngày hiện tại từ mọi ứng dụng.
- **Tasks:** Quản lý các hành động cần thực thi, giữ trọn vẹn context về nguồn gốc phát sinh task.
- **Calendar:** Trục thời gian hợp nhất hiển thị mọi sự kiện, hạn chót hoặc lịch hẹn từ các domain.
- **Search:** Công cụ tìm kiếm ngữ nghĩa xuyên qua toàn bộ dữ liệu người dùng được cấp quyền truy cập.
- **Activity:** Nhật ký kiểm toán ghi nhận những thay đổi và sự kiện diễn ra theo dòng thời gian.

### 2. Domain Apps và Tools (Ứng dụng nghiệp vụ và Công cụ)
Các ứng dụng chuyên môn hóa phục vụ từng khía cạnh đời sống như Contacts, Finance, Health, Projects, Home, Travel. Mỗi domain tự do tối ưu hóa mô hình dữ liệu nội bộ và chỉ tham gia vào context chung khi có nhu cầu kết nối:
- **Contacts:** Quản lý người và tổ chức. Một đối tượng Person trong Contacts có thể liên kết trực tiếp tới Project, Meeting hay Document mà các ứng dụng khác không cần sao chép dữ liệu người dùng.
- **Finance:** Quản lý tài khoản, ngân sách và giao dịch. Một Transaction vẫn duy trì mối liên hệ tự nhiên tới chuyến đi trong Travel hoặc một khoản chi của Project.
- **Health:** Quản lý hồ sơ sức khỏe và lịch khám. Một Appointment đồng thời giữ liên kết tới bác sĩ phụ trách, địa điểm phòng khám và sự kiện trên Calendar.

### 3. Shared Context Layer (Lớp ngữ cảnh chung)
Trọng tâm kỹ thuật của Nối Nốt nằm ở các primitives nền tảng:
- **Entities:** Định danh các thực thể độc lập trong thế giới thực như cá nhân, địa điểm, tổ chức hoặc dự án.
- **Relationships:** Thiết lập các cạnh nối có ngữ nghĩa giữa các thực thể, chẳng hạn như sở hữu, tham gia, phụ thuộc hoặc phát sinh từ.
- **Events:** Ghi nhận các mốc thời gian hoặc sự việc đã và đang xảy ra.
- **Actions:** Các hành động có chủ đích nhằm thay đổi trạng thái của thực thể hoặc hệ thống.
- **Time:** Hệ quy chiếu thời gian chuẩn hóa để đồng bộ lịch trình và thời hạn.
- **Resources:** Các tệp tin đính kèm, hình ảnh, tài liệu số gắn liền với thực thể.

---

## Trạng thái phát triển và Mã nguồn

Dự án hiện đang trong giai đoạn hoàn thiện tài liệu đặc tả kiến trúc, thiết kế hệ thống nhận diện thương hiệu và xây dựng nguyên mẫu cho lớp Shared Context Layer. Toàn bộ mã nguồn, thông số chuyển động và tài liệu thiết kế được phát triển công khai:

- **Kho lưu trữ GitHub:** [github.com/ngoctinn/noinot](https://github.com/ngoctinn/noinot)
- **Định dạng triển khai:** Nền tảng mã nguồn mở với định hướng hỗ trợ local-first và bảo vệ quyền riêng tư dữ liệu người dùng.
