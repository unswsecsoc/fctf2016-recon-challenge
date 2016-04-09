#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib, base64
import time
from flask import Flask, render_template_string, request, render_template, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_user import roles_required, current_user
from wtforms.validators import ValidationError

key = 'w0wM0R3M0kep0n'
flag1 = 'TBA' # cookie flag
flag2 = 'TBA' # secret URL flag
hostname = 'localhost:5000'

def hash(string):
    m = hashlib.sha512()
    m.update(key)
    m.update(string.encode('utf-8'))
    return m.hexdigest()

class ConfigClass(object):
    # Flask settings
    SECRET_KEY =              os.getenv('SECRET_KEY',       'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',     'sqlite:///basic_app.sqlite')
    SQLALCHEMY_ECHO             = True
    USER_ENABLE_EMAIL           = False
    USER_ENABLE_CONFIRM_EMAIL   = False
    USER_ENABLE_FORGOT_PASSWORD = False
    USER_ENABLE_LOGIN_WITHOUT_CONFIRM = True
    USER_AUTO_LOGIN                  = True
    USER_AUTO_LOGIN_AFTER_CONFIRM    = USER_AUTO_LOGIN
    USER_AUTO_LOGIN_AFTER_REGISTER   = USER_AUTO_LOGIN
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = USER_AUTO_LOGIN
    USER_PASSWORD_HASH_MODE = 'plaintext'

def create_app():
    # Setup Flask app and app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    # Initialize Flask extensions
    db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy

    # Define the Role data model
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

    def my_password_validator(form, field):
        password = field.data
        if len(password) < 1:
            raise ValidationError(_("no blank passwords dummy"))

    def init_pokemon():

        import products
        if (db.session.query(Product).count() == len(products.mokepon)):
            return

        for poke in products.mokepon:
            ball = Product(price = poke[0], name = poke[1], img = poke[2], desc = poke[3])
            db.session.add(ball)

        db.session.commit()

    def init_currency():
        import currency
        if (db.session.query(Currency).count() == len(currency.currsym)):
            return

        for curr in currency.currsym:
            dolla = Currency(abbrev = curr[0], sym = curr[1])
            db.session.add(dolla)
        db.session.commit()

    def init_donny():
        if not User.query.filter(User.username=='pokechampion').first():
            donny = User(username = 'pokechampion', password = user_manager.hash_password('dontyoulovelongpasswords'))
            donny.roles.append(Role(name='donnyspikachuhoodie'))
            db.session.add(donny)
            db.session.commit()

    def check_currency_cookie():
        result = {'new_currency': 'PKD-P-false', 'new_abbrev': 'PKD', 'new_sym': 'P'}
        if 'currency' in request.cookies:
            oreo = request.cookies['currency'].split('|')
            top_layer = base64.b64decode(oreo[1])
            if (oreo[0] != hash(top_layer.decode('utf-8'))[0:6]):
                raise
            else:
                cream = top_layer.split('-')
                result['new_currency'] = top_layer.decode('utf-8')
                result['new_abbrev'] = cream[0]
                result['new_sym'] = cream[1].decode('utf-8')
        return result
    # Create all database tables
    db.create_all()

    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model

    user_manager = UserManager(db_adapter, app,
                                password_validator=my_password_validator)

    init_pokemon()
    init_currency()
    init_donny()

    def load_currency():

        if 'currency' in request.cookies:
            try:
                reqcurr = check_currency_cookie()
            except:
                print '[-] failed to verify cookie, pls work', request.cookies['currency']
                new_currency = 'AUD-$-false'
                new_abbrev = 'AUD'
                new_sym = '$'
            else:
                print '[-] new cookie', reqcurr
                new_currency = reqcurr['new_currency']
                new_abbrev = reqcurr['new_abbrev']
                new_sym = reqcurr['new_sym']
        else:
                new_currency = 'AUD-$-false'
                new_abbrev = 'AUD'
                new_sym = '$'
        result = {'new_currency': new_currency,
                    'new_abbrev': new_abbrev,
                    'new_sym': new_sym}
        return result

    # user_manager.init_app(app)

    # # Create 'user007' user with 'secret' and 'agent' roles
    # if not User.query.filter(User.username=='user007').first():
    #     user1 = User(username='user007', email='user007@example.com', active=True,
    #             password=user_manager.hash_password('asdf'))
    #     user1.roles.append(Role(name='secret'))
    #     user1.roles.append(Role(name='agent'))
    #     db.session.add(user1)
    #     db.session.commit()
    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        currency = load_currency()
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Home page</h2>
                <p>This page can be accessed by anyone.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            {% endblock %}
            """,                        new_currency = currency['new_currency'],
                                        new_abbrev = currency['new_abbrev'],
                                        new_sym = currency['new_sym'])

    @app.route('/secretpassage')
    @roles_required('donnyspikachuhoodie')
    def flag2_page():
        currency = load_currency()
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Special Page</h2>
                <p>Congratulations you managed to XSS successfully and find the secret page.</p><br/>
                <p>{flag2}</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            {% endblock %}
            """ ,                       new_currency = currency['new_currency'],
                                        new_abbrev = currency['new_abbrev'],
                                        new_sym = currency['new_sym'])

    # The Members page is only accessible to authenticated users
    @app.route('/members')
    @login_required                                 # Use of @login_required decorator
    def members_page():
        currency = load_currency()
        return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p>This page can only be accessed by authenticated users.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
            {% endblock %}
            """,                        new_currency = currency['new_currency'],
                                        new_abbrev = currency['new_abbrev'],
                                        new_sym = currency['new_sym'])

    import forms

    @app.route('/deadlink', methods=['GET','POST'])
    @login_required
    def deadlink_page():
        form = forms.DeadlinkForm()

        if request.method == 'POST':
            print '[-] Im really trying i promsie'
            if not request.form['Link']:
                print '[-] i had a boo boo'
                flash('Please provide a link', 'error')
                return render_template('contact.html', form=form)

            elif form.validate_on_submit():
                thisdeadlink = Deadlink(user_id = current_user.get_id(),
                                    url = request.form['Link'],
                                    seen = 0,
                                    timestamp = time.ctime())
                db.session.add(thisdeadlink)
                db.session.commit()
                flash("deadlink {0} was successfully created".format(request.form['Link']))
                return render_template('contact.html', form=form, success=True)
            else:
                flash('please submit a url for this website')
                return render_template('contact.html', form=form, error=True)

        elif request.method == 'GET':
            return render_template('contact.html', form=form)

    @app.route('/livingdead')
    @roles_required('donnyspikachuhoodie')
    def livingdead_page():
        link_list = Deadlink.query.filter(Deadlink.seen == 0).all()
        # for link in link_list:
        #     link.seen = 1
        #     db.session.commit()
        print link_list
        return render_template("livingdead.html",link_list = link_list)

    @app.route('/wow')
    def wow_page():
        print '[-] wow visited'


    @app.route('/products')
    def products_page():
        products_list = Product.query.all()
        currency_list = Currency.query.all()
        if 'currency' in request.args:
            reqcurr = request.args['currency']
            resp = make_response(render_template("products.html",
                                    title="Products",
                                    products_list = products_list,
                                    currency_list = currency_list,
                                    new_currency = reqcurr,
                                    new_abbrev = reqcurr.split('-')[0],
                                    new_sym = reqcurr.split('-')[1]))
            resp.set_cookie('currency', value=hash(reqcurr)[0:6] +"|" + base64.b64encode(reqcurr.encode('utf-8')))
            return resp
        elif 'currency' in request.cookies:
            print "[-] HELLO IN CURRENCY COOKIES"
            try:
                reqcurr = check_currency_cookie()
                print reqcurr
            except:
                print "OHDEAR"
                return render_template("products.html", somethingwrong='YES',
                                        title="Products",
                                        products_list = products_list,
                                        currency_list = currency_list,
                                        new_currency = 'PKD-P-false',
                                        new_abbrev = 'PKD',
                                        new_sym = 'P')
            else:
                return render_template("products.html",
                                        title="Products",
                                        products_list = products_list,
                                        currency_list = currency_list,
                                        new_currency = reqcurr['new_currency'],
                                        new_abbrev = reqcurr['new_abbrev'],
                                        new_sym = reqcurr['new_sym'])
        else:
            return render_template("products.html",
                                    title="Products",
                                    products_list = products_list,
                                    currency_list = currency_list,
                                    new_currency = 'PKD-P-false',
                                    new_abbrev = 'PKD',
                                    new_sym = 'P')




    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
