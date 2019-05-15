# Django-Model Inheritance

>Django中有三種可能的繼承方式。
>
> > 1.如果您不想輸入的信息每個子類，您希望使用父類來保存訊息。 可以使用Abstract base classes
>
> > 2.如果你是現有模型的子類（可能完全是來自另一個應用程序的東西）並且想要每個模型model有自己的數據庫表，多表繼承是要走的路。
>
> > 3.最後，如果您只想修改模型的Python級行為，而不更改模型字段，無論如何，您可以使用代理模型。
    
## Abstract base classes
>  class Meta 寫入abstract=True，注意父類並不會建立Model在資料庫內

```python
from django.db import models
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    class Meta:
        abstract = True
class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```

### Meta inheritance
> 當創建一個抽象基類時，Django使在父類中聲明的任何Meta內部類可用一個屬性。 
> 如果子類沒有聲明它自己的Meta類，它將繼承父類的Meta。 如果子類別想要擴展父類的Meta類，它可以繼承它。 例如：

```python
from django.db import models
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    class Meta:
        abstract = True
        ordering = ['name']
        
class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
    class Meta(CommonInfo.Meta):
        db_table = 'student_info'from django.db import models

```

## Multi-table inheritance
Django支持的第二種模型繼承是當每個模型都是模型時本身。<br />
每個模型對應於自己的數據庫表，可以單獨查詢和創建。 <br />
繼承relationship引入了子模型與其父模型之間的鏈接（通過自動創建的模型）OneToOneField）<br />



```python
from django.db import models
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

```

Place的所有Field也能在Restaurant中取得，但數據將位於不同的數據庫中表。 這些都是可能的：<br />

```python
>>> Place.objects.filter(name="Bob's Cafe")
>>> Restaurant.objects.filter(name="Bob's Cafe")
```












