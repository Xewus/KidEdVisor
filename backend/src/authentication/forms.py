from fastapi import Form
from src.config import Limits
from src.core.validators import email_validator, password_validator


class EmailForm:
    def __init__(
        self,
        email: str = Form(max_length=Limits.MAX_LEN_EMAIL),
    ) -> None:
        self.email = email_validator(email)


class PasswordForm:
    def __init__(
        self,
        password: str = Form(
            min_length=Limits.MIN_LEN_PASSWORD,
            max_length=Limits.MAX_LEN_PASSWORD,
        ),
    ) -> None:
        self.password = password_validator(password)


class Oauth2EmailForm(EmailForm, PasswordForm):
    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        username: str = Form(max_length=Limits.MAX_LEN_EMAIL),
        password: str = Form(
            min_length=Limits.MIN_LEN_PASSWORD,
            max_length=Limits.MAX_LEN_PASSWORD,
        ),
        scope: str = Form(default=""),
        client_id: str | None = Form(default=None),
        client_secret: str | None = Form(default=None),
    ) -> None:
        EmailForm.__init__(self, username)
        PasswordForm.__init__(self, password)
        self.grant_type = grant_type
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
