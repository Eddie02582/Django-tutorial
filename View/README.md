# View


簡單的視圖函數

```python 

from django.http import HttpResponse

def home_page(request):
    return HttpResponse("Hello World!")  
```

將url

```python 
from . import views
...

urlpatterns = [
    # path函数将url映射到视图
    path('HonePage/', views.home_page, name='home_page'),
]
```

建立migrations folder
```
python manage.py makemigrations --empty app
```


以下Model相關介紹

<a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Field">Field</a>
<u1>
    <li>Field Introduction</li>
    <li>Field Option</li>
</ul>



<a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Relationships">Relationships</a>
<u1>
    <li>Many-to-One</li>
    <li>Many-to-Many</li>
    <li>One-to-One</li>
</ul>

<a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/Inheritance">Django-Model Inheritance</a>
<u1>
    <li>Abstract base classes</li>
    <li>Multi-table inheritance</li>
    <li>Proxy</li>
</ul>


<a href="https://github.com/Eddie02582/Django-tutorial/tree/master/Model/QuerySet">QuerySet</a>
<u1>
    <li>Create Object</li>
    <li><a href=https://github.com/Eddie02582/Django-tutorial/tree/master/Model/QuerySet#2query>Query</a></li>
    <li><a href=https://github.com/Eddie02582/Django-tutorial/tree/master/Model/QuerySet#3update>Update</a></li>
    <li><a href=https://github.com/Eddie02582/Django-tutorial/tree/master/Model/QuerySet#4orderby>Order By</a></li> 
</ul>




