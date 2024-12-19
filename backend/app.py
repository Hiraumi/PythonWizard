from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# MySQL 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:nyndd13hdyydc@localhost/pythonwizard'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义用户表模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Boolean, default=False)  # True 表示教师，False 表示学生

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Python Wizard Backend! (with MySQL)'})

# 注册接口
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # 从请求中获取 JSON 数据
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not username or not email or not password:
        return jsonify({'error': '部分栏位未选择'}), 400

    # 检查邮箱是否已经存在
    if User.query.filter_by(email=email).first():
        return jsonify({'error': '该邮件地址已经存在'}), 409

    # 将密码加密后存储
    hashed_password = generate_password_hash(password, method='sha256')

    # 创建新用户
    new_user = User(username=username, email=email, password=hashed_password, role=(role == "教师"))
    db.session.add(new_user)
    db.session.commit()
    print("Inserting user:", username, email, hashed_password)
    return jsonify({'message': '成功注册账户'}), 201

# 登录接口
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # 获取请求中的 JSON 数据
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': '请输入邮箱和密码'}), 400

    # 查询用户信息
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    # 验证密码是否匹配
    if not check_password_hash(user.password, password):
        return jsonify({'error': '密码错误'}), 401

    # 登录成功，打印日志
    print(f"用户 {user.username} 登录成功，角色为: {'教师' if user.role else '学生'}")

    # 登录成功
    return jsonify({'message': '登录成功',
                    'username': user.username,
                    'role': '教师' if user.role else '学生'}
                   ), 200

# 获取用户信息接口
@app.route('/users', methods=['GET'])
def get_users():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)

        # 查询用户信息，分页返回
        users_query = User.query.paginate(page=page, per_page=page_size, error_out=False)
        users = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password': user.password,
                'role': '教师' if user.role else '学生',
            }
            for user in users_query.items
        ]

        return jsonify({
            'total': users_query.total,
            'users': users
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 更新用户信息接口
@app.route('/update_user', methods=['PUT'])
def update_user():
    data = request.get_json()  # 从前端获取 JSON 数据
    print("Received data:", data)  # 打印接收到的数据

    current_username = data.get('current_username')  # 当前用户名
    new_username = data.get('new_username')  # 新用户名
    new_email = data.get('new_email')  # 新邮箱
    new_role = data.get('role')  # 新角色

    # 检查必要字段
    if not current_username:
        return jsonify({'error': '当前用户名不能为空'}), 400
    # if not new_username and not new_email and new_role is None:
    #     return jsonify({'error': '至少提供一个更新字段'}), 400

    # 校验角色是否合法
    if new_role not in ['教师', '学生']:  # 如果后端使用的是中文角色
        return jsonify({'error': '角色值不合法，仅支持 “教师” 和 “学生”'}), 400

    try:
        # 根据当前用户名查询用户
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404

        # 检查新用户名是否已存在
        if new_username:
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user:
                return jsonify({'error': '新用户名已被使用'}), 409
            user.username = new_username

        # 检查新邮箱是否已存在
        if new_email:
            existing_email = User.query.filter_by(email=new_email).first()
            if existing_email:
                return jsonify({'error': '新邮箱已被使用'}), 409
            user.email = new_email

        # 检查角色是否合法，并更新角色
        if new_role is not None:
            user.role = True if new_role == '教师' else False

        # 提交数据库更改
        db.session.commit()
        print(f"用户 {user.username} 信息更新成功，新角色为: {'教师' if user.role else '学生'}")
        return jsonify({'message': '用户信息更新成功'}), 200
    except Exception as e:
        db.session.rollback()
        print("Error while updating user:", str(e))
        return jsonify({'error': str(e)}), 500

# 删除用户接口
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'用户 {user.username} 已删除'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)

'''
启动前端
cd frontend
npm run serve

数据库后台
mysql -u root -p

demo账号
|邮箱|密码|角色|
|111@111.com|1111111111|学生|
|teacher@demo.com|err11221213131|教师|
'''
