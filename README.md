# KidEdVisor


*Tested on Ubuntu 22 and Windows 10*
***


### `For backenders`
## Without docker-compose
First you need Postgres and Redis on your machine.

---
For Windows you need [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) to use Docker.


No need to install docker desktop, it only generates problems and makes things slower in windows. If you install Docker this way you will never ever again run into that problem:

#### `INSTALL DOCKER PACKAGE`
```
sudo -E apt update && sudo apt upgrade -y
sudo -E apt-get -qq install docker.io -y
```
#### `DOCKER DAEMON STARTUP` (Substitute .bashrc for .zshrc or any other shell you use)
```
rcfile=~/.bashrc
echo '# Start Docker daemon automatically when logging in if not running.' >> $rcfile
echo 'RUNNING=`ps aux | grep dockerd | grep -v grep`' >> $rcfile
echo 'if [ -z "$RUNNING" ]; then' >> $rcfile
echo '    sudo dockerd > /dev/null 2>&1 &' >> $rcfile
echo '    disown' >> $rcfile
echo 'fi' >> $rcfile
```
#### `ENABLE CURRENT USER AS SUDO FOR DOCKER`
```
echo $USER' ALL=(ALL) NOPASSWD: /usr/bin/dockerd' | sudo EDITOR='tee -a' visudo
sudo usermod -aG docker $USER
```
#### `REBOOT VM MACHINE`
```
wsl.exe --shutdown
```
---
Set and run Postgres:
```
docker run -d --name db-postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15-alpine
 ```
Set and run Redis:
```
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```
Or Redis for development (with RedisInsight):
```
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```
Load repo:
```
 git clone git@github.com:Xewus/KidEdVisor.git
```
Go to the project directory:
```
cd KidEdVisor\
```
Create a virtual environment
```
python[3.11] -m venv venv
```
Activate it.

For LINUX:
```
. venv/bin/activate
```
For WINDOWS:
```
 . .\venv\Scripts\activate
```
If you get a security error on Windows try:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

Go to the backend directory:
```
cd backend\
```
Install requirements.

For LINUX:
```
pip install -U pip && pip install -r requirements.txt
```
For WINDOWS:
```
python -m pip install -U pip
```
```
pip install -r .\dev.requirements.txt
```
Run migrations:
```
alembic upgrade head
```
Check that everything is working properly:
```
pytest
```
If tests are OK
---
Run the application:
```
uvicorn src.main:app --reload
```
`Then you can continue development.`
