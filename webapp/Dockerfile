# Sử dụng image cơ sở Python
FROM python:3.9

# Set thư mục làm việc trong container
WORKDIR /app

# Copy tất cả các file vào container
COPY . .

# Cài đặt các thư viện cần thiết
RUN pip install Flask psycopg2 flask-bcrypt python-dotenv

# Đặt biến môi trường
ENV ConnectionString="postgresql://username:password@host:port/database"

# Expose cổng mặc định cho ứng dụng Flask
EXPOSE 5000

# Command để khởi chạy ứng dụng khi container được khởi động
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
