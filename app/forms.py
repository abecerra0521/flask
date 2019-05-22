from flask import Flask
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm


class loginForm(FlaskForm):
    username = EmailField('Correo electronico', validators=[DataRequired()])
    password = PasswordField('Contrase&ntilde;a', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


class recoveryForm(FlaskForm):
    email = EmailField('Correo electronico', validators=[
                       DataRequired("Campo requerido")])
    submit = SubmitField('Recuperar contrasena')


class contactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired("Campo requerido")])
    email = EmailField('Correo electronico', validators=[
                       DataRequired("Campo requerido")])
    message = TextAreaField('Asunto')
    submit = SubmitField()


class taskForm(FlaskForm):
    description = StringField('Descripcion', validators=[
                              DataRequired('Campo reuerido')])
    submit = SubmitField('Guardar')


class deleteTask(FlaskForm):
    SubmitField = SubmitField('Eliminar')
