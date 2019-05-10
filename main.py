from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

colors = ['azul', 'amarillo', 'verde', 'rojo']


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)
    return response


@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'listColors': colors
    }
    return render_template('hello.html', **context)
