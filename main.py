import sys
import serial
import glob
import threading
import queue

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


def logan_set_mask(_port, _mask):
    if len(_mask) == 4:
        for i in range(0, 2):
            maskCmd = 'AT+M=[' + str(i) + '][' + _mask[2*i] + '][' + _mask[2*i+1] + ']\r\n'
            _port.write(maskCmd)
    return


def logan_set_filter(_port, _filter):
    if len(_filter) == 12:
        for i in range(0, 6):
            filterCmd = 'AT+F=[' + str(i) + '][' + _filter[2*i] + '][' + _filter[2*i+1] + ']\r\n'
            _port.write(filterCmd)
    return


def logan_enter_cmd(_port):
    _port.write('+++')
    return


def logan_exit_cmd(_port):
    _port.write('AT+Q\r\n')
    return


#   01      02      03      04      05      06      07      08      09      10      11      12      13      14      15      16      17      18
#   5 kbps  10      20      25      31.2    33      40      50      80      83.3    95      100     125     200     250     500(*)  666     1000
# (*) = default
def logan_set_canrate(_port, rate):
    canCmd = 'AT+C=' + rate + '\r\n'
    _port.write(canCmd)
    return


#   0           1           2           3           4
#   9600 bps(*) 19200       38400       57600       115200
# (*) = default
def logan_set_baudrate(_port, rate):
    canCmd = 'AT+S=' + rate + '\r\n'
    _port.write(canCmd)
    return


readThreadRun = False
readQueue = queue.Queue()
thePort = open()
logan_enter_cmd(thePort)
logan_set_canrate(thePort, '16')
logan_set_mask(thePort, mask)
logan_set_filter(thePort, filt)
logan_exit_cmd(thePort)



def read_thread(port):
    global readThreadRun
    global readQueue
    while readThreadRun:
        if port.in_waiting() > 0:
            readQueue.put(port.read(port.in_waiting()))
    return


def open(portName):
    global readThreadRun
    port = serial.Serial(portName, 9600)
    readThreadRun = True
    thread = threading.Thread(target=read_thread, args=(port,))
    thread.start()
    return port


def close(port):
    global readThreadRun
    readThreadRun = False
    readQueue.join()
    port.close()
    return


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
