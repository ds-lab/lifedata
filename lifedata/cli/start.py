import os
import shlex
from pathlib import Path

import click
from honcho.manager import Manager
from loguru import logger

from .main import main
from lifedata.cli.configure_db import db_option

BACKEND_DEFAULT_PORT = "8000"


def dev_option():
    return click.option(
        "--dev/--no-dev",
        default=False,
        help="Enable development features like reloading the service when source files have changed. Don't use in production.",
    )


def contribute_backend_process(
    manager: Manager,
    db_url: str,
    host: str,
    port: str,
    reload: bool,
    better_exceptions: bool,
) -> None:
    env = os.environ.copy()
    env.update(
        {
            "APP_DATABASE_URL": db_url,
            "ALLOW_CORS_ORIGINS": "http://localhost:3000 http://127.0.0.1:3000",
        }
    )
    if better_exceptions:
        env["BETTER_EXCEPTIONS"] = "1"
    framework_dir = Path(__file__).parent.parent
    reload_option = (
        f" --reload --reload-dir={shlex.quote(str(Path.cwd()))}"
        f" --reload-dir={shlex.quote(str(framework_dir))}"
        if reload
        else ""
    )

    command = (
        f"uvicorn lifedata.webapi.main:app --host={host} --port={port}{reload_option}"
    )
    manager.add_process("backend", command, env=env)


def contribute_annotationui_process(manager: Manager) -> None:
    lifedata_framework_root = Path(__file__).parent.parent / "webui"
    os.environ.update(
        {
            "REACT_APP_API_URL": f"http://localhost:{BACKEND_DEFAULT_PORT}/api",
        }
    )
    manager.add_process(
        "annotationui",
        "yarn start",
        cwd=lifedata_framework_root,
    )


def contribute_db_process(manager: Manager) -> None:
    # TODO: Make dependent on config instead of using the current working
    # directory.
    docker_compose_file = Path() / "docker-compose.yml"
    command = f"docker-compose -f {docker_compose_file} up db"
    manager.add_process("db", command)


@main.group(invoke_without_command=True)
@click.pass_context
@dev_option()
@db_option()
def start(ctx, dev, db):
    """
    Start a full setup of lifedata services be leaving of any arguments, or
    provide one of the commands from the list below to start an individual
    service.
    """
    if ctx.invoked_subcommand is None:
        manager = Manager()
        contribute_db_process(manager)
        contribute_backend_process(
            manager,
            db_url=db,
            host="127.0.0.1",
            port=BACKEND_DEFAULT_PORT,
            reload=dev,
            better_exceptions=dev,
        )
        contribute_annotationui_process(manager)
        manager.loop()
        ctx.exit(manager.returncode)


@start.command()
@click.pass_context
@db_option()
@click.option(
    "--host",
    default="127.0.0.1",
    help="Provide 0.0.0.0 to allow access from all hosts, default is to only allow localhost",
)
@click.option(
    "--port",
    type=click.IntRange(1, 65535),
    default=lambda: os.environ.get("PORT", BACKEND_DEFAULT_PORT),
    show_default=f"{BACKEND_DEFAULT_PORT} (or $PORT if set)",
)
@dev_option()
def backend(ctx, db, host, port, dev):
    manager = Manager()
    contribute_backend_process(
        manager, db, host, port, reload=dev, better_exceptions=dev
    )
    manager.loop()
    ctx.exit(manager.returncode)


@start.command()
@click.pass_context
@dev_option()
def annotationui(ctx, dev: bool) -> None:  # type: ignore
    manager = Manager()

    contribute_annotationui_process(manager)
    manager.loop()

    if manager.returncode != 0:
        logger.warning(
            "The annotationui failed, that might be because your installation is not complete. For now you need a full JS development setup in the lifedata/webui/ directory. Go to the lifedata/webui/ directory in your checkout of the lifedata repository and execute 'yarn install'"
        )

    ctx.exit(manager.returncode)


@start.command()
@click.pass_context
def db(ctx):
    """
    Starts the database, configured in the docker-compose file of the project instance.
    """
    manager = Manager()
    contribute_db_process(manager)
    manager.loop()
    ctx.exit(manager.returncode)
