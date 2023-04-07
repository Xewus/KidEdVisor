- Update SQLAlchemy to 2.0 -> remove SQLModel
- Add trigger to create auth
- Create test database with alembic.
- change date fields in schemes to int
- added docker containers for tests

### TODO

Deal with docker connections - why tests fail without the `sleep()` function after running containers.
