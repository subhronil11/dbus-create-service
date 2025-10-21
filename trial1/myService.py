#!/usr/bin/env python3
import gobject
import sys, os, time
from gi.repository import GLib
from vedbus import VeDbusService
from ve_utils import wrap_dbus_value  # already used by VeDbusService internally

def main():
    # 1) Create service on the system bus
    svc = VeDbusService('com.victronenergy.custom.myservice')

    # 2) Mandatory/standard-ish paths (good practice)
    svc.add_path('/DeviceInstance', 0)                   # choose a unique instance per class
    svc.add_path('/ProductName', 'Custom Service Demo')
    svc.add_path('/Mgmt/ProcessName', os.path.basename(__file__))
    svc.add_path('/Mgmt/ProcessVersion', 'v0.1')
    svc.add_path('/Connected', 1)

    # 3) Your own data paths
    svc.add_path('/Sensors/Temp/C', 22.5)                # number
    svc.add_path('/Status/Text', 'OK')                   # string
    svc.add_path('/Status/Code', 0)                      # int status code

    # 4) Update something periodically
    def tick():
        t = svc['/Sensors/Temp/C'] + 0.1
        svc['/Sensors/Temp/C'] = round(t, 1)
        return True  # reschedule

    GLib.timeout_add(1000, tick)  # every second
    GLib.MainLoop().run()

if __name__ == '__main__':
    main()
