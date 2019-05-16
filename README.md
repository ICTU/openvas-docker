OpenVAS Docker image with automatic scan script
==============

A Docker container for OpenVAS 9. This project is a clone of https://github.com/mikesplain/openvas-docker with an additional Python script to automatically start a scan. The Dockerfile is published at: https://hub.docker.com/r/ictu/openvas-docker

Requirements
------------
Docker

Usage
-----

Simply run:

```
docker pull ictu/openvas-docker
docker run --rm -v $(pwd):/openvas/results/ ictu/openvas-docker /openvas/run_scan.py 123.123.123.123,www.github.com openvas_scan_report
```

This will startup the container and update the NVTs. It can take some time (4-5 minutes while NVT's are scanned and databases rebuilt), so be patient. After that, the scan script will run and the progress is displayed. When ready, the script writes both an HTML and XML version of the report.


Thanks
------
Thanks to Mike Splain for creating the original OpenVAS docker image.
