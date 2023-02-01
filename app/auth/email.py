from flask import current_app, render_template

from flask_babel import _

from app.email import send_email


def send_password_reset_email(user):
    token = user.reset_password_token()
    send_email(
        _('[Microblog] Reset your Password'),
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        body=render_template('email/reset_password.txt', user=user, token=token),
        html=render_template('email/reset_password.html', user=user, token=token)
    )
