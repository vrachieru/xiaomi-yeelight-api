<p align="center">
    <img src="https://user-images.githubusercontent.com/5860071/48673419-f330c600-eb49-11e8-92e7-671174624e65.png" width="500px" border="0" />
    <br/>
    <a href="https://github.com/vrachieru/xiaomi-yeelight-api/releases/latest">
        <img src="https://img.shields.io/badge/version-1.0.0-brightgreen.svg?style=flat-square" alt="Version">
    </a>
    <a href="https://travis-ci.org/vrachieru/xiaomi-yeelight-api">
        <img src="https://img.shields.io/travis/vrachieru/xiaomi-yeelight-api.svg?style=flat-square" alt="Version">
    </a>
    <br/>
    Xiaomi Yeelight Smart Bulb API wrapper
</p>

## About Xiaomi Yeelight Smart Bulb

* [Xiaomi Yeelight Smart Bulb](https://www.yeelight.com/en_US/product/lemon-color) are light bulbs that can be turned on/off and their color/brightness changed remotely via an app 
* Can be operated either via cloud or lan

## Features

* Query device information
* Change bulb state

## Install

```bash
$ pip3 install git+https://github.com/vrachieru/xiaomi-yeelight-api.git
```
or
```bash
$ git clone https://github.com/vrachieru/xiaomi-yeelight-api.git
$ pip3 install ./xiaomi-yeelight-api
```

## Usage

### Reading device information

```python
from yeelight import SmartBulb

bulb = SmartBulb('192.168.xxx.xxx')

print('Name: %s' % bulb.name)
```

```bash
$ python3 info.py
Name: Bedroom Floor Lamp
```

### Change state

```python
from yeelight import SmartBulb

bulb = SmartBulb('192.168.xxx.xxx')

if bulb.is_on:
    bulb.power_off()
    print('Bulb powered off')
else:
    bulb.power_on()
    print('Bulb powered on')
```

```bash
$ python3 toggle.py
Bulb powered off

$ python3 toggle.py
Bulb powered on
```

## License

MIT