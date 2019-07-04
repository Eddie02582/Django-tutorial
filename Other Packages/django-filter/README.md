# Django-ckeditor

<a href="https://django-filter.readthedocs.io/en/master/">官方教學</a>



## Install

首先在cmd 執行

```
    pip install django-filter
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
    'django_filters',     
]
```


## Model

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField()
    description = models.TextField()
    release_date = models.DateField()
    manufacturer = models.ForeignKey(Manufacturer)
    
```

## Filter 

建立一個filters.py


```python
import django_filters

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['price', 'release_date']
```
### filter with lookup_expr

<ul>
    <li>field_name :指定欄位</li>
    <li>lookup_expr :指定收尋方式 ex:year__gt 表示尋找geater than year</li>  
</ul>

```python
class ProductFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
    release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')

    manufacturer__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
```

### filter with ChoiceFilter

假設 model
```python
from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    def __str__(self):
        return self.name
```

我們可以改寫 manufacturer__name = django_filters.CharFilter(lookup_expr='icontains'),讓選項從資料庫抓取

```
    manufacturer = django_filters.ModelChoiceFilter(queryset=PLTasks.objects.all())
```

也可以自訂選項

```python
    Location_CHOICES = (
    ('Taiwan', 'Taiwan'),
    ('Janpan', 'Janpan'),      
    ('', 'All'),  
    )  
    manufacturer__location = django_filters.ChoiceFilter(choices=Location_CHOICES) 
```

## Views

### FBV

```python
def product_list(request):
    f = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request, 'my_app/template.html', {'filter': f})
```


### CBV
```python
class product_list(FilterView):
    model = Product
    context_object_name = 'products'
    template_name =  'ListView.html'
    filterset_class=ProductFilter 
 
```



## Template

```
{% load bootstrap3 %}
{% if filter %}
    <form action="" method="get" class="form form-inline">  
        {% bootstrap_form filter.form layout='inline' %} 
        {% bootstrap_button 'filter' %}
    </form>
{% endif %} 
```
指定特殊欄位不顯示
```
{% load bootstrap3 %}
{% if filter %}
    <form action="" method="get" class="form form-inline">  
        {% bootstrap_form filter.form exclude='price,price__gt' layout='inline' %} 
        {% bootstrap_button 'filter' %}
    </form>
{% endif %} 
```













