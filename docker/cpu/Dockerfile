FROM python:3.9-slim

WORKDIR /main

RUN apt-get update && apt-get install -y\
  vim neovim nano \
  git git-lfs \
  zip unzip \
  curl make build-essential xz-utils file tree \
  sudo \
  && pip install --upgrade pip \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


# install python packages
RUN pip install poetry && \
  poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install
