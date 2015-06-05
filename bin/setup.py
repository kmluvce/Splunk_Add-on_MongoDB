#!/usr/bin/python

import json
import os

config = open(os.environ['SPLUNK_HOME'] + 'etc/apps/MongoDB_Splunk_app/bin/config.json').read()
data = json.loads(config)

file = open(os.environ['SPLUNK_HOME'] + '/etc/apps/MongoDB_Splunk_app/default/inputs.conf','w')

file.write('[monitor://' + os.environ['SPLUNK_HOME'] + '/etc/apps/MongoDB_Splunk_app/bin/mongodb_script.py]\n')
file.write("index = mongodb\n")
file.write("sourcetype = "+  data["collection"] + "\n")
file.write("source = " + data["database"] +"\n")

