import serial
import time
import logging


class serial_class:
    def __init__(self,COM_PORT,BAUD_RATES,bytesize,parity,stopbits,timeout,xonxoff,rtscts,dsrdtr):
        self.COM_PORT = COM_PORT
        self.BAUD_RATES = BAUD_RATES
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.xonxoff =xonxoff
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr

        self.connection_status = False

    def connect(self):
        try:
            self.ser = serial.Serial(self.COM_PORT, self.BAUD_RATES, self.bytesize, self.parity , self.stopbits, self.timeout,self.xonxoff,self.rtscts ,self.dsrdtr)#,writeTimeout = 0.5,xonxoff = False,rtscts = False,dsrdtr = False 
            self.connection_status = True
        except Exception as e:
            self.connection_status = False
            return e

    def serial_read(self):
        while True:
            while self.connection_status:
                try:
                    # res = self.ser.read_until(b'\r')
                    res = self.ser.readline()
                    if len(res) != 0:
                        # print(res)
                        logging.info('read = ' + str(res))
                except Exception as e:
                    logging.error(e)
                    pass
                finally:
                    self.ser.flushInput()
                time.sleep(.1)

    def serial_keep(self):
        while True:
            if self.connection_status == False :
                self.connect()
            time.sleep(5)
    
    def serial_flushO(self):
        try:
            self.ser.flushOutput()
        except Exception as e:
            logging.error(e)

class control_serial(serial_class):
    def __init__(self,COM_PORT):
        super().__init__(COM_PORT,BAUD_RATES=9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_TWO,timeout=120,xonxoff=False,rtscts=False,dsrdtr=False)
        

    def serial_write_hex(self,comm):
        # if self.ser_status == True :
        try:
            self.ser.write(bytes.fromhex(comm))
            logging.info('write = ' + str(comm))
        except Exception as e:
            logging.error(e)
            return e
        # finally:
        #     self.ser.flushOutput()

    def serial_write_asc(self,comm):
        # if self.ser_status == True :
        try:
            self.ser.write(bytes(comm, 'ascii'))
            logging.info('write = ' +str(bytes(comm, encoding = "ascii")))
        except Exception as e:
            logging.error(e)
            return e
        # finally:
        #     self.ser.flushOutput()

def find_serial_ports():
    p = ['COM%s' % (i + 1) for i in range(256)]
    using = []
    control_ports = 'control not match'
    # android_ports = 'android not match'
    # control_ports = 'COM62'
    # android_ports = 'COM63'
    for port in p:
        try:
            s = serial.Serial(port)
            s.close()
            using.append(port)
        except (OSError, serial.SerialException):
            pass
    for i in using:
        ser = serial.Serial(i,9600,serial.EIGHTBITS,serial.PARITY_NONE,serial.STOPBITS_TWO,3)
        if ser.isOpen():
            try:
                ser.flushInput() #flush input buffer
                ser.flushOutput() #flush output buffer
                ser.write(bytes.fromhex('0530304644303936393646380D'))
                # print("write 8 byte data: 0530304642303030303044380D")
                time.sleep(1)  #wait 0.5s
                response = ser.read_all()
                # print(response)
                if response == b'\x0600\r':
                    # print('match!!!')
                    control_ports = i
                # elif response.decode().find('Switch') != -1 or response.decode().find('Origin') != -1:
                #     android_ports = i
                
                ser.close()
                
            except Exception as e:
                pass
                # print ("communicating error " + str(e))
                # result = "communicating error " + str(e)
    result = control_ports
    return result


if __name__ == "__main__":
    import os
    import uuid

    path = 'logs/'
    if not os.path.isdir(path):
        os.makedirs(path, mode=0o777)
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    logging.basicConfig(level=logging.DEBUG, filename='logs/serial_%s.log' % str(uuid.uuid4()), filemode='a', format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
    
    print('serial port')
    test = control_serial('COM62')
    test.connect()
    
    import threading


    control_serial_read =  threading.Thread(target=test.serial_read)
    control_serial_read.setDaemon(True)
    control_serial_read.setName('control_serial_read')
    control_serial_read.start()
    
    import time
    while True:
        a = '05303042443031360D'
        b = '0530304641303030303044370D'
        c = '0530304644303936393646380D'
        d = '0530303734303130303743330D'
        test.serial_write_hex(c)
        time.sleep(1)
        pass
