# ĐỊNH TUYẾN KÍNH GỬI VÀ NƠI NHẬN

## Trạng thái

Ma trận AI trước đây chưa có dẫn chứng PDF/hồ sơ cho từng tuyến. Bảng dưới là hướng tìm bằng chứng, không phải danh bạ phòng ban hoặc kết luận quy trình hiện hành.

## Thứ tự xác định

1. Lấy người/cơ quan nhận được chỉ định trong yêu cầu hiện tại hoặc văn bản đến. Đơn vị ban hành văn bản đến có thể khác đơn vị được chỉ định nhận phúc đáp.
2. Tra QL văn bản/JSON để tìm tiền lệ cùng mục đích; kiểm tra lại tên đơn vị, `Kính gửi`, `Nơi nhận` trên PDF gốc.
3. Với tên đơn vị mới hoặc khác nhau giữa nguồn, giữ nguyên giá trị nguồn, ghi ngày và trạng thái; không tự coi TCCB/TCNS hoặc các tên phòng là đồng nghĩa.
4. Chỉ thêm đơn vị phối hợp khi có vai trò thực tế hoặc yêu cầu cụ thể. Không tự thêm Ban Chủ nhiệm, phòng chức năng, website và mọi nơi nhận trong mẫu cũ.
5. Tách người xử lý hồ sơ trong QL văn bản khỏi cơ quan nhận văn bản. Không suy ra hai trường là một chỉ từ tên cột.

## Hướng tra cứu theo công việc

| Nhu cầu | Bằng chứng cần tìm | Câu hỏi quyết định tuyến |
|---|---|---|
| Xin kinh phí/mua sắm | Tờ trình tương tự, văn bản hướng dẫn tiếp nhận | Ai phê duyệt, đơn vị nào nhận để tham mưu? |
| Sửa chữa cơ sở vật chất | Hồ sơ sửa chữa và dự toán cùng loại | Có cần đồng thời đầu mối thiết bị và tài chính? |
| Nhân sự/cử đi học | Văn bản yêu cầu, hồ sơ nhân sự tương tự | Phê duyệt ở cấp nào, nhận trực tiếp hay qua đầu mối? |
| Đào tạo | Hồ sơ cùng bậc học, chương trình | Đầu mối đại học/sau đại học nào được chỉ định? |
| Nghiên cứu/hợp tác | Văn bản chương trình/đề tài, phúc đáp trước | Đơn vị chuyên môn hay đối tác nhận trực tiếp? |
| Giới thiệu đến cơ sở | Yêu cầu tiếp nhận và PDF giấy giới thiệu | Tên pháp nhân, địa điểm và đầu mối tiếp nhận là gì? |
| Thông báo nội bộ | Danh sách đối tượng thực hiện được giao | Ai cần thực hiện, ai chỉ nhận để biết? |

## Kết quả định tuyến

Ghi `Kính gửi`, `Nơi nhận`, mục đích nhận, nguồn, ngày nguồn và trạng thái xác minh. Tên cơ quan và chức danh người đứng đầu không thay thế cho nhau tùy ý.

Dòng lưu hồ sơ giữ theo ký hiệu hiện được người dùng xác định hoặc mẫu đã kiểm chứng. Các ký hiệu lưu trong rules cũ chưa phải chuẩn đã xác nhận.
