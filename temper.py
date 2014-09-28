#!/usr/bin/env python

import sys, time
import json
from daemon import daemon_main
from pprint import pprint

import config
import temperature

def main():
    print config.temperature["add_url"]
    pprint(temperature.query())

if __name__ == '__main__':
    daemon_main('/tmp/temper-pi.pid', main)
