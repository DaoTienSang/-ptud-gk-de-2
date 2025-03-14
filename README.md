# Ứng dụng Quản lý Công việc

## Thông tin cá nhân
- **Họ và tên:** Đào Tiến Sang
- **MSSV:** [22705971]

## Mô tả dự án
Đây là ứng dụng quản lý công việc được xây dựng bằng Flask, cho phép người dùng tạo, theo dõi và quản lý các công việc của mình. Ứng dụng bao gồm các chức năng chính sau:

1. **Quản lý công việc (Task)**: Tạo, chỉnh sửa, xóa và cập nhật trạng thái công việc
2. **Theo dõi thời gian**: Ghi lại thời gian tạo công việc và thời gian hoàn thành
3. **Phân loại công việc**: Phân loại công việc theo danh mục (category) để dễ dàng theo dõi
4. **Quản lý người dùng**: Hỗ trợ hai vai trò: admin và user thông thường
5. **Hình đại diện**: Cho phép người dùng tải lên hình đại diện của mình

## Công nghệ sử dụng
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **Icons**: Font Awesome

## Hướng dẫn cài đặt

### Yêu cầu hệ thống
- Python 3.6+
- Pip (Python package manager)

### Các bước cài đặt
### Cách 1: Cài đặt nhanh bằng install.bat
1. **Clone repository từ GitHub**
   ```bash
   git clone https://github.com/DaoTienSang/-ptud-gk-de-2.git
   ```
2.   **Sau đó:**
   ```# Chỉ cần chạy file install.bat
       .\install.bat
   ```
### Cách 2: Cài đặt bình thường
1. **Clone repository từ GitHub**
   ```bash
   git clone https://github.com/DaoTienSang/ptud-gk-de-2.git

   ```

2. **Tạo môi trường ảo (Virtual Environment)**
   ```bash
   python -m venv venv
   ```

3. **Kích hoạt môi trường ảo**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Cài đặt các thư viện cần thiết**
   ```bash
   pip install -r requirements.txt
   ```
   
   Nếu tệp requirements.txt không tồn tại, hãy cài đặt các thư viện sau:
   ```bash
   pip install flask flask-sqlalchemy werkzeug
   ```

5. **Chạy ứng dụng**
   ```bash
   python app.py
   ```

6. **Truy cập ứng dụng**
   Mở trình duyệt web và truy cập địa chỉ: http://127.0.0.1:5000

## Thông tin đăng nhập mặc định
Sau khi chạy ứng dụng lần đầu tiên, hệ thống sẽ tự động tạo tài khoản admin và tài khoản test:

1. **Tài khoản Admin**
   - Username: admin
   - Password: admin123

2. **Tài khoản Test**
   - Username: test
   - Password: test123

## Chức năng chính

### Người dùng thông thường (User)
- Đăng ký tài khoản mới
- Đăng nhập/Đăng xuất
- Tải lên hình đại diện
- Xem danh sách công việc của mình
- Tạo công việc mới
- Chỉnh sửa thông tin công việc
- Đánh dấu công việc đã hoàn thành
- Xóa công việc
- Lọc công việc theo danh mục và trạng thái

### Quản trị viên (Admin)
- Tất cả các chức năng của người dùng thông thường
- Xem danh sách tất cả công việc của mọi người dùng
- Tạo và quản lý danh mục công việc
- Quản lý người dùng (cấp/hủy quyền admin)

## Cấu trúc thư mục
```
- app.py             # Tệp chính của ứng dụng Flask
- static/            # Thư mục chứa tài nguyên tĩnh
  - uploads/         # Thư mục chứa hình đại diện người dùng
- templates/         # Thư mục chứa các template HTML
  - base.html        # Template cơ sở
  - index.html       # Trang chủ
  - login.html       # Trang đăng nhập
  - register.html    # Trang đăng ký
  - dashboard.html   # Trang chính của ứng dụng
  - profile.html     # Trang cá nhân
  - ...
- tasks.db           # Database SQLite
- README.md          # Tệp này
```

## Lưu ý
- Ứng dụng này được thiết kế với giao diện dạng Card-Based (Dạng Thẻ) theo yêu cầu của đề bài
- Dữ liệu mẫu đã được tự động tạo khi chạy ứng dụng lần đầu tiên
- Thư mục `/static/uploads/` cần được tạo trước khi chạy ứng dụng để lưu trữ hình đại diện người dùng