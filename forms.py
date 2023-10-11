from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class UserAddForm(FlaskForm):
    """User signup form."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)]
    )

    email = StringField(
        'E-mail',
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=1, max=50)],
    )


class LoginForm(FlaskForm):
    """User login form."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=1, max=50)],
    )


class CSRFProtectForm(FlaskForm):
    """Form for CSRF protection."""