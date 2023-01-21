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

    def __init__(self, initial_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.initial_username = initial_username

    def validate_username(self, username):
        if username.data != self.initial_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField(
        "What's on your mind?",
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField('Post')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_two = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Reset Password')
