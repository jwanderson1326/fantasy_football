FROM python:3.7.4-slim-stretch

RUN apt-get update && apt-get install -y gcc

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


