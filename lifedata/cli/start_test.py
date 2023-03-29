import re
import string
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from unittest.mock import ANY
from unittest.mock import call
from unittest.mock import patch

from click.testing import CliRunner
from hypothesis import given
from hypothesis import strategies as st

from .configure_db import DATABASE_DEFAULT_URL
from .start import annotationui
from .start import backend
from .start import BACKEND_DEFAULT_PORT
from .start import db
from .start import start

db_url = partial(st.text, alphabet=string.ascii_letters + string.punctuation)


@contextmanager
def mock_honcho_manager():
    with patch("lifedata.cli.start.Manager") as manager_mock:
        # We return the instance of the manager for easier handling in test
        # cases.
        yield manager_mock.return_value


@given(
    exit_code=st.integers(0, 128),
)
def test_start_command_runs_all_services(exit_code):
    with mock_honcho_manager() as manager:
        manager.returncode = exit_code

        runner = CliRunner()
        result = runner.invoke(start)

        assert manager.add_process.call_count == 3

        # backend is added as process.
        backend_calls = [
            c for c in manager.add_process.call_args_list if c.args[0] == "backend"
        ]
        assert len(backend_calls) == 1
        backend_call = backend_calls[0]
        assert (
            backend_call.args[1]
            == "uvicorn lifedata.webapi.main:app --host=127.0.0.1 --port=8000"
        )

        # annotationui is added as process.
        assert (
            call("annotationui", "yarn start", cwd=ANY)
            in manager.add_process.call_args_list
        )

        # db is added as process.
        assert (
            call("db", "docker-compose -f docker-compose.yml up db")
            in manager.add_process.call_args_list
        )

        assert result.exit_code == exit_code


@given(
    dev_arg=st.booleans(),
    db_arg=db_url(),
    db_env=db_url(),
    host_arg=st.text(),
    port_arg=st.integers(1, 65535).map(str),
    port_env=st.integers(1, 65535).map(str),
    exit_code=st.integers(0, 128),
)
def test_backend_command(
    dev_arg, db_arg, db_env, host_arg, port_arg, port_env, exit_code
):
    with mock_honcho_manager() as manager:
        manager.returncode = exit_code

        runner = CliRunner()
        cli_args = []
        cli_env = {}

        if db_arg:
            cli_args.append("--db")
            cli_args.append(db_arg)
        if db_env:
            cli_env["APP_DATABASE_URL"] = db_env
        if port_arg:
            cli_args.append("--port")
            cli_args.append(port_arg)
        if port_env:
            cli_env["PORT"] = port_env
        if host_arg:
            cli_args.append("--host")
            cli_args.append(host_arg)
        if dev_arg:
            cli_args.append("--dev")

        result = runner.invoke(backend, cli_args, env=cli_env)

        (name, command), kwargs = manager.add_process.call_args

        command_env = kwargs["env"]

        assert name == "backend"
        assert re.match("^uvicorn lifedata.webapi.main:app", command)

        assert (
            command_env["ALLOW_CORS_ORIGINS"]
            == "http://localhost:3000 http://127.0.0.1:3000"
        )

        # The cli argument takes precedence over the env variable
        expected_db = db_arg or db_env or DATABASE_DEFAULT_URL
        assert command_env["APP_DATABASE_URL"] == expected_db

        # Argument takes precedence over env variable
        expected_port = port_arg or port_env or BACKEND_DEFAULT_PORT
        assert f" --port={expected_port}" in command

        expected_host = host_arg or "127.0.0.1"
        assert f" --host={expected_host}" in command

        if dev_arg:
            assert " --reload --reload-dir=" in command
            assert command_env["BETTER_EXCEPTIONS"] == "1"
        else:
            assert " --reload" not in command
            assert "BETTER_EXCEPTIONS" not in command_env

        # manager is brought into loop
        manager.loop.assert_called_with()
        assert result.exit_code == exit_code


def test_backend_command_fails_if_no_db_arg_is_given():
    with mock_honcho_manager() as manager:
        runner = CliRunner()
        result = runner.invoke(backend, ["--db="])

        manager.loop.assert_not_called()
        assert result.exit_code == 2
        assert "Invalid value for '--db'" in result.output


def test_backend_command_does_not_accept_additional_arguments():
    with mock_honcho_manager() as manager:
        runner = CliRunner()
        result = runner.invoke(backend, ["somearg"])

        manager.loop.assert_not_called()
        assert result.exit_code == 2
        assert "Usage:" in result.output


@given(
    dev_arg=st.booleans(),
    exit_code=st.integers(0, 128),
)
def test_annotationui(dev_arg, exit_code):
    with mock_honcho_manager() as manager:
        manager.returncode = exit_code

        cli_args = []
        if dev_arg:
            cli_args.append("--dev")

        runner = CliRunner()
        result = runner.invoke(annotationui, cli_args)

        # add_process has been called with db as name and the docker-compose command.
        manager.add_process.called_once_with("annotationui", "yarn start", cwd=ANY)

        # The process should be started in the webui directory.
        assert Path(manager.add_process.call_args.kwargs["cwd"]).name == "webui"

        # The --dev argument has no effect yet.

        # manager is brought into loop
        manager.loop.assert_called_with()

        # return code is passed through from manager to the exit code of the CLI.
        assert result.exit_code == exit_code


@given(exit_code=st.integers(0, 128))
def test_db(exit_code):
    with mock_honcho_manager() as manager:
        manager.returncode = exit_code

        runner = CliRunner()
        result = runner.invoke(db)

        # add_process has been called with db as name and the docker-compose command.
        args, kwargs = manager.add_process.call_args
        assert args[0] == "db"
        assert re.match("^docker-compose -f .+ up db$", args[1])

        # manager is brought into loop
        manager.loop.assert_called_with()

        # return code is passed through from manager to the exit code of the CLI.
        assert result.exit_code == exit_code
