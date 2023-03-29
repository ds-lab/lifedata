import sys
from pathlib import Path

import click
from cookiecutter.main import cookiecutter

from .main import main


@main.command()
@click.argument("project_name")
@click.option("--python_version")
def init(
    project_name,
    python_version,
):
    """
    Setup a project template
    """
    path = Path.cwd() / project_name.lower()
    if path.exists():
        raise click.UsageError(
            f"There already exists a directory for the given projectname: {path}"
        )

    if python_version is None:
        # Get python version of lifedata installation as default
        python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"

    print(f"Creating project in {path} ...")

    cookiecutter(
        "https://github.com/ds-lab/lifedata-project-template.git",
        no_input=True,
        extra_context={
            "project_name": project_name.lower(),
            "python_version": python_version,
        },
    )

    print("Project created at ", path)

    print("To get started ...")
    print(f"\t cd {path} \n")
    print(f"\t mamba env create {project_name} OR conda env create {project_name} \n")
    print(f"\t conda activate {project_name}\n")


# NOTE: It is possible to instanciate differenc cookiecutter projects with new methods (pure ML, ml with UI, etc.)
