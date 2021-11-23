from flaskweb import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    token = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String(20), nullable=False)
    title = db.Column(db.Text)
    text = db.Column(db.Text)

    def __init__(self, coin_name, text, title):
        self.coin_name = coin_name
        self.text = text
        self.title = title


class SummarizedArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String(20), nullable=False)
    summarized_text = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text)

    def __init__(self, coin_name, summarized_text, title):
        self.coin_name = coin_name
        self.summarized_text = summarized_text
        self.title = title
