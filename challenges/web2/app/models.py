from flask_user import UserManager
from flask_user import UserMixin
from flask_user import current_user
from app import db

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    roles = db.relationship(Role, secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))

    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        return True

# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    price = db.Column(db.String(50), nullable=False)
    name = db.Column(db.UnicodeText(100), index=True)
    img = db.Column(db.UnicodeText(100), index=True)
    desc = db.Column(db.UnicodeText(1000), index=True)

class Currency(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    abbrev = db.Column(db.String(5), index=True)
    sym = db.Column(db.UnicodeText(50), index=True)

class Deadlink(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    url = db.Column(db.UnicodeText(500), index=True)
    seen = db.Column(db.Integer(), index=True)
    timestamp = db.Column(db.String)

