# QuerySet

以下介紹Django 資料庫如何操作</br>
假設有一個模型如下</br>


```python    

class Person(models.Model):
    first_name = models.CharField(max_length=50,blank=True,default="") 
    last_name = models.CharField(max_length=50,blank=True,default="")    
    height = models.FloatField()
    weight = models.FloatField()   
```


## 1.Create Object


### Method 1

```python
    person = Person()
    person.first_name = 'LeBron' 
    person.last_name = 'James' 
    person.height = 206
    person.weight = 113
    person.save()
```
### Method 2

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


### Method 3
This method will automatically save
```python
    Person.objects.create(first_name = 'LeBron',last_name = 'James',height = 206 ,weight = 113 ) 
```
used dictionary

```python
    info = {first_name : 'LeBron',last_name : James,height : 206 ,weight : 113}
    Person.objects.create(**info)  
```

### 第四種
這種方法會判斷是否還有資料,會回傳兩個,person,bcreate

```python
    task,bcreate = Project.objects.get_or_create(first_name : 'LeBron',last_name : 'James') 
```

## 2.Query 

### 一般的使用方法


以下為常用query的方法
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

用法 FieldName__Fieldlookups

example:
取得名字含有James

```python
    Person.objects.filter(first_name__contains = "James") 
```
注意在django __(雙底線)用來進行連結，因此命名時請勿用__，可用_(單底線)</br>

其他Fieldlookups參考<a href="https://docs.djangoproject.com/en/2.1/ref/models/querysets/#methods-that-return-new-querysets">QuerySet API</a>


### Query API

#### filter 

owner 的first_name包含Eddie,James...,owner 是關聯User資料庫,User 資料庫包和 username,first_name....
```python
    Task.objects.filter(owner__first_name_in=['Eddie','James']) 
```

外鍵時可以透過select_related()和prefetch_related()可以減少數據庫提請求，以提高效能



#### exclude 
Returns a new QuerySet containing objects that do not match the given lookup parameters.

```python
    Task.objects.filter(status='Open').exclude(name_contaions ='Django')
```
#### values
指定欄位匯出,格式字典
```python
    Task.objects.value('project','status')
    #Task.objects.value(*['project','status'])
```

回傳格式
```
<QuerySet [{'project': 'project1', 'status': 'Open'},{'project': 'project2', 'status': 'Open'}]>
```


#### values_list
與value 相同但是回傳turple
```python
    Task.objects.values_list('project','status')   
```

##### order_by
假設我們想取出open 資料,然後照案名排序,照依照開始時間排序
若要降序排序就在filed name 前面加-
 ```python
    tasks= Task.objects.filter(status="Open").order_by("project",'start_date')    
    tasks= Task.objects.filter(status="Open").order_by("project",'-start_date')   
``` 

###### 自訂order_by
想要依照priority 排序

 ```python
 from django.db.models import Case, When
    pk_list =['High','Middle','Low']
    preserved = Case(*[When(priority=pk, then=pos) for pos, pk in enumerate(pk_list)]) 
    tasks= Task.objects.filter(status="Open").order_by(preserved)    
  
``` 


#### annotate

注意回傳為queryset,只是新增一個欄位
```python
from django.db.models.aggregates import Max,Min,Count

tasks = Task.objects.annotate(owner_cnt=Count('owner'))
tasks[0].owner_cnt
```



使用value進行分組,對Status 分組 ,並取出分組開始時間最早的日期,和最晚結束日期

```python
from django.db.models.aggregates import Max,Min,Count
request_values1 = Task.objects.values('status').annotate(min_start_date=Min('start_date'),max_end_date=Max('end_date'),status = Count('status')).order_by("status")
```

結果如下,這邊回傳一樣式字典的型式


```
>>><QuerySet [ {'status': 'Close', 'min_start_date': datetime.datetime(2017, 9, 15, 0, 0)},               
               {'status': 'Open', 'min_start_date': datetime.datetime(2017, 9, 25, 8, 0)},
               {'status': 'Pending', 'min_start_date': datetime.datetime(2019, 2, 19, 8, 0)}]>
```

#### aggregates
aggregate的中文意思是聚合, 源於SQL的聚合函數。 Django的aggregate()方法作用是對一組值

```python 

TestItem.objects.aggregate(Max('end_date'))
```
 result 
 ```python 
{'end_date__max': datetime.date(2020, 1, 3)}
```




#### update

更新符合特定規格的資料關閉結案,可以用下列方法,此方法會自動儲存

 ```python
    tasks= Task.objects.filter(project__contains="python").update(status="Close")    
``` 

在2.2版新增了bulk_update ,可以大量更新
 ```python
        tasks = [ Task.objects.get(id = id) for id in data_id]
        for i in range(len(objs)):          
            objs[i].status = data_status[i]           
            objs[i].priority = data_priority[i]             
        Task.objects.bulk_update(tasks, ['status','priority']) 
``` 

#### distinct(*fields)
過濾重複的
```
   Task.objects.distinct() 
```


#### select_related() 
適用Foreign key

 ```python
    tasks= Task.objects.all().select_related('project').distinct() 
``` 


#### prefetch_related() 
適用Many to Many

```python
    tasks= Task.objects.all().prefetch_related('owner')
``` 

## 3.Update

### 更新多筆

```python
    Task.objects.filter(priority = "High").update(status="Close")     
``` 

透過字典,但會無法更新auto_now的值

```python
    Task.objects.filter(priority = "High").update(**{'status':'Close'}))     
``` 


也可以使用bulk_update
```python 
    tasks = [ Task.objects.get(id = id) for id in data_id]
    for i in range(len(objs)):          
        objs[i].status = data_status[i]           
        objs[i].priority = data_priority[i]             
    Task.objects.bulk_update(tasks, ['status','priority'])    
```   

### 單筆更新
 ```python 
    task = Task.objects.get(id = 1)
    task.status = "Close"
    task.priority = "High"
    task.save()    
```   

透過字典,但會無法更新auto_now的值
```python 
    data = {'status':'Close'}
    task = Task.objects.get(id=1)
    task.__dict__.update(**data)
    task.save()   
```   


## 4.Advance



### Q

```python
from django.db.models import Q


models.objects.all().filter(Q(id=1)|Q(id__gt=3))#條件是or的關係
models.Uinfo.objects.all().filter(Q(id=1) & Q(id=4))# 條件是and的關係


```
另一種使用方法

```python
from django.db.models import Q
q1=Q()
q1.connector = 'OR'
q1.children.append(('id',1))
q1.children.append(('id',3))
q1.children.append(('id',6))

q2=Q()
q2.connector = 'OR'
q2.children.append(('c',2))
q2.children.append(('c',4))
q2.children.append(('c',6))

#con 通過and的條件把q1和q2 合在一起 
    con=Q()
    con.add(q1,'AND')
    con.add(q2,'AND')
```











