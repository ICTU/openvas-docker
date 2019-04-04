OpenVAS Docker image with custom script
==============

A Docker container for OpenVAS 9 on the Ubuntu 16.04 image. This project is a clone of https://github.com/mikesplain/openvas-docker with an added custom python script. The Dockerfile is published at: https://hub.docker.com/r/ictu/openvas-docker

Requirements
------------
Docker
Ports available: 443, 9390, 9391

Usage
-----

Simply run:

```
docker pull ictu/openvas-docker
docker run --rm -v $(pwd):/openvas/results/:rw ictu/openvas-docker /openvas/run_scan.py <target> openvas_scan_report
```

This will startup the container and update the NVTs. It can take some time (4-5 minutes while NVT's are scanned and databases rebuilt), so be patient. After that, the scan script will run and the progress is displayed. When ready, the script writes both an HTML and XML version of the report.


Thanks
------
Thanks to Mike Splain for creating the original OpenVAS docker image.
