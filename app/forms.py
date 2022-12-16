from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    log_in = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_two = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    register = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            message = f'User {username.data} is taken earlier on.'
            raise ValidationError(message)

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            message = 'The email address is taken earlier on.'
            raise ValidationError(message)


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=140)])
    save = SubmitField('Save')
