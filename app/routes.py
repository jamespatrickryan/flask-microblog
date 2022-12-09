from flask import flash, redirect, request, render_template, url_for

from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'James'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Doe'
        },
        {
            'author': {'username': 'Jane'},
            'body': 'Doe'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f'{form.username.data} {form.remember_me.data}')
        return redirect(url_for('index'))

    return render_template('login.html', title='Log In', form=form)
