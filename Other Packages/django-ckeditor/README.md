# Django-ckeditor


## 安裝

首先在cmd 執行

```
    pip install django-ckeditor
```

安裝成功後在setting.py 註冊

```python
INSTALLED_APPS = [   
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  
    'ckeditor',     
]
```


## 修改模型

將原模型 models.TextField 改成RichTextField

```python
from ckeditor.fields import RichTextField
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
    
    #issue=models.TextField(max_length=2000,blank=True,default="")   
    issue=RichTextField(max_length=2000,blank=True,default="")   


```

修改模型後要遷移資料

```
  python manage.py makemigrations
  python manage.py migrate
```
## admin結果

首先admin.py註冊
```
from django.contrib import admin
from .models import Tasks
admin.site.register(Task)
```





## 網頁結果
首先在form.py 建立model form

```python
class TaskForm(forms.ModelForm):     

    class Meta:
        model = Task       
```

view.py 以下以CBV 示範,亦也可以使用FBV
```python
class Task_Create(CreateView):
    model = Task
    form_class=TaskForm	
    template_name = 'Create.html'
    success_url = reverse_lazy('Task_View')
```
html 顯示
```
{{form.issue}}
```






















