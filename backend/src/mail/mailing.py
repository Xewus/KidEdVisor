import socket
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPAuthenticationError, SMTPSenderRefused

from fastapi.templating import Jinja2Templates
from jinja2 import Template

from src.config import CONFIRM_REG_HTML, MAIL_TEMPLATES_DIR, settings
from src.core.enums import SendEmailFrom

templates = Jinja2Templates(MAIL_TEMPLATES_DIR)


class Mailing:
    """Sending messages.

    #### Attrs:
    - connection (SMTP):
        Connecting to a mail server.
    - smtp_host (str): Default `Google Mail`.
        Mail server host.
    - smtp_port (int): Default from settings.
        Mail server port.
    - from_addr (str): Default from settings.
        Email address on behalf of which the mailing will be carried out.
    - smtp_password (str): Default from settings.
        Password to connect to mail server.
    """

    connection = None
    smtp_host = settings.google_smtp_host
    smtp_port = settings.google_smtp_port
    from_addr = SendEmailFrom.GOOGLE
    smtp_password = settings.google_smtp_password

    def __init__(
        self,
        smtp_host: str | None = None,
        smtp_port: int | None = None,
        from_addr: SendEmailFrom | None = None,
        smtp_password: str | None = None,
    ) -> None:
        if smtp_host is not None:
            self.smtp_host = smtp_host
        if smtp_port is not None:
            self.smtp_port = smtp_port
        if from_addr is not None:
            self.from_addr = from_addr
        if smtp_password is not None:
            self.smtp_password = smtp_password

        match self.from_addr:
            case SendEmailFrom.GOOGLE:
                self.__set_google_connection()
            case _:
                raise AttributeError(
                    f"{self.__class__}: attr `from_addr` unknown value"
                )

    def __set_google_connection(self) -> None:
        """Create a connection to the `Google SMTP server`."""
        try:
            connection = SMTP_SSL(
                host=self.smtp_host,
                port=self.smtp_port,
            )
            connection.login(
                user=self.from_addr,
                password=self.smtp_password.get_secret_value(),
            )
        except socket.timeout:
            return f"the smtp_host `{self.smtp_host}` didn`t respond"

        except (SMTPAuthenticationError, SMTPSenderRefused):
            return "incorrect from_addr or password."

        self.connection = connection
        return None

    def confirmation_message(self, recipient: str, link: str) -> MIMEMultipart:
        """Create the message to confirm registration.

        #### Args:
        - recipient (str):
            Message recipient email.
        - link (str):
            Link to confirm.

        #### Returns:
        - MIMEMultipart:
            Filled message.
        """
        email = MIMEMultipart("alternative")
        email["Subject"] = Header("Confirmation of registration")
        email["fROM"] = self.from_addr
        email["To"] = recipient
        template: Template = templates.get_template(CONFIRM_REG_HTML)
        content = template.render({"link": link})
        email.attach(MIMEText(content, "html"))
        return email

    def send_confirm_email(self, recipient: str, link: str) -> None:
        """Send a confirmation email to the recipient.

        #### Args:
        - recipient (str):
            Message recipient email.
        - link (str):
            Link to confirm.
        """
        if self.connection is None:
            return None

        msg = self.confirmation_message(recipient, link)
        try:
            self.connection.send_message(msg, from_addr=self.from_addr)
        except (SMTPAuthenticationError, SMTPSenderRefused) as exc:
            print("error:", exc.args[0])
            return None

        finally:
            self.connection.close()
        return None
