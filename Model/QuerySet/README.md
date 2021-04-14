# QuerySet

以下介紹Django 資料庫如何操作</br>
假設有一個模型如下</br>




```python  
class Team(models.Model):
    name = models.CharField(max_length=50,blank=True,default="") 

class Person(models.Model):
    position_choices = (('C','C'),('PF','PF'),('SF','SF'),('SG','SG'),('PG','PG'))
    team = models.ForeignKey(Team, on_delete = models.CASCADE,null = True,blank = True,related_name="players")
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField() 
    position = models.CharField(max_length=50,choices = position_choices) 

  
```

## Create Object

### create single

#### method 1
used create(**kwargs)

```python
    Person.objects.create(first_name = 'LeBron',last_name = 'James',height = 206 ,weight = 113 ) 
```

used dictionary

```python
    info = {first_name : 'LeBron',last_name : 'James',height : 206 ,weight : 113}
    Person.objects.create(**info)    
```

#### method 2
```python
    person = Person(first_name = 'LeBron',last_name = 'James',height = 206 ,weight = 113 ) 
    person.save()
```

used dictionary

```python
    info = {first_name : 'LeBron',last_name : 'James',height : 206 ,weight : 113}
    person = Person(**info) 
    person.save()
```
#### method 3

```python
    person = Person()
    person.first_name = 'LeBron' 
    person.last_name = 'James' 
    person.height = 206
    person.weight = 113
    person.save()
```
#### method 4

```python
    person,bcreate = Person.objects.get_or_create(first_name : 'LeBron',last_name : 'James') 
```


### create muliti

#### method 1
bulk_create

```python
datas = []
datas.append({first_name : 'LeBron',last_name : 'James',height : 206 ,weight : 113})
datas.append({first_name : 'Anthony',last_name : 'Davis',height : 208 ,weight : 115})

persons = [person(**data) for data in datas]
Person.objects.bulk_create(persons)
```



## Query 

### 常用query的方法
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
        <td>Task.objects.filter(status='Open',priority='High')</td>
    </tr>
    <tr>
        <td>Get objects, exclude by a  field</td>
        <td>Task.objects.exclude(status='Close')</td>
    </tr>
</table>

### Field lookups

使用用法 FieldName__Fieldlookups

example:取得名字含有James

```python
    Person.objects.filter(first_name__contains = "James") 
```




注意在django __(雙底線)用來進行連結，因此命名時請勿用__，可用_(單底線)</br>

其他Fieldlookups參考<a href="https://docs.djangoproject.com/en/2.1/ref/models/querysets/#methods-that-return-new-querysets">QuerySet API</a>


### Query AND

#### Method 1
```python
queryset = Person.objects.filter(first_name__startswith='R') & Person.objects.filter(last_name__startswith='D')
```

#### Method 2
```python
queryset = Person.objects.filter(first_name__startswith='R',last_name__startswith='D')
```

#### Method 3
使用Q
```python
from django.db.models import Q
queryset = Person.objects.all().filter(Q(first_name__startswith = 'R') & Q(last_name__startswith='D'))#條件是or的關係
```

### Query OR

#### Method 1
```python
queryset = Person.objects.filter(first_name__startswith='R')  Person.objects.filter(last_name__startswith='D')
```

#### Method 2
使用Q
```python
from django.db.models import Q
queryset = Person.objects.all().filter(Q(first_name__startswith = 'R')|Q(last_name__startswith='D'))#條件是or的關係
```


### Query API
以下皆可搭配使用

#### filter 
```python
    Person.objects.filter(team__name = "Lakers") 
```

#### exclude 
```python
    Person.objects.filter(team__name = "Lakers").exclude(first_name ='Lebron')
```

#### values(*fields, **expressions)

輸出為字典格式
```python
>>>Person.objects.values()
```

指定欄位
```python
>>>Person.objects.values('first_name','last_name') 
<QuerySet [{'first_name': 'Anthony', 'last_name': 'Davis'}, {'first_name': 'LeBron', 'last_name': 'James'}]>
```

使用 **expressions,輸出自訂欄位

```python
from django.db.models.functions import Lower
>>>Person.objects.values('first_name',lower_name = Lower('first_name'))
<QuerySet [{'first_name': 'Anthony', 'last_name': 'Davis'}, {'first_name': 'LeBron', 'last_name': 'James'}]>
```


也可以使用內嵌的
```
>>> from django.db.models import CharField
>>> from django.db.models.functions import Lower
>>> CharField.register_lookup(Lower)
>>>Person.objects.values('first_name__lower','last_name')
<QuerySet [{'first_name__lower': 'Anthony', 'last_name': 'Davis'}, {'first_name__lower': 'LeBron', 'last_name': 'James'}]>
```



#### values_list
與value 相同但回傳turple型態
```python
>>>Person.objects.values_list('first_name','last_name')   
<QuerySet [('Anthony', 'Davis'), ('LeBron', 'James')]>
```

##### order_by
排序,若加'-' 為降序
 ```python
    Person.objects.filter(team__name = "Lakers").order_by("-height",'first_name')     
``` 

###### 自訂order_by
想要依照priority 排序

 ```python
from django.db.models import Case, When
    order_list =['C','PF','SF','SG','PG']
    preserved = Case(*[When( position = pk, then = pos) for pos, pk in enumerate(order_list)]) 
    Person.objects.order_by(preserved)    
  
``` 


#### annotate

注意回傳為queryset,只是新增一個欄位
```python
from django.db.models.aggregates import Max,Min,Count

teams = Team.objects.annotate(teams_players = Count('players'))
teams[0].players_cnt
```



使用values對Team分組 ,搭配組annotate取出最高身高

```python
from django.db.models.aggregates import Max,Min,Count

Person.objects.values('team__name').annotate(max_height = Max('max_height'))
```

這邊使用values 所以回傳字典形式


```
>>><QuerySet [ {'status': 'Lakers', 'max_height': 211},               
               {'status': 'Clipper', 'max_height': 226},
               {'status': 'Net', 'max_height': 208}]>
```

#### aggregates
aggregate的中文意思是聚合, 源於SQL的聚合函數。 Django的aggregate()方法作用是對一組值


```python
    from django.db.models import Avg, Max, Min
    Person.objects.aggregate(Max('height'),Min('height'))
    >>{'height__max':211,height__min:185}
```

#### distinct(*fields)
過濾重複的
```
   Person.objects.distinct() 
```

```
   Person.objects.distinct('first_name') 
```


#### select_related() 
提高ForeignKey的效能
 ```python
    Person.objects.all().select_related('team')
``` 

#### prefetch_related() 
提高ManyToManyField的效能
```python
    Person.objects.all().prefetch_related('ManyToManyField')
``` 






## Update

### update multi

```python
    Person.objects.filter(id__in[1,2]).update(position = "C")     
``` 

使用字典,但會無法更新auto_now的值

```python
    Person.objects.filter(id__in[1,2]").update(**{'position':'C'}))     
``` 


#### bulk_update
適用於更新資料不同
```python 
    objs = [ Person.objects.get(id = id) for id in [1,2,3]]    
    for i in range(len(objs)):          
        objs[i].weight = data_weight[i]           
        objs[i].height = data_height   [i]   
        
    Task.objects.bulk_update(tasks, ['weight','height'])  
  
```   

### update single
 ```python 
    person = Person.objects.get(id = 1)
    person.position = "C"   
    person.save()    
```   

使用字典,但會無法更新auto_now的值
```python 
    data = {'status':'Close'}
    task = Task.objects.get(id=1)
    task.__dict__.update(**data)
    task.save()   
```   


## instance to Dict 

### instance.__dict__
這邊會多回傳_state,但是少了many_to_many資料
```
    {
        '_state': <django.db.models.base.ModelState object at 0x0000000005D0A630>, 
        'id': 269, 
        'name': 'Cut 1 PCB Layout', 
        'duration': '20', 
        'start_date': datetime.datetime(2019, 2, 28, 8, 0), 
        'end_date': datetime.datetime(2019, 3, 27, 17, 0),
        'pl_id': 13
    }
```

### model_to_dict
```
    from django.forms.models import model_to_dict
    model_to_dict(instance)
```
注意這邊回傳為pl而非pl_id
```python
    {
        'id': 269, 
        'name': 'Cut 1 PCB Layout',
        'duration': '20',
        'start_date': datetime.datetime(2019, 2, 28, 8, 0),
        'end_date': datetime.datetime(2019, 3, 27, 17, 0),
        'pl': 13,
        'hw_owner': [], 
     }
```


可以搭配fields　取出想要的欄位
```python
    model_to_dict(instance, fields=[field.name for field in instance._meta.fields])
```



### query_set.values()
```python
    SomeModel.objects.filter(id=instance.id).values()[0]
```
return 
```python 
    {
        'id': 269, 
        'name': 'Cut 1 PCB Layout', 
        'duration': '20', 
        'start_date': datetime.datetime(2019, 2, 28, 8, 0), 
        'end_date': datetime.datetime(2019, 3, 27, 17, 0), 
        'pl_id': 13
     }
```



### Serializers
使用drf

## Advance



### Q

```python
from django.db.models import Q


models.objects.all().filter(Q(id = 1)|Q(id__gt = 3))#條件是or的關係
models.objects.all().filter(Q(id = 1) & Q(id = 4))  #條件是and的關係


```
other Method

```python
from django.db.models import Q
q1 = Q()
q1.connector = 'OR'
q1.children.append(('id',1))
q1.children.append(('id',3))
q1.children.append(('id',6))

q2 = Q()
q2.connector = 'OR'
q2.children.append(('c',2))
q2.children.append(('c',4))
q2.children.append(('c',6))

#con 通過and的條件把q1和q2 合在一起 
    con=Q()
    con.add(q1,'AND')
    con.add(q2,'AND')
```

### F

```python
from django.db.models import F
Person.objects.update(age = F("age")+ 1)  
```  





