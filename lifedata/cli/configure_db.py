import os

import click

DATABASE_DEFAULT_URL = (
    "postgresql://lifedata:password-for-development@127.0.0.1:5432/lifedata"
)


def validate_db_option(ctx, param, value):
    if not value:
        raise click.BadParameter(
            "You need to provide a database connection."
            f"Either via --{param.name} or via the $APP_DATABASE_URL env variable."
        )
    return value


def db_option():
    return click.option(
        "--db",
        default=lambda: os.environ.get("APP_DATABASE_URL", DATABASE_DEFAULT_URL),
        show_default="(read from $APP_DATABASE_URL)",
        callback=validate_db_option,
    )
