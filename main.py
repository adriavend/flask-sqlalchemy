#!/usr/bin/env python
# -*- coding: utf-8 -*-
from asyncio import constants
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session
from flask import flash # 18 - sirve para mensajes

from flask import redirect
from flask import url_for
import json

from flask_wtf import CSRFProtect

from flask import g #para usar variables globales.

from config import DevelopmentConfig

from model import db
from model import User
from model import Comment

from helpers import date_format

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

import formulario

@app.errorhandler(404)
def page_error(e):
    return render_template('404.html'), 404

#sirve para validar todas las acciones que necesitemos, entre ellas validaciones 
    #contadores de visitas, endpoint, permisos (url)
    # ejemplo
    # if 'username' not in session and request.endpoint not in ['index']:
    #     return redirect(url_for('index'))
@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['comment', 'reviews']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login', 'create']:
        return redirect(url_for('index'))

#sirve para poner ciertas acciones despues. como por ej cerrar conexion base datos.
@app.after_request
def after_request(response):
    return response

@app.route('/')
def index():
    # 16 - ectura de cookie
    custom_cookie = request.cookies.get('nombre_cookie', 'valor por defecto cookie')
    print(custom_cookie)

    # 17 - lectura de session
    if 'username' in session:
        print(session['username'])

    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST']) #hacemos que el metodo sea GET y POST
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
            return redirect(url_for('index'))
        else:
            error_message = "Usuario o password invalidos"
            flash(error_message)
                
        session['username'] = username

    title = 'Login'
    return render_template('login.html', title=title, form=login_form)

@app.route('/login-ajax', methods=['POST'])
def ajax_login():
    print(request.form)
    username = request.form['username']
    response = { 'status': '200', 'username': username, 'id': 1 }
    return json.dumps(response)

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    comment_form = formulario.CommentForm(request.form)

    if request.method == 'POST' and comment_form.validate():
        user_id = session['user_id']
        comment = Comment(user_id = user_id, text = comment_form.comment.data)

        db.session.add(comment)
        db.session.commit()

        success_message = "Nuevo comentario creado"
        flash(success_message)
        return redirect(url_for('comment')) # comment = name function

    title = "Comentarios"
    return render_template('comment.html', title=title, form=comment_form)

@app.route('/reviews/', methods=['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def reviews(page = 1):
    per_page = 3
    comments = Comment.query.join(User).add_columns(
        User.username, 
        Comment.text,
        Comment.create_date,
        Comment.id
        ).all()
        #.paginate(page,per_page,False) # page-> pagina inicial, per_page-> cant paginas
    # print(comments)

    return render_template('reviews.html', comments = comments, date_format = date_format)

@app.route('/review/<int:id>', methods=['DELETE'])
def review_delete_ajax(id):
    Comment.query.filter_by(id=id).delete()
    db.session.commit()
    return json.dumps({ 'ok': True, 'id': id})


@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    # 16 - creacion de cookie
    response.set_cookie('nombre_cookie', 'valor_cookie')
    return response

@app.route('/logout')
def logout():
    if 'username' in session:
        # 17 - destruccion session
        session.pop('username')
        session.pop('user_id')
        print('Se elimino exitosamente la cookie de session')

    return redirect(url_for('login')) # redirecciona a login, login = nombre de la funcion no de la url.

@app.route('/create', methods=['GET', 'POST'])
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
        return redirect(url_for('login'))
    
    return render_template('create.html', form = create_form)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app) #para que tome las configuraciones.

    with app.app_context():
        db.create_all(); #se encarga de crear todas las tablas que no esten creadas.

    app.run(port=5050)