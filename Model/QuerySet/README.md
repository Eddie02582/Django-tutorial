# QuerySet

以下介紹Django 資料庫如何操作</br>
假設有一個模型如下</br>

```python
class Task(models.Model):
    Status_CHOICES = (
        ('Close', 'Close'),       
		('Open', 'Open'), 
    )
    Priority_CHOICES = (         
        ('High', 'High'),       
		('Middle', 'Middle'),  
        ('Low', 'Low'),  
    )
    
    project=models.CharField(max_length=50,blank=True,default="") 
    start_date = models.DateField('開始日期',default=timezone.now,null=True,blank=True)	   
    end_date = models.DateField('結束日期',null=True,blank=True) 
    owner= models.ManyToManyField(User,related_name='+',blank=True)   
    priority=models.CharField(max_length=10, null=False,choices=Priority_CHOICES,default='Low') 
    status=models.CharField(max_length=10, null=False,choices=Status_CHOICES,default='Open') 
```

## 1.Create Object
介紹以下方法建立Object
### 第一種

```python
    task = Task()
    task.project='Django'
    task.priority='High'
    task.status='Open'
    ....
    task.save()
```
### 第二種

```python
    task = Task(project='Django',priority='High',status='Open') 
    task.save()
```

### 第三種
這種方法和上面不同會直接儲存
```python
    Task.objects.create(project='Django',priority='High',status='Open') 
```

### 第四種
這種方法會判斷是否還有資料,會回傳兩個,task,bcreate
```python
    task,bcreate,Task.objects.get_or_create(project='Django',priority='High',status='Open') 
```

## Query 
<table>
    <tr>
        <td>Operation</td>
        <td>Code sample</td>
    </tr>
    <tr>
        <td>List all objects</td>
        <td>Task.objects.all()</td>
    </tr>
        <tr>
        <td>Get a single object, identified by a field</td>
        <td>Task.objects.get(id=1)</td>
    </tr>
        <tr>
        <td>Get objects, identified by a description field</td>
        <td>Task.objects.filter(status='Open')</td>
    </tr>
    <tr>
        <td>Get objects, exclude by a  field</td>
        <td>Task.objects.exclude(status='Open')</td>
    </tr>
</table>

首先先取出所有



### Meta inheritance
如果子類別(child class)沒有定義它自己的Meta class，它將繼承父類的Meta class。<br/> 
如果子類別想要擴展父類的Meta類，它可以繼承它。 例如：<br/>

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
        db_table = 'student_info'

```

### Be careful with related_name and related_query_name
如果你使用related_name 或者 related_query_name 在 ForeignKey or ManyToManyField，必須是唯一的名字。</br>
這可能會在abstract base class造成問題，為了解決這個問題，在abstract base class使用related_name或related_query_name透過下列方法</br>



```python
from django.db import models
class Base(models.Model):
    m2m = models.ManyToManyField(
    OtherModel,
    related_name="%(app_label)s_%(class)s_related",
    related_query_name="%(app_label)s_%(class)ss",
    )
    class Meta:
        abstract = True
        
class ChildA(Base):
    pass
class ChildB(Base):
    pass
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
如果有一個Place剛好也是餐廳，您可以從Place物件取得Restaurant物件：<br/>
```python
>>> p = Place.objects.get(id=12)
# If p is a Restaurant object, this will give the child class:
>>> p.restaurant
<Restaurant: ...>
```

但是，如果上例中的p不是餐廳p.restaurant，會出現出現一個Restaurant.DoesNotExist 的例外。<br/>
在Restaurant自動創建的OneToOneField將其鏈接到Place，如下所示：
```python
place_ptr = models.OneToOneField(
Place, on_delete=models.CASCADE,
parent_link=True,
)
```

You can override that field by declaring your own OneToOneField with parent_link=True on Restaurant..<br/>

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

使用Multi-table inheritance時，每個子類會創建一個新的數據庫表。這是我們所預期的，因為子類需要一個位置來存儲base class上不存在的額外數據。但是有時您只想更改模型的Python行為，更改默認管理器或添加新方法。<br/>

這就是代理模型繼承的用途：為原始模型創建代理。 您可以創建，刪除和更新代理模型的實例和所有數據將被保存，就像使用原始(非代理)模型一樣。該區別在於您可以更改代理中的默認模型排序或默認管理器等內容。<br/>

For example, suppose you want to add a method to the Person model. You can do it like this:<br/>

```python
from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class MyPerson(Person):
    class Meta:
        proxy = True

    def do_something(self):
        # ...
        pass
```

您可以使用proxy model在模型上定義不同的默認排序。 你可能並不是每次想要排序Person model，但可以透過使用proxy model 按last_name屬性排序

```python

class OrderedPerson(Person):
    class Meta:
        ordering = ["last_name"]
        proxy = True
```
Person 查詢將是無序的，OrderedPerson查詢將按last_name排序。

### Base class restrictions

A proxy model must inherit from exactly one non-abstract model class. You can’t inherit from multiple non-abstract models as the proxy model doesn’t provide any connection between the rows in the different database tables. A proxy model can inherit from any number of abstract model classes, providing they do not define any model fields. A proxy model may also inherit from any number of proxy models that share a common non-abstract parent class.<br/>

### Proxy model managers
376/5000
如果未在proxy model上指定任何model managers，則它將從其模型父項繼承managers。 如果您在proxy model上定義managers，它將成為默認managers，儘管在父類上定義的任何管理器(managers)仍然可用。<br/>

繼續上面的示例，您可以更改查詢Person模型時使用的默認管理器，如下所示：<br/>


```python
from django.db import models

class NewManager(models.Manager):
    # ...
    pass

class MyPerson(Person):
    objects = NewManager()

    class Meta:
        proxy = True
```
如果要在不替換現有默認值的情況下向代理添加新管理器，可以使用自定義管理器文檔中描述的技術：創建包含新管理器的基類，並在主基類之後繼承：<br/>


```python 
class ExtraManagers(models.Model):
    secondary = NewManager()

    class Meta:
        abstract = True

class MyPerson(Person, ExtraManagers):
    class Meta:
        proxy = True
```













