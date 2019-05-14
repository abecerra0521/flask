from flask import render_template, make_response, redirect, flash, session, url_for
from . import auth
from app.forms import loginForm, recoveryForm
from flask_login import login_user
from app.firestore_services import get_user_by_id
from app.models import UserModel, UserData


@auth.route('/')
def index():
    response = make_response(redirect('/auth/login'))
    return response


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = loginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user_by_id(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']
            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo', 'success')
                redirect(url_for('hello'))
            else:
                flash('Usuario y/o contrasena incorrectos')
        return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('/logout')
def logout(self):
    session.clean()
    return redirect(url_for('index'))


@auth.route('/recovery')
def recovery():
    context = {
        'form': recoveryForm()
    }
    return render_template('recovery.html', **context)
