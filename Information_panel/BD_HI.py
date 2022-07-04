import platform
import paho.mqtt.client as mqtt
import threading
import logging
import psutil
import json
import time



LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, filename='BD_HI.log', filemode='w',format=LOGGING_FORMAT, datefmt=DATE_FORMAT)

class MQTT:
    def __init__(self,hostname):
        self.broker = '192.168.10.150'
        self.hostname = hostname
        self.client = mqtt.Client(client_id= self.hostname, clean_session=False)
        self.IsConnected = False
        

    def on_connect(self,client, userdata, flag, rc):
        # print("Connect with the result code " + str(rc))
        logging.info("Connect with the result code " + str(rc))
        # self.client.subscribe('#')

    def on_message(self,client, userdata, msg):
        out = str(msg.payload.decode('utf-8'))
        logging.info('mqtt receive : topic=%s value=%s' % (msg.topic , str(out)))
        # print(msg.topic)
        # print(out)
        out = json.loads(out)
        
    def on_publish(self,t, m):
        self.client.publish(t, m)

    # mqtt客户端启动函数
    def MQTT_Loop(self):
        # global client
        # 使用loop_start 可以避免阻塞Django进程，使用loop_forever()可能会阻塞系统进程
        # client.loop_start()
        #client.loop_forever() #有掉线重连功能
        self.client.loop_forever(retry_first_connection=True)
    
    # 启动函数
    def Start(self):
        # client.on_connect = on_connect
        # client.on_message = on_message
        # # 绑定 MQTT 服务器地址
        # broker = '192.168.10.150'
        # MQTT服务器的端口号
        try:
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.will_set('/master/status','Offline', 0, False)
            self.client.connect_async(self.broker, 1883, 120)
            #client.username_pw_set('user', 'user')
            self.client.reconnect_delay_set(min_delay=1, max_delay=120)
            self.MQTT_thread = threading.Thread(target=self.MQTT_Loop)
            self.MQTT_thread.setName('MQTT_thread')
            self.MQTT_thread.setDaemon(True)
            self.MQTT_thread.start()
            self.IsConnected = True
        except Exception as e:
            # print("Error : "+str(e))
            logging.error("Error : "+str(e))
            self.IsConnected = False
    
    def close(self):
        try:
            self.client.disconnect()
            self.IsConnected = False
        except Exception as e:
            # print("Error : "+str(e))
            logging.error("Error : "+str(e))


if __name__ == "__main__":
    print('BD_HI')
    hostname = platform.node().split('.')[0]
    hardwarelist = {"cpu": 0,"disk": 0,"memory": 0,"sent": 0,"recv": 0}
    MT = MQTT(hostname)
    MT.Start()
    
    def read_HI_loop():
        global hardwarelist
        while True:
            try:
                hardwarelist ={"cpu": psutil.cpu_percent(interval=1, percpu=False),
                                                "disk": psutil.disk_usage('/').percent,
                                                "memory": psutil.virtual_memory().percent,
                                                "sent": psutil.net_io_counters().packets_sent,
                                                "recv": psutil.net_io_counters().packets_recv}
            except Exception as e:
                logging.error("Error : "+str(e))
            time.sleep(1)
    
    def send_HI_loop():
        global hardwarelist
        while True:
            try:
                for key, value in hardwarelist.items():
                    topic = "/"+hostname+"/"+key
                    #print(topic)
                    MT.on_publish(topic,str(value))
                    logging.info('mqtt send : topic=%s value=%s' % (topic , str(value)))
            except Exception as e:
                logging.error("Error : "+str(e))
            time.sleep(3)

    read_HI_thread = threading.Thread(target=read_HI_loop)
    read_HI_thread.setName('read_HI_thread')
    read_HI_thread.setDaemon(True)
    read_HI_thread.start()

    send_HI_thread = threading.Thread(target=send_HI_loop)
    send_HI_thread.setName('send_HI_thread')
    send_HI_thread.setDaemon(True)
    send_HI_thread.start()

    while True:
        time.sleep(60)
        pass