FROM python:3.8

# Install libraries that can ease the use of the container, but are no direct
# dependencies of the project.
RUN pip install ipython

# Install dependencies that require compilation. We do this here to use
# docker's caching for fast re-builds of the image.
RUN pip install numpy uvicorn

ADD ./pytest.ini ./README.md /app/
COPY ./setup.py /app/setup.py
COPY ./lifedata /app/lifedata

ENV ALEMBIC_CONFIG=/app/lifedata/alembic.ini

WORKDIR /app

ARG VERSION=docker.dev
ENV DOCKER_BUILD_VERSION $VERSION

RUN SETUPTOOLS_SCM_PRETEND_VERSION=$DOCKER_BUILD_VERSION pip install -e .[dev]

ENV PORT 8000
EXPOSE 8000

CMD ["uvicorn", "lifedata.webapi.main:app", "--host=0.0.0.0", "--port=8000"]
