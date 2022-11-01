import datetime
from flask import Flask, redirect, render_template, request, session, url_for, g # g: global variables
from config import DevelopmentConfig
from routes.home_routes import home_bp
from routes.user_routes import users_bp
from routes.comment_routes import comments_bp
from routes.review_routes import reviews_bp

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

app.register_blueprint(home_bp)
app.register_blueprint(users_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(reviews_bp)

@app.errorhandler(404)
def page_error(e):
    return render_template('404.html'), 404

# sirve para validar todas las acciones que necesitemos, entre ellas validaciones 
# contadores de visitas, endpoint, permisos (url)
@app.before_request
def before_request():
    if 'username' not in session and request.endpoint not in ['users.login', 'users.create', 'static']:
        return redirect(url_for('users.login'))
    elif 'username' in session and request.endpoint in ['users.login', 'users.create']:
        return redirect(url_for('home.index'))

# sirve para poner ciertas acciones despues. como por ej cerrar conexion base datos.
@app.after_request
def after_request(response):
    return response

# Context Processors can be used to inject values into templates before rendering it.
@app.context_processor
def inject_today_date():
    return { 'current_year': datetime.date.today().year }
