import contextlib
import os
import re
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from .init import init

PROJECT_NAME = "myproject-name"
PYTHON_VERSION = "3.10"

ARGS_LIST = [
    "--python_version",
    PYTHON_VERSION,
]


@pytest.fixture
def cookiecutter_mock():
    with patch("lifedata.cli.init.cookiecutter") as cookiecutter_mock:
        yield cookiecutter_mock


@contextlib.contextmanager
def cd(path):
    """
    Changes working directory and returns to previous on exit.

    with cd("mypath"):
        pass
    """
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def test_init_calls_cookiecutter(cookiecutter_mock):
    runner = CliRunner()
    result = runner.invoke(init, [PROJECT_NAME] + ARGS_LIST)
    assert result.exit_code == 0, result.output

    cookiecutter_mock.assert_called_with(
        "https://github.com/ds-lab/lifedata-project-template.git",
        no_input=True,
        extra_context={
            "project_name": PROJECT_NAME,
            "python_version": PYTHON_VERSION,
        },
    )


def test_init_calls_cookiecutter_with_proper_python_version(cookiecutter_mock):
    runner = CliRunner()

    result = runner.invoke(init, [PROJECT_NAME] + ARGS_LIST)
    assert result.exit_code == 0, result.output

    args, kwargs = cookiecutter_mock.call_args
    assert re.match(r"\d\.\d+", kwargs["extra_context"]["python_version"])


def test_init_fails_when_path_already_exists(tmp_path: Path) -> None:
    runner = CliRunner()
    (tmp_path / "project").mkdir()

    with cd(tmp_path):
        result = runner.invoke(init, ["project"] + ARGS_LIST)

        assert result.exit_code == 2, result.output
