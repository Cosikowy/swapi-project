FROM python:3.11.2

WORKDIR /app/
ENV POETRY_VERSION=1.3.0

RUN apt update -y && apt upgrade -y

RUN pip install poetry==$POETRY_VERSION

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi
COPY . /app/
