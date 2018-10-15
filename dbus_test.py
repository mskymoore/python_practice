#!/usr/bin/env python

import time

t1 = time.time()
import dbus
import xml.etree.ElementTree as ET

#get session bus
session_bus = dbus.SessionBus()

#get device ids
devices_dbus_obj = session_bus.get_object('org.kde.kdeconnect','/modules/kdeconnect/devices')
devices_xml = devices_dbus_obj.Introspect(dbus_interface='org.freedesktop.DBus.Introspectable')
devices_xml = ET.fromstring(devices_xml)
nodes = devices_xml.findall('node')
deviceIDs = list()
for node in nodes:
    deviceIDs.append(node.get('name'))

#get device names
deviceID_Names = dict()
for ID in deviceIDs:
    device = session_bus.get_object('org.kde.kdeconnect', '/modules/kdeconnect/devices/' + ID)
    deviceName = device.GetAll('', dbus_interface='org.freedesktop.DBus.Properties')['name']
    deviceID_Names[str(deviceName)] = ID

print(deviceID_Names)
t2 = time.time()
elapsed1 = t2 - t1

#TODO: make a decorator, put these in functions, and time them that way.
t1 = time.time()
import subprocess as sp

devices = sp.run(['kdeconnect-cli','-l','--id-name-only'],stdout=sp.PIPE)
return_code = devices.returncode
if(return_code is not 0):
    print('Not found kdeconnect-cli, return code: ' + str(return_code))
devices = str(devices.stdout).splitlines()
device_id_name_pairs = dict()
for device in devices:
    if('0 devices' in device):
        print('Devices found not.')
for device in devices:
    device = device.strip('b\'\\n').split(' ', 1)
    device_id_name_pairs[device[1]] = device[0]

print(device_id_name_pairs)
t2 = time.time()
elapsed2 = t2 - t1

speedup = (elapsed2/elapsed1)
print('dumb way time elapsed: ' + str(elapsed2))
print('dbus way time elapsed: ' + str(elapsed1))
print('speedup: ' + str(speedup))
print('speedup percent: ' + str(speedup * 100) + '%')


#send a message
#aPhoneNumber = '1234567890'
#sendMessage = session_bus.get_object('org.kde.kdeconnect', '/modules/kdeconnect/devices/' + deviceID + '/sms')
#sendMessage.sendSms(aPhoneNumber, 'testmessage', dbus_interface='org.kde.kdeconnect.device.sms')
