#!/usr/bin/python
from __future__ import print_function

import base64, os, sys, time
import xml.etree.ElementTree as ET
import shutil

from functools import partial
from openvas_lib import VulnscanManager, VulnscanException
from threading import Semaphore

HOST = "localhost"
USER = "admin"
PASSWORD = "openvas"
BASEPATH = '/openvas/'

def print_status(i):
    print(str(i))


if len(sys.argv) < 3:
    sys.exit('Usage: %s <scan target> <output file>' % sys.argv[0])

os.system(BASEPATH + 'start.sh')

print('Starting scan')

try:
    scanner = VulnscanManager(HOST, USER, PASSWORD)
except VulnscanException as e:
    print("Error:")
    print(e)
    sys.exit(0)

sem = Semaphore(0)
scan_id, target_id = scanner.launch_scan(target = sys.argv[1],
        profile = "Full and fast",
        callback_end = partial(lambda x: x.release(), sem),
        callback_progress = print_status)

sem.acquire()
time.sleep(1)

report_id = scanner.get_report_id(scan_id)
report = scanner.get_report_html(report_id).find("report")

htmlb64 = report.find("report_format").tail

export_path = BASEPATH + 'results/' + os.path.split(sys.argv[2])[1]
print('Writing HTML report to ' + export_path)

f = open(export_path, 'w')
f.write(base64.b64decode(htmlb64))
f.close()

shutil.copy(BASEPATH + 'style.css', BASEPATH + 'results/style.css')

scanner.delete_scan(scan_id)
scanner.delete_target(target_id)

