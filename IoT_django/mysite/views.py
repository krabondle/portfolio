
import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from dongle import security
from Iot import settings
from rest_framework.views import APIView
import socket
from . import iotmqtt, models

def GetLocalIPByPrefix(prefix):
    localIP = ''
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith(prefix):
            localIP = ip
        else:
            localIP = '127.0.0.1'
    return localIP


# Create your views here.

MQTT = iotmqtt.MQTT()
try:
    MQTT.Start()
    print("MQTT Start")
except Exception as e:
    print("Error : "+str(e))

ck = security.check_key()
def dongle_check(html):
    if ck.login() != 0:
        return 'dongle.html'
    else:
        return (html)


sensors_dict = {'A00101':'Temperature', 'A00102':'Humidity','A10101':'UV','A20101':'Accelerometer','A20102':'Gyroscope','A20103':'Compass','A30101':'Light','A40101':'CO₂','A50101':'Hall','A60101':'Photo Interrupter','A70101':'Loudness','A80101':'Motion','A90101':'IR Distance','B00101':'PM2.5','B10101':'Ultrasonic', 'B20101':'Pressure','B30101':'Gas'}

def index(request):
    dongle_check(request)
    path = request.path
    title = ''
    picture_path = ''
    if path =='/Community/':
        title = 'Community'
        picture_path = 'images/community.png'
    elif path == '/Smarthome/':
        title = 'Home'
        picture_path = 'images/house02.png'
    elif path == '/Smartoffice/':
        title = 'Office'
        picture_path = 'images/office0.png'

    # return render(request, 'index.html' ,{'picture_path':picture_path,'title':title,'ck':dongle_check(request)})
    return render(request, dongle_check('index.html') ,{'picture_path':picture_path,'title':title,'ip_address': GetLocalIPByPrefix('192.168.8')})

#dongle page
def dongle(request):
    return render(request, 'dongle.html')

#Navigation page
def Navigation(request):
    return render(request, dongle_check('Navigation.html'))

# SmartHome content
def Smarthome(request):
    context = {"home_page":"active"}
    return render(request, dongle_check('smarthome.html'))

def Smartoffice(request):
    context = {"office_page":"active"}
    return render(request, dongle_check('smartoffice.html'))

def Smartparking(request):
    context = {"parking_page":"active"}
    return render(request, dongle_check('index004.html'))

# Node_red content
def Node_red(request):
    # context = {"node_page":"active"}
    ip = settings.PI_IP
    return render(request, dongle_check('Node_red.html'),{'NR_url': 'http://%s:1880' % ip,'ip_address': GetLocalIPByPrefix('192.168.8')})

def NodeRed_dashboard(request):
    ip = settings.PI_IP
    return render(request, dongle_check('NR_dashboard.html'),{'NRD_url': 'http://%s:1880/ui' % ip,'ip_address': GetLocalIPByPrefix('192.168.8')})

def ipcamera(request):
    ip = settings.PI_IP
    return render(request, dongle_check('camera.html'),{'RPC_url': 'http://%s:1879/?action=stream' % ip,'ip_address': GetLocalIPByPrefix('192.168.8')})

def data_update(request):
    item = request.GET['item']
    result = {}
    for i in sensors_dict.keys():
        if i in MQTT.Sensors_list:
            result.setdefault(i,MQTT.Sensors_dict[i][0])
        elif i not in MQTT.Sensors_list:
            result.setdefault(i,404)
    json_stuff =  json.dumps(result)

    if ck.login() != 0:
        json_stuff = {'ERROR':'dongle!'}

    return HttpResponse(json_stuff, content_type ="application/json")

def mqtt_publisher(request):
    topic = request.GET['topic']
    value = request.GET['value']
    MQTT.on_publish(topic,value)

    json_stuff = json.dumps({"result" : 100})
    return HttpResponse(json_stuff, content_type ="application/json")

class detail(APIView):
    def get(self, request, *args, **kwargs):
        item = kwargs['sensor']
        Isupdate = True
        try:
            firstdate = request.query_params['firstdate']
            lastdate = request.query_params['lastdate']
            d = datetime.datetime.strptime(lastdate, "%Y-%m-%d")
            d = d + datetime.timedelta(days=1)
            lastdate = d.strftime("%Y-%m-%d")
        except:
            firstdate = ''
            lastdate = ''

        if(firstdate =='' or lastdate ==''):
            if item in MQTT.Sensors_list :
                labels  = [i[1] for i in reversed(MQTT.Sensors_dict[item])]
                defaultData = [i[0] for i in reversed(MQTT.Sensors_dict[item])]
                Isupdate = True
            elif item not in MQTT.Sensors_list :
                labels  = ['0']*20
                defaultData = [0]*20
                Isupdate = False
        else:
            # sqlcmd = "SELECT * FROM iotdemo.mysite_sensor_data where Type = '{}' and Number = '{}' and Topic = '{}' and Time > date('{}') and Time < date('{}') ;"
            sqlcmd = "SELECT * FROM iotdemo.mysite_sensor_data where sensor_ID = '{}' and Time > date('{}') and Time < date('{}') ;"
            sqlcmd = sqlcmd.format(item,firstdate,lastdate)
            result = models.Sensor_Data.objects.raw(sqlcmd)
            value = []
            time = []
            for i in result:
                value.append(i.Value)
                time.append(str(i.Time.strftime("%Y-%m-%d %H:%M:%S")))
            if len(value) > 1000:
                value = value[1:len(value):int(len(value)/1000)]
                time = time[1:len(time):int(len(time)/1000)]
            elif len(value) == 0 :
                value = 0
                time = '0'
            labels=time
            defaultData=value
            Isupdate = False
        y =json.dumps({"labels" : labels})
        return render(request, dongle_check('detail.html') , {'defaultData': json.dumps(defaultData) , 'labels': json.dumps(labels), 'Isupdate': json.dumps(Isupdate),'sensor_name':sensors_dict[item],'ip_address': GetLocalIPByPrefix('192.168.8')})