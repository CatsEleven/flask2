from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # データベースURIを適切に設定してください
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def get_column_names(table_name):
    inspector = inspect(db.engine)
    columns = inspector.get_columns(table_name)
    column_names = [column['name'] for column in columns]
    return column_names

if __name__ == "__main__":
    with app.app_context():
        # 例として 'post' と 'user' テーブルのカラム名を取得
        post_columns = get_column_names('post')
        user_columns = get_column_names('user')

        print("Post table columns:", post_columns)
        print("User table columns:", user_columns)
