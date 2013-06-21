#!/usr/bin/env python

import xml.etree.cElementTree as ET
import urllib2
import requests  #if you don't have this, install with 'sudo easy_install requests'
import datetime, time

# this is the api URL for Dallas weather.  Adjust for your city.
url = 'http://api.openweathermap.org/data/2.5/weather?q=Dallas&units=imperial&mode=xml'

request = urllib2.urlopen(url)

tree = ET.parse(request)
root = tree.getroot()

# The function below is based on this:
#     print root.find('temperature').attrib['value']
# It is used to pull weather data from the openweathermap api.
def getElement(element):
    return root.find(element).attrib['value']

# load variables from openweathermap api
temp = getElement(element = 'temperature');
humid = getElement(element = 'humidity');
pressure = getElement(element = 'pressure');

# get epoch time in ms
timestamp = int(time.mktime(datetime.datetime.now().timetuple()) * 1000)

# form the POST for vCOPs ingestion
postinfo = """Dallas,HttpPost,City,,WXDallas,5,
Weather|Temperature|Temperature in Fahrenheit,3,NoValue,""" + str(timestamp) + """,""" + str(temp) + """,
Weather|Humidity|Humidity in percent,3,NoValue,""" + str(timestamp) + """,""" + str(humid) + """,
Weather|Air Pressure|Pressure in hPA,3,NoValue,""" + str(timestamp) + """,""" + str(pressure) + ""","""

#upload to vCOPs
def SendToVCOPS():
    vcopsurl = 'https://vcops:443/HttpPostAdapter/OpenAPIServlet'
    requests.post(vcopsurl, data=postinfo, verify=False, auth=('admin', 'password')) 

SendToVCOPS()
