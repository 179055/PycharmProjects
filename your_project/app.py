from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪现消息的加密密钥

# 获取数据库连接
def get_db_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='test',
        charset='utf8mb4'
    )

# 登录页面
@app.route('/')
def index():
    return render_template('login.html')

# 处理登录请求
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('name')
    password = request.form.get('password')

    # 连接数据库
    conn = get_db_connection()
    cursor = conn.cursor()

    # 查询数据库验证用户
    cursor.execute('SELECT * FROM users WHERE name = %s', (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # 判断用户是否存在
    if not user:
        flash('用户不存在！')  # 用户名不存在
        return redirect(url_for('index'))

    # 如果密码正确，登录成功
    if user[1] == password:  # user[1] 是数据库中的密码字段
        return redirect(url_for('home'))

    # 密码错误
    flash('密码错误！')
    return redirect(url_for('index'))

# 注册页面
@app.route('/register')
def register():
    return render_template('register.html')

# 处理注册请求
@app.route('/register', methods=['POST'])
def register_user():
    username = request.form.get('name')
    password = request.form.get('password')

    # 连接数据库
    conn = get_db_connection()
    cursor = conn.cursor()

    # 查询用户名是否已经存在
    cursor.execute('SELECT * FROM users WHERE name = %s', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        flash('用户名已存在，请选择其他用户名！')
        cursor.close()
        conn.close()
        return redirect(url_for('register'))

    # 插入新用户
    cursor.execute('INSERT INTO users (name, password) VALUES (%s, %s)', (username, password))
    conn.commit()

    cursor.close()
    conn.close()

    flash('注册成功！')  # 注册成功后显示提示
    return render_template('register.html', success=True)  # 显示注册成功的提示

# 登录成功后的首页
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
