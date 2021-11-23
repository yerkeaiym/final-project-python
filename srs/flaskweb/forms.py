from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskweb.models import User


class AuthorizationForm(FlaskForm):
    username = StringField('Name of users',
                           validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email of users', validators=[DataRequired(), Email()])
    password = PasswordField('Password of users', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def useful_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This account already exist!')

    def useful_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(' This email already exist!')


class LoginForm(FlaskForm):
    email = StringField('Email of users', validators=[DataRequired(), Email()])
    password = PasswordField('Password of users', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Remember Me!')
    submit = SubmitField('Login')


class CriptoCheakingForm(FlaskForm):
    coin_name = StringField('Crypto')
    check = SubmitField('Check')
