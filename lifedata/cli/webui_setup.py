import subprocess
from pathlib import Path

import click
from loguru import logger

from .main import main


@main.group()
def webui():
    """
    Collection of commands to setup webui
    """
    pass


@webui.command()
def install() -> None:
    """
    Command to execute yarn install, yarn build for the webui
    """
    execution_path = Path(__file__).parent.parent / "webui"

    if (execution_path).exists():
        logger.info("yarn install for lifedata started")
        yarn_install = ["yarn", "install"]
        subprocess.call(yarn_install, cwd=str(execution_path))
        logger.info("yarn install for lifedata finished")
        logger.info("yarn build for lifedata started")
        yarn_run_build = ["yarn", "run", "build"]
        subprocess.call(yarn_run_build, cwd=str(execution_path))
        logger.info("yarn build for lifedata finished")
        logger.info("yarn cache clean for lifedata started")
        yarn_cache_clean = ["yarn", "cache", "clean"]
        subprocess.call(yarn_cache_clean, cwd=str(execution_path))
        logger.info("yarn cache clean for lifedata finished")
    else:
        raise click.FileError(
            str(execution_path), hint=f"Ensure {execution_path} exists in lifedata"
        )


@webui.command()
def serve() -> None:
    """
    Command to execute yarn serve for the webui
    """
    execution_path = Path(__file__).parent.parent / "webui"

    if (execution_path).exists():
        logger.info("yarn run serve for lifedata started")
        yarn_run_serve = ["yarn", "run", "serve"]
        subprocess.call(yarn_run_serve, cwd=str(execution_path))
        logger.info("yarn run serve for lifedata finished")
    else:
        raise click.FileError(
            str(execution_path), hint=f"Ensure {execution_path} exists in lifedata"
        )
