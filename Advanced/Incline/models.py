from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
# Create your models here.



class Hardware(models.Model):
    project = models.CharField(max_length=100,null=False,blank=True)  
    def __str__(self):
        return self.project


class RF(models.Model):       
    chip_type = models.CharField(max_length=100)    
    transmit = models.IntegerField()
    recieve = models.IntegerField()
    hardware  = models.ForeignKey(Hardware, related_name='+', on_delete=models.CASCADE,null=True)	
        
    



