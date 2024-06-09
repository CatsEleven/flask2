# from flask import Flask
# from flask import render_template ,request, redirect
# from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# from flask_sqlalchemy import SQLAlchemy
# from db import db, User, Post

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # データベースURIを適切に設定してください
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = os.urandom(24)
# db = SQLAlchemy(app)

# loginManager = LoginManager()
# loginManager.init_app(app)
# loginManager.login_view = 'login'

# # ルーティング
# @loginManager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))



# @app.route("/", methods=['GET'])
# # @login_required
# def index():
#     if request.method == 'GET':
#         posts = Post.query.all()
#         return render_template('index.html', posts=posts)



# @app.route("/signup", methods=['GET', 'POST'])
# def signup():
#     if request.method =='POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
#         db.session.add(user)
#         db.session.commit()
#         return redirect('/login')
#     else:  
#         return render_template('signup.html')
    

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method =='POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         user = User.query.filter_by(username=username).first()
#         if check_password_hash(user.password, password):
#             login_user(user)
#             return redirect('/')
#     else:  
#         return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('/login')



# @app.route("/create", methods=['GET', 'POST'])
# @login_required
# def create():
#     if request.method =='POST':
#         title = request.form.get('title')
#         body = request.form.get('body')

#         post = Post(title=title, body=body)
#         db.session.add(post)
#         db.session.commit()
#         return redirect('/')
#     else:  
#         return render_template('create.html')
    

# @app.route("/<int:id>/update", methods=['GET', 'POST'])
# @login_required
# def update(id):
#     post = Post.query.get(id)
#     if request.method =='GET':
#         return render_template('update.html', post=post)
#     else:  
#         # インスタンス化したpostに上書きしてコミットする
#         post.title = request.form.get('title')
#         post.body = request.form.get('body')
#         db.session.commit()
#         return redirect('/')
    

# @app.route("/<int:id>/delete", methods=['GET'])
# @login_required
# def delete(id):
#     post = Post.query.get(id)

#     db.session.delete(post)
#     db.session.commit()
#     return redirect('/')

# # 実行
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
# from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from db import db, User, Post, init_app
from PIL import Image
import magic

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/icons/'  # アップロードフォルダの設定

# DB初期化
init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        post = Post(title=title, body=body, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')

@app.route("/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        db.session.commit()
        return redirect('/')

@app.route("/<int:id>/delete", methods=['GET'])
@login_required
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')


@app.route("/posts/<int:post_id>", methods=['GET'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


@app.route("/users/<int:user_id>", methods=['GET'])
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('user_detail.html', user=user, posts=posts)


@app.route("/users", methods=['GET'])
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)


# MINEを使ってファイルの種類を判定
# ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg'}
# def allowed_file_type(file_path):
#     # mine = magic.Magic(mine=True)
#     # file_mine = mine.from_file(file_path)
#     result = magic.from_file(file_path, mime=True)
#     return result in ALLOWED_MIME_TYPES


# @app.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
# @login_required
# def edit_user(user_id):
#     user = User.query.get_or_404(user_id)
#     if request.method == 'POST':
#         new_username = request.form.get('username')
#         if new_username:
#             user.username = new_username
#         if 'icon' in request.files:
#             icon = request.files['icon']
#             filename = secure_filename(icon.filename)
#             icon_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             icon.save(icon_path)
#             if icon.filename != '' and allowed_file_type(icon_path):
#                 icon.save(icon_path)
                
#                 img = Image.open(icon_path)
#                 img = img.resize((60, 60))
#                 img.save(icon_path)
#                 user.icon = filename
#             else:
#                 os.remove(icon_path)
#                 return render_template('user_edit.html', user=user, error="不正なファイルが含まれています。")

#         db.session.commit()
#         return redirect(f'/users/{user.id}')
#     return render_template('user_edit.html', user=user)
ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg'}
def allowed_file_type(file_path):
    result = magic.from_file(file_path, mime=True)
    return result in ALLOWED_MIME_TYPES

@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        new_username = request.form.get('username')
        if new_username:
            user.username = new_username
        
        if 'icon' in request.files:
            icon = request.files['icon']
            filename = secure_filename(icon.filename)
            icon_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # 一時的にファイルを保存
            icon.save(icon_path)
            
            # ファイルタイプの確認
            if allowed_file_type(icon_path):
                # 画像の処理
                img = Image.open(icon_path)
                img = img.resize((60, 60))
                img.save(icon_path)
                user.icon = filename
            else:
                os.remove(icon_path)  # 許可されていないファイルの場合ファイルを削除
                return render_template('user_edit.html', user=user, error="不正なファイルが含まれています。")
        
        db.session.commit()
        return redirect(f'/users/{user.id}')
    return render_template('user_edit.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
