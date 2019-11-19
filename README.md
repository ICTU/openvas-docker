OpenVAS Docker with automated CLI scan script
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

Or with SSH authentication to perform an authenticated scan: (also possible with -k 'private key')

```
docker pull ictu/openvas-docker
docker run --rm -v $(pwd):/openvas/results/ ictu/openvas-docker /openvas/run_scan.py 123.123.123.123 openvas_scan_report -u root -p password
```

This will startup the container and update the NVTs. It can take some time (4-5 minutes while NVT's are scanned and databases rebuilt), so be patient. After that, the scan script will run and the progress is displayed. When ready, the script writes both an HTML and XML version of the report.

Getting OpenVAS configurations
-----

All scan configurations:

```
omp -u admin -w admin -g
8715c877-47a0-438d-98a3-27c7a6ab2196  Discovery
085569ce-73ed-11df-83c3-002264764cea  empty
daba56c8-73ec-11df-a475-002264764cea  Full and fast
698f691e-7489-11df-9d8c-002264764cea  Full and fast ultimate
708f25c4-7489-11df-8094-002264764cea  Full and very deep
74db13d6-7489-11df-91b9-002264764cea  Full and very deep ultimate
2d3f051c-55ba-11e3-bf43-406186ea4fc5  Host Discovery
bbca7412-a950-11e3-9109-406186ea4fc5  System Discovery
```

All reporting configurations:

```
omp -u admin -w admin -F
5057e5cc-b825-11e4-9d0e-28d24461215b  Anonymous XML
910200ca-dc05-11e1-954f-406186ea4fc5  ARF
5ceff8ba-1f62-11e1-ab9f-406186ea4fc5  CPE
9087b18c-626c-11e3-8892-406186ea4fc5  CSV Hosts
c1645568-627a-11e3-a660-406186ea4fc5  CSV Results
6c248850-1f62-11e1-b082-406186ea4fc5  HTML
77bd6c4a-1f62-11e1-abf0-406186ea4fc5  ITG
a684c02c-b531-11e1-bdc2-406186ea4fc5  LaTeX
9ca6fe72-1f62-11e1-9e7c-406186ea4fc5  NBE
c402cc3e-b531-11e1-9163-406186ea4fc5  PDF
9e5e5deb-879e-4ecc-8be6-a71cd0875cdd  Topology SVG
a3810a62-1f62-11e1-9219-406186ea4fc5  TXT
c15ad349-bd8d-457a-880a-c7056532ee15  Verinice ISM
50c9950a-f326-11e4-800c-28d24461215b  Verinice ITG
a994b278-1f62-11e1-96ac-406186ea4fc5  XML
```

Thanks
------
Thanks to Mike Splain for creating the original OpenVAS docker image.
