from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import psycopg2

app = Flask(__name__)
app.secret_key = b'\x90\xe6-\x85\xdd\nfLH~_\xbc\x0b\xae\xe4\x0b\x86%E\xc4\x8b%T\xb4'  # Thay thế bằng một secret key bảo mật

# Kết nối đến PostgreSQL
conn = psycopg2.connect(user="postgresql", password="Dang0511!", host="postgresqlwebapp.postgres.database.azure.com", port=5432, database="user_database")
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
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return redirect('/')
    except psycopg2.Error as e:
        conn.rollback()
        return f"Lỗi khi đăng ký: {e}"

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
    app.run(debug=True)
