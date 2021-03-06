from flask import request, make_response, redirect, render_template, session, url_for, flash
# from flask_bootstrap import Bootstrap
from app.forms import contactForm, taskForm, deleteTask
import unittest
from flask_login import login_required, current_user
from app import create_app
from app.firestore_services import get_users, get_tasks, post_task, delete_task, update_task
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


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    # user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    username = current_user.id

    task_form = taskForm()
    delete_task = deleteTask()

    context = {
        'user_ip': user_ip,
        'tasks': get_tasks(user_id=username),
        'username': username,
        'task_form': task_form,
        'delete_task': delete_task
    }

    if task_form.validate_on_submit():
        post_task(user_id=username, task=task_form.description.data)
        flash('Tarea creada exitosamente', 'success')
        return redirect(url_for('hello'))
    return render_template('hello.html', **context)


@app.route('/task/delete/<task_id>')
def delete(task_id):
    delete_task(current_user.id, task_id)
    return redirect(url_for('hello'))


@app.route('/task/update/<task_id>/<int:done>')
def update(task_id, done):
    print(done)
    print(task_id)
    update_task(current_user.id, task_id, done)
    return redirect(url_for('hello'))


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
