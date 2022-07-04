from django.db import models


class Sensor(models.Model):
    sensor_ID =  models.CharField(max_length=6,primary_key=True)
    sensor_type = models.CharField(max_length=2)
    sensor_no = models.CharField(max_length=2)
    sensor_topic = models.CharField(max_length=2)
    Community = models.BooleanField(default = False)
    Home = models.BooleanField(default = False)
    Office = models.BooleanField(default = False)
    
    def __str__(self):
        return self.sensor_ID

class Sensor_Data(models.Model):
    sensor_ID = models.ForeignKey( "Sensor" ,  to_field="sensor_ID" ,on_delete = models.CASCADE, db_column='sensor_ID')
    Value = models.CharField (max_length=10)
    Time = models.DateTimeField(auto_now_add=True)

