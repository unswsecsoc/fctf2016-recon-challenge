from app import app
from app import db

from app.models import User
from app.models import Currency
from app.models import Product
from app.models import Role
from app.products import mokepon
from app.currency import currsym

from flask_user import SQLAlchemyAdapter
from flask_user import UserManager

def init_pokemon():
    if (db.session.query(Product).count() == len(mokepon)):
        return
    for poke in mokepon:
        ball = Product(price = poke[0], name = poke[1], img = poke[2], desc = poke[3])
        db.session.add(ball)
    db.session.commit()

def init_currency():
    if (db.session.query(Currency).count() == len(currsym)):
        return
    for curr in currsym:
        dolla = Currency(abbrev = curr[0], sym = curr[1])
        db.session.add(dolla)
    db.session.commit()

def init_donny():
    if not User.query.filter(User.username=='pokechampion').first():
        donny = User(username = 'pokechampion', password = user_manager.hash_password('dontyoulovelongpasswords'))
        donny.roles.append(Role(name='donnyspikachuhoodie'))
        db.session.add(donny)
        db.session.commit()

def load_flags():
    print '[+] Loading flags from files'
    global flag1
    with open('flag1.txt') as f:
        flag1 = f.read().strip()

    global flag2
    with open('flag2.txt') as f:
        flag2 = f.read().strip()

    global flag3
    with open('flag3.txt') as f:
        flag3 = f.read().strip()

def my_password_validator(form, field):
    password = field.data
    if len(password) < 1:
        raise ValidationError(_("no blank passwords dummy"))

def app_init():
# Setup Flask-User
    global db_adapter
    global user_manager
    db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
    user_manager = UserManager(db_adapter, app,
                                password_validator=my_password_validator)
    init_pokemon()
    init_currency()
    init_donny()
    load_flags()

