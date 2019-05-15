# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Team_CHOICES = (
        ('PL', 'PL'),       
		('HW', 'HW'), 
		('Layout', 'Layout'), 
		('Validation', 'Validation'),
		('Automation', 'Automation'), 
		('Others', 'Others'),  			
	)  		
	
    Team = models.CharField(max_length=30,default='Others',choices=Team_CHOICES)
    Ext = models.CharField(max_length=30,null=True,blank=True,default="")	
    Supervisor =  models.ForeignKey(User, on_delete=models.SET_NULL,related_name="+",null=True,blank=True)   
    incumbent = models.BooleanField(default=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

	
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()	
	
def get_first_name(self):
    if (self.first_name==""):
	    return self.username
    return self.username+"/"+self.first_name

User.add_to_class("__str__", get_first_name)