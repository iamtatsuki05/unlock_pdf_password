FROM ubuntu:22.04 AS base

ARG PYTHON_VERSION=3.10

ENV DEBIAN_FRONTEND=noninteractive
ENV WORKDIR /app/

WORKDIR /opt

# install dev tools
RUN apt-get update && apt-get install -y \
  vim neovim nano \
  git git-lfs \
  zip unzip \
  curl wget make build-essential xz-utils file tree \
  sudo \
  dnsutils \
  tzdata language-pack-ja \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# for Japanese settings
# ENV TZ Asia/Tokyo
# ENV LANG ja_JP.utf8

# for US settings
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US

# install Python
RUN apt-get update && apt-get -yV upgrade && DEBIAN_FRONTEND=noninteractive apt-get -yV install \
  build-essential libssl-dev libffi-dev \
  python${PYTHON_VERSION} python${PYTHON_VERSION}-distutils python${PYTHON_VERSION}-dev \
  && ln -s /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python3 \
  && ln -s /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

## install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3 get-pip.py \
  && pip3 --no-cache-dir install --upgrade pip

## install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH $PATH:/root/.local/bin
RUN poetry config virtualenvs.create true \
  && poetry config virtualenvs.in-project false

WORKDIR ${WORKDIR}

# install python packages
COPY poetry.lock pyproject.toml ./
COPY src ./src
RUN poetry install --no-dev

FROM base AS dev
WORKDIR ${WORKDIR}

# install python packages
COPY poetry.lock pyproject.toml ./
COPY src ./src
RUN poetry install

# Hugging Face Hub Settings
FROM dev AS hf
WORKDIR ${WORKDIR}

# REF: https://huggingface.co/docs/hub/spaces-sdks-docker-first-demo#:~:text=As%20discussed%20in,the%20Dockerfile.
# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
  PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app
## install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH $PATH:/root/.local/bin
RUN poetry config virtualenvs.create true \
  && poetry config virtualenvs.in-project false

RUN poetry install --no-dev
RUN poetry install

CMD ["poetry", "run", "streamlit", "run", "src/app.py", "--server.port", "7860"]
