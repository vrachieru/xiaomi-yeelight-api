import sys
sys.path.append('../')

from yeelight import SmartBulb

bulb = SmartBulb('192.168.xxx.xxx')

if bulb.is_on:
    bulb.power_off()
    print('Bulb powered off')
else:
    bulb.power_on()
    print('Bulb powered on')