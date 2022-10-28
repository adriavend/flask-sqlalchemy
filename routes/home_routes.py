from flask import Blueprint, render_template, request, session, make_response

home_bp = Blueprint("home", __name__)

@home_bp.route('/')
def index():
    # Lectura de cookie
    custom_cookie = request.cookies.get('nombre_cookie', 'valor por defecto cookie')
    print(custom_cookie)

    # Lectura de session
    if 'username' in session:
        print(session['username'])

    return render_template('index.html')


@home_bp.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    # Creacion de cookie
    response.set_cookie('nombre_cookie', 'valor_cookie')
    return response
