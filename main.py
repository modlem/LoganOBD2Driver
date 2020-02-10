import sys
import serial
import glob
import threading

mask = ['0', '000007F8',
        '0', '000007F8']
filt = ['0', '000007E8',
        '0', '000007E8',
        '0', '000007E8',
        '0', '000007E8',
        '0', '000007E8',
        '0', '000007E8']
factoryMask = ['0', '00000000',
               '0', '00000000']
factoryFilt = ['0', '00000000',
               '0', '00000000',
               '0', '00000000',
               '0', '00000000',
               '0', '00000000',
               '0', '00000000']


def serial_data_callback(_data):
    return


def set_mask(_port, _mask):
    if len(_mask) == 4:
        for i in range(0, 2):
            maskCmd = 'AT+M=[' + str(i) + '][' + _mask[2*i] + '][' + _mask[2*i+1] + ']\r\n'
            #_port.write(maskCmd)
            print(maskCmd, end='')
    return


def set_filter(_port, _filter):
    if len(_filter) == 12:
        for i in range(0, 6):
            filterCmd = 'AT+F=[' + str(i) + '][' + _filter[2*i] + '][' + _filter[2*i+1] + ']\r\n'
            #_port.write(filterCmd)
            print(filterCmd, end='')
    return


#set_mask(1, mask)
#set_filter(1, filt)


def open_serial_port(portName):
    return serial.Serial(portName, 9600)


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
