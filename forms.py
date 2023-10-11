from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, Email, Optional


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


class ListingAddForm(FlaskForm):
    """Add a listing. """

    title = StringField(
        'Title',
        validators=[InputRequired(), Length(max=30)]
    )

    description = TextAreaField(
        'Description',
        validators=[Optional(), Length(max=1000)])

    status = SelectField(
        'Status',
        choices=[('available', "Available"),
                 ('pending', 'Pending'),
                 ('reserved', 'Reserved')],
        validators=[InputRequired()]
    )