# QuerySet

以下介紹Django 資料庫如何操作</br>
假設有一個模型如下</br>

```python

class Project (models.Model): 
    name = models.CharField(max_length=50,blank=True,default="") 
    

class Task(models.Model):
    Status_CHOICES = (
        ('Close', 'Close'),       
		('Open', 'Open'),
        ('Pending', 'Pending'),      
    )
    Priority_CHOICES = (         
        ('High', 'High'),       
		('Middle', 'Middle'),  
        ('Low', 'Low'),  
    )
    project = models.ForeignKey(Project, related_name='tasks',on_delete=models.CASCADE,null=True, blank=True)	    
    name = models.CharField(max_length=50,blank=True,default="") 
    start_date = models.DateField('開始日期',default=timezone.now,null=True,blank=True)	   
    end_date = models.DateField('結束日期',null=True,blank=True) 
    owner = models.ManyToManyField(User,related_name='+',blank=True)     
    priority=models.CharField(max_length=10, null=False,choices=Priority_CHOICES,default='Low')    
    status = models.CharField(max_length=10, null=False,choices=Status_CHOICES,default='Open') 
```


## 1.Create Object


介紹以下方法建立Object
### 第一種

```python
    project = Project()
    project.name = 'Django' 
    project.save()
```
### 第二種

```python
    project = Project(name = 'Django') 
    project.save()
```

### 第三種
這種方法和上面不同會直接儲存
```python
    Project.objects.create(name = 'Django') 
```

### 第四種
這種方法會判斷是否還有資料,會回傳兩個,task,bcreate
```python
    task,bcreate = Project.objects.get_or_create(name = 'Django') 
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

取得案名含有有python有關.

```python
    Task.objects.filter(priority='High',status='Open',projects__contains='python') 
```
注意在django __(雙底線)用來進行連結，因此命名時請勿用__，可用_(單底線)</br>

詳情其他與法可以參考<a href="https://docs.djangoproject.com/en/2.1/ref/models/querysets/#methods-that-return-new-querysets">QuerySet API</a>


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
    Task.objects.filter(status='Open').exclude(project_contaions ='Django')
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
    tasks= Task.objects.all().select_related('project')..distinct() 
``` 


#### select_related() 
適用Foreign key

 ```python
    tasks= Task.objects.all()..prefetch_related('owner')
``` 

