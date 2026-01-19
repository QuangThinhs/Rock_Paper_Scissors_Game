```plaintext
Tính Năng Nổi Bật
🕹️ Real-time Multiplayer: Sử dụng socket và threading để xử lý kết nối nhiều người chơi cùng lúc với độ trễ thấp.

🔐 Hệ thống Tài khoản: Đăng ký, Đăng nhập an toàn với mật khẩu được mã hóa SHA-256.

🎨 Giao diện Hiện đại (Modern UI):

Dark Mode theme (chủ đề tối) bảo vệ mắt.

Các components (Nút, Input, Card) được tùy biến riêng (Custom Tkinter Widgets).

Hiệu ứng Hover và Animation mượt mà.

📊 Thống kê & Lưu trữ: Tự động lưu lịch sử đấu, số trận Thắng/Thua/Hòa vào MySQL.

🤝 Matchmaking: Hệ thống phòng chờ (Waiting Room) tự động ghép cặp người chơi.

🛠️ Công Nghệ Sử Dụng
Dự án được xây dựng dựa trên các thư viện và công nghệ cốt lõi:

Ngôn ngữ: Python 3.x

Giao diện (GUI): Tkinter (Standard Library)

Mạng (Networking): Python Socket (TCP/IP)

Cơ sở dữ liệu: MySQL (sử dụng mysql-connector-python)

Xử lý dữ liệu: JSON

📂 Cấu Trúc Dự Án
Bash

RPS-Online/
├── client.py           # Mã nguồn chính phía Client (Giao diện & Logic)
├── server.py           # Mã nguồn phía Server (Xử lý kết nối & Game logic)
├── database.py         # Class quản lý kết nối MySQL & Queries
├── network_handler.py  # Class xử lý gửi/nhận gói tin Socket
├── ui_components.py    # Thư viện UI tùy chỉnh (Modern Button, Entry, Cards)
├── game_logic.py       # Logic xác định thắng thua
├── config.py           # File cấu hình (IP, Port, DB info)
└── requirements.txt    # Danh sách thư viện cần cài đặt
🚀 Hướng Dẫn Cài Đặt
Làm theo các bước sau để chạy dự án trên máy cục bộ của bạn.

1. Yêu cầu tiên quyết
Python 3.8 trở lên.

MySQL Server đã được cài đặt và đang chạy.

2. Cài đặt thư viện
Mở terminal và chạy lệnh sau để cài đặt các thư viện cần thiết:

Bash

pip install mysql-connector-python
3. Cấu hình Database
Mở file server.py (hoặc config.py nếu bạn đã tách riêng) và cập nhật thông tin kết nối MySQL của bạn:

Python

# Cấu hình Database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',       # Tên đăng nhập MySQL của bạn
    'password': 'your_password', # Mật khẩu MySQL của bạn
    'database': 'rps_game'
}
Lưu ý: Hệ thống sẽ tự động tạo Database rps_game và các bảng cần thiết trong lần chạy đầu tiên.

4. Chạy Server
Mở một cửa sổ terminal và khởi động Server:

Bash

python server.py
Bạn sẽ thấy thông báo: [LISTENING] Server is listening on 0.0.0.0:5555

5. Chạy Client
Mở hai cửa sổ terminal khác (để giả lập 2 người chơi) và chạy lệnh:

Bash

python client.py
🎮 Cách Chơi
Đăng ký/Đăng nhập: Tạo tài khoản mới hoặc đăng nhập.

Tìm trận: Nhấn nút "TÌM TRẬN ĐẤU".

Chờ đối thủ: Hệ thống sẽ đưa bạn vào phòng chờ. Khi có người chơi thứ 2 tham gia, trận đấu sẽ bắt đầu.

Ra quyết định: Chọn Kéo, Búa hoặc Bao.

Kết quả: Hệ thống hiển thị kết quả Thắng/Thua và cập nhật thống kê ngay lập tức.

📝 Roadmap (Dự kiến phát triển)
[ ] Thêm tính năng Chat trong phòng chờ và trong trận.

[ ] Bảng xếp hạng (Leaderboard) toàn server.

[ ] Thêm hiệu ứng âm thanh (Sound Effects).

[ ] Đóng gói thành file .exe để dễ dàng phân phối.

🤝 Đóng Góp (Contributing)
Mọi đóng góp đều được hoan nghênh! Nếu bạn muốn cải thiện dự án này:

Fork dự án.

Tạo branch tính năng mới (git checkout -b feature/AmazingFeature).

Commit thay đổi của bạn (git commit -m 'Add some AmazingFeature').

Push lên branch (git push origin feature/AmazingFeature).

Tạo Pull Request.