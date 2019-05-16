# Django-Model Inheritance

>Django中有三種可能的繼承方式。
>
> > 1.如果您不想輸入的信息每個子類，您希望使用父類來保存訊息。 可以使用Abstract base classes
>
> > 2.如果你是現有模型的子類（可能完全是來自另一個應用程序的東西）並且想要每個模型model有自己的數據庫表，多表繼承是要走的路。
>
> > 3.最後，如果您只想修改模型的Python級行為，而不更改模型字段，無論如何，您可以使用代理模型。
    
## 1.Abstract base classes 
class Meta 寫入abstract=True，注意父類並不會建立Model在資料庫內<br/>

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
Student模型將包含三個字段：name，age和home_group。CommonInfo模型不能用作普通的Django模型，因為它是一個抽象的基類。它不會生成數據庫表無法直接實例化或保存。從抽象基類繼承的字段可以被覆寫，或者使用None移除。


### Meta inheritance
當創建一個抽象基類時，Django使在父類中聲明的任何Meta內部類可用一個屬性。<br /> 
如果子類沒有聲明它自己的Meta類，它將繼承父類的Meta。 如果子類別想要擴展父類的Meta類，它可以繼承它。 例如：<br/>

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

## 2.Multi-table inheritance
Django支持的第二種模型繼承是當每個模型都是模型時本身。每個模型對應於自己的數據庫表，可以單獨查詢和創建。繼承relationship引入了子模型與其父模型之間的鏈接(通過自動創建的模型)OneToOneField<br />


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


但是，如果上例中的p不是餐廳p.restaurant出現一個Restaurant.DoesNotExist 的例外。<br/>
在Restaurant自動創建的OneToOneField將其鏈接到Place，如下所示：
```python
place_ptr = models.OneToOneField(
Place, on_delete=models.CASCADE,
parent_link=True,
)
```

### Meat and Multi-table inheritance

在多表繼承情況下，子類從其父類的Meta類繼承是沒有意義的。所有Meta選項都已應用於父類，並且再次應用它們通常只會導致矛盾的行為(這與抽象基類的情況形成對比，其中基類不存在於其中自己的權利)因此，子模型無法訪問其父類的Meta類。 但是，有幾個有限的情況下，如果子類別沒有指定排序屬性或get_latest_by屬性，它將從其父級繼承它們。<br/>
如果父級有一個排序，並且您不希望子級具有任何自然順序，則可以明確禁用它：

```python
class ChildModel(ParentModel):
    # ...
    class Meta:
        # Remove parent's ordering effect
        ordering = []
```

## 3.Proxy
