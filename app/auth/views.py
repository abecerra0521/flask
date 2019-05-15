from flask import render_template, make_response, redirect, flash, url_for
from . import auth
from app.forms import loginForm, recoveryForm
from flask_login import login_user, login_required, logout_user, current_user
from app.firestore_services import get_user_by_id, insert_user
from app.models import UserModel, UserData
from werkzeug.security import generate_password_hash, check_password_hash


@auth.route('/')
def index():
    response = make_response(redirect('/auth/login'))
    return response


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = loginForm()
    context = {
        'form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user_by_id(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if check_password_hash(password_from_db, password):
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo', 'success')
                redirect(url_for('hello'))
            else:
                flash('Usuario y/o contrasena incorrectos', 'warning')
        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    sign_form = loginForm()
    context = {
        'form': sign_form
    }

    if sign_form.validate_on_submit():
        username = sign_form.username.data
        password = sign_form.password.data

        user_doc = get_user_by_id(username)

        if user_doc.to_dict() is None:
            pass_hash = generate_password_hash(password)
            user_data = UserData(username, pass_hash)
            insert_user(user_data)

            user = UserModel(user_data)
            login_user(user)

            flash('Usuario creado correctamente', 'success')
            return redirect(url_for('hello'))
        else:
            flash('El usuario ya existe', 'warning')

    return render_template('signup.html', **context)


@auth.route('/recovery')
def recovery():
    context = {
        'form': recoveryForm()
    }
    return render_template('recovery.html', **context)
