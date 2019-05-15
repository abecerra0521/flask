from flask import request, make_response, redirect, render_template, session, url_for, flash
# from flask_bootstrap import Bootstrap
from app.forms import contactForm
import unittest
from flask_login import login_required, current_user
from app import create_app
from app.firestore_services import get_users, get_tasks
from requests import get, post

app = create_app()

#colors = ['azul', 'amarillo', 'verde', 'rojo']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    # response.set_cookie('user_ip', user_ip)
    return response


@app.route('/hello')
@login_required
def hello():
    # user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    username = current_user.id
    print(username)
    context = {
        'user_ip': user_ip,
        'tasks': get_tasks(user_id=username),
        'username': username
    }

    return render_template('hello.html', **context)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/apis')
@login_required
def apis():
    context = {
        'pokemons': get('https://pokeapi.co/api/v2/pokemon?offset=0&limit=150').json()
    }
    return render_template('apis.html', **context)


@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    contact_form = contactForm()
    contact_name = current_user.id

    context = {
        'form': contact_form,
        'name': contact_name
    }

    if contact_form.validate_on_submit():
        name = contact_form.name.data
        #session['name'] = name
        flash('Gracias, nos pondremos en contacto contigo ' +
              contact_name, 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', **context)


@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    return render_template('shared/error.html', error=error)
