# Relationships
關聯數據庫的力量在於將表相互關聯。 Django提供了定義三者的方法，最常見的數據庫關係類型：多對一，多對多和一對一。


## Many-to-One

定義多對一關係，使用django.db.models.ForeignKey。 你可以像其他任何一樣使用它</br>
字段類型：將其包含為模型的類屬性。ForeignKey需要一個位置參數：與模型相關的類。</br>
以下為範例，有一個公告的模型，使用者可以發布多個公告，相反來說多個公告由同一位使用者發布，</br>
可以定義

```python 
user = models.ForeignKey(User, related_name='News',on_delete=models.CASCADE)	
```

```python 
class Proclamation(models.Model):
    Category_CHOICES = (
        ('公告', '公告'),       
    )
    category = models.CharField(max_length=10, null=False,choices=Category_CHOICES) #類別關聯   
    title = models.CharField(max_length=50, null=False) #標題
    user = models.ForeignKey(User, related_name='News',on_delete=models.CASCADE)	
    message = models.TextField(max_length=4000)
    pubtime = models.DateTimeField(auto_now_add=True) #發布時間  
    press =  models.PositiveIntegerField(default=0) #點擊次數
    def __str__(self):
        return self.title
```

## Many-to-Many

定義多對多關係，請使用ManyToManyField。 可以像使用任何其他Field類型一樣使用它</br>
ManyToManyField需要一個位置參數：與模型相關的類。</br>
以下為範例，有一個案子的模型，一個案子有多位負責人，但是每個人可能負責多個案子</br>
可以定義</br>

```python 
owner= models.ManyToManyField(User,related_name='+',blank=True)  </br>	
```

```python 
class AbstractTask(models.Model):
    Status_CHOICES = (
        ('Close', 'Close'),       
		('Open', 'Open'),  
    )
    start_date = models.DateField('Task 開始日期',default=timezone.now,null=True)	
    end_date = models.DateField('Task 結束日期',null=True)	
    establishment_date = models.DateTimeField('建立日期時間',auto_now_add=True)	
    modify_date = models.DateTimeField('修改日期',auto_now=True)	
    issue=models.TextField(max_length=2000,blank=True,default="")    
    owner= models.ManyToManyField(User,related_name='+',blank=True)  
```


## One-to-One

要定義一對一關係，請使用OneToOneField。 您可以像使用任何其他Field類型一樣使用它：通過包含它作為模型的類屬性。</br>	
當對像以某種方式“擴展”另一個對象時，這對於對象的主鍵最有用。</br>	
以下為範例，使用django.contrib.auth.models 的User 模型，但是這個模型只有基本的使用者資訊，我們想要擴展，讓使用者資訊更多，以符合我們的需求</br>	

```python 
owner= models.ManyToManyField(User,related_name='+',blank=True)  </br>	
```

```python 
from django.db import models
from django.contrib.auth.models import User
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
    incumbent = models.BooleanField(default=True)
```