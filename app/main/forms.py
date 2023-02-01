from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import User


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
