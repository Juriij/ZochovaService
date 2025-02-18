from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class AddRequest(FlaskForm):
    title = StringField('Title name', validators=[DataRequired()])
    description = TextAreaField('Request description', validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    priority = StringField('Priority (0/1/2)', validators=[DataRequired()])
    submit = SubmitField('Submit request')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('teacher', 'Teacher'), ('janitor', 'Janitor')], validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')