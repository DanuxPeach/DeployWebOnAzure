# Sử dụng image cơ sở Python
FROM python:3.9

# Set thư mục làm việc trong container
WORKDIR /app

# Copy tất cả các file vào container
COPY . .

# Cài đặt các thư viện cần thiết
RUN pip install Flask psycopg2 flask-bcrypt

# Expose cổng mặc định cho ứng dụng Flask
EXPOSE 5000

# Command để khởi chạy ứng dụng khi container được khởi động
CMD ["python", "app.py"]
