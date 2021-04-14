# Mode1

## Create Model
```python
from django.db import models
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 
    height = models.FloatField()
    weight = models.FloatField()    
```

使用cmd執行以下指令 即可新增model
```python
    python manage.py makemigrations

    python manage.py migrate
```
也可以指定特定app

```python
    python manage.py makemigrations [app]

    python manage.py migrate [app]
```

## Model method
```python
from django.db import models
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30) 
    height = models.FloatField()
    weight = models.FloatField() 

    def __str__(self):
        return "{0} {1}".format(first_name,last_name)
        
    def get_bmi(self):
        return weight /(height/100)**2
```



   
## FileField Path used instance

model如下
```python
def path(instance, filename):    
    return '{0}/{1}/{2}'.format("File",instance.pk,filename
    
class FileUpload(models.Model):
    ....
    file = models.FileField(upload_to = path)   
    
```
objects 在尚未create 時,所以instance會為空,此時需分兩次儲存,修改save

```python
class FileUpload(models.Model):    
    file = models.FileField(upload_to = path
    def save(self, *args, **kwargs):
        if self.id is None:
            file = self.file 
            self.file = None        
            super().save(*args, **kwargs)
            self.file = file         
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)  
```