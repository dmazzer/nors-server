# NORS Project - The Server #

## Preparing Environment ##

The server may be used as stand-alone application or as a Docker container. The Docker container is recommended as it will prepare all environment, start the server and connect to MongoDB server container.
For developers, the stand-alone way may be preferred.

### Preparing Native Stand-Alone Environment ###

Setting up Python virtual environment:

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
(venv) $ deactivate
```

After prepare the virtual environment the server may be run like follows:

```
$ source venv/bin/activate
(venv) $ ./nors_srv.py -c nors.conf
(venv) $ deactivate
```


### Building Docker Container ###

Install Docker as instructed [here](https://docs.docker.com/engine/installation/linux/ubuntulinux/)

For Ubuntu 14.04:

```
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates
$ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
```

Insert the above line in file `/etc/apt/sources.list.d/docker.list`:

```
deb https://apt.dockerproject.org/repo ubuntu-trusty main
```

Then:

```
$ sudo apt-get update
$ sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
$ sudo apt-get install docker-engine
$ sudo service docker start
```

### Building the Container ###

Clone the repository and build the container:

```
$ git clone https://github.com/dmazzer/nors-server.git
$ cd nors-server/docker
$ docker build --no-cache --rm -t nors-server .
```

Run the container:

This command will start the server for the first time and will map the container port 9270 to host port 9270:

```
$ docker run --rm -ti --name=nors-server -p 9270:9270 nors-server
```

After the first time the container named as nors-server was used, it can be started as a daemon with the command:

```
$ docker run -ti -d -p 9270:9270 nors-server
```

It is possible to run the container linked with the nors-mongodb container:

```
$ docker run -ti --rm -p 9270:9270 --link nors-mongodb --name nors-server nors-server
```
