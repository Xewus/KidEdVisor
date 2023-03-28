"""This is an authentication and registration module.

It should not depend on other modules, except for settings,
databases and utilities.
Imports from other modules are strictly prohibited in order to avoid problems
when extending the application.
"""
from .router import router as auth_router  # noqa
