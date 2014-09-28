#!/usr/bin/env python

from pprint import pprint

import sys
import time
import datetime
import urllib2
import httplib

import json
import requests

import config

import config
from daemon import daemon_main

def query():
    temperatures = {}

    for name, sensor in config.temper["sensors"].iteritems():

        text = '';
        while text.split("\n")[0].find("YES") == -1:
            tfile = open("/sys/bus/w1/devices/"+ sensor +"/w1_slave")
            text = tfile.read()
            tfile.close()

        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:]) / 1000

        temperatures[name] = temperature

    return temperatures

# accept input of query and unix time
def format(values, time):
    request = {}
    request["time"] = int(time)
    request["sensors"] = values

    return json.dumps(request)

def send():
    payload = format(query(), time.time())

    url = config.temper["add_url"]
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=payload, headers=headers)

    if r.status_code != requests.codes.ok:
        print(time.ctime())
        print("Error: server responded " + str(r.status_code))
        print(r.text)

def main():
    print(time.ctime() + " Started")
    while True:
        send()
        time.sleep(60)

if __name__ == '__main__':
    daemon_main(main, config.temper["pidfile"], config.temper["logfile"])
