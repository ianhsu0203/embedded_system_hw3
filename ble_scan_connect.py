from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate

import sys
import select
import time

def enable_notifications(peripheral, char_uuid, cccd_uuid):
    ch = peripheral.getCharacteristics(uuid=UUID(char_uuid))[0]
    if ch.supportsRead():
        val = ch.read()
        print(f"Characteristic {char_uuid} value: {val}")

    cccd = ch.getDescriptors(forUUID=UUID(cccd_uuid))[0]
    write_value = bytes([0x02, 0x00])
    cccd.write(write_value, withResponse=True)
    print(f"Enabled notifications for {char_uuid} with value: {write_value.hex()}")
    
class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("Received notification from handle", cHandle, "with data", data)


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n=0
addr = []
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr,
dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print (" %s = %s" % (desc, value))
number = input('Enter your device number: ')
print ('Device', number)
num = int(number)
print (addr[num])


#
print ("Connecting...")
dev = Peripheral(addr[num], 'random')
dev.withDelegate(MyDelegate())

print ("Services...")
for svc in dev.services:
    print (str(svc))
#

print("Press 'q' to quit...")

try:
    testService = dev.getServiceByUUID(UUID('D90BB629-423A-4BB2-87A6-CC0C3C9853B3'))
    for ch in testService.getCharacteristics():
        print(str(ch))

    char_uuid = '34711F5C-6739-4C6F-8F28-096E858542A4'  # 这是特征的UUID
    cccd_uuid = '00002902-0000-1000-8000-00805f9b34fb'  # 这是CCCD的UUID

    enable_notifications(dev, char_uuid, cccd_uuid)

    while True:
        if dev.waitForNotifications(1.0):
            # handleNotification() was called
            continue
        print("Waiting for notifications...")
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if line.strip().lower() == 'q':
                break
        time.sleep(0.1)

    ch = dev.getCharacteristics(uuid=UUID('34711F5C-6739-4C6F-8F28-096E858542A4'))[0]
    if (ch.supportsRead()):
        print (ch.read())
#
except Exception as e:
    print(f"An error occurred: {e}")


finally:
    print("Disconnecting...")
    dev.disconnect()
