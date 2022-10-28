from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.db import db
import formulario
from models.user import User
import json

users_bp = Blueprint("users", __name__)

@users_bp.route('/login', methods = ['GET', 'POST']) #hacemos que el metodo sea GET y POST
def login():
    login_form = formulario.LoginForm(request.form)

    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username = username).first()

        if user is not None and user.verify_password(password):
            sucess_message = "Bienvenido {}".format(username)
            flash(sucess_message)
            # creacion de session
            session['username'] = username
            session['user_id'] = user.id
            print(session)
            return redirect(url_for('home.index'))
        else:
            error_message = "Usuario o password invalidos"
            flash(error_message)
                
        session['username'] = username

    title = 'Login'
    return render_template('login.html', title=title, form=login_form)


@users_bp.route('/login-ajax', methods=['POST'])
def ajax_login():
    print(request.form)
    username = request.form['username']
    response = { 'status': '200', 'username': username, 'id': 1 }
    return json.dumps(response)


@users_bp.route('/logout')
def logout():
    if 'username' in session:
        # 17 - destruccion session
        session.pop('username')
        if session.get('user_id') is not None:
            session.pop('user_id')
        print('Se elimino exitosamente la cookie de session')

    return redirect(url_for('users.login')) # redirecciona a login, users = blueprint, login = nombre de la funcion no de la url.


@users_bp.route('/create', methods=['GET', 'POST'])
def create():
    create_form = formulario.CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():

        user = User(create_form.username.data,
                    create_form.email.data,
                    create_form.password.data,
                    )

        db.session.add(user)
        db.session.commit()

        success_message = 'Usuario registrado en la base de datos'
        flash(success_message)
        return redirect(url_for('users.login'))
    
    return render_template('create.html', form = create_form)