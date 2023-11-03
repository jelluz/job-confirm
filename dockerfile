FROM python:3.11-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4 \
  POETRY_NO_INTERACTION=1

RUN apt-get -y update \
  && apt-get install --no-install-recommends -y \
  bash \
  nano \
  && pip install "poetry>=$POETRY_VERSION"

COPY poetry.lock pyproject.toml /pysetup/

WORKDIR /pysetup
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

WORKDIR /app

COPY . /app

CMD ["python", "start.py" ]

