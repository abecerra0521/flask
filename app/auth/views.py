from flask import render_template
from . import auth
from app.forms import loginForm


@auth.route('/login')
def login():
    context = {
        'form': loginForm()
    }
    return render_template('login.html', **context)
