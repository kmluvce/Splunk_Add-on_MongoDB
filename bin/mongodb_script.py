#!/usr/bin/python

import pymongo
import re
import json
import os
import sys
import datetime
import time
from bson.objectid import ObjectId


last_id = 0
config_file = '/etc/apps/MongoDB_Splunk_app/bin/config.json'

def get_config(config_file_name):
    config = open(os.environ['SPLUNK_HOME'] + config_file_name).read()
    data = json.loads(config)
    database=data["database"]
    collection = data["collection"]
    return (data)

def check_file(config_file_name):
    last_id_filepath = os.environ['SPLUNK_HOME'] + "/etc/apps/MongoDB_Splunk_app/bin/last_id" # user supplies correct path

# Open file containing the last ID and get the last record read
    if os.path.isfile(last_id_filepath):
        try:
            last_id_file = open(last_id_filepath,'r')
            last_id = int(last_id_file.readline())
            last_id_file.close()
            return (last_id,last_id_filepath)
    # Catch the exception. Real exception handler would be more robust    
        except IOError:
            sys.stderr.write('Error: failed to read last_eventid file, ' + last_id_filepath + '\n')
            sys.exit(2)
    else:
        sys.stderr.write('Error: ' + last_id_filepath + ' file not found! Starting from zero. \n')

def connect(data,last_id,last_id_filepath):
    try:
        client = pymongo.MongoClient('mongodb://' + data["server"] + ":" + data["port"] + "/")
        max_id=[]
        this_last_id = 0
        database=data["database"]
        collection = data["collection"]
        db = client[database]
        db.authenticate(data["user"], data["password"], mechanism='MONGODB-CR')
        db_data = db[collection]
        gen_time = datetime.datetime.fromtimestamp(last_id)
        dummy_id = ObjectId.from_datetime(gen_time)
        result = db_data.find()
        pattern = "%Y-%m-%d %H:%M:%S"
        for line in result:
            date_time = line['_id'].generation_time
            date_time = date_time.strftime("%Y-%m-%d %H:%M:%S") 
            id = int(time.mktime(time.strptime(date_time, pattern)))
            if id > last_id:
               max_id.append(id)
               print line
               this_last_id = 1
        if this_last_id == 1:
            update_id(max(max_id),last_id_filepath)
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e

def update_id(this_last_id,last_id_filepath):
    if this_last_id > 0:
        try:
            last_id_file = open(last_id_filepath,'w')
            last_id_file.write(str(this_last_id))
            last_id_file.close()
   # Catch the exception. Real exception handler would be more robust    
        except IOError:
            sys.stderr.write('Error writing last_eventid to file: ' + last_id_filepath + '\n')
            sys.exit(2)

if __name__ == '__main__':
    data = get_config(config_file)
    (last_id, last_id_filepath)=  check_file(config_file)
    connect(data,last_id,last_id_filepath)
