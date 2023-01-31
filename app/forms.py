from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    log_in = SubmitField(_l('Log In'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password_two = PasswordField(
        _l('Confirm Password'),
        validators=[DataRequired(), EqualTo('password')]
    )
    register = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    bio = TextAreaField(_l('Bio'), validators=[Length(min=0, max=140)])
    save = SubmitField(_l('Save'))

    def __init__(self, initial_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.initial_username = initial_username

    def validate_username(self, username):
        if username.data != self.initial_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField(
        _l("What's on your mind?"),
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField(_l('Post'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password_two = PasswordField(
        _l('Confirm Password'),
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(_l('Reset Password'))
