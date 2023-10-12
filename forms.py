from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    MultipleFileField,
    IntegerField,
    DecimalField,
    DateField,
    TimeField,
    )

from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    Optional,
    NumberRange,
    )

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
    """Add a listing."""

    title = StringField(
        'Title',
        validators=[InputRequired(), Length(max=30)]
    )

    description = TextAreaField(
        'Description',
        validators=[Optional(), Length(max=1000)])

    images = MultipleFileField(
        'Upload images',
        validators=[InputRequired()]
    )

    sq_ft = IntegerField(
        'Square ft',
        validators=[InputRequired(), NumberRange(min=1, message="Mininum is 1.")]
    )

    max_guests = IntegerField(
        'Maximum number of guests',
        validators=[InputRequired(), NumberRange(min=1, message="Mininum is 1.")]
    )

    hourly_rate = DecimalField(
        "Hourly rate",
        places=2,
        validators=[InputRequired(), NumberRange(min=1, message="Mininum is 1.")]
    )

    status = SelectField(
        'Status',
        choices=[('available', "Available"),
                 ('pending', 'Pending'),
                 ('reserved', 'Reserved')],
        validators=[InputRequired()]
    )


class ReservationAddForm(FlaskForm):
    """Request a reservation for a specific listing."""

    start_date = DateField(
        "Start Date",
        validators=[InputRequired()]
    )

    start_time = TimeField(
        "Start Time",
        validators=[InputRequired()]
    )

    hours = IntegerField(
        'Hours',
        validators=[InputRequired(), NumberRange(min=1, message="Mininum is 1.")]
    )

    guests = IntegerField(
        'Number of Guests',
        validators=[InputRequired(), NumberRange(min=1, message="Mininum is 1.")]
    )