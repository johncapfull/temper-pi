import time
import datetime
import urllib2
import httplib

import config

def query():
    temperatures = {}

    for name, sensor in config.temperature["sensors"].iteritems():

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

def send():
    time = datetime.datetime.now().isoformat('T')
    celsius = query()[0]

    request = (
	config.temperature["add_url"] + 
	"?time=" + time + 
	"&celsius=" + str(celsius)
    )

#   print request

    try:
        r = urllib2.urlopen(request)
    except urllib2.HTTPError, err:
        print "HTTPError: " + str(err.code)
    except httplib.BadStatusLine, err:
        print "BadStatusLine error!"

#    print r.getcode()

#while True:
#    send()