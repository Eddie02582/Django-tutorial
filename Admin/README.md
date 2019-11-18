# Admin



model.py
```python 

from django.contrib import admin
from .models import Question

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Team_CHOICES = (
        ('PL', 'PL'),       
		('HW', 'HW'), 
		('Layout', 'Layout'), 
		('Validation', 'Validation'),
        ('Antenna', 'Antenna'),
		('Automation', 'Automation'), 
        ('Driver', 'Driver'), 
        ('Sales', 'Sales'), 
		('Others', 'Others'),  			
	) 	
	
    Team = models.CharField(max_length=30,default='Others',choices=Team_CHOICES)
    Ext = models.CharField(max_length=30,null=True,blank=True,default="")	
    Short_number= models.CharField(max_length=30,null=True,blank=True,default="")	
    Cellphone_number= models.CharField(max_length=30,null=True,blank=True,default="")
    WeChat_ID= models.CharField(max_length=30,null=True,blank=True,default="")	
    Supervisor =  models.ForeignKey(User, on_delete=models.SET_NULL,related_name="+",null=True,blank=True)   
    incumbent = models.BooleanField(default=True)
```

admin.py 透過 admin.site.register 註冊 Profile


```python 
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

admin.site.register(Profile)

```

<img src="admin_1.png" alt="Smiley face">