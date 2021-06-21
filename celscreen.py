#!/usr/bin/env python3

import sys
import os

phoneid = sys.argv[1]
file = sys.argv[2]

os.system("adb -s {} wait-for-device && adb -s {} shell screencap -p /sdcard/{}".format(phoneid, phoneid, file))
os.system("adb -s {} wait-for-device && adb -s {} pull /sdcard/{} 1>/dev/null 2>/dev/null".format(phoneid, phoneid, file))
os.system("adb -s {} wait-for-device && adb -s {} shell rm /sdcard/{}".format(phoneid, phoneid, file));
