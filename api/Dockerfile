FROM python:3.7.4-slim-stretch as base

RUN apt-get update && apt-get install -y gcc \
      libpq-dev \
      python3-dev

RUN pip install poetry==0.12.17

RUN useradd -u 1000 -m justin
USER justin
RUN mkdir /home/justin/src
WORKDIR /home/justin/src

# Files needed for long-running setup operation
COPY --chown=justin:justin pyproject.toml .
COPY --chown=justin:justin poetry.lock .

# Install dependencies
RUN poetry install -v

##################################################################
FROM base as release

COPY --chown=justin:justin app/ app/
COPY --chown=justin:justin main.py main.py
COPY --chown=justin:justin manipulations.py manipulation.py
COPY --chown=justin:justin config.py config.py

ENTRYPOINT ["poetry", "run", "python3", "main.py"]

