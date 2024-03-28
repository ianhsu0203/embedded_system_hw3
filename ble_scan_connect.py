from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate

import sys
import select
import time

def enable_notifications(peripheral, char_uuid, cccd_uuid):
    try:
        # 获取特征对象
        ch = peripheral.getCharacteristics(uuid=UUID(char_uuid))[0]
        print(f"Found characteristic {char_uuid}")

        # 尝试读取当前特征的值（如果支持）
        if ch.supportsRead():
            current_value = ch.read()
            print(f"Current value of characteristic {char_uuid}: {current_value}")

        # 查找CCCD
        cccd = ch.getDescriptors(forUUID=UUID(cccd_uuid))[0]
        print(f"Found CCCD descriptor for characteristic {char_uuid}")

        # 准备写入的值，这里是启用通知的标准值0x0001或0x0002（这里用0x0002代表通知）
        notification_enable_value = bytes([0x02, 0x00])
        print(f"Preparing to write to CCCD to enable notifications: {notification_enable_value}")

        # 执行写入操作
        cccd.write(notification_enable_value, withResponse=True)
        print(f"Successfully wrote to CCCD to enable notifications for {char_uuid}")

    except Exception as e:
        print(f"Error enabling notifications for characteristic {char_uuid}: {e}")
    

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
    testService = dev.getServiceByUUID(UUID(0xfff0))
    for ch in testService.getCharacteristics():
        print(str(ch))

    char_uuid = 0xfff2  # 这是特征的UUID
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

    ch = dev.getCharacteristics(uuid=UUID(0xfff2))[0]
    if (ch.supportsRead()):
        print (ch.read())
#
except Exception as e:
    print(f"An error occurred: {e}")


finally:
    print("Disconnecting...")
    dev.disconnect()
