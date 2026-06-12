import os

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .extensions import db
from .forms import CredentialForm, LoginForm, PasswordGeneratorForm, RegisterForm
from .models import Credential, User
from .security import (
    PasswordOptions,
    decrypt_text,
    derive_vault_key,
    encrypt_text,
    generate_secure_password,
)

main_bp = Blueprint("main", __name__)
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
vault_bp = Blueprint("vault", __name__, url_prefix="/vault")


def _vault_key_or_redirect():
    key_text = session.get("vault_key")
    if key_text:
        return key_text.encode("utf-8")

    logout_user()
    session.clear()
    flash("Your vault key expired. Log in again to unlock your passwords.", "warning")
    return None


def _encrypt_credential_from_form(credential: Credential, form: CredentialForm, vault_key: bytes) -> None:
    credential.service_enc = encrypt_text(vault_key, form.service.data.strip())
    credential.login_name_enc = encrypt_text(vault_key, form.login_name.data.strip())
    credential.password_enc = encrypt_text(vault_key, form.password.data)
    credential.url_enc = encrypt_text(vault_key, form.url.data.strip() if form.url.data else "")
    credential.notes_enc = encrypt_text(vault_key, form.notes.data.strip() if form.notes.data else "")


def _credential_to_view(credential: Credential, vault_key: bytes) -> dict:
    return {
        "id": credential.id,
        "service": decrypt_text(vault_key, credential.service_enc),
        "login_name": decrypt_text(vault_key, credential.login_name_enc),
        "password": decrypt_text(vault_key, credential.password_enc),
        "url": decrypt_text(vault_key, credential.url_enc),
        "notes": decrypt_text(vault_key, credential.notes_enc),
        "created_at": credential.created_at,
        "updated_at": credential.updated_at,
    }


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("vault.dashboard"))
    return render_template("index.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("vault.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip().lower()
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("That username is already taken.", "danger")
            return render_template("auth/register.html", form=form)

        user = User(username=username, encryption_salt=os.urandom(16))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Log in to unlock your vault.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("vault.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip().lower()
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return render_template("auth/login.html", form=form)

        vault_key = derive_vault_key(form.password.data, user.encryption_salt)
        session.clear()
        session.permanent = True
        login_user(user)
        session["vault_key"] = vault_key.decode("utf-8")

        flash("Vault unlocked.", "success")
        return redirect(url_for("vault.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Logged out and vault key cleared.", "info")
    return redirect(url_for("main.index"))


@vault_bp.route("/")
@login_required
def dashboard():
    vault_key = _vault_key_or_redirect()
    if vault_key is None:
        return redirect(url_for("auth.login"))

    search_term = request.args.get("q", "").strip().lower()
    credentials = current_user.credentials.order_by(Credential.updated_at.desc()).all()
    views = [_credential_to_view(item, vault_key) for item in credentials]

    if search_term:
        views = [
            item for item in views
            if search_term in item["service"].lower()
            or search_term in item["login_name"].lower()
            or search_term in item["url"].lower()
        ]

    return render_template("vault/dashboard.html", credentials=views, search_term=search_term)


@vault_bp.route("/credentials/new", methods=["GET", "POST"])
@login_required
def add_credential():
    vault_key = _vault_key_or_redirect()
    if vault_key is None:
        return redirect(url_for("auth.login"))

    form = CredentialForm()
    if form.validate_on_submit():
        credential = Credential(owner=current_user)
        _encrypt_credential_from_form(credential, form, vault_key)
        db.session.add(credential)
        db.session.commit()
        flash("Credential saved securely.", "success")
        return redirect(url_for("vault.dashboard"))

    return render_template("vault/form.html", form=form, title="Add credential")


@vault_bp.route("/credentials/<int:credential_id>")
@login_required
def view_credential(credential_id: int):
    vault_key = _vault_key_or_redirect()
    if vault_key is None:
        return redirect(url_for("auth.login"))

    credential = Credential.query.filter_by(id=credential_id, user_id=current_user.id).first_or_404()
    view = _credential_to_view(credential, vault_key)
    return render_template("vault/detail.html", credential=view)


@vault_bp.route("/credentials/<int:credential_id>/edit", methods=["GET", "POST"])
@login_required
def edit_credential(credential_id: int):
    vault_key = _vault_key_or_redirect()
    if vault_key is None:
        return redirect(url_for("auth.login"))

    credential = Credential.query.filter_by(id=credential_id, user_id=current_user.id).first_or_404()
    view = _credential_to_view(credential, vault_key)
    form = CredentialForm(data=view)

    if form.validate_on_submit():
        _encrypt_credential_from_form(credential, form, vault_key)
        db.session.commit()
        flash("Credential updated securely.", "success")
        return redirect(url_for("vault.view_credential", credential_id=credential.id))

    return render_template("vault/form.html", form=form, title="Edit credential")


@vault_bp.route("/credentials/<int:credential_id>/delete", methods=["POST"])
@login_required
def delete_credential(credential_id: int):
    credential = Credential.query.filter_by(id=credential_id, user_id=current_user.id).first_or_404()
    db.session.delete(credential)
    db.session.commit()
    flash("Credential deleted.", "info")
    return redirect(url_for("vault.dashboard"))


@vault_bp.route("/generator", methods=["GET", "POST"])
@login_required
def generator():
    form = PasswordGeneratorForm()
    generated_password = None

    if form.validate_on_submit():
        try:
            options = PasswordOptions(
                length=form.length.data,
                use_uppercase=form.use_uppercase.data,
                use_lowercase=form.use_lowercase.data,
                use_digits=form.use_digits.data,
                use_symbols=form.use_symbols.data,
            )
            generated_password = generate_secure_password(options)
        except ValueError as exc:
            flash(str(exc), "danger")

    return render_template(
        "vault/generator.html",
        form=form,
        generated_password=generated_password,
    )
