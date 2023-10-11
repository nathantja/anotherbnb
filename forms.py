from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, TextAreaField, SelectField, MultipleFileField
from wtforms.validators import InputRequired, Length, Email, Optional
from flask_wtf.file import FileAllowed


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

    images = MultipleFileField(
        'Upload images',
        validators=[InputRequired(),
                    FileAllowed(['png', 'jpg', 'jpeg'], 'Only png, jpg, & jpeg supported.')]
    )

    status = SelectField(
        'Status',
        choices=[('available', "Available"),
                 ('pending', 'Pending'),
                 ('reserved', 'Reserved')],
        validators=[InputRequired()]
    )