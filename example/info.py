import sys
sys.path.append('../')

from yeelight import SmartBulb

bulb = SmartBulb('192.168.xxx.xxx')

print('Name: %s' % bulb.name)