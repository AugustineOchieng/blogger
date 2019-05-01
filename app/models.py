
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
#...


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blog = db.relationship('Blog', backref='username', lazy='dynamic')
    comments = db.relationship('Comments', backref='username', lazy='dynamic')
    pass_secure = db.Column(db.String(255))

#to link tables what you add after backreft matters
    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'Username: {self.username}'


class Blog(db.Model):
    __tablename__= 'blog'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    category = db.Column(db.String(255))
    blog = db.Column(db.String(255))
    date = db.Column(db.DateTime(250), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comments', backref='title', lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

   
    @classmethod
    def get_blogs(cls,category):
        blog = Blog.query.filter_by(category = category).all()
        return blog

    @classmethod
    def get_blog(cls,id):
        blog = Blog.query.filter_by(id = id).first()

        return blog
    def __repr__(self):
        return f"Blog {self.blog}','{self.date}')"

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime(250), default=datetime.utcnow)
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(cls,id):
        comments = Comments.query.filter_by(blog_id=id).all()
        return comments

    def __repr__(self):
        return f"Comments('{self.comment}', '{self.date_posted}')"
class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(), unique = True)