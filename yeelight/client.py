import json
import socket

class SmartBulb(object):

    def __init__(self, host, port=55443, timeout=5):
        '''
        Create a new Bulb instance

        :param str host: host name or ip address on which the device listens
        :param int port: port on which the device listens (default: 9999)
        :param int timeout: socket timeout (default: 5)
        '''
        self._host = host
        self._port = port
        self._timeout = timeout
        
        self.__cmd_id = 0
        self.__socket = None

    @property
    def _cmd_id(self):
        '''
        Get next command id in sequence

        :return: command id
        '''
        self.__cmd_id += 1
        return self.__cmd_id - 1

    @property
    def _socket(self):
        '''
        Get, optionally create, the communication socket

        :return: the communication socket
        '''
        if self.__socket is None:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.settimeout(self._timeout)
            self.__socket.connect((self._host, self._port))

        return self.__socket

    def send_command(self, method, params=None):
        '''
        Request information and return the response

        :param str method: control method id
        :param list params: list of params for the specified method
        :return: the command response
        '''
        command = {'id': self._cmd_id, 'method': method, 'params': params}

        try:
            self._socket.send((json.dumps(command) + '\r\n').encode('utf8'))
        except socket.error as ex:
            self.__socket.close()
            self.__socket = None
            raise_from(Exception('A socket error occurred when sending the command.'), ex)

        # The bulb will send us updates on its state in addition to responses,
        # so we want to make sure that we read until we see an actual response.
        response = None
        while response is None:
            try:
                data = self._socket.recv(4 * 1024)
            except socket.error:
                self.__socket.close()
                self.__socket = None
                response = {'error': 'Bulb closed the connection.'}
                break

            for line in data.split(b'\r\n'):
                if not line:
                    continue

                try:
                    line = json.loads(line.decode('utf8'))
                except ValueError:
                    response = {'result': ['invalid command']}

                if line.get('method') != 'props':
                    response = line

        return response

    @property
    def name(self):
        '''
        Get the device name

        :return: device name
        '''
        return self.send_command('get_prop', ['name'])['result']
    
    @name.setter
    def name(self, name):
        '''
        Set the device name

        :param name: new name
        '''
        self.send_command('set_name', [name])

    @property
    def is_on(self):
        '''
        Get whether device is on

        :return: True if device is on, False otherwise
        '''
        return self.send_command('get_prop', ['power'])['result'][0] == 'on'

    def power_on(self):
        '''
        Turn the bulb on
        '''
        self.send_command('set_power', ['on'])

    def power_off(self):
        '''
        Turn the bulb off
        '''
        self.send_command('set_power', ['off'])

    def set_rgb(self, red, green, blue):
        '''
        Set the bulb's RGB value

        :param int red: the red value to set (0-255)
        :param int green: the green value to set (0-255)
        :param int blue: the blue value to set (0-255)
        '''
        red = clamp(red, 0, 255)
        green = clamp(green, 0, 255)
        blue = clamp(blue, 0, 255)

        self.send_command('set_rgb', [red * 65536 + green * 256 + blue])
