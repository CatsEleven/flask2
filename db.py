# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from datetime import datetime
# import pytz

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # データベースURIを適切に設定してください
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50), nullable=False)
#     body = db.Column(db.String(300), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_post'), nullable=False)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), unique=True)
#     password = db.Column(db.String(12))
#     posts = db.relationship('Post', backref='author', lazy=True)

    
# def init_app(app):
#     db.init_app(app)
#     Migrate(app, db)

# 第二版
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from datetime import datetime
# import pytz
# from flask_login import UserMixin

# db = SQLAlchemy()

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50), nullable=False)
#     body = db.Column(db.String(300), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_post'), nullable=False)

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), unique=True)
#     password = db.Column(db.String(12))
#     posts = db.relationship('Post', backref='author', lazy=True)
#     icon = db.Column(db.String(120), default='default.png')  # アイコンフィールドを追加

# def init_app(app):
#     db.init_app(app)
#     Migrate(app, db)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from datetime import datetime
import pytz

db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    init_app(app)

    return app

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_post'), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))
    icon = db.Column(db.String(120), default='default.png')  # アイコンフィールドを追加
    posts = db.relationship('Post', backref='author', lazy=True)
