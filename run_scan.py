#!/usr/bin/python
from __future__ import print_function

import os, sys, time, random
import subprocess
import optparse
from lxml import etree
from datetime import datetime

parser = optparse.OptionParser()

parser.add_option('-u', '--username',
    action="store", dest="ssh_username",
    help="SSH Username", default="")

parser.add_option('-p', '--password',
    action="store", dest="ssh_password",
    help="SSH Password", default="")

parser.add_option('-k', '--key',
    action="store", dest="ssh_key",
    help="SSH Private Key", default="")

parser.add_option('-v', '--verbose',
    action="store_true", dest="verbose",
    help="Print verbose log", default=False)

options, args = parser.parse_args()

if len(sys.argv) < 3:
    sys.exit('Usage: %s <scan targets> <output file>\r\nUse -h or --help to view options' % sys.argv[0])

hosts = args[0]
outputfile = args[1]

#omp -u admin -w admin -g
#8715c877-47a0-438d-98a3-27c7a6ab2196  Discovery
#085569ce-73ed-11df-83c3-002264764cea  empty
#daba56c8-73ec-11df-a475-002264764cea  Full and fast
#698f691e-7489-11df-9d8c-002264764cea  Full and fast ultimate
#708f25c4-7489-11df-8094-002264764cea  Full and very deep
#74db13d6-7489-11df-91b9-002264764cea  Full and very deep ultimate
#2d3f051c-55ba-11e3-bf43-406186ea4fc5  Host Discovery
#bbca7412-a950-11e3-9109-406186ea4fc5  System Discovery

config_id = "daba56c8-73ec-11df-a475-002264764cea" #  Full and fast

print('Starting OpenVAS')

os.system('BUILD=true /start')

print('Starting scan')

omp_logon = "omp -u admin -w admin -h 127.0.0.1 -p 9390"
create_target_sshcredential = ""

if options.ssh_username:
	if options.ssh_password:
		creds_key = "<password>{}</password>".format(options.ssh_password)
	elif options.ssh_key:
		creds_key = "<key><private>{}</private></key>".format(options.ssh_key)
	else:
		print("No SSH Password or Private Key provided.")
		exit()

	create_credential = "{} --xml '<create_credential><name>Credentials-{}</name><login>{}</login>{}</create_credential>'".format(omp_logon, random.randint(1,101), options.ssh_username, creds_key)
	create_credential_response = subprocess.check_output(create_credential, stderr=subprocess.STDOUT, shell=True)
	credential_id = etree.XML(create_credential_response).xpath("//create_credential_response")[0].get("id")
	print("credential_id: {}".format(credential_id))
	create_target_sshcredential = "<ssh_credential id=\"{}\"><port>22</port></ssh_credential>".format(credential_id)

create_target = "{0} --xml '<create_target><name>{1}-{2}</name><hosts>{1}</hosts>{3}</create_target>'".format(omp_logon, hosts, random.randint(1,101), create_target_sshcredential)
create_target_response = subprocess.check_output(create_target, stderr=subprocess.STDOUT, shell=True)
target_id = etree.XML(create_target_response).xpath("//create_target_response")[0].get("id")
print("target_id: {}".format(target_id))

create_task = "{} -C --target={} --config={} --name=scan".format(omp_logon, target_id, config_id)
task_id = subprocess.check_output(create_task, stderr=subprocess.STDOUT, shell=True).strip()
print("task_id: {}".format(task_id))

start_task = "{} -S {}".format(omp_logon, task_id)
start_task_response = subprocess.check_output(start_task, stderr=subprocess.STDOUT, shell=True)
print("start_task: {}".format(start_task_response))

print("Waiting for task to finish")

status = ""
get_status = "{} --xml '<get_tasks task_id=\"{}\"/>'".format(omp_logon, task_id)

while status != "Done":
	try:
		time.sleep(5)
		get_status_response = subprocess.check_output(get_status, stderr=subprocess.STDOUT, shell=True)
		status = etree.XML(get_status_response).xpath("//status")[0].text
		progress = etree.XML(get_status_response).xpath("//progress")[0].text
		current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		sys.stdout.write("\x1b[2K") # Erase line
		sys.stdout.write("[{}] Progress: {} {}%\r".format(current_time, status, progress))
		sys.stdout.flush()
	except subprocess.CalledProcessError as exc:
		print("\nError: {}".format(exc.output))

if options.verbose:
    openvaslog = open("/var/log/openvas/openvassd.messages", "r").read()
    print("openvassd.messages: {}".format(openvaslog))
    
report_id = etree.XML(get_status_response).xpath("//report")[0].get("id")
print("report_id: {}".format(report_id))

#omp -u admin -w admin -F
#5057e5cc-b825-11e4-9d0e-28d24461215b  Anonymous XML
#910200ca-dc05-11e1-954f-406186ea4fc5  ARF
#5ceff8ba-1f62-11e1-ab9f-406186ea4fc5  CPE
#9087b18c-626c-11e3-8892-406186ea4fc5  CSV Hosts
#c1645568-627a-11e3-a660-406186ea4fc5  CSV Results
#6c248850-1f62-11e1-b082-406186ea4fc5  HTML
#77bd6c4a-1f62-11e1-abf0-406186ea4fc5  ITG
#a684c02c-b531-11e1-bdc2-406186ea4fc5  LaTeX
#9ca6fe72-1f62-11e1-9e7c-406186ea4fc5  NBE
#c402cc3e-b531-11e1-9163-406186ea4fc5  PDF
#9e5e5deb-879e-4ecc-8be6-a71cd0875cdd  Topology SVG
#a3810a62-1f62-11e1-9219-406186ea4fc5  TXT
#c15ad349-bd8d-457a-880a-c7056532ee15  Verinice ISM
#50c9950a-f326-11e4-800c-28d24461215b  Verinice ITG
#a994b278-1f62-11e1-96ac-406186ea4fc5  XML

report_formats = [("html", "6c248850-1f62-11e1-b082-406186ea4fc5"), ("xml", "a994b278-1f62-11e1-96ac-406186ea4fc5")]

for report_format, report_format_id in report_formats:
    get_report = "{} -R {} -f {}".format(omp_logon, report_id, report_format_id)
    report_response = subprocess.check_output(get_report, stderr=subprocess.STDOUT, shell=True)
    print("{}-report: {}...".format(report_format.upper(), report_response[:30]))

    report_filename = os.path.split(outputfile)[1]
    if report_filename.endswith(".html"):
        report_filename = report_filename[:-len(".html")]
    export_path = "/openvas/results/{}.{}".format(report_filename, report_format)
    print('Writing {}-report to {}'.format(report_format.upper(), export_path))

    f = open(export_path, 'w')
    f.write(report_response)
    f.close()

print('Done!')
