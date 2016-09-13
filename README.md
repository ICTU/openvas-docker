OpenVAS image for Docker
==============

A Docker container for OpenVAS 8 on the Ubuntu 14.04 image.  By default, the latest images includes the OpenVAS Base as well as the NVTs and Certs required to run OpenVAS.

This project is a clone of https://github.com/mikesplain/openvas-docker with an added custom script script.

The Dockerfile is published at: https://hub.docker.com/r/ictu/openvas-docker

Requirements
------------
Docker
Ports available: 443, 9390, 9391

Usage
-----

Simply run:

```
docker build -t openvas openvas-docker
docker run openvas /openvas/run_scan.py <target> <target file>
```

This will build the container and start it up.  Openvas startup can take some time (4-5 minutes while NVT's are scanned and databases rebuilt), so be patient. After that, the scan script will be run.

In the output, look for the process scanning data.  It contains a percentage.

Config
------
By default GSAD will run on 443 with self signed certs.  If you would like to run
this on 80 without certs you can pass the following param and change the port in
docker run from 443 to 80

```
docker run -d -p 80:80 -p 9390:9390 -p 9391:9391 -e HTTP_ONLY=true  --name openvas openvas
```

Thanks
------
Thanks to Mike Splain for creating the original OpenVAS docker
