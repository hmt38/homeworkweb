from flask import Flask, send_from_directory, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
import uuid
import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "static/img"
db = SQLAlchemy(app)
app.config.update(dict(
    MAIL_SERVER="smtp.qq.com",
    MAIL_PORT='587',
    MAIL_USE_TLS=True,
    # MAIL_USE_SSL
    MAIL_USERNAME="2028148042@qq.com",
    MAIL_PASSWORD="kwsthhnkzjnudbbe",  # 生成授权码，授权码是开启smtp服务后给出的
    MAIL_DEFAULT_SENDER="2028148042@qq.com"
))
# 配置秘密密钥，用于 JWT 编码和解码
app.config['JWT_SECRET_KEY'] = 'jjjIsASB'  # 请替换为安全的密钥
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    job = db.Column(db.String(120))
    sign = db.Column(db.String(120))
    headImg = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.username


class VerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, code, email, expiration_time):
        self.code = code
        self.email = email
        self.expiration_time = expiration_time

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(120), db.ForeignKey('user.phone'), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))  # 图片文件路径
    video_path = db.Column(db.String(255))  # 视频文件路径


with app.app_context():
    db.create_all()

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_video(filename):
    ALLOWED_EXTENSIONS = {'mp4'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/static/register')
def static_register():
    return send_from_directory("static", "register.html")


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    job = data.get('job')
    password = data.get('password')
    code = data.get('code')
    # headImg = data.get('headImg')

    # 简单的验证
    if not all([username, email, phone]):
        return jsonify({"error": "Missing fields"}), 400

    # 检查电子邮件是否已存在
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # 检查电子邮件是否已存在
    if User.query.filter_by(phone=phone).first():
        return jsonify({"error": "Phone already exists"}), 400

    # 检查验证码是否正确
    verification_code = VerificationCode.query.filter_by(email=email).first()
    if not verification_code or verification_code.code != code or verification_code.expiration_time < datetime.datetime.now():
        return jsonify({'error': 'Invalid or expired verification code'}), 400

    new_user = User(username=username, email=email, phone=phone, job=job, password=password,
                    sign="这个人很懒，签名栏什么都没有留下", headImg="img/jjjhead.jpg")
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 200


@app.route('/static/login')
def static_login():
    return send_from_directory("static", "login.html")


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')

    # 查找用户
    user = User.query.filter_by(phone=phone).first()

    # 验证用户和密码
    if user and user.password == password:
        access_token = create_access_token(identity=phone)
        print(access_token)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route('/static/list')
def static_list():
    return send_from_directory("static", "list.html")


mail = Mail(app)


@app.route("/captcha/email", methods=['GET', 'POST'])
def get_email_captcha():
    message = Message(subject="theme", recipients=["2028148042@qq.com"], body="content")
    mail.send(message)
    return "success"


@app.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "请输入邮箱"}), 401
    '''
    生成随机验证码，保存到memcache中，然后发送验证码，与用户提交的验证码对比
    '''
    captcha = str(uuid.uuid1())[:6]  # 随机生成6位验证码
    # 给用户提交的邮箱发送邮件
    message = Message('your verify code about WebHomework: ', recipients=[email],
                      body='your verify code is : %s' % captcha)
    try:
        mail.send(message)  # 发送
    except:
        return jsonify({"error": "send error"}), 401

    # 存储验证码
    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=5)  # 假设验证码5分钟后过期
    verification_code = VerificationCode(code=captcha, email=email, expiration_time=expiration_time)
    try:
        db.session.add(verification_code)
        db.session.commit()
    except:
        return jsonify({"error": "邮箱已经注册，不再发送验证码验证"}), 401

    return jsonify({"message": "Send succuss"}), 200

@app.route("/userinfo")
@jwt_required()
def userinfo():
    current_user = get_jwt_identity()
    # 获取当前用户
    user = User.query.filter_by(phone=current_user).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user:
        # 将用户信息转换为字典
        user_data = {
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "job": user.job,
            "sign": user.sign,
            "headImg": user.headImg
        }
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/userInfoEditor', methods=['POST'])
@jwt_required()
def user_info_editor():
    current_user = get_jwt_identity()

    # 获取当前用户
    user = User.query.filter_by(phone=current_user).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # 处理图片上传
    if 'headImg' in request.files:
        file = request.files['headImg']
        if file and allowed_file(file.filename):  # 需要定义 allowed_file 函数
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)


    # 处理其他表单数据
    user.username = request.form.get('username', user.username)
    user.job = request.form.get('job', user.job)
    user.sign = request.form.get('sign', user.sign)
    user.headImg = "img/" +filename

    # 更新数据库
    db.session.commit()

    return jsonify({"message": "User information updated successfully"})

@app.route('/question_edit', methods=['POST'])
@jwt_required()
def question_edit():
    current_user = get_jwt_identity()
    # 获取当前用户

    user = User.query.filter_by(phone=current_user).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # 获取表单数据
    title = request.form.get('title')
    content = request.form.get('content')


    # 验证数据（例如，检查标题和内容是否存在）
    if not title or not content:
        return jsonify({'error': 'Title and content are required.'}), 400

    # 创建新帖子或更新现有帖子
    # 假设使用 phone 来查找已存在的帖子

    # 处理图片上传
    if 'image_s' in request.files:
        file = request.files['image_s']
        if file and allowed_file(file.filename):  # 需要定义 allowed_file 函数
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_path = "img/" + filename

    # 处理视频上传
    if 'video_s' in request.files:
        file = request.files['video_s']
        if file and allowed_video(file.filename):  # 需要定义 allowed_file 函数
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            video_path = "img/" + filename

    phone = user.phone

    post = Post(phone=phone, title=title, content=content, image_path=image_path, video_path=video_path)
    db.session.add(post)

    # 保存到数据库
    db.session.commit()

    return jsonify({'message': 'Post saved successfully'}), 200

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    post_list = []
    for post in posts:
        post_list.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "image_path": post.image_path,
            "video_path": post.video_path
        })
        print(post_list)
    return jsonify(post_list)


@app.route('/postedQuestion_edit', methods=['POST'])
@jwt_required()
def edit_post():
    try:
        current_user_phone = get_jwt_identity()
    except e:
        return jsonify({"error": e}), 500
    if not current_user_phone:
        return jsonify({"error": "User not found"}), 404
    post_id = request.form.get('post_id')
    new_title = request.form.get('title')
    new_content = request.form.get('content')

    # 处理图片上传
    if 'image_s' in request.files:
        file = request.files['image_s']
        if file and allowed_file(file.filename):  # 需要定义 allowed_file 函数
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            new_image_path = "img/" + filename

    # 处理视频上传
    if 'video_s' in request.files:
        file = request.files['video_s']
        if file and allowed_video(file.filename):  # 需要定义 allowed_file 函数
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            new_video_path = "img/" + filename


    # new_image_path = request.form.get('image_path')
    # new_video_path = request.form.get('video_path')

    # 查找帖子并验证用户
    post = Post.query.filter_by(id=post_id, phone=current_user_phone).first()
    if not post:
        return jsonify({"error": "Post not found or unauthorized"}), 404

    # 更新帖子内容
    post.title = new_title if new_title else post.title
    post.content = new_content if new_content else post.content
    post.image_path = new_image_path if new_image_path else post.image_path
    post.video_path = new_video_path if new_video_path else post.video_path

    db.session.commit()

    return jsonify({"message": "Post updated successfully"}), 200





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="11405")
