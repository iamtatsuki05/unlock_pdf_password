# Python-template

## How to operate docker
### setup
1. Install with : `git clone`
### docker configuration
1. `docker compose up -d --build`
### Connect to and disconnect from docker
1. connect : `docker compose exec <service name(ex:python-cpu)> bash`
2. disconect : `exit`
### Using jupyterlab
1. Access with a browser http://localhost:8888/lab
### Starting and Stopping Containers
1. Starting : `docker stop <container name>`
2. Stopping : `docker start <container name>`

## Directory structure
```text
./
├── .dockerignore
├── .git
├── .gitattributes
├── .github
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── Makefile
├── README.md
├── compose.yaml
├── config
├── data
│   ├── misc
│   ├── outputs
│   └── raw
├── docker
│   └── cpu
├── docs
├── env.sample
├── notebooks
├── poetry.lock
├── pyproject.toml
├── scripts
│   └── main.py
├── src
│   ├── __init__.py
│   └── project
│       ├── common
│       ├── config
│       ├── env.py
│       └── main.py
└── tests
    └── project
```
