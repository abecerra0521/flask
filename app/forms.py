from flask import Flask
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm


class loginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = EmailField('Correo electronico', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


class contactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired("Campo requerido")])
    email = EmailField('Correo electronico', validators=[
                       DataRequired("Campo requerido")])
    message = TextAreaField('Asunto')
    # password = PasswordField('Contrase&ntilde;a', validators=[DataRequired()])
    submit = SubmitField()
