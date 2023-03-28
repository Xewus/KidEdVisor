from typing import Callable

from .mailing import Mailing


async def get_send_confirm_link() -> Callable:
    mailing = Mailing()
    return mailing.send_confirm_email
