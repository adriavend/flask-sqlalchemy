#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import session

from flask import redirect
from flask import url_for

from flask_wtf import CSRFProtect

from flask import g #para usar variables globales.

from config import DevelopmentConfig

from db.db import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

from routes.home_routes import home_bp
from routes.user_routes import users_bp
from routes.comment_routes import comments_bp
from routes.review_routes import reviews_bp

app.register_blueprint(home_bp)
app.register_blueprint(users_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(reviews_bp)

csrf = CSRFProtect()

@app.errorhandler(404)
def page_error(e):
    return render_template('404.html'), 404

#sirve para validar todas las acciones que necesitemos, entre ellas validaciones 
    #contadores de visitas, endpoint, permisos (url)
@app.before_request
def before_request():
    print(request.endpoint)
    # if request.endpoint == 'static':
    #     return
    if 'username' not in session and request.endpoint not in ['users.login', 'users.create', 'static']:
        return redirect(url_for('users.login'))
    elif 'username' in session and request.endpoint in ['users.login', 'users.create']:
        return redirect(url_for('home.index'))

#sirve para poner ciertas acciones despues. como por ej cerrar conexion base datos.
@app.after_request
def after_request(response):
    return response

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app) #para que tome las configuraciones.

    with app.app_context():
        db.create_all(); #se encarga de crear todas las tablas que no esten creadas.

    app.run(port=5050)