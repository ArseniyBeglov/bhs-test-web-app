from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('userName')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.hased_password, password):
                flash(f'This is your token: h', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('username does not exist.', category='error')

    return render_template("login.html", user= current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == "POST":
        username = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(username)
        user = User.query.filter_by(username=username).first()
        print(user)
        if user:
            flash('Email already exists.', category='error')
        elif len(username) < 2:
            flash('user name should be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('password one and two not equal', category='error')
        elif len(password1) < 7:
            flash('password should be more than 7 chars', category='error')
        else:
            newUser = User(username=username, hased_password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(newUser)
            db.session.commit()

            flash('account created', category='sucsess')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
