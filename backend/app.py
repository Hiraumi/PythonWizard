from flask import Flask, jsonify
from flask_cors import CORS

from backend.routes.auth_routes import auth_bp
from backend.models import db  # 导入数据库实例和用户模型
from backend.routes.user_routes import user_bp

app = Flask(__name__)
CORS(app)

# MySQL 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:nyndd13hdyydc@localhost/pythonwizard'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 创建数据库表（如果尚未创建）
with app.app_context():
    db.create_all()

# 注册路由蓝图
app.register_blueprint(auth_bp, url_prefix='/auth')  # 认证相关接口
app.register_blueprint(user_bp, url_prefix='/user')  # 用户管理相关接口

# 首页接口
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Python Wizard Backend! (with MySQL)'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)