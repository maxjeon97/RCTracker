"""Forms for Flask Cafe."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, Length, URL, Optional, AnyOf


ALL_US_STATES = [
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA",
    "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO",
    "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI",
    "WV", "WY"]


class CafeInfoForm(FlaskForm):
    """Form for adding/editing cafes."""

    name = StringField(
        'Name',
        validators=[InputRequired(), Length(max=50)],
    )

    description = TextAreaField('Description (Optional)')

    url = StringField(
        'URL',
        validators=[Optional(), URL()]
    )

    address = StringField(
        'Address',
        validators=[InputRequired()]
    )

    city_code = SelectField('City')

    image_url = StringField(
        'Image URL (Optional)',
        validators=[Optional(), URL(), Length(max=255)]
    )


class AddCityForm(FlaskForm):
    """Form for adding cities."""

    code = StringField(
        'Code',
        validators=[InputRequired()],
    )

    name = StringField(
        'Name',
        validators=[InputRequired()],
    )

    state = StringField(
        'State (Two-letter Abbreviation)',
        validators=[InputRequired(), Length(max=2),
                    AnyOf(ALL_US_STATES, message="Must enter a valid U.S. state.")],
    )


class UserSignupForm(FlaskForm):
    """Form for signing up users."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    first_name = StringField(
        'First Name',
        validators=[InputRequired(), Length(max=30)],
    )

    last_name = StringField(
        'Last Name',
        validators=[InputRequired(), Length(max=30)],
    )

    description = TextAreaField('Description (Optional)')

    email = StringField(
        'Email',
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )

    image_url = StringField(
        'Image URL (Optional)',
        validators=[Optional(), URL(), Length(max=255)]
    )


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        'Username',
        validators=[InputRequired()]
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired()]
    )


class ProfileEditForm(FlaskForm):
    """Form for editing user profile."""

    first_name = StringField(
        'First Name',
        validators=[InputRequired(), Length(max=30)],
    )

    last_name = StringField(
        'Last Name',
        validators=[InputRequired(), Length(max=30)],
    )

    description = TextAreaField('Description (Optional)')

    email = StringField(
        'Email',
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    image_url = StringField(
        'Image URL (Optional)',
        validators=[Optional(), URL(), Length(max=255)]
    )


class CSRFProtectForm(FlaskForm):
    """ Form for CSRF protection """
