"""This is an authentication and registration module.

It should not depend on other modules, except for settings,
databases and utilities.
Imports from other modules are strictly prohibited in order to avoid problems
when extending the application.
"""
from .crud import auth_crud
from .models import AuthModel, TempUserModel
from .router import router as auth_router
from .schemes import ResponseAuthScheme, TokenDataScheme
from .security import get_token_data, get_token_user
