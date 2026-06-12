from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, Optional, URL


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"autocomplete": "username"},
    )
    password = PasswordField(
        "Master password",
        validators=[DataRequired(), Length(min=10, max=128)],
        render_kw={"autocomplete": "new-password"},
    )
    confirm_password = PasswordField(
        "Confirm master password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"autocomplete": "new-password"},
    )
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"autocomplete": "username"},
    )
    password = PasswordField(
        "Master password",
        validators=[DataRequired(), Length(min=1, max=128)],
        render_kw={"autocomplete": "current-password"},
    )
    submit = SubmitField("Unlock vault")


class CredentialForm(FlaskForm):
    service = StringField("Service name", validators=[DataRequired(), Length(max=120)])
    login_name = StringField("Username / Email", validators=[DataRequired(), Length(max=180)])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(max=256)],
        widget=PasswordInput(hide_value=False),
        render_kw={"autocomplete": "new-password"},
    )
    url = StringField("Website URL", validators=[Optional(), URL(), Length(max=255)])
    notes = TextAreaField("Private notes", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Save credential")


class PasswordGeneratorForm(FlaskForm):
    length = IntegerField(
        "Length",
        default=20,
        validators=[DataRequired(), NumberRange(min=8, max=128)],
    )
    use_uppercase = BooleanField("Uppercase", default=True)
    use_lowercase = BooleanField("Lowercase", default=True)
    use_digits = BooleanField("Numbers", default=True)
    use_symbols = BooleanField("Symbols", default=True)
    submit = SubmitField("Generate password")
