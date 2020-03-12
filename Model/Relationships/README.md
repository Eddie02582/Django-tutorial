# Relationships
關聯數據庫的力量在於將表相互關聯。 Django提供了定義三者的方法，最常見的數據庫關係類型：多對一，多對多和一對一。


## Many-to-One

定義多對一關係，使用django.db.models.ForeignKey。 你可以像其他任何一樣使用它</br>
字段類型：將其包含為模型的類屬性。ForeignKey需要一個位置參數：與模型相關的類。</br>
定義了兩個模型，一個是老師模型，一個是學生模型，一個老師對應多個學生，這個算是一個一對多的類型(如下)</br>


幾個重點
<ul>
    <li>related_name:用來反向查詢,teacher.has_students() 即可查詢某位老師的學生,不必透過Student.objects.filter(teacher = teacher)</li>     
    <li>on_delete:用來設定當ForeignKey 的model 資料被刪除時,處理動作(modle.CASCADE,models.SET_NULL)</li>
</ul>

```python 
class Teacher(models.Model):
    name = models.CharField(max_length = 50)

class Student(models.Model):
    name = models.CharField(max_length = 50)
    #設定modle.CASCADE 當teacher 被刪除,學生也會跟著被刪除
    teacher = models.ForeignKey(Teacher , related_name = "has_students",on_delete = models.CASCADE)
```


## Many-to-Many

定義多對多關係，請使用ManyToManyField。 可以像使用任何其他Field類型一樣使用它</br>
ManyToManyField需要一個位置參數：與模型相關的類。</br>
定義了兩個模型，一個是老師模型，一個是學生模型，一個老師對應多個學生，每個學生對應多個老師(如下)</br>


```python 
class Teacher(models.Model):
    name = models.CharField(max_length = 50)

class Student(models.Model):
    name = models.CharField(max_length = 50)    
    teacher = models.ManyToManyField(Teacher , related_name = "+",on_delete = models.SET_NULL)
```


## One-to-One

要定義一對一關係，請使用OneToOneField。 您可以像使用任何其他Field類型一樣使用它：通過包含它作為模型的類屬性。</br>	
當對像以某種方式“擴展”另一個對象時，這對於對象的主鍵最有用。</br>	
以下為範例，使用django.contrib.auth.models 的User 模型，但是這個模型只有基本的使用者資訊，我們想要擴展，讓使用者資訊更多，以符合我們的需求</br>	

```python 
from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)   
    Ext = models.CharField(max_length=30,null=True,blank=True,default="")	
    incumbent = models.BooleanField(default=True)
```