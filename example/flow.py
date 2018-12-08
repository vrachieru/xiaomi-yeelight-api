import sys
sys.path.append('../')

from yeelight import SmartBulb, Flow, RGBTransition, SleepTransition

RED   = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE  = [0, 0, 255]

flow = Flow(
    10,
    Flow.actions.recover,
    [
        RGBTransition(*RED, 1000, 100),
        SleepTransition(1000),
        RGBTransition(*GREEN, 1000, 100),
        SleepTransition(1000),
        RGBTransition(*BLUE, 1000, 100),
        SleepTransition(1000)
    ]
)

bulb = SmartBulb('192.168.1.103')
bulb.start_flow(flow)