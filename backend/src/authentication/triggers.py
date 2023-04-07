"""Insert this into first migration.
"""
from alembic import op

from src.core.enums import TableNames, UserType


def upgrade():
    # trigger for postgresql
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION insert_other_table()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.user_type = {UserType.PARENT} THEN
                INSERT INTO {TableNames.PARENT} (auth_id) VALUES (NEW.id);
            ELSEIF NEW.user_type = {UserType.OWNER} THEN
                INSERT INTO {TableNames.OWNER} (auth_id) VALUES (NEW.id);
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """  # nosec B608
    )
    op.execute(
        f"""
        CREATE TRIGGER {TableNames.AUTH}_insert_trigger
        AFTER INSERT ON {TableNames.AUTH}
        FOR EACH ROW
        EXECUTE FUNCTION insert_other_table();
        """
    )


def downgrade() -> None:
    op.execute(
        f"DROP TRIGGER {TableNames.AUTH}_insert_trigger ON {TableNames.AUTH};"
    )
    op.execute("DROP FUNCTION insert_other_table();")
