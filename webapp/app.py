from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = b'\x90\xe6-\x85\xdd\nfLH~_\xbc\x0b\xae\xe4\x0b\x86%E\xc4\x8b%T\xb4'  # Thay thế bằng một secret key bảo mật

# Kết nối đến PostgreSQL
#ConnectionString="postgresql://postgresql:Dang0511!@postgresqlwebapp.postgres.database.azure.com:5432/user_database"
#conn = psycopg2.connect(user="postgresql", password="Dang0511!", host="postgresqlwebapp.postgres.database.azure.com", port=5432, database="user_database")
connectString = os.getenv("ConnectionString")
conn = psycopg2.connect(connectString)
cur = conn.cursor()

# Route cho trang đăng nhập
@app.route('/')
def login():
    return render_template('login.html')

# Route cho trang đăng ký
@app.route('/register')
def register():
    return render_template('register.html')

bcrypt = Bcrypt(app)

# Xử lý đăng ký với hash mật khẩu
@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password != confirm_password:
        return redirect('/register?error=Mật khẩu và nhập lại mật khẩu không khớp. Vui lòng thử lại.')
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            return redirect('/')
        except psycopg2.Error as e:
            conn.rollback()
            error_message = f"Lỗi khi đăng ký: {e}"
            return redirect(f'/register?error={error_message}')

# Xử lý đăng nhập
@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    
    if user and bcrypt.check_password_hash(user[2], password):
        session['username'] = username
        return redirect('/dashboard')
    else:
        return 'Đăng nhập không thành công'

# Route cho trang dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        cur.execute("SELECT username FROM users WHERE username != %s", (session['username'],))
        users = cur.fetchall()
        return render_template('dashboard.html', users=users)
    else:
        return redirect('/')

# Route cho việc đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
