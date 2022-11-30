# Python-template
## How to operate docker
### setup
1. Install with`git clone`
2. Go to directory`cd docker/{cpu or gpu}`
### docker configuration
1. `docker-compose up -d --build`
### Connect to and disconnect from docker
1. connect`docker-compose exec <service name(ex:python-cpu)> bash`
2. disconect`exit`
### Using jupyterlab
1. Access with a browser http://localhost:8888/lab
### Starting and Stopping Containers
1. Starting`docker stop <container name>`
2. Stopping`docker start <container name>`
