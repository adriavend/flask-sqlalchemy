from wtforms import Form
from wtforms import StringField, HiddenField, PasswordField, StringField
# from wtforms.fields.html5 import EmailField
from wtforms.fields import EmailField
from model import User

from wtforms import validators

def validate_custom_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe estar vacio.')

class CommentForm(Form):
    comment = StringField('Comentario', 
                            [
                                validators.DataRequired(message='Ingrese un comment'),
                            ])
    honeypot = HiddenField('', [validate_custom_honeypot])

class CreateForm(Form):
    username = StringField('Username', 
                            [
                                validators.DataRequired(message='El usuario es requerido'),
                                validators.Length(min=4, max=25, message='Debe ingresar un nombre de usuario de entre 4 y 25 caracteres')
                            ])
    email = EmailField('Email', 
                            [
                                validators.DataRequired(message='Debe ingresar un email'),
                                # validators.Email()
                            ])
    password = PasswordField('Password', 
                            [
                                validators.DataRequired(message='Debe ingresar un password')
                            ])

    #esto es un metodo overrride de username -> validate_<nombre_campo> para hacer la validacion de override.
    def validate_username(self, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('El username ya se encuentra registrado.')

class LoginForm(Form):
    username = StringField('Username', 
                            [
                                validators.DataRequired(message='El usuario es requerido'),
                                validators.Length(min=5, max=255, message='Debe ingresar un nombre de usuario de entre 4 y 25 caracteres')
                            ])
    password = PasswordField('Password', [validators.DataRequired(message='Debe ingresar un password')])
