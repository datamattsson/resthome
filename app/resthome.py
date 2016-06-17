#!/usr/bin/env python

#
# resthome.py - Retrieves your SmartThings sensor metrics and inserts them into
#               an InfluxDB database for lush visualization with Grafana
#
# Copyright (c) 2016, Michael Mattsson
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#         * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
from time import (sleep, time)
from datetime import datetime
from os import environ
from smartthings import SmartThings
from influxdb import InfluxDBClient
from sys import stderr

class ReSTHome(SmartThings):

    def __init__(self):

        self.influxhost = environ.get('INFLUX_NODENAME', 'localhost')
        self.influxdb = environ.get('INFLUX_DB', 'resthomedb')
        self.influxport = environ.get('INFLUX_PORT', 8086)
        self.influxuser = environ.get('INFLUX_USERNAME', 'root')
        self.influxpass = environ.get('INFLUX_PASSWORD', 'root')
        self.poll_interval = environ.get('IOTDB_POLL_INTERVAL', 900)
        self.device_exclusion = environ.get('IOTDB_DEVICE_EXCLUSION', 
                '').split(',')
        self.retry_intervals = environ.get('IOTDB_RETRY_INTERVAL', 60)
        self.verbose = False

# main
rh = ReSTHome()

try:
    rh.load_settings()
except IOError as e:
    stderr.write("Error accessing smarthings.json (%s)\n" % str(e))
except (AttributeError, ValueError) as e:
    stderr.write("Error parsing JSON (%s)\n" % str(e))
except:
    stderr.write("Unknown error parsing smarthings.json\n")
    raise

while True:

    timer = time()
    
    try:
        rh.request_endpoints()
    except:
        stderr.write("Unable to connect or parse endpoints, will retry in %ss\n" % 
                rh.retry_intervals)
        sleep(rh.retry_intervals)
        continue 
    
    try:
        client = InfluxDBClient(rh.influxhost, rh.influxport, rh.influxuser,
                rh.influxpass, rh.influxdb)
    except:
        stderr.write("Unable to connect to InfluxDB\n")
        continue

    payload = [] 

    for sensor in rh.device_types():
        if not sensor in rh.device_exclusion:
            try:
                ds = rh.request_devices(sensor)
            except:
                stderr.write("Unable to connect/retreive your %s device(s)\n" %
                        sensor)
                continue

            if(ds):
                for dev in ds:
                    item = {}
                    key = "%s.%s.%s" % (dev['hub'], dev['label'], sensor)
                    key = key.lower()
                    key = key.replace(' ', '_')

                    item['measurement'] = key
                    item['tags'] = { 'label': dev['label'] }
                    item['tags']['type'] = dev['type']
                    item['tags']['hub'] = dev['hub']
                    item['time'] = "%sZ" % datetime.isoformat(datetime.utcnow())
                    item['fields'] = { 'value': dev['value'][sensor] }

                    payload.append(item)

    try:
        client.write_points(payload)
    except:
        stderr.write("Unable to write data series to InfluxDB\n")
        pass

    timer = time() - timer

    if timer < rh.poll_interval:
        sleep(rh.poll_interval - timer)
