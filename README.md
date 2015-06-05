# Splunk_Add-on_MongoDB
This Splunk add-on for MongoDB is used to fetch data from MongoDB database and send data to Splunk. This is a quick solution to analyze MongoDB database in splunk. pymongo module is used here.

How to Install
===============
Install PyMongo module https://pypi.python.org/pypi/pymongo/.

Install this add-on in your splunk forwarder. Write details of your MongoDB in file config.json

"server":"server_name", 

 "port":"27017", 
 
  "database" : "database_name",
  
 "collection" : "collection_name",
 
 "user": "user_name",
 
 "password" : "passwd"


Setup
================
Run script setup.py, this script setup your configuration.

Other Information
=================
* You need to change timestamp format if it is diffrent than timestamp format in mongodb_script.py
* Currently it supports single database and collection in MongoDB
* It supports Python 2.* version
