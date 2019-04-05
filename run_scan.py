#!/usr/bin/python
from __future__ import print_function

import os, sys, time
from lxml import etree
import subprocess

configs = [
    "8715c877-47a0-438d-98a3-27c7a6ab2196", #  Discovery
    "085569ce-73ed-11df-83c3-002264764cea", #  empty
    "daba56c8-73ec-11df-a475-002264764cea", #  Full and fast
    "698f691e-7489-11df-9d8c-002264764cea", #  Full and fast ultimate
    "708f25c4-7489-11df-8094-002264764cea", #  Full and very deep
    "74db13d6-7489-11df-91b9-002264764cea", #  Full and very deep ultimate
    "2d3f051c-55ba-11e3-bf43-406186ea4fc5", #  Host Discovery
    "bbca7412-a950-11e3-9109-406186ea4fc5" ] #  System Discovery

if len(sys.argv) < 3:
    sys.exit('Usage: %s <scan target> <output file>' % sys.argv[0])

print('Starting OpenVAS')

os.system('BUILD=true /start')

print('Starting scan')

omp_logon = "-u admin -w admin -h 127.0.0.1 -p 9390"

create_target = "omp {0} --xml '<create_target><name>{1}</name><hosts>{1}</hosts></create_target>'".format(omp_logon, sys.argv[1])
create_target_response = subprocess.check_output(create_target, stderr=subprocess.STDOUT, shell=True)
print(create_target_response)
target_id = etree.XML(create_target_response).xpath("//create_target_response")[0].get("id")
print("target_id: {}".format(target_id))

create_task = ("omp {} -C --target={} --config={} --name=scan").format(omp_logon, target_id, configs[2])
task_id = subprocess.check_output(create_task, stderr=subprocess.STDOUT, shell=True).strip()
print("task_id: {}".format(task_id))

start_task = "omp {} -S {}".format(omp_logon, task_id)
start_task_response = subprocess.check_output(start_task, stderr=subprocess.STDOUT, shell=True)
print("start_task: {}".format(start_task_response))

print("Waiting for task to finish")

status = ""
get_status = "omp {} --xml '<get_tasks task_id=\"{}\"/>'".format(omp_logon, task_id)

while status != "Done":
	try:
		time.sleep(2)
		get_status_response = subprocess.check_output(get_status, stderr=subprocess.STDOUT, shell=True)
		status = etree.XML(get_status_response).xpath("//status")[0].text
		progress = etree.XML(get_status_response).xpath("//progress")[0].text
		print("Status: {} {}%".format(status, progress))
	except subprocess.CalledProcessError as exc:
		print("Error: ", exc.output) 

openvaslog = open("/var/log/openvas/openvassd.messages", "r").read()
print("openvassd.messages: {}".format(openvaslog))
report_id = etree.XML(get_status_response).xpath("//report")[0].get("id")
print("report_id: {}".format(report_id))

report_formats = [("html", "6c248850-1f62-11e1-b082-406186ea4fc5"), ("xml", "a994b278-1f62-11e1-96ac-406186ea4fc5")]
for report_format, report_format_id in report_formats:
    get_report = "omp {} -R {} -f {}".format(omp_logon, report_id, report_format_id)
    report_response = subprocess.check_output(get_report, stderr=subprocess.STDOUT, shell=True)
    print("{}-report: {}...".format(report_format.upper(), report_response[:30]))

    report_filename = os.path.split(sys.argv[2])[1]
    if report_filename.ensdwith(".html"):
        report_filename = report_filename[:-len(".html")]
    export_path = "/openvas/results/{}.{}".format(report_filename, report_format)
    print('Writing {}-report to {}'.format(report_format.upper(), export_path))

    f = open(export_path, 'w')
    f.write(report_response)
    f.close()

print('Done!')
