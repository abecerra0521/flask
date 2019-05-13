from flask import request, make_response, redirect, render_template, session, url_for, flash
#from flask_bootstrap import Bootstrap
from app.forms import contactForm
import unittest
from app import create_app

app = create_app()

colors = ['azul', 'amarillo', 'verde', 'rojo']


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
def hello():
    # user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    context = {
        'user_ip': user_ip,
        'listColors': colors
    }
    return render_template('hello.html', **context)


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = contactForm()
    contact_name = session.get('name')

    context = {
        'form': contact_form,
        'name': contact_name
    }

    if contact_form.validate_on_submit():
        name = contact_form.name.data
        session['name'] = name
        flash('Recibimos tu mensaje', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', **context)


@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    return render_template('shared/error.html', error=error)
