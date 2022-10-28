import datetime
from db.db import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(256))
    comments = db.relationship('Comment')
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email,
        self.password = self.__create_password(password)

    def __create_password(self, password):
        return generate_password_hash(password, method='pbkdf2:sha1') #por defecto = 256

    def verify_password(self, password):
        b = check_password_hash(self.password, password)
        return b