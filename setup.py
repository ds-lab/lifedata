import os
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

setup(
    name="lifedata",
    maintainer="LIFEDATA Research Group",
    packages=find_packages(
        os.path.dirname(os.path.abspath(__file__)),
        include=["lifedata", "lifedata.*"],
        exclude=[],
    ),
    include_package_data=True,
    package_data={
        "lifedata": [
            str(file)
            for file in (
                Path(os.path.dirname(os.path.abspath(__file__))) / "webui"
            ).rglob("*")
        ]
    },
    entry_points={"console_scripts": ["lifedata = lifedata.cli.cli:main"]},
    long_description=open("README.md").read(),
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=[
        "alembic",
        "aiofiles",
        "click",
        "cookiecutter",
        "fastapi",
        "honcho",
        "pyjwt",
        "pandas",
        "loguru",
        "numpy",
        "orjson",
        "pydantic",
        "psycopg2-binary",
        "sqlalchemy",
        "toolz",
        # Required to start the backend services.
        "uvicorn",
        # Dependencies for frontend development
        # lifedata required packages
        # "conda install -c conda-forge nodejs==16",
        # NOTE: We enforce a version >1, since conda would otherwise prefer a rather old
        # version in the defaults channel.
        # "conda install -c conda-forge yarn>1"
    ],
    extras_require={
        "dev": [
            "black",
            # For testing purposes:
            "hypothesis",
            "pytest",
            "pytest-cov",
            # Required for the fastapi Testclient.
            "requests",
        ],
    },
)
