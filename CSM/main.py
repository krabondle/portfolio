import os
import time
import logging
import wmi
import serialport
import threading
import pygame
import uuid

switch = False
last_switch = False
processing = False
origin = False
axis = 0
ports_state =  False
origin_input = False
switch_input = False
joystick_first_read = False

vibrate_command = {'CU': '0530304642303030303044380D',
                'start':'0530304641303030303244390D',
                'stop' : '0530304641303030303044370D'}

spin_command = {'Control_Servo' : ':0110061E00020400010000C4\r\n',
                'Servo_ON' : ':0110063000020400010000B2\r\n',
                'Servo_OFF' : ':0110063000020400000000B3\r\n',
                'Origin' : ':011008A2000204000000003F\r\n',
                'PR20' : ':011008A2000204001400002B\r\n',
                'PR24' : ':011008A20002040018000027\r\n',
                'PR25' : ':011008A20002040019000026\r\n',
                'PR26' : ':011008A2000204001A000025\r\n',
                'PR27' : ':011008A2000204001B000024\r\n',
                'PR28' : ':011008A2000204001C000023\r\n',
                'PR29' : ':011008A2000204001D000022\r\n',
                'PR30' : ':011008A2000204001E000021\r\n',
                'PR31' : ':011008A2000204001F000020\r\n',
                'PR35' : ':011008A2000204002300001C\r\n',
                'PR36' : ':011008A2000204002400001B\r\n',
                'PR37' : ':011008A2000204002500001A\r\n',
                'PR38' : ':011008A20002040026000019\r\n',
                'PR39' : ':011008A20002040027000018\r\n',


                '12' : ':011008A20002040019000026\r\n',
                '13' : ':011008A2000204001A000025\r\n',
                '14' : ':011008A2000204001B000024\r\n',
                '15' : ':011008A2000204001C000023\r\n',
                '16' : ':011008A2000204001D000022\r\n',

                '0' : ':011008A2000204001E000021\r\n',

                '5' : ':011008A2000204002300001C\r\n',
                '4' : ':011008A2000204002400001B\r\n',
                '3' : ':011008A2000204002500001A\r\n',
                '2' : ':011008A20002040026000019\r\n',
                '1' : ':011008A20002040027000018\r\n',

    'forward_600' : [':010609010003EC\r\n', ':010609040001EB\r\n',
            ':010609010003EC\r\n', ':01060903025893\r\n'],
    'forward_1000' : [':010609010003EC\r\n',':010609040001EB\r\n',
            ':010609010003EC\r\n',':0106090303E802\r\n'],
    'forward_1200' : [':010609010003EC\r\n', ':010609040001EB\r\n',
            ':010609010003EC\r\n', ':0106090304B039\r\n'],
    'Reverse_600' : [':010609010003EC\r\n', ':010609040002EA\r\n',
            ':010609010003EC\r\n', ':01060903025893\r\n'],
    'Reverse_1000' : [':010609010003EC\r\n',':010609040002EA\r\n',
            ':010609010003EC\r\n',':0106090303E802\r\n'],
    'Reverse_1200' : [':01 0609010003EC\r\n', ':010609040002EA\r\n',
            ':010609010003EC\r\n', ':0106090304B039\r\n']}

def freq_c(f):
    freq = f * 100

    freq_hex = format(freq, 'x').upper()

    if len(freq_hex) < 4:
        freq_hex = '0' + freq_hex

    count = 0
    sum = 0x11A
    hexOutput = []
    command = '053030454530'

    for i in freq_hex:
        sum += ord(i)
        command += format(ord(i), "x")

    sum_str = format(sum, 'x').upper()

    if len(sum_str) > 2:
        sum_str = sum_str[-2]+sum_str[-1]

    for i in sum_str:
        command += format(ord(i), "x")
    command += '0D'
    return command

def origin_func():
    global origin_input
    # control_serial.serial_write_asc(spin_command['Control_Servo'])
    # time.sleep(.1)
    # control_serial.serial_write_asc(spin_command['Servo_ON'])
    # time.sleep(.1)
    control_serial.serial_write_asc(spin_command['Origin'])
    time.sleep(.1)
    while  bool(not origin_input):
        control_serial.serial_write_asc(spin_command['Origin'])
        time.sleep(1)
        # pass
    # control_serial.serial_write_asc(spin_command['Servo_OFF'])
    # time.sleep(.2)

def switch_on():
    global processing,origin_input
    # if control_serial.ser.is_open == False :
    #     control_serial.ser.open()
    control_serial.serial_flushO()
    time.sleep(.1)
    control_serial.serial_write_hex(vibrate_command['CU'])
    time.sleep(.1)
    # control_serial.serial_write_hex(vibrate_command['stop'])
    # time.sleep(1)
    control_serial.serial_write_hex(freq_c(30))
    time.sleep(.1)
    control_serial.serial_write_hex(vibrate_command['start'])
    time.sleep(2)
    control_serial.serial_write_hex(freq_c(20))
    time.sleep(1)
    control_serial.serial_write_hex(freq_c(7))
    time.sleep(.5)

    if bool(not origin_input):
        origin_func()
    control_serial.serial_write_asc(spin_command['PR24'])
    time.sleep(12)
    processing = False
    logging.info('Process finished ')

def switch_off():
    global processing ,origin_input
    control_serial.serial_flushO()
    time.sleep(.1)
    control_serial.serial_write_hex(vibrate_command['stop'])
    time.sleep(.1)
    if bool(not origin_input):
        origin_func()
    # if control_serial.ser.is_open == True :
    #     control_serial.ser.close()
    processing = False
    logging.info('Process finished ')

def switch_loop():
    global processing ,switch ,switch_input
    while True:
        try:
            if switch_input != switch and processing == False:
                time.sleep(2)
                if switch_input == switch:
                    continue
                if switch_input == False:
                    t = threading.Thread(target=switch_off)
                    t.setName('switch_off')
                elif switch_input == True:
                    t = threading.Thread(target=switch_on)
                    t.setName('switch_on')
                t.setDaemon(True)
                t.start()
                processing = True
                switch = switch_input
                logging.info('Switch = %s ' % str(switch))
        except Exception as e:
            logging.error(e)
        time.sleep(.1)

def spin_loop():
    global processing ,axis  ,switch ,switch_input ,origin_input
    last_spin_state = 0
    spin_state = 0
    last_read = 0
    while True:
        if (not processing) * switch *  switch_input:
            set_volume = axis * 100
            pot_adjust = abs(set_volume - last_read)
            if pot_adjust > 1:
                spin = int(set_volume)
                last_read = set_volume
                logging.info('spin = %s ' % str(spin))
                if int(spin) > 70 :
                    spin_state = int((spin+1)  / 6)
                elif int(spin) < 30 :
                    spin_state = int(spin / 6 + 1)
                else :
                    spin_state = 0

            if spin_state != last_spin_state : # or spin_state == 0
                # control_serial.serial_write_asc(spin_command['Control_Servo'])
                # time.sleep(.1)
                # control_serial.serial_write_asc(spin_command['Servo_ON'])
                # time.sleep(.1)
                control_serial.serial_flushO()
                # time.sleep(.1)
                control_serial.serial_write_asc(spin_command[str(spin_state)])
                logging.info('command %s' % str(spin_state))
                last_spin_state = spin_state
                time.sleep(.1)
                if spin_state == 0 :
                    control_serial.serial_write_asc(spin_command[str(spin_state)])
                    logging.info('command %s' % str(spin_state))
                    last_spin_state = spin_state
                    # time.sleep(.1)
        elif switch_input == False and switch == True:
            spin_state = 0
            control_serial.serial_flushO()
            # time.sleep(.1)
            control_serial.serial_write_asc(spin_command[str(spin_state)])
            logging.info('command %s' % str(spin_state))
            last_spin_state = spin_state
        time.sleep(.1)



def joystick_read_value():
    global joystick_first_read,switch_input,origin_input,axis
    pygame.init()
    pygame.joystick.init()
    while  True:
        try:
            # EVENT PROCESSING STEP
            pygame.event.get() # User did something
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

            origin_input = bool(joystick.get_button(1))
            switch_input = bool(joystick.get_button(0))

            axis = joystick.get_axis(5)

            if joystick_first_read == False :
                if  axis != 0.0 :
                    joystick_first_read = True

        except Exception as e:
            logging.error(e)
        time.sleep(.1)

def main():
    logging.info('Main program start!!!!!!')
    global origin ,origin_input ,switch_input ,last_switch
    while True:
        try:
            if origin_input != origin:
                origin = origin_input
                logging.info('origin = %s ' % str(origin))

            if last_switch != switch_input :
                last_switch = switch_input
                logging.info('last_switch = %s ' % str(last_switch))

        except Exception as e:
            logging.error(e)
        time.sleep(.1)


if __name__ == "__main__":
    path = 'logs/'
    if not os.path.isdir(path):
        os.makedirs(path, mode=0o777)
    LOGGING_FORMAT = '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s'
    DATE_FORMAT = '%Y%m%d %H:%M:%S'
    logging.basicConfig(level=logging.DEBUG, filename='logs/CSM_%s.log' % str(uuid.uuid4()), filemode='a', format=LOGGING_FORMAT, datefmt=DATE_FORMAT)
    # logging.basicConfig(level=logging.DEBUG, filename='logs/CSM_%s.log' % time.strftime("%Y%m%d_%H%M%S", time.localtime()), filemode='w', format=LOGGING_FORMAT, datefmt=DATE_FORMAT)

    # print(wmi.WMI().Win32_Processor()[0].ProcessorId.strip())
    # 1
    BaseBoardID = '210585710700914'
    DiskDriveID = 'E823_8FA6_BF53_0001_001B_448B_4199_B167.'
    # 2
    # BaseBoardID = '210483765401141'
    # DiskDriveID = 'E823_8FA6_BF53_0001_001B_444A_4919_64B3.'
    # 3
    # BaseBoardID = '210483765400179'
    # DiskDriveID = 'E823_8FA6_BF53_0001_001B_444A_4919_6243.'
    # 4
    # BaseBoardID = '210484183900837'
    # DiskDriveID = 'E823_8FA6_BF53_0001_001B_448B_418A_4B73.'
    # 5
    # BaseBoardID = '210484183900020'
    # DiskDriveID = 'E823_8FA6_BF53_0001_001B_444A_4919_6C86.'

    if (wmi.WMI().Win32_BaseBoard()[0].SerialNumber.strip() != BaseBoardID) and (wmi.WMI().Win32_DiskDrive()[0].SerialNumber.strip() != DiskDriveID ):
        logging.error('Authentication error')
        print('Authentication error')
        while True :
            time.sleep(10)
        exit(0)

    while not ports_state:
        ports = serialport.find_serial_ports()
        # if 'control not match' in ports or 'android not match' in ports:
        if 'control not match' in ports:
            ports_state = False
            logging.error('COM Port Error : ' + str(ports))
            logging.error('Please turn of  motor power and reboot computer')
            # exit()
        else :
            ports_state = True
            logging.info('COM Port check done')
        time.sleep(5)

    control_serial = serialport.control_serial(ports)
    control_serial.connect()

    CSR_thread =  threading.Thread(target=control_serial.serial_read)
    CSR_thread.setDaemon(True)
    CSR_thread.setName('CSR_thread')

    JRV_thread = threading.Thread(target=joystick_read_value)
    JRV_thread.setDaemon(True)
    JRV_thread.setName('JRV_thread')

    switch_loop_thread  = threading.Thread(target=switch_loop)
    switch_loop_thread.setDaemon(True)
    switch_loop_thread.setName('switch_loop_thread')

    spin_thread = threading.Thread(target=spin_loop)
    spin_thread.setDaemon(True)
    spin_thread.setName('spin_thread')
    logging.info('Create thread')

    JRV_thread.start()
    CSR_thread.start()

    while not joystick_first_read:
        pass

    switch = switch_input
    logging.info('Switch = %s ' % str(switch))
    last_switch =  switch_input
    logging.info('last_switch = %s ' % str(last_switch))
    origin = origin_input
    logging.info('Origin = %s ' % str(origin))

    logging.info('Variable initial reading')

    switch_loop_thread.start()
    spin_thread.start()
    logging.info('Start threading')

    main()