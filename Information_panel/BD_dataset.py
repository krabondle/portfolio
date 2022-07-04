import paho.mqtt.client as mqtt
import threading
import logging
import json
import time
import pandas as pd
import numpy as np
from hdfs import Client
import multiprocessing as mp
import os

LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, filename='BD_dataset.log', filemode='w',format=LOGGING_FORMAT, datefmt=DATE_FORMAT)

class MQTT:
    def __init__(self):
        self.broker = '192.168.10.150'
        self.client = mqtt.Client(client_id= 'dataset', clean_session=False)
        self.IsConnected = False
        self.panel_dataset_button = {'/DataSet/1' : 0,'/DataSet/2' : 0,'/DataSet/3' : 0,'/DataSet/4' : 0,'/DataSet/5' : 0,'/DataSet/6' : 0}
        

    def on_connect(self,client, userdata, flag, rc):
        # print("Connect with the result code " + str(rc))
        logging.info("Connect with the result code " + str(rc))
        self.client.subscribe('/DataSet/#')
        # self.client.subscribe('#')

    def on_message(self,client, userdata, msg):
        out = str(msg.payload.decode('utf-8'))
        logging.info('mqtt receive : topic=%s value=%s' % (msg.topic , str(out)))
        # print(msg.topic)
        # print(out)
        out = json.loads(out)
        if msg.topic in self.panel_dataset_button:
            self.panel_dataset_button[msg.topic] = out
        
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

def ALS(count):
    # d = {'id': np.random.randint(1,count/100+1,count) ,'movid' : np.random.randint(1,1683,count),'rating' : np.random.uniform(1,5,count)}
    d = {'id': np.random.randint((count-1)*10000+1,count*10000+1,1000000) ,'movid' : np.random.randint(1,1683,1000000),'rating' : np.random.uniform(1,5,1000000)}
    df = pd.DataFrame(data= d)
    # df.to_csv(path+"ALS_%s.csv"%count,index=False,header=False)
    df.to_csv("ALS_%s.csv"%count,index=False,header=False)

    

def ALS_Process():
    pool = mp.Manager().Pool(processes=8)
    pool.map(ALS,range(1,26))
    pool.close()  
    pool.join()
    try:
        # print('ALS'+str(count))
        for count in range(1,26) :
            delete_hdfs_file(client,'/file/random/ALS_%s.csv'%count)
            put_to_hdfs(client,'ALS_%s.csv'%count, '/file/random/ALS_%s.csv'%count)
            os.remove('ALS_%s.csv'%count)
            # time.sleep(.5)
    except Exception as e:
        # print("Error : "+e)
        logging.error("Error : "+str(e))
   
    return

def stumbleupon(n):
    # df = pd.read_csv(path+'stumbleupon.tsv',delimiter="\t")
    df = pd.read_csv('stumbleupon.tsv',delimiter="\t")
    # df = pd.read_csv('C:/Users/kh/Desktop/BD101_Panel/test.tsv',delimiter="\t")
    
    for i in df.columns :
        if i =='url' or i =='urlid' or i =='boilerplate' or i =='alchemy_category' :
            continue
        min = df[i].min()
        max = df[i].max()
        # print(df[i].sum())
        if min == 0 and max == 0 :
            df[i] = 0
        elif  df[i].sum()%1 == 0 :
            df[i] = np.random.randint(min,max+1,df[i].shape[0])
        else :
            df[i] = np.random.uniform(min,max,df[i].shape[0])
        # print(df[i].sum())
    filename = ''
    if n == 2:
        filename = 'Decision_Tree.tsv'
    elif n == 3:
        filename = 'SVM.tsv'
    elif n == 5:
        filename = 'Naive_bayes_binary.tsv'
    elif n == 6:
        filename = 'Decision_tree_regression.tsv'
    
    # df.to_csv(path+filename, sep = '\t',encoding='utf-8',index=False)
    df.to_csv(filename, sep = '\t',encoding='utf-8',index=False)
    # df.to_csv('C:/Users/kh/Desktop/BD101_Panel/'+filename, sep = '\t',encoding='utf-8',index=False)

    try:
        pass
        delete_hdfs_file(client,'/file/random/%s'%filename)
        put_to_hdfs(client, filename, '/file/random/%s'%filename)
        os.remove(filename)
    except Exception as e:
        # print("Error : "+e)
        logging.error("Error : "+str(e))
        
    return

def titanic():
    # df = pd.read_csv(path+'titanic.csv',delimiter=",")
    df = pd.read_csv('titanic.csv',delimiter=",")
    # df = pd.read_csv('C:/Users/kh/Desktop/BD101_Panel/titanic.csv',delimiter=",")
    for i in df.columns :
        # count = df[i].shape[0]
        if i =='PassengerId' or i =='Name' or i =='Ticket' or i =='Cabin' :
            continue
        elif i == 'Sex' :
            randlist = ['male', 'female']
            df[i] = np.random.choice(randlist,df.shape[0])
        elif i == 'Embarked' :
            randlist = ['Q', 'S','C']
            df[i] = np.random.choice(randlist,df[i].shape[0])
        elif i == 'Age' :
            df[i] = np.random.randint(0,77,df[i].shape[0])
        else :
            min = df[i].min()
            max = df[i].max()
            # print(df[i].sum())
            if min == 0 and max == 0 :
                df[i] = 0
            elif  df[i].sum()%1 == 0 :
                df[i] = np.random.randint(min,max+1,df[i].shape[0])
            else :
                df[i] = np.random.uniform(min,max,df[i].shape[0])
            # print(df[i].sum())
    #print(df.shape[0])	# 深度418   
    filename = 'Binary_classification.csv'  
    # df.to_csv('C:/Users/kh/Desktop/BD101_Panel/'+filename, sep = ',',encoding='utf-8',index=False) 
    # df.to_csv(path+filename, sep = ',',encoding='utf-8',index=False) 
    df.to_csv(filename, sep = ',',encoding='utf-8',index=False) 
    try:
        pass
        delete_hdfs_file(client,'/file/random/%s'%filename)
        put_to_hdfs(client, filename, '/file/random/%s'%filename)
        os.remove(filename)
    except Exception as e:
        # print("Error : "+e)
        logging.error("Error : "+str(e))

    return


client = Client("http://master.com:50070/",timeout=3)

#上传文件到hdfs
def put_to_hdfs(client, local_path, hdfs_path):
    client.upload(hdfs_path, local_path, cleanup=True)

def write_to_hdfs(client, hdfs_path, data): # 覆寫
    client.write(hdfs_path, data, overwrite=True, append=False)

def delete_hdfs_file(client,hdfs_path):
    client.delete(hdfs_path)



if __name__ == "__main__":
    print('BD_dataset')
    # panel_dataset_button = {'/DataSet/1' : 0,'/DataSet/2' : 0,'/DataSet/3' : 0,'/DataSet/4' : 0,'/DataSet/5' : 0,'/DataSet/6' : 0}
    panel_dataset_state = {'/DataSet/1' : 0,'/DataSet/2' : 0,'/DataSet/3' : 0,'/DataSet/4' : 0,'/DataSet/5' : 0,'/DataSet/6' : 0}
    panel_dataset_building = {'/DataSet/1' : 0,'/DataSet/2' : 0,'/DataSet/3' : 0,'/DataSet/4' : 0,'/DataSet/5' : 0,'/DataSet/6' : 0}

    MT = MQTT()
    MT.Start()
    
    def dataset_loop():
        global panel_dataset_state,panel_dataset_building

        while True:
            thread = []
            for i in panel_dataset_state.keys():
                if (MT.panel_dataset_button[i] != panel_dataset_state[i]) and panel_dataset_state[i] == 0 and panel_dataset_building[i] == 0:
                    # print(i)
                    if i == '/DataSet/1' :
                        t = threading.Thread(target = ALS_Process)
                    elif i == '/DataSet/2' :
                        t = threading.Thread(target = stumbleupon, args=(2,))
                    elif i == '/DataSet/3' :
                        t = threading.Thread(target = stumbleupon, args=(3,))
                    elif i == '/DataSet/4' :
                        t = threading.Thread(target = titanic)
                    elif i == '/DataSet/5' :
                        t = threading.Thread(target = stumbleupon, args=(5,))
                    elif i == '/DataSet/6' :
                        t = threading.Thread(target = stumbleupon, args=(6,))
                    t.setName(str(i).replace('/', ''))
                    t.setDaemon(True)
                    t.start()
                    panel_dataset_building[i] = 1
                    MT.on_publish('Notice','%s : Start' % str(i).replace('/', ''))
                    logging.info('%s : Start' % str(i).replace('/', ''))
                panel_dataset_state[i] = MT.panel_dataset_button[i]
                time.sleep(.1)

    def dataset_finish_loop():
        global panel_dataset_state,panel_dataset_building

        while True:
            thread = []
            for i in threading.enumerate():
                thread.append(i.getName())
            for i in panel_dataset_state.keys():
                if panel_dataset_building[i] == 1:
                    if str(i).replace('/', '') not in thread:
                        panel_dataset_building[i] = 0
                        MT.on_publish('Notice','%s : Done!' % str(i).replace('/', ''))
                        logging.info('%s : Done' % str(i).replace('/', ''))
            time.sleep(.1)

    dataset_loop_thread = threading.Thread(target=dataset_loop)
    dataset_loop_thread.setName('dataset_loop_thread')
    dataset_loop_thread.setDaemon(True)
    dataset_loop_thread.start()

    DFL_thread = threading.Thread(target=dataset_finish_loop)
    DFL_thread.setName('dataset_finish_loop_thread')
    DFL_thread.setDaemon(True)
    DFL_thread.start()

    while True:
        time.sleep(60)
        pass