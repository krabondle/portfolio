from django.contrib import admin
from .models import Sensor,Sensor_Data


# Register your models here.
# 
# class Sensor_DataAdmin(admin.ModelAdmin):
#     list_display = ('Type', 'Number', 'Topic', 'Value','Time') 

# admin.site.register(Sensor_Data,Sensor_DataAdmin)

class SensorAdmin(admin.ModelAdmin):
    list_display = ('sensor_ID', 'sensor_type', 'sensor_no', 'sensor_topic','Community','Home','Office')

admin.site.register(Sensor,SensorAdmin)