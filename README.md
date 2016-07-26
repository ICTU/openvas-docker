OpenVAS image for Docker
==============

A Docker container for OpenVAS 8 on the Ubuntu 14.04 image.  By default, the latest images includes the OpenVAS Base as well as the NVTs and Certs required to run OpenVAS.

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

In the output, look for the process scanning cert data.  It contains a percentage.

To run bash inside the container run:

```
docker exec -it openvas bash
```

Config
------
By default GSAD will run on 443 with self signed certs.  If you would like to run
this on 80 without certs you can pass the following param and change the port in
docker run from 443 to 80

```
docker run -d -p 80:80 -p 9390:9390 -p 9391:9391 -e HTTP_ONLY=true  --name openvas mikesplain/openvas
```

Contributing
------------

I'm always happy to accept [pull requests](https://github.com/mikesplain/openvas-docker/pulls) or [issues](https://github.com/mikesplain/openvas-docker/issues).

Thanks
------
Thanks to hackertarget for the great tutorial: http://hackertarget.com/install-openvas-7-ubuntu/
Thanks to Serge Katzmann for contributing with some great work on OpenVAS 8: https://github.com/sergekatzmann/openvas8-complete
