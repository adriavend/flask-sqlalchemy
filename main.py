#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import CSRFProtect
from db.db import db
from app import app

csrf = CSRFProtect()

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app) # para que tome las configuraciones.

    with app.app_context():
        db.create_all(); # se encarga de crear todas las tablas que no esten creadas.

    app.run(port=5050)