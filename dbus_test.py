#!/usr/bin/env python

import time
import dbus
import xml.etree.ElementTree as ET
import subprocess as sp


def timer(func):
    def time_wrapper():
        print(f'function: {func.__name__}')
        t1 = time.time()
        result = func()
        t2 = time.time()
        elapsed_time = t2 - t1
        print(f"elapsed time: {elapsed_time:.6f} seconds")
        return elapsed_time, result
    return time_wrapper


@timer
def dbus_kdeconnect():
    # get session bus
    session_bus = dbus.SessionBus()
    try:
        # get device ids
        devices_dbus_obj = session_bus.get_object('org.kde.kdeconnect','/modules/kdeconnect/devices')
        devices_xml = devices_dbus_obj.Introspect(dbus_interface='org.freedesktop.DBus.Introspectable')
        devices_xml = ET.fromstring(devices_xml)
        nodes = devices_xml.findall('node')
        deviceIDs = list()
    except dbus.exceptions.DBusException as e:
        print(f'dbus.exceptions.DBusException: {e}')
        pass
    for node in nodes:
        deviceIDs.append(node.get('name'))

    # get device names
    deviceID_Names = dict()
    for ID in deviceIDs:
        device = session_bus.get_object('org.kde.kdeconnect', '/modules/kdeconnect/devices/' + ID)
        deviceName = device.GetAll('', dbus_interface='org.freedesktop.DBus.Properties')['name']
        deviceID_Names[ID] = str(deviceName)

    return deviceID_Names


@timer
def cli_kdeconnect():
    devices = sp.run(['kdeconnect-cli','-l','--id-name-only'],stdout=sp.PIPE)
    return_code = devices.returncode
    if(return_code is not 0):
        print(f'Not found kdeconnect-cli, return code: {return_code}')
    devices = str(devices.stdout).splitlines()
    deviceID_Names = dict()
    for device in devices:
        if('0 devices' in device):
            print('Devices found not.')
    for device in devices:
        device = device.strip('b\'\\n').split(' ', 1)
        deviceID_Names[device[0]] = device[1]

    return deviceID_Names


if __name__ == '__main__':
    elapsed1, output1 = dbus_kdeconnect()
    print(f'output: {output1}\n')
    elapsed2, output2 = cli_kdeconnect()
    print(f'output: {output2}\n') 
    speedup = (elapsed2/elapsed1)
    print(f'speedup: {speedup:.3f}, {speedup*100:.0f}%')


# send a message
# aPhoneNumber = '1234567890'
# sendMessage = session_bus.get_object('org.kde.kdeconnect', '/modules/kdeconnect/devices/' + deviceID + '/sms')
# sendMessage.sendSms(aPhoneNumber, 'testmessage', dbus_interface='org.kde.kdeconnect.device.sms')
