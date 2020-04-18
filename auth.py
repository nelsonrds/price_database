import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, session
)
from werkzeug.security import check_password_hash, generate_password_hash

from .document import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = email.split('@')[0]
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        password = request.form['password']
        password2 = request.form['password2']

        error = None

        if not username:
            error = {
                'code': 'username',
                'message': 'Username is required.'
            }
        elif not password and not password2:
            error = {
                'code': 'password',
                'message': 'Password is required.'
            }
        elif password != password2:
            error = {
                'code': 'password',
                'message': "Passwords don't match."
            }
        #elif User.objects(username=username) is not None:
            #error = {
                #'code': 'username',
                #'message': 'User already exists.'
           # }
        if error is None:
            new_user = User(username=username,
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            password=generate_password_hash(password))
            new_user.save()
            return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        if "remember" in request.form:
            print("Sim")
        else:
            print("Não")

        error = None
        user = User.objects(username=username.split('@')[0]).first()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = str(user['id'])
            session["url"] = []
            return redirect(url_for('product.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/forgot-password')
def forgot_password():
    return render_template('auth/forgot_password.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user = User.objects(id=user_id)        
        g.user = user.first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def protected(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return '<p>not authorized</p>'

        return view(**kwargs)
    return wrapped_view
