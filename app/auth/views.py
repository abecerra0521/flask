from flask import render_template
from . import auth
from app.forms import loginForm, recoveryForm


@auth.route('/login')
def login():
    context = {
        'form': loginForm()
    }
    return render_template('login.html', **context)


@auth.route('/recovery')
def recovery():
    context = {
        'form': recoveryForm()
    }
    return render_template('recovery.html', **context)
