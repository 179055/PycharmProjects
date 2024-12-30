from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import cx_Oracle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪现消息的加密密钥

# 获取数据库连接
def get_db_connection():
    dsn = cx_Oracle.makedsn('localhost', 1521, service_name='XE')  # 数据库配置
    connection = cx_Oracle.connect(user='C##YUANWEIHUA', password='root', dsn=dsn)
    return connection


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
    cursor.execute('SELECT * FROM "user" WHERE "NAME" = :username', {'username': username})
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # 判断用户是否存在
    if not user:
        flash('用户不存在！')  # 用户名不存在
        return redirect(url_for('index'))

    # 如果密码正确，登录成功
    if user[0] == username and user[1] == password:  # user[0] 是用户名，user[1] 是密码
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
    cursor.execute('SELECT * FROM "user" WHERE "NAME" = :username', {'username': username})
    existing_user = cursor.fetchone()

    if existing_user:
        flash('用户名已存在，请选择其他用户名！')
        cursor.close()
        conn.close()
        return redirect(url_for('register'))  # 返回到注册页面

    # 插入新用户
    cursor.execute('INSERT INTO "user" ("NAME", "PASSWORD") VALUES (:username, :password)', {'username': username, 'password': password})
    conn.commit()

    cursor.close()
    conn.close()

    flash('注册成功！')  # 注册成功后显示提示
    return redirect(url_for('index'))  # 重定向到登录页面

# 登录成功后的首页
@app.route('/home')
def home():
    # 连接数据库
    conn = get_db_connection()
    cursor = conn.cursor()

    # 执行查询获取 10 条随机记录
    cursor.execute('SELECT * FROM (SELECT * FROM C##YUANWEIHUA.数量统计 ORDER BY DBMS_RANDOM.VALUE) WHERE ROWNUM <= 15')
    rows = cursor.fetchall()  # 获取所有的 10 条记录

    cursor.close()
    conn.close()

    # 提取数据
    ids = [row[0] for row in rows if row[0] is not None]
    region_names = [row[1] for row in rows if row[1] is not None]
    counts = [row[2] for row in rows if row[2] is not None]
    detection_times = [row[3] for row in rows if row[3] is not None]

    return render_template('home.html', ids=ids, region_names=region_names, counts=counts, detection_times=detection_times)

if __name__ == '__main__':
    app.run(debug=True)
