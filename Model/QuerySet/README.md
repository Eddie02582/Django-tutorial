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
#### 第一種

```python
    task = Task()
    task.project='Django'
    task.priority='High'
    task.status='Open'
    ....
    task.save()
```
#### 第二種

```python
    task = Task(project='Django',priority='High',status='Open') 
    task.save()
```

#### 第三種
這種方法和上面不同會直接儲存
```python
    Task.objects.create(project='Django',priority='High',status='Open') 
```

#### 第四種
這種方法會判斷是否還有資料,會回傳兩個,task,bcreate
```python
    task,bcreate,Task.objects.get_or_create(project='Django',priority='High',status='Open') 
```

## 2.Query 

#### 一般的使用方法
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

#### Field lookupst

用法FilesName__Fieldlookups

假設我們想得到案名跟含有python有關.

```python
    Task.objects.filter(priority='High',status='Open',projects__contains='python') 
```
注意在django __(雙底線)用來進行連結，因此命名時請勿用__，可用_(單底線)</br>

詳情其他與法可以參考<a href="https://docs.djangoproject.com/en/2.1/ref/models/querysets/#methods-that-return-new-querysets">QuerySet API</a>

#### filter or 用法
假設我們想找Project 是open 或是 priority 是 High
```python
    tasks= Task.objects.filter(Q(status='Open') | Q(priority='High')) 
```


#### filter 外鍵
假設我們想得到owner 的first_name包含Eddie,James...,owner 是關聯User資料庫,User 資料庫包和 username,first_name....
```python
    Task.objects.filter(owner__first_name_in=['Eddie','James']) 
```


外鍵時可以透過select_related()和prefetch_related()可以減少數據庫提請求，以提高效能

## 3.Update
假設我們一筆資料
 ```python
    tasks= Task.objects.get(id=1)  
    tasks.status="Close"
    tasks.save()
```   

假設更新我們一群符合特定規格的資料關閉結案,可以用下列方法,此方法會自動儲存
 ```python
    tasks= Task.objects.filter(project__contains="python").update(status="Close")    
``` 

## 3.Orderby

#### order_by
假設我們想取出open 資料,然後照案名排序,照依照開始時間排序
若要降序排序就在filed name 前面加-
 ```python
    tasks= Task.objects.filter(status="Open").order_by("project",'start_date')    
    tasks= Task.objects.filter(status="Open").order_by("project",'-start_date')   
``` 
#### 自訂order_by
想要依照priority 排序,

 ```python
 from django.db.models import Case, When
    pk_list =['High','Middle','Low']
    preserved = Case(*[When(priority=pk, then=pos) for pos, pk in enumerate(pk_list)]) 
    tasks= Task.objects.filter(status="Open").order_by(preserved)    
  
``` 


