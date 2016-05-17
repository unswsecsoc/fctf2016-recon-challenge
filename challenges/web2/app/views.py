import os
import time
from flask import render_template_string
from flask import request
from flask import render_template
from flask import make_response
from flask import flash
from flask_user import login_required
from flask_user import roles_required
from flask_user import forms
from app.main import user_manager
from wtforms.validators import ValidationError
from app import myforms
from app import app
from app import custom
from app import db
from app.models import User
from app.main import flag1
from app.main import flag2
from app.main import flag3

@app.route('/')
def home_page():
    currency = custom.load_currency()
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>Grand Opening of the PokeStore</h2>
            <p>Welcome to the PokeStore</p>
            {% if call_or_get(current_user.is_authenticated) %}
                Congratulations. Isn't that a dodgy CSRF {{flag1}}
            {% endif %}
        {% endblock %}
        """,          new_currency = currency['new_currency'],
                                    new_abbrev = currency['new_abbrev'],
                                    new_sym = currency['new_sym'],
                                    flag1 = flag1)

@app.route('/secretpassage')
@roles_required('donnyspikachuhoodie')
def flag2_page():
    currency = custom.load_currency()
    resp = make_response(render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>Special Page</h2>
            <p>Congratulations you managed to XSS successfully and find the secret page.</p><br/>
            <p>{{flag3}}</p><br/>
            <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
            <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
        {% endblock %}
        """,                       new_currency = currency['new_currency'],
                                    new_abbrev = currency['new_abbrev'],
                                    new_sym = currency['new_sym'],
                                    flag3 = flag3))
    resp.set_cookie("totally_not_the_second_flag", flag2)
    return resp

# The Members page is only accessible to authenticated users
@app.route('/create_user')
@login_required
def user_create():
    currency = custom.load_currency()
    if 'username' not in request.args:
        flash('Please include a username');
        return render_template('flask_user/register.html', form=user_manager.register_form(), error=True)
    if 'password' not in request.args:
        flash('Please include a username');
        return render_template('flask_user/register.html', form=user_manager.register_form(), error=True)

    #process the user add because we're secure like that
    if not User.query.filter(User.username == request.args.get('username')).first():
        newuser = User(username = request.args.get('username'), password = user_manager.hash_password(request.args.get('password')))
        db.session.add(newuser)
        db.session.commit()
    flash('New User created')
    return render_template('flask_user/register.html', form=user_manager.register_form(), error=False)

@app.route('/members')
@login_required                                 # Use of @login_required decorator
def members_page():
    currency = custom.load_currency()
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


@app.route('/deadlink', methods=['GET','POST'])
@login_required
def deadlink_page():
    form = myforms.DeadlinkForm()

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
    link_list = Deadlink.query.filter(Deadlink.seen == 0).limit(1).all()
    # for link in link_list:
    #     link.seen = 1
    #     db.session.commit()
    print link_list
    return render_template("livingdead.html",link_list = link_list)

@app.route('/wow')
def wow_page():
    print '[-] wow visited'
    return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <p>wow</p>
        {% endblock %}
        """,                        new_currency = currency['new_currency'],
                                    new_abbrev = currency['new_abbrev'],
                                    new_sym = currency['new_sym'])


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

